import pandas as pd
import numpy as np
import sklearn
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import k_means
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
import argparse

features = ['danceability', 'energy', 'key', 'loudness', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']


def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--bestattr', dest='bestattr', action='store_true', default=False)
    parser.add_argument('-p', '--path', dest='path', required=True)
    parser.add_argument('-f', '--frac', dest='frac', default=0.01, type=float)
    args = parser.parse_args()
    # read data and take samples
    df = pd.read_csv(args.path)
    samples = df.sample(frac=args.frac, random_state=0)
    plt.figure(figsize=(8, 9))
    # standardize
    x = samples.loc[:, features].values
    x = StandardScaler().fit_transform(x)
    # PCA
    pca = PCA(n_components=2, random_state=0)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=principalComponents, columns=['principal component 1', 'principal component 2'])
    # plot graph and compute metrics
    plot_kmeans(x, principalDf, samples, args.bestattr)

    plot_hierarchical(x, principalDf, samples, args.bestattr)

    plot_dbscan(x, principalDf, samples, args.bestattr)

    plot_gaussian(x, principalDf, samples, args.bestattr)
    # show plot
    plt.tight_layout()
    plt.show()


def plot_kmeans(x, principalDf, samples, bestattr):
    kmeans_model = k_means(x, n_clusters=4, random_state=1)  # do k-means
    cluster_labels = kmeans_model[1]  # get labels
    plt.subplot(221)  # create subplot
    plot(samples, principalDf, cluster_labels,
         bestattr)  # plot on subplot. if bestattr is True, plot the projection in best attribute pair
    plt.title('K-Means')  # add title
    kmeans_s_score = metrics.silhouette_score(x, cluster_labels, metric='euclidean')  # compute metrics
    kmeans_c_score = metrics.calinski_harabasz_score(x, cluster_labels)
    print('Calinski-Harabasz Index of K-Means:' + str(kmeans_c_score))


def plot_hierarchical(x, principalDf, samples, bestattr):
    hierarchical_model = AgglomerativeClustering(n_clusters=3, linkage='ward')  # create model
    hierarchical_model.fit(x)  # fit model
    plt.subplot(222)  # create subplot
    plot(samples, principalDf, hierarchical_model.labels_, bestattr)
    plt.title('Hierarchical')
    hierarchical_s_score = metrics.silhouette_score(x, hierarchical_model.labels_, metric='euclidean')
    hierarchical_c_score = metrics.calinski_harabasz_score(x, hierarchical_model.labels_)
    print('Calinski-Harabasz Index of Ward:' + str(hierarchical_c_score))


def plot_dbscan(x, principalDf, samples, bestattr):
    dbscan_model = DBSCAN(eps=2, min_samples=4)
    dbscan_model.fit(x)
    plt.subplot(223)
    plot(samples, principalDf, dbscan_model.labels_, bestattr)
    plt.title('DBScan')
    dbscan_s_score = metrics.silhouette_score(x, dbscan_model.labels_, metric='euclidean')
    dbscan_c_score = metrics.calinski_harabasz_score(x, dbscan_model.labels_)
    print('Calinski-Harabasz Index of DBSCAN:' + str(dbscan_c_score))


def plot_gaussian(x, principalDf, samples, bestattr):
    gaussian_model = GaussianMixture(n_components=2, random_state=0)
    gaussian_model.fit(x)
    Y_ = gaussian_model.predict(x)
    splot = plt.subplot(224)
    plot(samples, principalDf, Y_, bestattr)
    plt.title('Gaussian mixture')
    gaussian_s_score = metrics.silhouette_score(x, Y_, metric='euclidean')
    gaussian_c_score = metrics.calinski_harabasz_score(x, Y_)
    print('Calinski-Harabasz Index of Gaussian Mixture:' + str(gaussian_c_score))


def plot(samples, principalDf, lables, bestattr):
    if bestattr:
        m, mi, mj = 0, 0, 0
        for i in range(len(features)):  # find the attribute pair with largest C-H index
            for j in range(i + 1, len(features)):
                t = metrics.calinski_harabasz_score(list(zip(samples[features[i]].values, samples[features[j]].values)),
                                                    lables)
                if t > m:
                    m, mi, mj = t, i, j
        plt.scatter(samples[features[mi]], samples[features[mj]], .8, c=lables)
        plt.xlabel(features[mi])
        plt.ylabel(features[mj])
    else:
        plt.scatter(principalDf['principal component 1'], principalDf['principal component 2'], .4, c=lables)


if __name__ == '__main__':
    main()
