import pandas as pd
import os


#Artists data(artists.csv)
print('-'*50)
print('Artists data(artists.csv)')
print('-'*50)
df=pd.read_csv(f'{os.getcwd()}\Data\\Artists.csv',usecols=[1,2,3,4,5,6],names=['name','id','followers','popularity','type','genres'],encoding='utf-8')
df=df.drop(df.index[0])

#show the first 5 of the datasets
print(df.head(5))


#check each data type in all column
print('-----data type for each column-----')
print(df.dtypes)


#show how many index and column
print('-----shape of datasets-----')
print(df.shape)


#show the total amount of data
print('-----total data amount-----')
print(df.shape[0]*df.shape[1])


#check the missing value
print('-----check the missing value (numbers)-----')
print(df.isnull().sum().sort_values(ascending=False))
print('-----check the missing value (percentage%)-----')
print(df.isnull().sum().sort_values(ascending=False)[:]/df.shape[0]*100)


#check the noise
print("-----checking the data noise-----")
#id
print('1.id')
tmp=0
for i in df['id']:
    if len(i)!=22 or not i.isalnum():
        tmp+=1
print(f'the noise number in id is {tmp}')
print(f'the noise number are {tmp/df.shape[0]*100}%')

#followers
print('2.followers')
tmp=0
for i in df['followers']:
    if(type(eval(i))!=int) or int(i)<0:
        tmp+=1
print(f'the noise number in followers is {tmp}')
print(f'the noise number are {tmp/df.shape[0]*100}%')

#popularity
print('popularity')
tmp=0
for i in df['popularity']:
    if(type(eval(i))!=int) or int(i)<0:
        tmp+=1
print(f'the noise number in popularity is {tmp}')
print(f'the noise number are {tmp/df.shape[0]*100}%')

#type
print('type')
tmp=0
for i in df['type']:
    if i !='artist':
        tmp+=1
print(f'the noise number in type is {tmp}')
print(f'the noise number are {tmp/df.shape[0]*100}%')


#duplication
print('-----check duplication-----')
tmp=0
print(f'the duplicate number are {len(df["id"])-len(set(df["id"]))}')
print(f'{(len(df["id"])-len(set(df["id"])))/len(df["id"])*100}% are duplicated')

del df





#Songs data(allfeature.for_all.csv)
print('-'*50)
print('Songs data(allfeature.for_all.csv)')
print('-'*50)

#open the datasets
column=['id_song', 'name_song', 'id_artist', 'name_artist', 'release_date', 'release_date_precision',
            'total_tracks', 'type_song', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type','genres']


df=pd.read_csv(f'{os.getcwd()}\Data\\allfeature.for_all.csv',encoding='utf-8',
            usecols=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],
            names=column)# the file must already in the Data file. if not, run the build_csv.py to create the allfeature.for_all.csv file, or download at the link at ReadMe.


#show the first 5 of the datasets
print(df.head(5))


#check each data type in all column
print('-----data type for each column-----')
print(df.dtypes)


#show how many index and column
print('-----shape of datasets-----')
print(df.shape)


#show the total amount of data
print('-----total data amount-----')
print(df.shape[0]*df.shape[1])


#check the missing value
print('-----check the missing value (numbers)-----')
print(df.isnull().sum().sort_values(ascending=False))
print('-----check the missing value (percentage%)-----')
print(df.isnull().sum().sort_values(ascending=False)[:]/df.shape[0]*100)


#check the data format
#id data
print('------check the data format-----')
print('1.id data')
col=['id_song','id_artist']
for c in col:
    tmp = 0
    for i in range(df.shape[0]):
        if not df[c][i].isalnum() or len(df[c][i])!=len(df[c][0]):
            tmp+=1
    print(f'{tmp} numbers of id in \'{c}\' are in wrong format, which has percentage {tmp/df.shape[0]*100}%.')


#datetime data
print('2.datetime data')
pd.to_datetime(df['release_date'],format='%Y/%m/%d',errors='coerce')
tmp=0
for i in range(df.shape[0]):
    if df['release_date'][i]==None:
        tmp+=1
print(f'There are {tmp/df.shape[0]*100}% of wrong datetime value')

tmp=0
for d in df['release_date_precision']:
    if d=='year':
        tmp+=1
print(f'the number of datetime in format with only year is {tmp}, which has {tmp/df.shape[0]*100}% in the total column.')


#track data
print('3.track data')
tmp=0
temp=[]
for i in range(df.shape[0]):
    if int(df['total_tracks'][i])<=0:
        temp.append(df['total_tracks'][i])
        tmp+=1
print(f'The percentage of noise in the track data is {tmp/df.shape[0]*100}%')
if temp!=[]:
    print('The noise is:')
    print(temp)



#data type
print('4.datatype')
tmp=0
temp=[]
for i in range(df.shape[0]):
    if df['type_song'][i]!='track':
        temp.append(df['type_song'][i])
        tmp+=1
print(f'The percentage of noise in the data_type is {tmp/df.shape[0]*100}%')
if temp!=[]:
    print('The noise is:')
    print(temp)


#features_data
print('5.features_data')
for i in range(df.shape[0]):
    tmp=[0,0,0,0,0,0,0]
    if df['danceability'][i]<0 and df['danceability'][i]>=1:
        print(df['danceability'][i])
        tmp[0]+=1
    if df['energy'][i]<0 and df['energy'][i]>=1:
        tmp[1]+=1
    if df['speechiness'][i]<0 and df['speechiness'][i]>=1:
        tmp[2] += 1
    if df['acousticness'][i]<0 and df['acousticness'][i]>=1:
        tmp[3] += 1
    if df['instrumentalness'][i]<0 and df['instrumentalness'][i]>=1:
        tmp[4] += 1
    if df['liveness'][i]<0 and df['liveness'][i]>=1:
        tmp[5] += 1
    if df['valence'][i]<0 and df['valence'][i]>=1:
        tmp[6] += 1

for i in tmp:
    print(f'The noise number is{i}')


#tempo number
print('6.tempo number')
tmp=0
for i in range(df.shape[0]):
    if df['tempo'][i]<=0:
        tmp+=1
print(f'There is {tmp} number in tempo, which has percentage {tmp/df.shape[0]*100}')


#check duplication
print('-----check the id duplication-----')
col=['id_song','id_artist']
tmp2=[]
for i in range(df.shape[0]):
    tmp2.append(f'{df[col[0]][i]}{df[col[1]][i]}')

print(f'There are {len(tmp2)-len(set(tmp2))} songs with the same song_id and the same artist_id, which has percentage {(len(tmp2)-len(set(tmp2)))/len(tmp2)}%')






