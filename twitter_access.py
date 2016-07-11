# -*- coding: utf-8 -*-
import json
import urllib.request
import os
import sys
import re
from twitter import *
import time
from sklearn.feature_extraction.text import CountVectorizer
import MeCab
import scipy as sp


previous_user = ""

def twitter_access(secret_json):
    t = Twitter(auth=OAuth(secret_json["access_token"],
                       secret_json["access_token_secret"],
                       secret_json["consumer_key"],
                       secret_json["consumer_secret"]))
    return t

def get_my_profile(twitter_OAuth):
    return twitter_OAuth.account.verify_credentials()

def get_user_profile(twitter_OAuth, name):
    return  twitter_OAuth.users.show(screen_name=name)

def get_user_time_line(twitter_OAuth, name, count):
    return twitter_OAuth.statuses.user_timeline(screen_name=name, count=count)

def get_friends_list(twitter_OAuth):
    return twitter_OAuth.statuses.mentions_timeline()

#screen_name -> time_line
def protected_checker(twitter_OAuth, name):
    try:
        time_line = get_user_time_line(twitter_OAuth, name)
        return time_line
    except:
        print('this user has been protected:(')
        return 0



if __name__ == '__main__':

    MY_SCREEN_NAME = ''
    secret_json = {
  "access_token": "",
  "access_token_secret": "",
  "consumer_key": "",
  "consumer_secret": ""}

    m = MeCab.Tagger()
    vectorizer = CountVectorizer(min_df=1, stop_words=['こと','マン','さん','ちゃん'])

    t = twitter_access(secret_json)
    time_line = get_user_time_line(t,MY_SCREEN_NAME,200)


    all_text = []

    for post in time_line:
        #前処理１：メディアのURLを抜く
        text = post['text']
        if 'media' in post['entities'] :
            url = post['entities']['media'][0]['url']
            text = text.replace(url, "")
        #前処理２：リプのスクリーンネームを抜く
        if post['in_reply_to_user_id'] is not None:
            print(text)
            text = text.replace('@'+post['entities']['user_mentions'][0]['screen_name'], "")
        keywords = ""
        node = m.parseToNode(text)
        while node:
            meta = node.feature.split(",")
            if meta[0] == "名詞":
                keywords += node.surface + " "
            node = node.next
        all_text.append(keywords)

    X = vectorizer.fit_transform(all_text)
    print(vectorizer.get_feature_names())
