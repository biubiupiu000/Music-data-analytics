# -*- coding:utf-8 -*-

import argparse
import collections
import pandas as pd
import json
import os

def main():
    parser = argparse.ArgumentParser(description='load data')
    parser.add_argument('file1', type=str)
    parser.add_argument('file2', type=str)
    args = parser.parse_args()
    merge(args.file1,args.file2)

def merge(file1,file2):
    #get name from other dataset
    # file1 --> influence csv
    #file2 --> json from Spotify

    data = pd.read_csv(file1)
    influencer = set(list(data['influencer_name']))
    follower = set(list(data['follower_name']))
    #union name of whole influencial dataset
    final_name = influencer.union(follower)

    musician=collections.defaultdict(int)
    with open(file2,'rb') as f:
        json_data=json.load(f)
        index=json_data.keys()
        for i in index:
            musician[i]=[]
            for j in json_data[i]:
                #print(j['name'])
                if j['name'] in musician:
                   continue
                else:
                   musician[i].append(j['name'])
    name=[]
    for i in musician.values():
        name=name+i
    #remove duplication and union all musician names
    name=set(name)
    final_name=final_name.union(name)
    data=pd.DataFrame(final_name,columns=['musician_name'])
    #write name to csv
    try:
        os.makedirs('temp')
        data.to_csv('name.csv')
    except:
        print('Has temp files')
    return final_name

if __name__ == '__main__':
    main()