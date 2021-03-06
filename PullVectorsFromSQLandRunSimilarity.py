import sys
sys.path.append('../')
import config
import pymysql.cursors
import pandas as pd
import numpy as np
from scipy import io as scipyio
from tempfile import SpooledTemporaryFile
from scipy.sparse import vstack as vstack_sparse_matrices

# Function to reassemble the p matrix from the vectors

def reconstitute_vector(bytesblob):
    f = SpooledTemporaryFile(max_size=1000000000)
    f.write(bytesblob)
    f.seek(0)
    return scipyio.mmread(f)

def youtubelink(vidid):
    return ('https://www.youtube.com/watch?v=' + vidid)    


connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', 
                             cursorclass=pymysql.cursors.DictCursor)

    
with connection.cursor() as cursor:                                 
            # https://stackoverflow.com/questions/612231/how-can-i-select-rows-with-maxcolumn-value-distinct-by-another-column-in-sql?rq=1
            # Note - this is a very interesting query! never seen it before..
            sql = """SELECT * FROM
            (SELECT DISTINCT(videoId) AS v, videoTitle FROM search_api) A
            INNER JOIN
            (SELECT * FROM captions c
            INNER JOIN(SELECT videoId AS InnerVideoId, 
            MAX(wordCount) AS MaxWordCount, 
            MAX(id) AS MaxId
            FROM captions 
            WHERE tfidfVector IS NOT NULL 
            GROUP BY videoId) grouped_c
            ON c.videoId = grouped_c.InnerVideoId
            AND c.wordCount = grouped_c.MaxWordCount
            AND c.id = grouped_c.MaxId) B
            ON A.v = B.videoId;"""
            cursor.execute(sql)
            manyCaptions = cursor.fetchall()
            videos_df = pd.read_sql(sql, connection)                        
connection.close()

# note that the other program which put the vectors there only did it on captions WHERE language like '%en%'
# for that reason this query does not contain language. It has instead WHERE tfidfVector IS NOT NULL

videos_df = videos_df.drop('v', 1)

videos_df['tfidfVector_NP'] = videos_df['tfidfVector'].apply(reconstitute_vector)

listOfSparseVectors = list(videos_df['tfidfVector_NP'].values.flatten())

p = vstack_sparse_matrices(listOfSparseVectors)

video_titles = list(videos_df['videoTitle'].values.flatten())
video_ids = list(videos_df['videoId'].values.flatten())

# Apply the transformation to the term document matrix to compute similarity between all pairs

pairwise_similarity = (p * p.T).A #  In Scipy, .A transforms a sparse matrix to a dense one

# df9 = pd.DataFrame(pairwise_similarity, columns=video_ids, index=video_ids)

# s = pd.Series(video_titles, index=df9.index)

# df9 = pd.concat((s.rename('videoTitles'), df9), axis=1)  


def nth_similar_tuple(n, ps):
    title = (np.array(video_titles))[((-ps).argsort()[n])]
    vid_id = (np.array(video_ids))[((-ps).argsort()[n])]
    return (title, vid_id) 

d = [] 
for a,b,c in zip(video_titles, video_ids, pairwise_similarity):
    d.append({'a':(a,b),
              'b': nth_similar_tuple(1,c),
              'c': nth_similar_tuple(2,c),
              'd': nth_similar_tuple(3,c)})
# takes about a minute to run through the 7000 unique rows.
    

similarity_df = pd.DataFrame(d)
similarity_df.columns = ['original', 'first_similar', 'second_similar', 'third_similar']
# split the tuples into two-level columns.
similarity_df = pd.concat(
    [pd.DataFrame(x, columns=['video_title','youtube_id']) for x in similarity_df.values.T.tolist()],     
    axis=1,                 
    keys=similarity_df.columns)    

print ("Finished running, the Pandas DataFrame variable similarity_df should now be in scope.")