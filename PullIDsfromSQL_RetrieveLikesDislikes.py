# ok.. it does not want a python list but a long string, comma separated, eg:
# stringTogether(smallSample)
# be careful not to create a gigantic string that is too much for requests
# Probably safer to do it one at a time in a loop 
# Nevertheless, it seems to be able to handle a string of 10 id's without a problem

import pymysql.cursors
import config
import requests
from datetime import datetime
import time

connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', # deals with the exotic emojis
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = "SELECT videoId FROM search_api"
    cursor.execute(sql)
    videoIdsDicts = cursor.fetchall()

videoIds = [d.get('videoId') for d in videoIdsDicts]

smallSample = videoIds[:10]
stringTogether(smallSample)

for element in chunks(videoIds, 10):
    print (element)   # a chunk of 10!
    
    
    
    
def printDateNicely(timestamp):
    reg_format_date = timestamp.strftime("%d %B %Y %I:%M:%S %p")
    return reg_format_date

printDateNicely(datetime.now())

payload = {'key': config.GOOGLE_API_KEY,
           'part':'statistics,contentDetails,topicDetails',
           'id' : stringTogether(smallSample)}
time.sleep( 1/5 ) 
r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=payload)

queriedAt = printDateNicely(datetime.now())

r.status_code

videosInfo = r.json()

for item in list(videosInfo['items']):
    print (list(item))
    

def stringTogether(vi):
    videoIdsString = ""
    for v in vi:
        videoIdsString += v + "," 
    # chop off the final comma
    videoIdsString = videoIdsString[:-1]
    return videoIdsString

# sent requests sets of 10 ids at a time
# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def tryget(dictionary, key):
    if key in list(dictionary):
        return dictionary[key]
    else:
        print ("No %s in dictionary!" %(key))
        return False
    
totalcount = 0        
with connection.cursor() as cursor:  
    
    for element in chunks(videoIds, 10):
        
        loopings = 0
        for item in list(videosInfo['items']):
            # clear all the variables from the previous run of a loop
            kind=etag=ID=contentDetails=duration=dimension=definition=caption=licensedContent=projection=None
            statistics=viewCount=likeCount=dislikeCount=favoriteCount=commentCount=None
            topicDetails=relevantTopicIds=topicCategories=None

            kind = tryget(item,'kind')
            etag = tryget(item,'etag')
            videoId = tryget(item,'id')

            contentDetails = tryget(item,'contentDetails') #****
            if contentDetails != False:
                duration = tryget(contentDetails,'duration')
                dimension = tryget(contentDetails,'dimension')
                definition = tryget(contentDetails,'definition')
                caption = tryget(contentDetails,'caption')
                licensedContent = str(tryget(contentDetails,'licensedContent')) # was a bool
                projection = tryget(contentDetails,'projection')
            else:
                duration = None
                dimension = None
                definition = None
                caption = None
                licensedContent = None
                projection = None            

            statistics = tryget(item,'statistics')  #****
            if statistics != False:
                viewCount = int(tryget(statistics, 'viewCount'))
                likeCount = int(tryget(statistics, 'likeCount'))
                dislikeCount = int(tryget(statistics, 'dislikeCount'))
                favoriteCount = int( tryget(statistics, 'favoriteCount'))
                commentCount = int(tryget(statistics, 'commentCount'))
            else:
                viewCount = None
                likeCount = None
                dislikeCount = None
                favoriteCount = None
                commentCount = None
            print (favoriteCount)
            topicDetails = tryget(item,'topicDetails') #****
            if topicDetails != False:
                relevantTopicIds = str(tryget(topicDetails, 'relevantTopicIds')) # was a list
                topicCategories = tryget(topicDetails, 'topicCategories')
            else:
                relevantTopicIds = None
                topicCategories = None

            # 17 columns to insert
            sql = "INSERT INTO statistics (videoId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, duration, dimension, definition, caption,licensedContent, projection, relevantTopicIDs, topicCategories, kind, etag, queriedAt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (videoId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, duration, dimension, definition, caption,licensedContent, projection, relevantTopicIds, topicCategories, kind, etag, queriedAt))        

            print ("Loopings: ", loopings)
            loopings += 1
            totalcount += 1

print ("Totalcount: ", totalcount)