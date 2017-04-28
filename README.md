# youtube-curation

So higher aim of this project was to see if you can curate youtube videos based mainly on the quality of the transcript of the video and how close the text of that transcript is to a quality published work. In particular, curating materials that can be used for learning, be it how-to's, recipes, or tutorials. 

Most of the scripts here create and populate a MySQL database full of youtube video transcripts (aka captions, subtitles), and other video statistics and metadata. 

[runAll.py](https://github.com/aktivkohle/youtube-curation/blob/master/runAll.py) will run the 4 main files that populate the database one after the other. It will ask the user two questions when run about the desired query and date range the proceed to populate the various tables including the captions table with all the texts. These multiple files were necessary, the YouTube V3 API does not let you get all this information with just one query. 

There are many .sql files which create and modify the tables. It turned out along the way that the initial schemas had to be modified for one reason or another, at some point I will consolidate them into fewer files that create the schemas in their finished state. 

[usefulQueries.sql](https://github.com/aktivkohle/youtube-curation/blob/master/usefulQueries.sql) are a lot of useful queries which show you what you have in the finished database. They were also helpful to work out the logic between the Python scripts and SQL. 

In the notebooks folder, [whatsInThere.ipynb](https://github.com/aktivkohle/youtube-curation/blob/master/notebooks/whatsInThere.ipynb) shows you in a nice graphical way the initial query and over which date ranges how many videos are stored. 

As for the natural language processing, the file [TextbooksAndCaptions_Similarity.ipynb](https://github.com/aktivkohle/youtube-curation/blob/master/notebooks/TextbooksAndCaptions_Similarity.ipynb) steps through text cleaning and tokenizing with the spaCy library and computes similarities between a subset of the videos captions and a list of textbooks contained in a folder on the hard drive based on their texts. At the bottom of this page is the output which shows the 3 most similar captions or textbooks in the set - it has actually worked quite well!

