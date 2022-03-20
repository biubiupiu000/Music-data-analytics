import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics


def get_file():
    """
    read the data set, return as dataFrame.
    :return df:
    """
    # column = ['id_song', 'name_song', 'id_artist', 'name_artist', 'release_date', 'release_date_precision',
    #           'total_tracks', 'type_song', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
    #           'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'genres']

    df = pd.read_csv(f'{os.getcwd()}/Data/clean_allfeature.for_all.csv', encoding='utf-8',
                     usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
                     )
    return df


def changeTimeFormat(df):
    """
    change the time format from datetime to integer(year).
    :param df:
    :return data:
    """
    x = df.loc[:,'release_date']
    x = list(x)
    y = df.loc[:,'loudness']
    y = list(y)
    for i in range(len(x)):
        x[i] = int(x[i][0:4])
        if x[i] < 1899:
            x[i] = 1990
    data = pd.DataFrame({'time': x, 'loudness': y})
    data = data.sort_values(by='time', axis=0, ascending=True)
    return data


def getMean(data):
    """
    only get the mean value of loudness in each year.
    :param data:
    :return dataFrame: new dataFrame with column time and loudness.
    """
    da = data.groupby(['time'])['loudness'].mean()
    x = list(da.index)
    y = list(da.values)

    return pd.DataFrame({"time":x,"loudness":y})


def getScore(name, y_test, y_pred):
    """
    calculate the mean absolute error, mean squared error, median absolute error and R2 score.
    print the score.
    :param name:
    :param y_test:
    :param y_pred:
    :return:
    """
    print('-' * 50)
    print(f'The score of {name}:')
    print('mean_absolute_error ', metrics.mean_absolute_error(y_test, y_pred))
    print('mean_squared_error ', metrics.mean_squared_error(y_test, y_pred))
    print('median_absolute_error ', metrics.median_absolute_error(y_test, y_pred))
    print('R2 score', metrics.r2_score(y_test, y_pred))
    print('-' * 50)


def linearRegression(data):
    """
    Linear regression model.
        randomly split the data into 80% train set and 20% test set.
        use the train set to fit both the simple linear regression model and polynomial regression mdoel, use test set to calculate how good the model are.
        using the whole data set to draw the figure.
    :param data:
    :return:
    """
    print('LinearRegression')
    x_data = data.time.values.reshape(-1,1)
    y_data = data['loudness'].values.reshape(-1,1)
    x_train, x_test, y_train, y_test = train_test_split(x_data,y_data,test_size=0.2)
    linreg = LinearRegression()
    model = linreg.fit(x_train,y_train)
    y_pred = model.predict(x_test)

    # obtain the score
    getScore('simple linear regression', y_test, y_pred)

    plt.figure()    # draw the simple regression model
    plt.scatter(x_data, y_data, s=1.5, c='black', label='trueLoudness')
    plt.plot(x_data, model.predict(x_data), color='orange', label='predictLine')
    plt.xlim(1899, 2021)
    plt.title('Linear Regression')
    plt.xlabel('time')
    plt.ylabel('loudness')
    plt.show()
    model2 = make_pipeline(PolynomialFeatures(5), linreg)
    model2.fit(x_train, y_train)
    y_pred = model2.predict(x_test)

    # obtain the score
    getScore('polynomial regression',y_test, y_pred)

    plt.figure()    # draw the polynomial regression model
    plt.scatter(x_data, y_data, s=1.5, c='black', label='trueLoudness')
    plt.plot(x_data, model2.predict(x_data), color='orange')
    plt.xlim(1899, 2021)
    plt.title('Polynomial Regression')
    plt.xlabel('time')
    plt.ylabel('loudness')
    plt.show()
    del data


def svmRegression(data):
    """
    SVM Regression.
        randomly split the data into 80% train set and 20% test set.
        use the train set to fit model, use test set to calculate how good the model are.
        using the whole data set to draw the figure.
    :param data:
    :return:
    """
    print('svmRegression')
    x_data = data.time.values.reshape(-1,1)
    y_data = data['loudness'].values.reshape(-1,1)
    x_train, x_test, y_train, y_test = train_test_split(x_data,y_data, test_size=0.2)
    svr = SVR(kernel='rbf',C=2)
    svr.fit(x_train,y_train)
    y_pred = svr.predict(x_test)

    # obtain the score
    getScore('SVR', y_test, y_pred)

    plt.figure()
    plt.scatter(x_data, y_data, s=1.1, c='black')
    plt.plot(x_data, svr.predict(x_data), color='orange')
    plt.xlim(1899, 2021)
    plt.title('SVR Regression')
    plt.xlabel('time')
    plt.ylabel('loudness')
    plt.show()

    del data


def main():
    """
    create the model in following order:
        using the whole data set to fit the linear regression model.
        use mean value to fit the linear regression model.
        use mean value to fit the SVM regression model.
    :return:
    """
    df = changeTimeFormat(get_file())

    # regression
    linearRegression(df)
    linearRegression(getMean(df))
    svmRegression(getMean(df))


if __name__ == '__main__':
    main()