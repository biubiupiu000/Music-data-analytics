# COSC-587-P3
A project for hypothesis tesing of music data.<br>
You can find the report from [report pdf](https://github.com/singh-classes/project-2-newbee/blob/main/report.pdf).
## How to use
Environment: Python3.8<br>

Source codes can be found in [*srcs*](https://github.com/singh-classes/project-3-newbee/tree/main/srcs) folder.
### Command line
```
git clone https://github.com/singh-classes/project-3-newbee.git
```
> * Unzip clean_allfeature.for_all at file path: `<proj3_file>/project-3-newbee/srcs/Data`.<br>
```
cd <proj3_file>/project-3-newbee
```
> Move into the project directory
```
pip install -r requirments.txt
```
> Must run this command line to install all required libraries before other codes.
```
cd srcs
```
* Hypothesis 1(*Loudness change with time*)
```
python regression.py
```
> This script is used to see how the loudness change in different time.<br>
>
> The used data set `clean_allfeature.for_all.csv should be in the path`should be in the path `/srcs/Data/influence_data.csv`.<br>

* Hypothesis 2(*Classify music genres*)
```
python Classification.py -m 
```
> This script is used to test hypothesis 2 through four classification models. <br>
> 
> `-m` is the sampling mode. The default is False which means it would use the whole dataset.(It would take about 20 minutes.) By setting True the models would implement down-sampling to run the unbalanced data.<br>
> 
> The script would output figures about ROC curve and confusion matrix. If you choose False, the figures are same to those in the [*Graphs*](https://github.com/singh-classes/project-3-newbee/tree/main/srcs/Graphs) folder. Since Down-sampling select different data each time, so the figures may have minor differences.
* Hypothesis 3(*ANOVA on influenced groups*)
```
python ANOVA.py -i path-to-influence-data -s path-to-song-data
```
>This script is used to perform ANOVA on groups of artists that claiming to have the same influencer.<br>
>Influence data is located by `/srcs/Data/influence_data.csv`.<br>
>Song data is located in `/srcs/Data/clean_allfeature.for_all.zip`, make sure you unzip it first, and use the path to `clean_allfeature.for_all.csv`.<br>
>The script would out put p-values and statistics mentioned in project report, and show some figures. Note that the script might take up to ten minutes to run.<br>


  
