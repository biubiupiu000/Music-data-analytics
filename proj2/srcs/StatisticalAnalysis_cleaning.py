import pandas as pd
import os
from sklearn.neighbors import LocalOutlierFactor as LOF

#get the datasets
def get_file():
    column = ['id_song', 'name_song', 'id_artist', 'name_artist', 'release_date', 'release_date_precision',
              'total_tracks', 'type_song', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
              'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'genres']

    df = pd.read_csv(f'{os.getcwd()}\Data\\clean_allfeature.for_all.csv', encoding='utf-8',
                     usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
                     )
    return df


# get the statistical analysis. Result are written to stat.csv & anomoly.csv
def StatisticalAnalysis():
    print('statistical analysis...')
    df=get_file()

    # output the statistical analysis:
    df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                   'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']].describe().to_csv(f'{os.getcwd()}\Data\\stat.csv', encoding='utf_8_sig')

    # LOF anomaly detection
    k = [10, 20, 30]  # set k=10,20,30
    anomaly = pd.DataFrame(columns=['k', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                 'instrumentalness','liveness', 'valence', 'tempo']) # result

    for k_ in k: # test LOF with different k
        model = LOF(n_neighbors=k_, contamination=0.001)  # set the contamination to 0.1%
        # attribute can be used in anomaly detection: 'danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo'

        x = df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'tempo']].values.tolist()
        # model.fit(x)
        y = model.fit_predict(x)

        for i in range(len(y)):  # print the anomaly
            if y[i] == -1:
                new=pd.DataFrame({"k":k_,"danceability":df['danceability'][i],"energy":df['energy'][i],"key":df['key'][i],"loudness":df['loudness'][i],"mode":df['mode'][i],
                                  "speechiness":df['speechiness'][i],"acousticness":df['acousticness'][i],"instrumentalness":df['instrumentalness'][i],"liveness":df['liveness'][i],
                                  "valence":df['valence'][i],"tempo":df['tempo'][i]},index=[1])
                anomaly=anomaly.append(new,ignore_index=True)
                del new


    anomaly.to_csv(f'{os.getcwd()}\Data\\anomaly.csv', encoding='utf_8_sig')



# data cleaning insight
def cleaning():
    print('cleaning...')
    # Since there is not necessary to delete or adjust the data, the function remains empty.
    # df=get_file()
    # del df

#binning method
def binning():
    print('binning...')
    df=get_file()
    key_region=[]

    for k in df['key']:
        key_region.append(int(k/4))# divide the key into 3 part.

    if df.shape[0]==len(key_region):# create new coloumn
        df['key_region']=key_region
        df.to_csv(f'{os.getcwd()}\Data\\clean_allfeature_binning.csv', encoding='utf_8_sig')
    else:
        print('wrong')

    del df



if __name__ == '__main__':
    StatisticalAnalysis()
    cleaning()
    binning()







