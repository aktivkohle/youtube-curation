import config
import datetime
import dateutil.parser
import pymysql.cursors
import pickle
import argparse

parser = argparse.ArgumentParser()                                               
parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

# run the program with: 
# python loadSearchintoSQL.py -f savedDictionary.pickle

with open(args.file, 'rb') as f:
    youtubeObjects = pickle.load(f)

YOUTUBE_API_q_TERM = 'dog+training'

connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', # deals with the exotic emojis
                             cursorclass=pymysql.cursors.DictCursor)


with connection.cursor() as cursor:
    
    sql = "INSERT INTO search_api (videoTitle, channelTitle, videoId, description, publishedAt, queriedAt, kind, etag, regionCode, items_etag, channelId, query_q) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    for element in list(youtubeObjects):
        print (element)
        queriedAt = element
        kind = youtubeObjects[element]['kind']
        etag = youtubeObjects[element]['etag']
        regionCode = youtubeObjects[element]['regionCode']
        query_q = YOUTUBE_API_q_TERM                      

        for thing in list(youtubeObjects[element]['items']):
            videoTitle = thing['snippet']['title']
            channelTitle = thing['snippet']['channelTitle']
            videoId = thing['id']['videoId']
            description = thing['snippet']['description']
            pa = thing['snippet']['publishedAt']
            e = dateutil.parser.parse(pa).replace(tzinfo=None)
            publishedAt = e.strftime('%Y-%m-%d %H:%M:%S') 
            items_etag = thing['etag']
            channelId = thing['snippet']['channelId']
            cursor.execute(sql, (videoTitle, channelTitle, videoId, description, publishedAt, queriedAt, kind, etag, regionCode, items_etag, channelId, query_q))

# To be safe should let the program run without errors before 
# executing the following line:
connection.commit() 

# Uncomment as needed if something goes wrong:
# connection.rollback()

connection.close()
