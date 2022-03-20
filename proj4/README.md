# COSC-587-P4
The final project for music data.<br>
You can find our whole story in the [*website*](https://hedylun.wixsite.com/cosc587).

## Visualization
Through network analysis, we draw four interesting figures. In addition, we draw four more interactive figures by Plotly (You can view them by running the codes). 
You can see these eight figures in the ([*visualization*](https://github.com/singh-classes/project-4-newbee/tree/main/visualization)) directory.<br>
The remaining bunch of others are shown in the website. Read our story and view them!

## How to use
Environment: Python3.8<br>

Source codes can be found in the main directory.
### Command line
```
git clone https://github.com/singh-classes/project-4-newbee.git
```
> * Unzip clean_allfeature.for_all at file path: `<proj4_file>/project-4-newbee/Data`.<br>
```
cd <proj4_file>/project-4-newbee
```
> Move into the project directory
```
pip install -r requirments.txt
```
> Must run this command line to install all required libraries before other codes.

* Network analysis
```
python network.py
```
> This script is used to see the directed graph of influence within musicians.<br>
>
> The used data [*graph.pkl*](https://github.com/singh-classes/project-4-newbee/blob/main/Data/graph.pkl) is in the Data folder. All the figures generated
> are same as those in the visualization folder.<br>

* Plotly visualizations on clustering results
```
python Cluster_plotly.py
```
> This script will draw interactive plots for clustering results.<br>
> The script will use relative paths so please make sure the working directory is root of the repo.<br>
> The script will open two webpages to show the plots, and save the html file to `visualization` folder.
> The clustering result if from project 2. To get the csv used by this script, add
> ```
> df=pd.concat([samples.reset_index(),pd.DataFrame(data=model.labels_,columns=['cluster'],dtype=str)],axis=1)
> with open('cluster.csv',mode='w',newline='',encoding='utf-8')as f:
>     df.to_csv(f)
> ```
> to the end of `plot_hierarchical` function in `project-2-newbee/srcs/Clustering.py` and run that script.
  
