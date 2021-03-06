import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import random
import time
import re
import pickle
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary_argument = FirefoxBinary(r'/usr/bin/firefox')
options = Options()
options.add_argument('--headless')
options.binary = binary_argument

executable_path="geckodriver"

capabilities_argument = DesiredCapabilities().FIREFOX
capabilities_argument["marionette"] = True

from pyvirtualdisplay import Display 
display = Display(visible=0, size=(1024, 768)) 
display.start() 

timeDelay = random.randrange(5, 10)
def products_cards(category):
    url = "https://www.influenster.com/reviews/" + category + "/"
    try:
	 myDriver=webdriver.Firefox(executable_path=executable_path, options=options, firefox_binary=binary_argument,capabilities=capabilities_argument)
	 myDriver.get(url)
	 print(myDriver.get_cookies())
	 cookies = pickle.load(open("cookies.pkl", "rb"))
         for cookie in cookies:
            if 'expiry' in cookie:
               del cookie['expiry']
         myDriver.add_cookie(cookie)

	#myDriver.find_element_by_xpath('//*[@id="CookielawBanner"]/div/p/a').click();
    except TimeoutException:
        print("Page expired")
        
    product_link = 'https://www.influenster.com/reviews/'
    product_list = []
    product_detail_list = []
    click_count = 0
    while click_count < 100: #50000
        try:
            product_template = WebDriverWait(myDriver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "category-products")))#myDriver.find_element_by_class_name('category-products')
            cards = product_template.find_elements_by_class_name('category-product')
            for card in cards:
                link = card.get_attribute('href')
                if link not in product_list:
                    product_list.append(link)
                    name = card.find_element_by_class_name('category-product-title').text
                    brand = card.find_element_by_class_name('category-product-brand').text
                    star_rating = card.find_element_by_class_name('avg-stars.small').get_attribute('data-stars')
                    reviews = card.find_element_by_class_name('category-product-rating').text
                    image = card.find_element_by_css_selector('img').get_attribute('src')
                    
                    product_detail_list.append({'product_link': link, 'product_name': name, 'brand': brand, 'star_rating': star_rating, 
                                                'total_reviews': re.findall(r'[0-9.,]+', reviews)[-1], 'image_url': image})

                    print('name:', name, 'link:', link, 'brand:', brand, 'star_rating:', 
                          star_rating, 'reviews:', re.findall(r'[0-9.,]+', reviews)[-1], 'image_url:', image)
            time.sleep(timeDelay)
            load_more = product_template.find_element_by_class_name("category-products-pagination-page.next")
            load_more.click()
            click_count+=1
            time.sleep(timeDelay)
            
        except Exception as e:
            print(e)
            return product_detail_list
            break
    else:
        print(click_count)
        return product_detail_list
    
try:
    # set up chromedriver
    myDriver=webdriver.Firefox()
    actions = ActionChains(myDriver)
    prod_list = products_cards("multivitamins")
    prod_data_frame = pd.DataFrame(prod_list)
    prod_data_frame.to_csv("influenster_product_list_multivitamins_2.csv", index=False)
except Exception as e:
    print(e)
finally:
    myDriver.quit()
    print('exit')

