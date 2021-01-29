
# coding: utf-8

# In[1]:


from sqlalchemy import create_engine, insert
from sqlalchemy.sql import text
import pandas as pd
import os
import yaml
import traceback


# In[2]:


def get_engine(db):
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(db['DB_USER'], db['DB_PASSWD'], db['DB_HOST'], db['DB_PORT'],
                                                                db['DB_NAME']))
    print('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(db['DB_USER'], db['DB_PASSWD'], db['DB_HOST'], db['DB_PORT'],
                                                                db['DB_NAME']))
    return engine


# In[3]:


def load_config():
    yaml_file = open("/Users/Nidhi/Documents/python_scripts/account_conf.yaml", 'r')
    config = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    yaml_file.close()
    return config

config = load_config()


# In[4]:


def account_category_map(account_id, category_id):
    try:
        check_category = pd.read_sql("select * from account_category_map where account_id = {} and category_id = {};".format(account_id, category_id), con)
        if check_category.shape[0] > 0:
            print("Given category is already mapped to account")
        else:
            default_category = input("Enter default_category ('Y' or 'N'): ")
            print("default_category: {}".format(default_category))
            smaartpulse = input("Enter smaartpulse ('Y' or 'N'): ")
            print("smaartpulse: {}".format(smaartpulse))
            con.execute("INSERT INTO account_category_map (account_id, category_id, is_default, smaartpulse) VALUES({}, {}, '{}', '{}');".format(account_id, category_id, default_category, smaartpulse))     
    except Exception as Ex:
        print(traceback.format_exc())   


# In[5]:


def account_feature_subscription(account_id):
    try:
        check_feature_sub = pd.read_sql("select * from account_feature_subscription where account_id = {};".format(account_id), con)
        if check_feature_sub.shape[0] > 0:
            print("Given account is already present in account_feature_subscription")
        else:
            ai_response = input("Enter ai_response ('Y' or 'N'): ")
            print("ai_response: {}".format(ai_response))
            smaart_summary = input("Enter smaart_summary ('Y' or 'N'): ")
            print("smaart_summary: {}".format(smaart_summary))
            smaart_sight = input("Enter smaart_sight ('Y' or 'N'): ")
            print("smaart_sight: {}".format(smaart_sight))
            smaart_compare = input("Enter smaart_compare ('Y' or 'N'): ")
            print("smaart_compare: {}".format(smaart_compare))
            
#             user_reviews = raw_input("Enter user_reviews ('Y' or 'N'): ")
#             print("user_reviews: {}".format(user_reviews))
#             social_reviews = raw_input("Enter social_reviews ('Y' or 'N'): ")
#             print("social_reviews: {}".format(social_reviews))
#             expert_reviews = raw_input("Enter expert_reviews ('Y' or 'N'): ")
#             print("expert_reviews: {}".format(expert_reviews)) 
#             video_reviews = raw_input("Enter video_reviews ('Y' or 'N'): ")
#             print("video_reviews: {}".format(video_reviews))
#             question_answers = raw_input("Enter question_answers ('Y' or 'N'): ")
#             print("question_answers: {}".format(question_answers))
#             brand_compare = raw_input("Enter brand_compare ('Y' or 'N'): ")
#             print("brand_compare: {}".format(brand_compare))
#             product_compare = raw_input("Enter product_compare ('Y' or 'N'): ")
#             print("product_compare: {}".format(product_compare))
#             dynamic_aspect = raw_input("Enter dynamic_aspect ('Y' or 'N'): ")
#             print("dynamic_aspect: {}".format(dynamic_aspect)) 
#             product_type = raw_input("Enter product_type ('Y' or 'N'): ")
#             print("product_type: {}".format(product_type)) 
#             price_trend = raw_input("Enter price_trend ('Y' or 'N'): ")
#             print("price_trend: {}".format(price_trend)) 
#             insights_duration_years = raw_input("Enter insights_duration_years: ")
#             print("insights_duration_years: {}".format(insights_duration_years))
#             smaartchat_duration_days = raw_input("Enter smaartchat_duration_days: ")
#             print("smaartchat_duration_days: {}".format(smaartchat_duration_days))
            
