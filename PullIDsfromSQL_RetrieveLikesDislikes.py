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

def printDateNicely(timestamp):
    reg_format_date = timestamp.strftime("%d %B %Y %I:%M:%S %p")
    return reg_format_date


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

        
def stringTogether(vi):
    videoIdsString = ""
    for v in vi:
        videoIdsString += v + "," 
    # chop off the final comma
    videoIdsString = videoIdsString[:-1]
    return videoIdsString


def tryget(dictionary, key):
    if key in list(dictionary):
        return dictionary[key]
    else:
    #   print ("No %s in dictionary!" %(key))     # too much output
        return False

# Section 1 - Connect to MySQL and pull a list of videoID 's
# _________________________________________________________________________________

connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', # deals with the exotic emojis
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor1:
    sql = "SELECT DISTINCT(videoId) FROM search_api"
    cursor1.execute(sql)
    videoIdsDicts = cursor1.fetchall()

videoIds = [d.get('videoId') for d in videoIdsDicts]

time.sleep(2) 
# _________________________________________________________________________________




# Processing - connect the list of IDs into one gigantic string seperated by commas
# _________________________________________________________________________________

# See the function at the top of the page

# for testing 
# smallSample = videoIds[:10]
# stringTogether(smallSample)


# Section 2 - split the long list into chunks of 10 and sent each list of 10 as a string to requests.
# ___________________________________________________________________________________________________

# sent requests sets of 10 ids at a time
# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks

totalcount = 0 
payload = {}
with connection.cursor() as cursor2:  
    for sample_of_ten in chunks(videoIds, 10):
        stringOfTen = stringTogether(sample_of_ten)

        payload.update({'key': config.GOOGLE_API_KEY,
                        'part':'statistics,contentDetails,topicDetails',
                        'id' : stringOfTen})

        time.sleep( 1/5 ) 

        r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=payload)
        queriedAt = printDateNicely(datetime.now())

        statuscode = r.status_code

        if statuscode == 200:
            videosInfo = r.json()
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
            #   print (favoriteCount)
                topicDetails = tryget(item,'topicDetails') #****
                if topicDetails != False:
                    relevantTopicIds = str(tryget(topicDetails, 'relevantTopicIds')) # was a list
                    topicCategories = str(tryget(topicDetails, 'topicCategories'))
                else:
                    relevantTopicIds = None
                    topicCategories = None

                # 17 columns to insert
                sql = "INSERT INTO statistics (videoId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, duration, dimension, definition, caption,licensedContent, projection, relevantTopicIDs, topicCategories, kind, etag, queriedAt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor2.execute(sql, (videoId, viewCount, likeCount, dislikeCount, favoriteCount, commentCount, duration, dimension, definition, caption,licensedContent, projection, relevantTopicIds, topicCategories, kind, etag, queriedAt))        

        #      print ("Loopings: ", loopings) # too much output - crashing notebook
                loopings += 1
                totalcount += 1        
        else:
            print ("Status Code: ", statuscode)

connection.commit() 
#connection.rollback()
connection.close()

print ("Totalcount: ", totalcount, " written to DB.")
