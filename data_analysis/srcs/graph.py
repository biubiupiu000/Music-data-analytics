# -*- coding:utf-8 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import numpy as np

def main():
    influence_graph()
    artists_graph()
    allfeature_graph()



def influence_graph():
    data = pd.read_csv('Data/inf_data_clean.csv')
    data['length'] = data['follower_active_start'] - data['influencer_active_start']
    # get data of graphs
    data_follow = data.groupby(['follower_main_genre'], as_index=False)['length'].mean()
    data_follow = pd.DataFrame(data_follow)
    data_influ = data.groupby(['influencer_main_genre'], as_index=False)['length'].mean()
    data_influ = pd.DataFrame(data_influ)

    print('start figuration')
    # hist of gap year
    fig = plt.figure()
    sns.histplot(data['length'], binwidth=10, alpha=0.7, edgecolor='r')
    plt.xlim((-70, 80))
    plt.title('hist of influence gap year', fontdict={'size': 12})
    plt.xlabel('influence gap year', fontdict={'size': 10})
    plt.ylabel('Frequency', fontdict={'size': 10})
    # plt.show()
    fig.savefig('gap year.png')
    plt.close(fig)

    # bar of influencer and follower
    fig = plt.figure(figsize=(23, 16))
    plt.barh(data_follow['follower_main_genre'], data_follow['length'], height=0.8, alpha=0.7)
    plt.ylabel('genre', fontdict={'size': 25})
    plt.xlabel('influence gap year', fontdict={'size': 25})
    plt.title('Correlation of follower\'s genre and gap year', fontdict={'size': 30})
    plt.tick_params(labelsize=21)
    # plt.show()
    fig.savefig('corr_follower_year.png')
    plt.close(fig)

    fig = plt.figure(figsize=(23, 16))
    plt.barh(data_influ['influencer_main_genre'], data_influ['length'], height=0.8, alpha=0.7)
    plt.ylabel('genre', fontdict={'size': 25})
    plt.xlabel('influence gap year', fontdict={'size': 25})
    plt.title('Correlation of influencer\'s genre and gap year', fontdict={'size': 30})
    plt.tick_params(labelsize=21)
    # plt.show()
    fig.savefig('corr_influencer_year.png')
    plt.close(fig)

    # distribution of genres by year
    data1 = data[['influencer_main_genre', 'influencer_active_start']]
    fig = plt.figure(figsize=(24, 13))
    for i in range(9):
        data2 = data1[data1['influencer_active_start'] == 1930 + i * 10]
        plt.subplot(331 + i)
        plt.ylabel('genre', fontdict={'size': 10})
        plt.xlabel('frequency', fontdict={'size': 10})
        plt.title('distribution of genres at ' + str(1930 + i * 10), fontdict={'size': 10})

        data2['influencer_main_genre'].value_counts().plot.barh(alpha=0.7)
    plt.suptitle('Distribution of influence genres', fontdict={'size': 30})
    # plt.show()
    fig.savefig('distribution of influence genre.png')
    plt.close(fig)

    data1 = data[['follower_main_genre', 'follower_active_start']]
    fig = plt.figure(figsize=(24, 13))
    for i in range(9):
        data2 = data1[data1['follower_active_start'] == 1930 + i * 10]
        plt.subplot(331 + i)
        plt.ylabel('genre', fontdict={'size': 10})
        plt.xlabel('frequency', fontdict={'size': 10})
        plt.title('distribution of genres at ' + str(1930 + i * 10), fontdict={'size': 10})

        data2['follower_main_genre'].value_counts().plot.barh(alpha=0.7)
    plt.suptitle('Distribution of follower genres', fontdict={'size': 30})
    # plt.show()
    fig.savefig('distribution of follower genre.png')
    plt.close(fig)
    print('influence figuration complete')


def artists_graph():
    q={}
    data = pd.read_csv('Data/clean_Artists.csv')
    #plot hist of popularity
    fig=plt.figure()
    sns.histplot(data['popularity'],binwidth=10,alpha=0.7)
    plt.title('hist of popularity',fontdict={'size':15})
    #plt.show()
    fig.savefig('hist_popularity.png')
    plt.close(fig)


    for i in range(data.shape[0]):
        genres=data.loc[i]['genres']
        genres=re.sub(r'[\[\]\']','',genres)
        genres=genres.split(sep=',')

        follower=data.loc[i]['followers']
        for g in genres:
            if g in q:
                q[g]+=follower
            else:
                q[g]=follower
    #plot hist of followers by genre
    # plt.figure()
    # p={'genre':q.keys(),'follower':q.values()}
    # data1=pd.DataFrame(p)
    # plt.ylim((0,1000))
    #
    # sns.histplot(data1['follower'],binwidth=50000000)
    # plt.show()
    # plt.close()

    #get top20 genres
    q=sorted(q.items(),reverse=True,key=lambda x:x[1])
    q=q[:20]
    fig=plt.figure(figsize=(24,13))
    plt.barh([i[0] for i in q],[i[1] for i in q])
    plt.xlabel('followers',fontdict={'size':25})
    plt.ylabel('top20 genres',fontdict={'size':25})
    plt.title('top20_genres',fontdict={'size':30})
    #plt.show()
    plt.savefig('top20_genres.png')
    plt.close(fig)
    #plot correlation
    fig=plt.figure()
    plt.scatter(data['popularity'],data['followers'])
    plt.xlabel('popularity',fontdict={"size":10})
    plt.ylabel('follower',fontdict={'size':10})
    plt.title('correlation of popularity and follower',fontdict={'size':15})
    plt.ylim((0,70000000))
    #plt.show()
    fig.savefig('corr_pop_follower.png')
    plt.close(fig)
    print('artists figuration complete')

