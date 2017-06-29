# youtube-curation

This project tests if you can curate youtube videos based mainly on the quality of the transcript of the video and how close the text of that transcript is to a quality published work. In particular, curating materials that can be used for learning, be it how-to's, recipes, or tutorials. 

The code in the repository carries out several functions:
* setting up MySQL database schema, querying youtube video data and populating the database with captions text and some video statistics such as numbers of views, likes and dislikes [1](https://github.com/aktivkohle/youtube-curation/blob/master/searchAPIandLoad_ProductionVersion.py), [2](https://github.com/aktivkohle/youtube-curation/blob/master/PullIDsfromSQL_RetrieveLikesDislikes.py), [3](https://github.com/aktivkohle/youtube-curation/blob/master/captionsYoutube_dl_SQL.py), [4](https://github.com/aktivkohle/youtube-curation/blob/master/wordCountColumn.py), [5](https://github.com/aktivkohle/youtube-curation/blob/master/runAll.py)
* natural language processing scripts which clean and vectorise each caption text with spaCy and Scikit Learn and store the vectors as blob type back in the database
* a script which pulls the vectors out and reassembles them into a matrix, then performs some matrix algebra to create a 'similarity' matrix where also one new piece of text from the user can be compared against all the other captions and  the six most similar are shown to the user
* frontend scripts which create a basic website with Twitter Bootstrap, Python Flask and Jinja2 templating engine to accept the text from the user and call the videos onto the screen from Youtube which were found by the algorithm
* In addition there are some Jupyter notebooks that were used to originally develop the main scripts 




[usefulQueries.sql](https://github.com/aktivkohle/youtube-curation/blob/master/usefulQueries.sql) are a lot of useful queries which show you what you have in the finished database. They were also helpful to work out the logic between the Python scripts and SQL. 

In the notebooks folder, [whatsInThere.ipynb](https://github.com/aktivkohle/youtube-curation/blob/master/notebooks/whatsInThere.ipynb) shows you in a nice graphical way the initial query and over which date ranges how many videos are stored. 

As for the natural language processing, the file [TextbooksAndCaptions_Similarity.ipynb](https://github.com/aktivkohle/youtube-curation/blob/master/notebooks/TextbooksAndCaptions_Similarity.ipynb) steps through text cleaning and tokenizing with the spaCy library and computes similarities between a subset of the videos captions and a list of textbooks contained in a folder on the hard drive based on their texts. At the bottom of this page is the output which shows the 3 most similar captions or textbooks in the set - it has actually worked quite well!

That however was for a subset of 35 out of about 8000 documents. While that took perhaps 15 minutes of computing time, doing the whole lot will take longer. That's okay if it's a one-off but what about every time you add a new document?