#             con.execute("INSERT INTO account_feature_subscription (account_id, summary, response, sight, compare, user_reviews, social_reviews, expert_reviews, video_reviews, question_answers, brand_compare, product_compare, dynamic_aspect, product_type, price_trend, insights_duration_years, smaartchat_duration_days) "/
#                         "VALUES({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {});"
#                         .format(account_id, smaart_summary, ai_response, smaart_sight, smaart_compare, user_reviews, social_reviews, expert_reviews, video_reviews, question_answers, brand_compare, product_compare, dynamic_aspect, product_type, price_trend, insights_duration_years, smaartchat_duration_days))
            
            con.execute("INSERT INTO account_feature_subscription (account_id, summary, response, sight, compare) VALUES({}, '{}', '{}', '{}', '{}');"
                        .format(account_id, smaart_summary, ai_response, smaart_sight, smaart_compare))
    except Exception as Ex:
        print(traceback.format_exc())  


# In[6]:


def account_source_map(account_id):
    try:
        while True:
            source_id = input("Enter source_id: ")
            print("source_id: {}".format(source_id))

            check_source = pd.read_sql("select * from account_source_map where account_id = {} and source_id = {};".format(account_id, source_id), con)
            if check_source.shape[0] > 0:
                print("Given source is already present in account_source_map")
            else:
                ai_response = input("Enter ai_response ('Y' or 'N'): ")
                print("ai_response: {}".format(ai_response))
                con.execute("INSERT INTO account_source_map (account_id, source_id, ai_response) VALUES({}, {}, '{}');"
                            .format(account_id, source_id, ai_response))
            cont = input("Do you want to add more sources(Y or N): ")
            if cont == 'N':
                break
    except Exception as Ex:
        print(traceback.format_exc())  


# In[7]:


def account_brand_subscription(account_id, category_id):
    try:
        brands = pd.read_sql("select distinct brand_id from product where id in (select distinct product_id "                             " from product_detail where country_id = {} and category_id = {});"
                             .format(country_id, category_id), con)
        acc_brand_sub = [(account_id, id) for id in brands.brand_id]
        #print(acc_brand_sub)
        con.execute(text("INSERT INTO account_brand_subscription (account_id, brand_id) VALUES {} "                         "on duplicate key update account_id = VALUES(account_id), brand_id = VALUES(brand_id);".format(','.join(str(item) for item in acc_brand_sub))))
        
        default_brand = input("Enter default_brand_id: ")
        print("default_brand: {}".format(default_brand))
        
        if default_brand:
            con.execute(text("UPDATE account_brand_subscription set is_owner = 'Y' "                         "WHERE account_id = {} and brand_id = {};".format(account_id, default_brand)))   
    except Exception as Ex:
        print(traceback.format_exc())   


# In[8]:


def create_account():
    category_id = input("Enter category_id: ")
    print("category_id: {}".format(category_id))
    try:
        acc_id = con.execute("INSERT INTO account (country_id, account_name, account_desc, account_code "        " ) VALUES({}, '{}', '{}', '{}')".format(country_id, account_name, account_desc, account_code))
        print(acc_id.lastrowid)
        account_category_map(acc_id.lastrowid, category_id)
        account_feature_subscription(acc_id.lastrowid)
        account_source_map(acc_id.lastrowid)        
        account_brand_subscription(acc_id.lastrowid, category_id)
    except Exception as Ex:
        print(traceback.format_exc())


# In[9]:


def add_category(account_id):
    category_id = input("Enter category_id: ")
    print("category_id: {}".format(category_id))
    try:
        account_category_map(account_id, category_id)
        account_feature_subscription(account_id)
        account_source_map(account_id)         
        account_brand_subscription(account_id, category_id)
    except Exception as Ex:
        print(traceback.format_exc())


# In[10]:


account_name = input("Enter account_name: ")
print("account_name: {}".format(account_name))
country_id = input("Enter country_id: ")
print("country_id: {}".format(country_id))

if int(country_id) == 1:
    con = get_engine(config['IND_DB'])
else:
    con = get_engine(config['US_DB'])
    
check_acc = pd.read_sql("SELECT * from account where account_name = '{}';".format(account_name), con)
if check_acc.shape[0] > 0:
    existing_acc_id = list(check_acc.id.unique())[0]
    print("Account already exists with id: {}".format(existing_acc_id))
    add_category(existing_acc_id)
    print("Category is added in existing account.")
else:
    account_desc = input("Enter account_desc: ")
    print("account_desc: {}".format(account_desc))
    account_code = input("Enter account_code: ")
    print("account_code: {}".format(account_code))
    create_account()
    print("New account is created.")
con.dispose()

