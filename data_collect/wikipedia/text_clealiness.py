# -*- coding:utf-8 -*-

import collections
import pickle
import re
import time
import argparse
import pandas as pd


def main():
    # parser = argparse.ArgumentParser(description='scrape data from wikipedia')
    # parser.add_argument('file', type=str, help='please enter correct data address(only for pickle)')
    # args = parser.parse_args()
    data=output('data/influence.pkl','biograph')
    # value for biograph
    missing=compute_missing_value(data,'biograph')
    cons=compute_consistency(data,'biograph')
    print('missing value for this attribute is:',missing)
    print('consistency value for this attribute is:',cons)


def output(file,attribute):
    #file --> file address
    #attribute --> attribute you want to generate dataset
    with open(file,'rb') as f:
        data=pickle.load(f)
    f.close()
    name,bio=data.keys(),data.values()
    temp_map=collections.defaultdict(int)
    temp_map['name']=name
    temp_map[attribute]=bio
    #generate dataframe
    data=pd.DataFrame(temp_map)
    return data

def compute_missing_value(data,attribute):
    #attribute --> the attribute to computer missing value
    data[attribute]=data[attribute].apply(lambda x:'no content' if x==[''] else x)
    print(data.shape)
    missing_sum = data[data[attribute]=='no content'].count()
    return missing_sum[0]/data.shape[0]

def compute_consistency(data,attribute):
    data[attribute] = data[attribute].apply(lambda x: 'no content' if x == [''] else x)

    #the num of valid information
    non_part=data.shape[0]-data[data[attribute]=='no content'].count()[0]


    data[attribute]=data[attribute].apply(lambda x:0 if re.search('</?ref',str(x)) else x)

    #num of data with tags
    num=data[data[attribute]==0].count()

    return num[0]/non_part


if __name__ == '__main__':
    main()