import pandas as pd
import plotly.express as px

FEATURES = ['danceability', 'energy', 'key', 'loudness', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']


def main():
    df = pd.read_csv('Data/cluster.csv')  # read clustering results
    df['cluster'] = df['cluster'].astype(str)  # convert cluster group name to string

    fig = px.scatter_matrix(df[FEATURES + ['cluster']].sample(frac=0.05),  # draw matrix
                            dimensions=FEATURES,
                            color="cluster",
                            title="Scatter matrix of features",
                            labels={col: col.replace('_', ' ') for col in df.columns},
                            opacity=0.7, size_max=0.1)  # remove underscore
    fig.update_traces(diagonal_visible=False)  # remove diagonal subplots
    fig.update_traces(marker_size=5)  # resize markers
    fig.show()
    fig.write_html('visualization/matrix.html')

    df['release_year'] = df['release_date'].map(lambda x: int(x[:4]))  # convert release date to release year
    fig = px.scatter(df[['release_year', 'loudness', 'cluster']].sample(frac=0.1),  # draw scatter plot
                     y="release_year", x="loudness",color="cluster", marginal_y="violin",
                     opacity=0.7, range_y=[1945, 2028], range_x=[-40, 1])
    fig.update_traces(marker_size=10)  # resize markers
    fig.show()
    fig.write_html('visualization/loudness.html')


if __name__ == '__main__':
    main()
