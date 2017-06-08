# youtube-curation

So higher aim of this project was to see if you can curate youtube videos based mainly on the quality of the transcript of the video and how close the text of that transcript is to a quality published work. In particular, curating materials that can be used for learning, be it how-to's, recipes, or tutorials. 

Most of the scripts here create and populate a MySQL database full of youtube video transcripts (aka captions, subtitles), and other video statistics and metadata. 

There are 4 scripts which populate the various tables, [searchAPIandLoad_ProductionVersion.py](https://github.com/aktivkohle/youtube-curation/blob/master/searchAPIandLoad_ProductionVersion.py), [PullIDsfromSQL_RetrieveLikesDislikes.py](https://github.com/aktivkohle/youtube-curation/blob/master/PullIDsfromSQL_RetrieveLikesDislikes.py), [captionsYoutube_dl_SQL.py](https://github.com/aktivkohle/youtube-curation/blob/master/captionsYoutube_dl_SQL.py) and [wordCountColumn.py](https://github.com/aktivkohle/youtube-curation/blob/master/wordCountColumn.py).

[runAll.py](https://github.com/aktivkohle/youtube-curation/blob/master/runAll.py) will run these one after the other. It will ask the user two questions when run about the desired query and date range then proceed to populate the various tables including the captions table with all the texts. These multiple files were necessary, the YouTube V3 API does not let you get all this information with just one query. 

There are many .sql files which create and modify the tables. It turned out along the way that the initial schemas had to be modified for one reason or another, at some point I will consolidate them into fewer files that create the schemas in their finished state. 

[usefulQueries.sql](https://github.com/aktivkohle/youtube-curation/blob/master/usefulQueries.sql) are a lot of useful queries which show you what you have in the finished database. They were also helpful to work out the logic between the Python scripts and SQL. 

In the notebooks folder, [whatsInThere.ipynb](https://github.com/aktivkohle/youtube-curation/blob/master/notebooks/whatsInThere.ipynb) shows you in a nice graphical way the initial query and over which date ranges how many videos are stored. 

As for the natural language processing, the file [TextbooksAndCaptions_Similarity.ipynb](https://github.com/aktivkohle/youtube-curation/blob/master/notebooks/TextbooksAndCaptions_Similarity.ipynb) steps through text cleaning and tokenizing with the spaCy library and computes similarities between a subset of the videos captions and a list of textbooks contained in a folder on the hard drive based on their texts. At the bottom of this page is the output which shows the 3 most similar captions or textbooks in the set - it has actually worked quite well!

That however was for a subset of 35 out of about 8000 documents. While that took perhaps 15 minutes of computing time, doing the whole lot will take longer. Ther's okay if it's a one-off but what about every time you add a new document?

Well, thankfully it looks like there is a [solution](https://stackoverflow.com/questions/13986518/how-to-efficiently-compute-similarity-between-documents-in-a-stream-of-documents). Here is the relevant quote:

> What do I do when I get a new document doc(k)? Well, I have to compute the similarity of this document with all the previous ones, which doesn't require to build a whole matrix. I can just take the inner-product of doc(k) dot doc(j) for all previous j, and that result in S(k, j), which is great.

