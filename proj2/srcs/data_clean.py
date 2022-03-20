# -*- coding:utf-8 -*-

import pickle
import pandas as pd
import argparse
import os
import re
def main():

    clean_influence()
    clean_text()

def clean_influence():

    data = pd.read_csv('Data/influence_data.csv')
    data = data[~(data['influencer_main_genre'].isin(['Unknown']) | data['follower_main_genre'].isin(['Unknown']))]
    data = data[
        ~(data['influencer_main_genre'].isin(['Children\'s']) | data['follower_main_genre'].isin(['Children\'s']))]
    if os.path.exists('Data'):
        data.to_csv('Data/inf_data_clean.csv',index=False)
    else:
        os.makedirs('Data')
        data.to_csv('Data/inf_data_clean.csv',index=False)
    print('influence data cleariness complete')

def clean_text():
    pre = re.compile(r'(>(\{.*?}?)+<)')
    with open('Data/influence.pkl', 'rb') as f:
        data = pickle.load(f)
        num = 0
        for i, j in data.items():
            if j != 'no content':
                j = re.sub(pre, '><', j)
                j = re.sub(r'<[^<]*?>', '', j)
                j = re.sub(r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", "", j)
                j = re.sub(r'[\[\]{}()\']', '', j)
                j = re.sub(r'\|', ' ', j)
                data[i] = j

                num += 1
    a = {'name': data.keys(), 'influence': data.values()}
    influence = pd.DataFrame(a)
    f.close()
    with open('Data/biograph.pkl', 'rb') as f:
        data = pickle.load(f)
        for i, j in data.items():
            if j != 'no content' and j != ['']:
                try:
                    j = re.sub(pre, '><', j)

                    j = re.sub(r'<[^<]*?>', '', j)
                    # j = re.sub(r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", "", j)
                    j = re.sub(r'[\[\]{}()\']', '', j)
                    j = re.sub(r'\|', ' ', j)
                    data[i] = j
                except:
                    continue
    a = {'name': data.keys(), 'biography': data.values()}
    bio = pd.DataFrame(a)
    bio['biography'] = bio['biography'].apply(lambda x: x if x != [''] else 'no content')
    f.close()
    data = bio.merge(influence, on=['name'])
    data.to_csv('Data/text_clean.csv',index=False)
    print('text data cleaniness complete')





if __name__ == '__main__':
    main()