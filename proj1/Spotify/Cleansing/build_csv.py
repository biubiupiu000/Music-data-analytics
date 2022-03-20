import os
import bson
import json
import pandas as pd
from itertools import chain

#bulid csv for artist
filepath = f'{os.getcwd()}\Data\\artists.json' #get the data file path(all the data should store in the Data file)
with open(filepath,'r',encoding='utf-8') as f:
    Artist=json.load(f)


#get the file name of all the filetype data
def get_filename(filepath,filetype):
    tmp=[]
    for root, dirs, files in os.walk(filepath):
        for i in files:
            if filetype in i:
                tmp.append(f'{filepath}\{i}')
    return tmp


# Convert data from json dictionary to dataframe
# both function get_target_value and _get_value is use to obtain the value in the given key.
def get_target_value(key,dic,tmp_list,p=None):#if the input data is dictionary
    if not isinstance(dic,dict) or not isinstance(tmp_list,list):
        return "not a list or dict"
    if p==f'{os.getcwd()}\Data\\allfeatures.turkish.bson':
        if len(str(dic.keys())) < 233 and len(str(dic.keys())) > 150:
            tmp_list.append({'danceability': None, 'energy': None, 'key': None, 'loudness': None, 'mode': None,
                            'speechiness': None, 'acousticness': None, 'instrumentalness': None, 'liveness': None,
                            'valence': None, 'tempo': None, 'type': None, 'id': '0wyAE7rd2H4EVVKKqwDUZt',
                            'uri': None, 'track_href': None, 'analysis_url': None, 'duration_ms': None,
                            'time_signature': None})
    if key in dic.keys():
        tmp_list.append(dic[key])
    else:
        for value in dic.values():
            if isinstance(value,dict):
                get_target_value(key,value,tmp_list,p)
            elif isinstance(value,(list,tuple)):
                _get_value(key,value,tmp_list,p)
    return tmp_list

def _get_value(key,val,tmp_list,p=None):#if the input data is list
    for val_ in val:
        if isinstance(val_,dict):
            get_target_value(key,val_,tmp_list,p)
        elif isinstance(val_,(list,tuple)):
            _get_value(key,val_,tmp_list,p)


tmp=[]

# Convert data from json dictionary to dataframe
#obtain the data with attributes: name, id, genres, popularity, type
name=get_target_value('name',Artist,tmp)
tmp=[]
id=get_target_value('id',Artist,tmp)
tmp=[]
followers=get_target_value('total',Artist,tmp)
tmp=[]
popularity=get_target_value('popularity',Artist,tmp)
tmp=[]
type=get_target_value('type',Artist,tmp)
tmp=[]
genres=get_target_value('genres',Artist,tmp)

df=pd.DataFrame({'name':name,'id':id,'followers':followers,'popularity':popularity,'type':type,'genres':genres})

# df = df.drop_duplicates(subset=['id'],#duplicate by 'id'
#                         keep='first'
# )

#output the artists.csv file
df.to_csv(f'{filepath[:-4]}csv',encoding='utf_8_sig')
print(f'Success in output the file {filepath[:-4]}csv')

#free data
del df




#build the csv for song at allfeature.for_all

filepath = f'{os.getcwd()}\Data' #get the data file path(all the data should store in the Data file)
filetype ='.bson'#choose the data type



# get all the data from the filetype(bson) file at the Data file.
file_list=get_filename(filepath,filetype)
for path in file_list:
    bson_file = open(path, 'rb')
    bson_data = bson.decode_all(bson_file.read())


    #temporary list to store the needed data
    tmp = []
    name_song = []
    name_artist = []
    id_song = []
    id_artist = []
    release_date = []
    release_date_precision = []
    total_tracks = []
    type_song = []
    audio_features = []


    # obtain the value from the dictionary: id,name,release_date,release_date_precision,total_tracks,type,audio_features
    for data in bson_data:
        for key, value in data.items():
            if key != '_id':
                name_artist.append(str(key))
            else:
                id_artist.append(str(value))

        tmp = []
        name_song.append(get_target_value('name', data, tmp))
        tmp = []
        id_song.append(get_target_value('id', data, tmp))
        tmp = []
        release_date.append(get_target_value('release_date', data, tmp))
        tmp = []
        release_date_precision.append(get_target_value('release_date_precision', data, tmp))
        tmp = []
        total_tracks.append(get_target_value('total_tracks', data, tmp))
        tmp = []
        type_song.append(get_target_value('type', data, tmp))
        tmp = []
        audio_features.append(get_target_value('audio_features', data, tmp,path))
        tmp = []


    #temporary list to store the feature data
    danceability = []
    energy = []
    key = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    liveness = []
    instrumentalness = []
    valence = []
    tempo = []
    type = []


    #obtain the audio feature data

    features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'tempo', 'type']
    features_set = [danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness,
                    valence, tempo, type]

    for ft in audio_features:
        for each_feature in ft:
            if not isinstance(each_feature, dict):
                for i in range(len(features)):
                    features_set[i].append(None)
            else:
                for i in range(len(features)):
                    features_set[i].append(each_feature[features[i]])

    tmp = []
    tmp2 = []
    for i in range(len(id_song)):
        for j in range(len(id_song[i])):
            tmp.append(name_artist[i])
            tmp2.append(id_artist[i])

    name_artist = tmp
    id_artist = tmp2
    del tmp
    del tmp2


    #change the list format
    name_song = list(chain.from_iterable(name_song))
    id_song = list(chain.from_iterable(id_song))
    release_date = list(chain.from_iterable(release_date))
    release_date_precision = list(chain.from_iterable(release_date_precision))
    total_tracks = list(chain.from_iterable(total_tracks))
    type_song = list(chain.from_iterable(type_song))


    #create final DataFrame
    df = pd.DataFrame({'id_song': id_song,
                       'name_song': name_song,
                       'id_artist': id_artist,
                       'name_artist': name_artist,
                       'release_date': release_date,
                       'release_date_precision': release_date_precision,
                       'total_tracks': total_tracks,
                       'type_song': type_song,
                       'danceability': danceability,
                       'energy': energy,
                       'key': key,
                       'loudness': loudness,
                       'mode': mode,
                       'speechiness': speechiness,
                       'acousticness': acousticness,
                       'instrumentalness': instrumentalness,
                       'liveness': liveness,
                       'valence': valence,
                       'tempo': tempo,
                       'type': type,
                       'genres': path.split('.')[-2]})


    #output the file to csv, not re-wirte the csv.
    df.to_csv(f'{os.getcwd()}\Data\\allfeature.for_all.csv',header=False, mode='a',encoding='utf_8_sig')

    print(f'Success in output the file {path}')

    #free the data
    del df
    del bson_data