# COSC-587-P2
A project for cleaning, description of music data.

## How to use
Environment: Python3.8<br>

Required libraries: pickle, os, pandas, scikit-learn, seaborn, numpy, matplotlib, nltk, gensim(All correspond with Python 3.8)

Source codes can be found in [*srcs*](https://github.com/singh-classes/project-2-newbee/tree/main/srcs) folder.
### Command line
```
git clone https://github.com/singh-classes/project-2-newbee.git
```
>Unzip allfeature.for_all.zip at file path: `<proj2_file>/project-2-newbee/srcs/Data`
```
cd <proj2_file>/project-2-newbee/srcs
```
```
python Data_cleaning.py
```
>This Script is to do the data cleaning process in the datasets (artist.csv, allfeature.for_all.csv). These two datasets are in the file path: `<proj2_file>/project-2-newbee/srcs/Data`
>By running the Data_cleaning.py, there are two new file are created (clean_Artists.csv and clean_allfeature.for_all.csv) which is store at the same path of the original datasets. These two output datasets can be also obtained from the link: https://drive.google.com/file/d/1RXW5fSpsOLl5_tz48NQvwYTGymYHv1Ad/view?usp=sharing <br>
```
python data_clean.py
```
>This script cleans the data sets of text data and influence data.
The outputs of this script can be found in *Data* folder. (inf_data_clean.csv and text_clean.csv)<br>
```
python StatisticalAnalysis_cleaning.py
```
>This Script is to do the statistic analysis, detect the anomoly, and do the binning method. the needed datasets (clean_Artists.csv and clean_allfeature.for_all.csv) created by "Data_cleaning.py" should be store into the path: <proj2_file>/project-2-newbee/srcs/Data. 
>By running the StatisticalAnalysis&cleaning_insight.py, three new csv file(stat.csv, anomaly.csv,and clean_allfeature_binning.csv) are created at the file Data. "stat.csv" represent the basic statistical analysis; "anomaly.csv" is the datasets of anomaly data; "clean_allfeature_binning.csv" is the datasets with binning. These three datasets can be also obtained from the link: https://drive.google.com/file/d/1NIo9mBLajFSKc_khVIBal3eisa-EAOVj/view?usp=sharing<br>

```
python graph.py
```
>This script would output all diagrams for the four cleaned data sets. The outputs are same to those in the [*graph*](https://github.com/singh-classes/project-2-newbee/tree/main/srcs/graph) folder.

```
python topic_modeling.py
```
>This script would use the topic model, *Lda* to output the top topics and the top distributions of text corpus.(Since passes is set as 10, it would take several minutes.)<br>
>There are four outputs and they are stored in *npy files*, you should use numpy to load them.
> * For example, ```
>                 numpy.load('topics_bio.npy')
>                 ```<br>

```
python Clustering.py -p path-to-spotify-data
```
>This script would do clustering to the Spotify dataset (since the influence dataset is simply edges of a directional graph, it makes no sense to run clustering on it), and plot the clustering result in PCA projections (or best divided attribute pairs) and output their Calinski Harabasz Index to `stdout`.<br>
>Arguments:<br>
>`-p` or `--path` and path to data file after it. This argument is required.<br>
>`-f` or `--frac` and a positive float number less than 1 after it, indicating the sampling fraction from the dataset to run clustering, by default 0.01 for acceptable instant results. Note that by setting `frac` greater than 0.1, it would take a few minuets for the script to run and at least 32GB of RAM to do so. This argument is optional.<br>
>`--bestattr` to plot the clustering results in projections of best divided attribute pairs instead of PCA projection, for this is a dense and multi-dimensional dataset, ploting it with best devided attribute pairs might be better looking than the PCA. This argument is optional.<br>



  
