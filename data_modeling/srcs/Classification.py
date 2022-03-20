# -*- coding:utf-8 -*-

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import k_means
from sklearn.preprocessing import label_binarize
import seaborn as sns
from parameters import *

'''
sample_mode: The default is False. It would use the whole data.
            True is down_sampling If you choose down_sampling, the results gained will have minor differences.          
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--sample_mode', default=False)
    args = parser.parse_args()

    data = pd.read_csv('Data/clean_allfeature.for_all.csv', index_col=0)
    attris = ['danceability',
              'energy', 'loudness', 'mode', 'speechiness', 'acousticness',
              'instrumentalness', 'liveness', 'valence', 'tempo', 'genres']
    temp_data = data[attris]
    sta_data = temp_data.groupby('genres').agg('mean')
    sta_data = sta_data.values
    sta_data = StandardScaler().fit_transform(sta_data)
    types = 10
    songs = cluster(data, sta_data, types)
    for i in range(types):
        q = [k for k, j in songs.items() if j == i]
        print('genres in the cluster '+str(i)+' is:', q)
    data = data[data['genres'].isin(songs)]

    # feature normalize
    for i in ['danceability',
              'energy', 'loudness', 'speechiness', 'acousticness',
              'instrumentalness', 'liveness', 'valence', 'tempo']:
        # M, m = data[i].max(), data[i].min()
        # print(M,m)
        # data[i]=data[i].apply(lambda x:x-m/(M-m))
        temp = data[i].to_numpy()
        temp = (temp - np.min(temp)) / (np.max(temp) - np.min(temp))
        data[i] = temp

    attris = ['danceability',
              'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
              'instrumentalness', 'liveness', 'valence', 'tempo', 'genres']
    data = data[attris]

    # map y-value
    data['genres'] = data['genres'].map(songs)

    # lower sampling
    min_num = min(data['genres'].value_counts())
    data0 = pd.DataFrame()
    for i in range(types):
        temp_data = data[data['genres'] == i]
        index = np.random.randint(len(temp_data), size=min_num)
        lower_data = temp_data.iloc[list(index)]
        data0 = pd.concat([data0, lower_data])

    # split data
    if args.sample_mode:
        X_train, X_validate, Y_train, Y_validate = split(data0)
    else:
        X_train, X_validate, Y_train, Y_validate = split(data)
    '''
    Grid search for parameters
    '''
    # parameters={'max_depth':[15,16,17,18,19,20],'min_samples_leaf': [8,9]}
    # parameters={'p':[1,2],'weights':['uniform','distance'],'n_neighbors':[5,10,15,20]}
    # dt1=RandomForestClassifier()
    # best_params=grid_search(dt1,parameters,X_train,Y_train)

    # models
    dt1 = DecisionTreeClassifier(**dt_parameters)
    Model(dt1, X_train, Y_train, X_validate, Y_validate, types, 'Decision Tree')
    dt2 = GaussianNB()
    Model(dt2, X_train, Y_train, X_validate, Y_validate, types, 'Bayes')
    dt3 = RandomForestClassifier(**rf_parameters)
    Model(dt3, X_train, Y_train, X_validate, Y_validate, types, 'Random Forest')
    dt4 = KNeighborsClassifier(**knn_parameters)
    Model(dt4, X_train, Y_train, X_validate, Y_validate, types, 'Knn')


def split(data):
    valueArray = data.values
    X = valueArray[:, 0:-1]
    Y = valueArray[:, -1]
    test_size = 0.2
    seed = 5
    x_train, x_validate, y_train, y_validate = train_test_split(X, Y,
                                                                test_size=test_size, random_state=seed)
    return x_train, x_validate, y_train, y_validate


def grid_search(model, params, x_data, y_data):
    clf = GridSearchCV(model, param_grid=params, cv=5, scoring='f1_micro')
    clf.fit(x_data, y_data)
    print(clf.best_score_, clf.best_params_)
    return clf.best_params_


def cluster(ori_data, data, nums):
    kmeans_model = k_means(data, n_clusters=nums, random_state=1)
    cluster_labels=kmeans_model[1]
    songs={}
    c = ori_data['genres'].value_counts()
    d = ori_data['genres'].unique()
    n=0
    for i in range(len(d)):
        # if c[d[i]]>9000:
        #     songs[d[i]]=n
        #     n+=1
        songs[d[i]]=cluster_labels[i]
    return songs


def Model(model, x_train, y_train, x_valid, y_valid, nums, name):

    model.fit(x_train, y_train)
    dt_predictions = model.predict(x_valid)
    print(name+' accuracy is:', round(accuracy_score(y_valid, dt_predictions),4))
    y_roc, pre_roc = label_binarize(y_valid, classes=[i for i in range(nums)]), label_binarize(dt_predictions,
                                                                                                   classes=[i for i in
                                                                                                            range(
                                                                                                              nums)])
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(nums):
        fpr[i], tpr[i], _ = roc_curve(y_roc[:, i], pre_roc[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(nums)]))
    mean_tpr = np.zeros_like(all_fpr)
    fig=plt.figure()
    for i in range(nums):
        plt.plot(fpr[i], tpr[i], lw=2,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                       ''.format(i, roc_auc[i]))
    fpr["micro"], tpr["micro"], _ = roc_curve(y_roc.ravel(), pre_roc.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    plt.plot(fpr["micro"], tpr["micro"],label='average ROC curve (area = {0:0.2f})'''.format(roc_auc["micro"]),
                      color='deeppink', linestyle=':', linewidth=4)

    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC '+name)
    plt.legend(loc="lower right", markerscale=0.5, fontsize=6)
    # plt.show()
    fig.savefig('ROC '+name+'.png')
    plt.close(fig)

    c1 = confusion_matrix(y_valid, dt_predictions)
    c1 = c1 / np.sum(c1, axis=1, keepdims=True)
    c1 = np.around(c1, 2)
    fig = plt.figure(figsize=(14, 12))
    sns.heatmap(c1, annot=True)
    plt.title('Confusion Matrix '+ name,fontdict={'size':20})
    plt.xlabel('Predict',fontdict={'size':18})
    plt.ylabel('True',fontdict={'size':18})
    # plt.show()
    fig.savefig('Confusion Matrix '+ name + '.png')
    plt.close(fig)

    num_folds = 10
    seed = 5
    scoring = 'accuracy'
    cross_valid(model, num_folds, seed, scoring, x_train, y_train)


def cross_valid(model, nums, random_seed, scoring_way, x_train, y_train):
    results = []
    kfold = KFold(n_splits=nums, random_state=random_seed, shuffle=True)
    cv_results = cross_val_score(model, x_train, y_train, cv=kfold, scoring=scoring_way)
    results.append(cv_results)
    print('The precision by cross-validation',round(np.average(results),4))


if __name__ == '__main__':
    main()