def allfeature_graph():
    data=pd.read_csv('Data/clean_allfeature.for_all.csv')
    fig=plt.figure()
    sns.histplot(data['danceability'],binwidth=0.1)
    plt.title('hist of danceability', fontdict={'size': 15})
    fig.savefig('hist_danceability.png')
    plt.close(fig)
    # hist of danceability
    fig = plt.figure()
    sns.histplot(data['energy'], binwidth=0.1)
    plt.title('hist of energy', fontdict={'size': 15})
    fig.savefig('hist_energy.png')
    plt.close(fig)
    # hist of energy
    fig = plt.figure()
    sns.histplot(data['loudness'], binwidth=0.1)
    plt.title('hist of loudness', fontdict={'size': 15})
    fig.savefig('hist_loudness.png')
    plt.close(fig)
    # hist of loudness
    fig = plt.figure()
    sns.histplot(data['acousticness'], binwidth=0.1)
    plt.title('hist of acousticness', fontdict={'size': 15})
    fig.savefig('hist_acousticness.png')
    plt.close(fig)
    # hist of acousticness
    fig = plt.figure()
    sns.histplot(data['speechiness'], binwidth=0.1)
    plt.title('hist of speechiness', fontdict={'size': 15})
    fig.savefig('hist_speechiness.png')
    plt.close(fig)
    # hist of speechiness
    fig = plt.figure()
    sns.histplot(data['liveness'], binwidth=0.1)
    plt.title('hist of liveness', fontdict={'size': 15})
    fig.savefig('hist_liveness.png')
    plt.close(fig)
    # hist of liveness
    fig = plt.figure()
    sns.histplot(data['valence'], binwidth=0.1)
    plt.title('hist of valence', fontdict={'size': 15})
    fig.savefig('hist_valence.png')
    plt.close(fig)
    # hist of valence
    fig = plt.figure()
    sns.histplot(data['instrumentalness'], binwidth=0.1)
    plt.title('hist of instrumentalness', fontdict={'size': 15})
    fig.savefig('hist_instrumentalness.png')
    plt.close(fig)
    # hist of instrumentalness
    fig = plt.figure()
    sns.histplot(data['tempo'], binwidth=0.1)
    plt.title('hist of tempo', fontdict={'size': 15})
    fig.savefig('hist_tempo.png')
    plt.close(fig)
    # hist of tempo

    #corr of nine variables
    data = data[['danceability', 'energy', 'loudness', 'acousticness', 'speechiness', 'liveness',
                'valence', 'instrumentalness', 'tempo']]
    score=data.corr(method='spearman')
    score=score.applymap(lambda x:abs(x))
    #score.to_csv('../data/correlation.csv')
    fig=plt.figure()
    ax=fig.add_subplot(111)
    hot_img=ax.matshow(np.abs(score),vmin=0,vmax=1)
    fig.colorbar(hot_img,cmap='Qualitative')
    plt.title('correlation of song features')
    #fig.show()
    fig.savefig('corr_song.png')
    plt.close(fig)

    #scatter of specific variables
    fig=plt.figure(figsize=(25,15))
    #plt.subplot(131)
    data=data.sample(3000)
    plt.subplot(131)
    plt.scatter(data['energy'],data['acousticness'])
    plt.xlabel('energy',fontdict={'size': 15})
    plt.ylabel('acousticness',fontdict={'size': 15})
    plt.subplot(132)
    plt.scatter(data['energy'],data['loudness'])
    plt.xlabel('energy',fontdict={'size': 15})
    plt.ylabel('loudness',fontdict={'size': 15})
    plt.subplot(133)
    plt.scatter(data['acousticness'],data['loudness'])
    plt.xlabel('acousticness',fontdict={'size': 15})
    plt.ylabel('loudness',fontdict={'size': 15})
    #plt.show()
    fig.savefig('scatter_specific_variables.png')
    print('song figuration complete')



if __name__ == '__main__':
    main()
