# -*- coding:utf-8 -*-

import collections
import time
import pickle
import mwclient
from get_name import merge
import re
import os
import argparse

def main():

    file1=input('please enter data address')
    file2=input('please enter json address')
    data=merge(file1,file2)
    influ_map=collections.defaultdict(int)
    scrape_influ(data,influ_map)

def scrape_influ(names, dict_influ):
    #user_agent should follow the Wikipedia policy(must include contact info.)
    #choose one way to scrape data(has text or text with tags)
    site = mwclient.Site('en.wikipedia.org', clients_useragent='Mozilla/5.0 ')
    # start=time.time()
    for name in names:
        try:
            start_page = site.Pages[name]
            text=start_page.text().split(sep='\n')
            for i in range(len(text)):
                if re.match(r'^==',text[i]):
                    if record:
                        dict_influ[name]= ''.join(text[index + 1:i])
                        record=False
                        break
                if re.match(r'^==.*[Ii]nfluence.*',text[i]):
                    # print(name)
                    index=i
                    record=True
        except:
            dict_influ[name]= 'no content'
        if not dict_influ.get(name):
            dict_influ[name]= 'no content'
    try:
        os.makedirs('data')
    except:
        print('Has temp files')
    #write influence text
    with open(r'data/influence.pkl', 'wb') as f:
        pickle.dump(dict_influ, f)
    f.close()


if __name__ =='__main__':
    main()