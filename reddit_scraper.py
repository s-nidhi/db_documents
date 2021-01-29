#!/usr/bin/env python
# coding: utf-8

# In[1]:


import praw
import pandas as pd
import datetime as dt
from pprint import pprint
import requests
import json


# In[2]:


topics_dict = { "subreddit_id":[], "subreddit":[],
                "id":[],
                "author":[], "name":[],
                "title":[], "ups":[], "downs":[],
                "score":[], 
                "url":[], 
                "comms_num": [],
                "domain":[],
                "created": [], 
                "body":[]}

reddit_dict = { "subreddit_id":[], "subreddit":[],
                "id":[],
                "title":[],
                "score":[], 
                "url":[], "reddit_url":[],
                "comms_num": [],
                "created": [], 
                "body":[]}

comments_dict = { 
                "subreddit_id":[], "subreddit":[],"link_id":[],
                "id":[],
                "author":[], "name":[],
                "title":[], "ups":[], "downs":[],
                "score":[], 
                "url":[], "reddit_url":[],
                "comms_num": [],
                "domain":[],
                "created": [],
                "text":[],
                "body":[]}

def get_date(created):
    return dt.datetime.fromtimestamp(created)

def catch_ex(data=None):
    if (data):
        return data
    else:
        return ""
# In[3]:

def tmp_fun(comment):
    try:
        link_id = catch_ex(comment['data']['link_id'])
    except:
        link_id = None
    comments_dict["link_id"].append(link_id)

    try:
        subreddit_id = catch_ex(comment['data']['subreddit_id'])
    except:
        subreddit_id = None
    comments_dict["subreddit_id"].append(subreddit_id)

    try:
        subreddit = catch_ex(comment['data']['subreddit'])
    except:
        subreddit = None
    comments_dict["subreddit"].append(subreddit)

    try:
        id = catch_ex(comment['data']['id'])
    except:
        id = None
    comments_dict["id"].append(id)

    try:
        author = catch_ex(comment['data']['author'])
    except:
        author = None
    comments_dict["author"].append(author)

    try:
        name = catch_ex(comment['data']['name'])
    except:
        name = None
    comments_dict["name"].append(name)

    try:
        title = catch_ex(comment['data']['title'])
    except:
        title = None
    comments_dict["title"].append(title)

    try:
        ups = catch_ex(comment['data']['ups'])
    except:
        ups = None
    comments_dict["ups"].append(ups)

    try:
        downs = catch_ex(comment['data']['downs'])
    except:
        downs = None
    comments_dict["downs"].append(downs)

    try:
        score = catch_ex(comment['data']['score'])
    except:
        score = None
    comments_dict["score"].append(score)

    try:
        reddit_url = catch_ex(comment['data']['permalink'])
    except:
        reddit_url = ""
    comments_dict["reddit_url"].append(str('https://www.reddit.com') + reddit_url)

    try:
        url = catch_ex(comment['data']['url'])
    except:
        url = None
    comments_dict["url"].append(url)

    try:
        num_comments = catch_ex(comment['data']['num_comments'])
    except:
        num_comments = None
    comments_dict["comms_num"].append(num_comments)

    try:
        created = catch_ex(comment['data']['created'])
    except:
        created = ""
    comments_dict["created"].append(created)

    try:
        domain = catch_ex(comment['data']['domain'])
    except:
        domain = None
    comments_dict["domain"].append(domain)

    try:
        selftext = catch_ex(comment['data']['selftext'])
    except:
        selftext = None
    comments_dict["text"].append(selftext)

    try:
        body = catch_ex(comment['data']['body'])
    except:
        body = None
    comments_dict["body"].append(body)

    comments_dict["reddit_url"]

def reddit_posts(url, header):
    post_comments = requests.get(str('https://www.reddit.com') + url + str('.json'),headers=header)
    #print(post_comments.text)
    post_comments = json.loads(post_comments.text)
    #print(comments)
    url_list = []
    for comments in post_comments: 
        for comment in comments['data']['children']:
            url_list.append(tmp_fun(comment))
    return url_list


