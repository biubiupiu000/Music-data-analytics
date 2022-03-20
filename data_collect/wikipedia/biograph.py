# -*- coding:utf-8 -*-

import collections
import time
import pickle
import mwclient
from mediawiki import MediaWiki
from get_name import merge
import re
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='scrape data from wikipedia')
    parser.add_argument('mode', type=str,help='only have text or tags mode')
    args = parser.parse_args()
    file1=input('please enter data address')
    file2=input('please enter json address')
    data=merge(file1,file2)
    bio_map=collections.defaultdict(int)
    scrape_bio(data,bio_map,args.mode)

def scrape_bio(names,dict_bio,mode):
    #user_agent should follow the Wikipedia policy(must include contact info.)
    #choose one way to scrape data(has text or text with tags)
    wikipedia = MediaWiki(
        user_agent='Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36')
    site = mwclient.Site('en.wikipedia.org', clients_useragent='Mozilla/5.0 ')
    start=time.time()
    if mode=='text':
        for name in names:
            try:
                #use scraperobot by wikipedia
                scrape = wikipedia.page(name)
                con = scrape.summary
                dict_bio[name]=con
            except:
                dict_bio[name]='no content'
    elif mode=='tags':
        for name in names:
            try:
                start_page=site.Pages[name]
                text=start_page.text(section=0).split(sep='\n')
                for i in range(len(text)):
                    if re.match(r'\'\'',text[i]):
                        #join all split info
                        text=''.join(text[i:])
                        break
                if text and text!=['']:
                    dict_bio[name]=text
                else:
                    dict_bio[name]='no content'
            except:
                dict_bio[name]='no content'
    try:
        os.makedirs('data')
    except:
        print('Has temp files')
    #write biograph
    with open(r'data/biograph.pkl', 'wb') as f:
        pickle.dump(dict_bio, f)
    f.close()



if __name__ =='__main__':
    main()