# -*- coding:utf-8 -*-

import plotly.express as px
import pandas as pd


def main():
    # influence gap year figure
    data=pd.read_csv('Data/influence_data.csv')
    data['length'] = data['follower_active_start'] - data['influencer_active_start']
    gap=dict(data['length'].value_counts())
    gap=pd.DataFrame.from_dict(gap,orient='index',columns=['count'])
    gap=gap.reset_index().rename(columns={'index':'gap_year'})
    fig=px.bar(gap,x='gap_year',y='count')
    fig.show()
    fig.write_html('visualization/influential_gap_year.html')
    # chart_studio.plotly.plot(fig,filename='hist_gap',auto_open=True)

    # difference between traditional genres
    data=pd.read_csv('Data/clean_allfeature.for_all.csv')
    genres=['country','pop','blues','classical']
    data=data[data['genres'].isin(genres) ]
    data=data[['danceability','energy','loudness','valence','instrumentalness','genres']]
    fig=px.scatter_matrix(data,dimensions=['danceability','energy','loudness','valence','instrumentalness'],
                          color='genres',symbol='genres',opacity=0.7)
    fig.update_traces(diagonal_visible=False)
    fig.show()
    fig.write_html('visualization/scatterplot_songs.html')
    # chart_studio.plotly.plot(fig,filename='var_corr',auto_open=True)


if __name__ == '__main__':
    main()