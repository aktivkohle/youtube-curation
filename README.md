# youtube-curation

This project tests if you can curate youtube videos based mainly on the transcript of the video and how close the text of that transcript is to a published work supplied by the user. In particular, curating materials that can be used for learning, be it how-to's, recipes, or tutorials. 

The code in the repository carries out several functions:
* setting up MySQL database schema, querying youtube video data and populating the database with captions text and some video statistics such as numbers of views, likes and dislikes [1](https://github.com/aktivkohle/youtube-curation/blob/master/searchAPIandLoad_ProductionVersion.py), [2](https://github.com/aktivkohle/youtube-curation/blob/master/PullIDsfromSQL_RetrieveLikesDislikes.py), [3](https://github.com/aktivkohle/youtube-curation/blob/master/captionsYoutube_dl_SQL.py), [4](https://github.com/aktivkohle/youtube-curation/blob/master/wordCountColumn.py), [5](https://github.com/aktivkohle/youtube-curation/blob/master/runAll.py)
* natural language processing scripts which clean and vectorise each caption text with spaCy and Scikit Learn and store the vectors as blob type back in the database
* a script which pulls the vectors out and reassembles them into a matrix, then performs some matrix algebra to create a 'similarity' matrix where also one new piece of text from the user can be compared against all the other captions and  the six most similar are shown to the user
* frontend scripts which create a basic website with Twitter Bootstrap, Python Flask and Jinja2 templating engine to accept the text from the user and call the videos onto the screen from Youtube which were found by the algorithm


* Jupyter notebooks that were used to originally develop the NLP scripts [5](https://github.com/aktivkohle/youtube-curation/blob/master/notebooks/TextbooksAndCaptions_Similarity.ipynb)
* A notebook which graphically tells you what is in the database with respect to time and topic [6](https://github.com/aktivkohle/youtube-curation/blob/master/notebooks/whatsInThere.ipynb)
* A listing of all useful SQL queries for looking into the database and creating queries for the ETL scripts [7](https://github.com/aktivkohle/youtube-curation/blob/master/usefulQueries.sql)

