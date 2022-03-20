import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import f_oneway
import argparse

FEATURES = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']


def main():
    parser = argparse.ArgumentParser()  # parse arguments
    parser.add_argument('-s', '--songpath', dest='spath', required=True)
    parser.add_argument('-i', '--influencepath', dest='ipath', required=True)
    args = parser.parse_args()

    songs = pd.read_csv(args.spath)  # read dataset
    songs.set_index('name_artist', inplace=True, drop=False)  # build index for better search performance

    artists = pd.read_csv(args.ipath)  # read dataset

    influence = dict()
    for index, i in artists.iterrows():  # group followers by influencers
        iname = i['influencer_name']
        if iname in influence:
            influence[iname].append(i['follower_name'])
        else:
            influence[iname] = [i['follower_name']]

    groups = []
    for index, i in enumerate(influence.values()):  # get followers' songs for each group
        follower_songs = []
        for j in i:
            if j in songs['name_artist']:
                follower_songs.append(songs[songs['name_artist'] == j][FEATURES])
        if len(follower_songs) == 0:
            continue
        groups.append(pd.concat(follower_songs)[FEATURES].values)

    _, p = f_oneway(*groups)  # perform ANOVA for all groups and calculate p-value
    for index, i in enumerate(FEATURES):
        print('The p-value of ' + i + 'among all groups is %f' % p[index])
    print()

    Ps = [f_oneway(i, songs[FEATURES].values)[1] for i in
          groups]  # perform ANOVA for each group against the whole dataset and calculate p-value

    print('The following is the count within each feature of how many groups are considered ' +
          'statistically significant for being influenced:')
    Ps = np.array(Ps)
    count = [np.where(Ps[:, i] < 0.05)[0].size for i in range(len(FEATURES))]  # count the number of groups with p<0.05
    for index, i in enumerate(FEATURES):
        print('For feature ' + i + ', %d among %d' % (count[index], len(groups)))

    print('\nShowing boxplots between whole dataset against groups with smallest 5 p-values.')
    for index, i in enumerate(FEATURES):  # iterate within features
        smallest = Ps[:, index].argsort()[:5]  # get index of 5 groups have least p-value
        origin = [pd.DataFrame(data=songs[i].values, columns=['All'])]  # prepare the feature of all data
        origin.extend([pd.DataFrame(data=groups[k][:, index], columns=[ind + 1]) for ind, k in enumerate(smallest)])
        # concat the groups and whole dataset
        df = pd.concat(origin)
        plt.title(i)
        df.boxplot()  # plot boxplots
        plt.show()


if __name__ == '__main__':
    main()
