import pandas as pd
import os

#get the artists file (Artists.csv)
def get_Datasets_Artists(filename):
    df = pd.read_csv(f'{os.getcwd()}\Data\\{filename}', usecols=[1, 2, 3, 4, 5, 6],
                     names=['name', 'id', 'followers', 'popularity', 'type', 'genres'], encoding='utf-8')
    df = df.drop(df.index[0])

    return df

#get the songs file(allfeature.for_all.csv)
def get_Datasets_Songs(filename):
    column = ['id_song', 'name_song', 'id_artist', 'name_artist', 'release_date', 'release_date_precision',
              'total_tracks', 'type_song', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
              'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'genres']

    df = pd.read_csv(f'{os.getcwd()}\Data\\{filename}', encoding='utf-8',
                     usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                     names=column)  # the file must already in the Data file. if not, run the build_csv.py to create the allfeature.for_all.csv file, or download at the link at ReadMe.
    return df


def get_mean_value(array):
    sum=0
    count=0
    for a in array: # get the mean value
        if a!=None:
            sum+=a
            count+=1

    return (sum/count)


def cleanDatasets():

    # Artists data(artists.csv)
    filename=['artists.csv','allfeature.for_all.csv']
    df=get_Datasets_Artists(filename[0])

    # remove the duplicatesa
    df=df.drop_duplicates(subset='id', keep='first')
    # build csv
    print(df.shape)
    df['index']=range(df.shape[0])
    df.set_index('index')
    df=df.reset_index(drop=True)
    df.drop(['index'], axis=1, inplace=True)
    df.to_csv(f'{os.getcwd()}\Data\\clean_{filename[0]}', encoding='utf_8_sig')
    del df


    # Song_data(allfeature.for_all.csv)
    df=get_Datasets_Songs(filename[1])

    # remove the duplicate
    df.drop_duplicates(subset='id_song', keep='first',inplace=True)
    df.drop(df[df['loudness']>=0].index,inplace=True)

    # drop the row that cannot be replace
    df.dropna(subset=['name_song'],inplace=True)
    df.dropna(subset=['tempo'], inplace=True)
    df.dropna(subset=['type'],inplace=True)

    # noise value
    mean=get_mean_value(df['tempo'])
    df['tempo'].loc[df['tempo']<=0]=mean

    # missing value
    # fill the mean value
    mean = get_mean_value(df['danceability'])
    df['danceability'].fillna(mean,inplace=True)
    mean = get_mean_value(df['energy'])
    df['energy'].fillna(mean, inplace=True)
    mean = get_mean_value(df['key'])
    df['key'].fillna(mean, inplace=True)
    mean = get_mean_value(df['loudness'])
    df['loudness'].fillna(mean, inplace=True)
    mean = get_mean_value(df['mode'])
    df['mode'].fillna(mean, inplace=True)
    mean = get_mean_value(df['speechiness'])
    df['speechiness'].fillna(mean, inplace=True)
    mean = get_mean_value(df['acousticness'])
    df['acousticness'].fillna(mean, inplace=True)
    mean = get_mean_value(df['instrumentalness'])
    df['instrumentalness'].fillna(mean, inplace=True)
    mean = get_mean_value(df['liveness'])
    df['liveness'].fillna(mean, inplace=True)
    mean = get_mean_value(df['valence'])
    df['valence'].fillna(mean, inplace=True)

    df['index']=range(df.shape[0])
    df.set_index('index')
    df=df.reset_index(drop=True)
    df.drop(['index'], axis=1, inplace=True)


    # build csv
    df.to_csv(f'{os.getcwd()}\Data\\clean_{filename[1]}', encoding='utf_8_sig')

    del df


if __name__ == '__main__':
    cleanDatasets()

