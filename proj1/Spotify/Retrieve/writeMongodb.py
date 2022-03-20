import json
import pymongo

def writeMongodb():
    with open('alltracksFeature.json', mode='r', encoding='utf-8') as f:
        features = json.load(f)  # load raw data
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # edit the link to match your DB's credentials
    mydb = myclient["cs589"]
    mycol = mydb["allfeatures"]

    for genre in features:
        for artist in features[genre]:
            x = mycol[genre].insert_one({artist: features[genre][artist]})
            print(x.inserted_id)


if __name__ == '__main__':
    writeMongodb()
