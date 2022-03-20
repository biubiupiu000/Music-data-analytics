# COSC-587-P1
A project for collecting music-related data from Allmusic, Spotify and Wikipedia.


## Data from Spotify API
Required packages: spotipy, pymongo, pandas, os, bson, chain

Required softwares: MongoDB 5.0.3 Comunity, MongoDB Database Tools 100.5.0

Source code of this section can be found in `Spotify/Retrieve` folder
### Directly import data into MongoDB
1. Download and decompress `Spotify.rar` https://drive.google.com/file/d/17CVfMiSlNZwt1Iwk6jQdnQVXNjDJilkm/view?usp=sharing
2. Use `mongorestore` from MongoDB Database Tools to import database `cs589`

### View raw data in JSON format
1. Download `alltracksFeature.json` https://drive.google.com/file/d/1iOOsWkgVDFERLWicPnnGy8B2bgsPZYxZ/view?usp=sharing
2. Load it with your preferred JSON tool (please keep in mind that to load a JSON in this size, you may need enough RAM to do so. e.g. using json.load() in python requires at least 32GB of RAM during loading or you may encounter a `MemoryError`)

### Retrieve data from Spotify
(Note that this is not a fully automated process and requires massive time and operations.)
1. Get at least 4 Client ID and Client Secret pairs from https://developer.spotify.com/dashboard/applications .
2. Add your first Client ID and Client Secret pair to environment variables by adding `SPOTIPY_CLIENT_ID=your-client-id`, `SPOTIPY_CLIENT_SECRET=your-client-cecret`, `SPOTIPY_REDIRECT_URI=http://127.0.0.1:9090` 
3. Firstly, we start with getting artist names. Run `getArtists.py`. Once done, you should get a file named `artists.json`https://drive.google.com/file/d/1KotbvzEETPUiYJ2j9Ex2kz5YwI-MsnR7/view?usp=sharing under current directory.
4. Then we collect Top Tracks from the artists we got in the previous step. Run `getTracks.py` in **debug mode**. You probably won't successfully get all the data we need from one execution. Once you notice the new names are not bumping out from `stdout` for a long time, it means you've probably hit your client's daily limits. What you should do now is to firstly, record the last artist name output from `stdout`, then pause the script (that's why you should run it in debug mode), and run `json.dump(albums,f, indent=4, ensure_ascii=False)` and `f.close()` in the debug console. Then you will get `Tracks.json` in the current directory, containing the tracks you get from this run. To continue the process, you should 1) update your Client ID and Client Secret pair in environment variables to a new one. 2) change the source code of `getTracks.py` at line 12 to `startFlag=False`, line 13 to `startName='last-name-on-previous-execution'`, `'tracks.json'` in line 14 to another file name and keep at record. 3) repeat step 4. until the script terminates it self automatically.
5. Edit the source code in `mergeTracks.py` in line 5, list all the names of files generated from last step in **reverse order**. Then run `mergeTracks.py`. Once done, you should get a file named `alltracks.json`
6. In this step we collect audio features. Firstly update a new Client ID and Client Secret pairs in environment variables, then run `getAudioFeatures.py`. Once done, you should ge a file named `alltracksFeature.json` it should be identical to what we've uploaded.
7. Write data into MongoDB. Run `writeMongodb.py`. Note that you should have at least 32GB of RAM to run this script or you may encounter a `MemoryError`. You should also ensure that your MongoDB have no login credentials. You can update the connect link in line 7 to add your credentials.<br>

### Change bson File to csv
1. Run `build_csv.py` to remove the useless data and store the needed data into one csv file.
* (1)The new csv data could also be obtain by this link: https://drive.google.com/file/d/1V4B7TUZwQBWSWODh_oifR74Abbupo9qk/view?usp=sharing
         
* (2)Both of the csv files should store at the file named 'Data'.
      
### Check Cleanliness
1. Run `checkCleanliness.py` to obtain the data quality score.

## Data from Wikipedia API
Source code of this section can be found in `wikipedia/` folder.
Use wikirobot to parse API from Wikipedia.
### Library Requirments
Pandas, mwclient, mediawiki

### Usage
1. Run command-line `cd wikipedia` to change to wikipedia.
2. Run `python get_data.py --file1 --file2` to collect name ranges for scraping. 
#### options
`--file1` The csv dataset address(data/influence.csv)

`--file2` The json dataset address(musician names scraped from Spotify)
* These two files only correspond with data we have and scrape, so don't use your own datasets.

3. Run `python biograph.py --mode` to scrape summary text from Wikipedia. Upon done, the script would create data file if not exists and generate `biography.pkl`. 
* When scraping data from Wikipedia, you must follow the User-Agent policy `<client name>/<version> (<contact information>) <library/framework name>/<version>)` Website:https://meta.wikimedia.org/wiki/User-Agent_policy
  
  The script just remove the user-agent used, you should change your own one.
* When scraping data, Wikipedia may limit the request quantities. So you should record the last name and store whole information scraped into disc.
#### options
`--mode` Have two modes of text and tags. If you choose text one, you can scrape complete text from Wikipedia. Otherwise, you can get more diverse text data.(We recommend 
use tags mode)

4. Run`python text_influence.py` to collect influence text from Wikipedia. Just use mwclient to extract influence section from the whole page. After done, you should get `influence.pkl`.
5. Run`python text clealiness.py --file` to compute data quality of text data.
   Have two metrics(Missing value and Consistency)
#### options
`--file` The data address to compute quality

### Text Data
The final text data can be found in [`data/`](https://github.com/singh-classes/project-1-newbee/tree/main/wikipedia/data) folder. 
* The two files(biograph and influence) should be opened by pickle. Both have two attributes, name and correspond text.

## Data from Allmusic 
This dataset is download online which is sorted by [Allmusic](https://www.allmusic.com/). You can find it in [`data/`](https://github.com/singh-classes/project-1-newbee/tree/main/wikipedia/data) folder either.
### Attributes
The dataset has eight attributes which relate to music influence among musicians.You can see the example as the following:
>[influence_id, influence_name, influence_main_genre, influence_active_start, follower_id, follower_name, follower_active_start]