# In[ ]:


"""
reddit = praw.Reddit(client_id='JMgbGNgkSVeOLw',
                     client_secret='EPQ_T-A78lM91iV5ksG4VBTWeso',
                     user_agent='d_reviewers',
                     username='nidhis-enixta',
                     password='nidhi@2615')



subreddit = reddit.subreddit('detergent')
top_subreddit = subreddit.top(limit=500)

for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)
    
topics_data = pd.DataFrame(topics_dict)
_timestamp = topics_data["created"].apply(get_date)
topics_data = topics_data.assign(timestamp = _timestamp)

topics_data
"""


# In[4]:

if __name__ == '__main__':
    #url = "https://www.reddit.com/r/detergent/.json?count=20"
    url = "https://www.reddit.com/search.json?q=title%3A%22laundry%20detergent%22%20AND%20self%3A1&limit=100"
    agent = {"User-Agent": "Chrome/67.0.3396.87"}
    posts = requests.get(url,headers=agent)
    data = json.loads(posts.text)
    tmp = []
    for child in data['data']['children']:
        url = child['data']['permalink']
        tmp.extend(reddit_posts(url,agent))

    #flattened_list = [y for x in tmp for y in x]
    #res = []
    #[res.extend(x) for x in flattened_list if x not in res]
    #print(len(res))
    #res = res[:100]
    #for i in res:
    #    print(i)
    comments_data = pd.DataFrame(comments_dict)
    _timestamp = comments_data["created"].apply(get_date)
    comments_data = comments_data.assign(timestamp = _timestamp)

    comments_data.to_csv('comments_data2.csv', index=False)
    print("done....")


# In[ ]:

"""
if __name__ == '__main__':
    #url = "https://www.reddit.com/r/detergent/.json?count=20"
    #url = "https://www.reddit.com/search.json?q=title%3A%22laundry%20detergent%22&limit=100"
    url = "https://www.reddit.com/search.json?q=title%3A%22laundry%20detergent%22%20AND%20self%3A1&limit=100"
    agent = {"User-Agent": "Chrome/67.0.3396.87"}
    posts = requests.get(url,headers=agent)
    data = json.loads(posts.text)
    
    for child in data['data']['children']:
        reddit_dict["title"].append(child['data']['title'])
        reddit_dict["score"].append(child['data']['score'])
        reddit_dict["id"].append(child['data']['id'])
        reddit_dict["url"].append(child['data']['url'])
        try:
            if (child['data']['num_comments']): 
                num_comments=child['data']['num_comments'] 
            else: 
                num_comments=""
        except:
            num_comments=""
        reddit_dict["comms_num"].append(num_comments)
        reddit_dict["created"].append(child['data']['created'])
        try:
            if (child['data']['body']): 
                body=child['data']['body'] 
            else: 
                body=""
        except:
            body=""
        reddit_dict["body"].append(body)
        try:
            if (child['data']['subreddit_id']): 
                subreddit_id=child['data']['subreddit_id'] 
            else: 
                subreddit_id=None
        except:
            subreddit_id=None
        reddit_dict["subreddit_id"].append(subreddit_id)
    
        try:
            if (child['data']['subreddit']): 
                subreddit=child['data']['subreddit'] 
            else: 
                subreddit=None
        except:
            subreddit=None
        reddit_dict["subreddit"].append(subreddit)
        
        try:
            if (child['data']['permalink']): 
                reddit_url=child['data']['permalink'] 
            else: 
                reddit_url=""
        except:
            reddit_url=""
        reddit_dict["reddit_url"].append(str('https://www.reddit.com') + reddit_url)
    
    comments_data = pd.DataFrame(reddit_dict)
    #_timestamp = comments_data["created"].apply(get_date)
    #comments_data = comments_data.assign(timestamp = _timestamp)
    
    comments_data.to_csv('comments_data4.csv', index=False)
    print("done....")
    """

# In[ ]:




