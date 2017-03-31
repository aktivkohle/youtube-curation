import sys
from userInteraction import askTheUser
import requests
import config
import dateutil.parser
import dateutil.parser
import datetime
from dateutil.relativedelta import relativedelta
import time
import pprint
import pymysql.cursors
import re

def printUnixTimestampNicely(Tstamp):
    return (datetime.datetime.fromtimestamp(Tstamp).strftime("%d %B %Y %I:%M:%S %p"))

logfileName = datetime.datetime.now().strftime("%d%B%Y%I:%M:%S%p") + '_Logfile.txt'
f = open("./logfiles/" + logfileName, 'w')

def printDateNicely(timestamp):
    reg_format_date = timestamp.strftime("%d %B %Y %I:%M:%S %p")
    print(reg_format_date)

def wr(message, p, fi):    # to write to log file
    fi.write(str(message))
    fi.write('\n')
    q = dict(p)
    q['key'] = 'googleAPIkey'
    pprint.pprint(q, fi)
    fi.write('\n')
    
def zed(ts):
    dotOooz = re.compile(".*[.]\d{3}Z$")
    if (dotOooz.match(ts) != None):
        return ts    
    ending = ts[-1:]
    if ending == 'Z':
        return ts[:-1] + '.000Z'   
    else:
        return ts + '.000Z'
    

def storeMeInSQL(element, qq, SQLconnection, openlogfileHandle):
    queriedAt = printUnixTimestampNicely(time.time())
    kind = element['kind']
    etag = element['etag']
    regionCode = element['regionCode']
    # Although query_q has scope outside this function, it is safer to actually pass it in as an
    # argument, as it is very important, one day this function might not be in this program anymore
    # and that saves us from running into a problem.
    # In fact to make it even safer, I have renamed query_q to qq!
    for thing in list(element['items']):
        videoTitle = thing['snippet']['title']
        channelTitle = thing['snippet']['channelTitle']
        videoId = thing['id']['videoId']
        description = thing['snippet']['description']
        pa = thing['snippet']['publishedAt']
        e = dateutil.parser.parse(pa).replace(tzinfo=None)
        publishedAt = e.strftime('%Y-%m-%d %H:%M:%S') 
        items_etag = thing['etag']
        channelId = thing['snippet']['channelId']
        with connection.cursor() as cursor1:                     # CPU times: user 0 ns, sys: 0 ns, total: 0 ns
            sql1 = "SELECT DISTINCT(videoId) FROM search_api"    # Wall time: 14.3 µs
            cursor1.execute(sql1)                                # (Not Expensive)   
            videoIdsDicts = cursor1.fetchall()
            videoIds = [d.get('videoId') for d in videoIdsDicts]        
        if videoId not in videoIds:
            with SQLconnection.cursor() as cursor2:
                sql2 = "INSERT INTO search_api (videoTitle, channelTitle, videoId, description, publishedAt, queriedAt, kind, etag, regionCode, items_etag, channelId, query_q) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"        
                cursor2.execute(sql2, (videoTitle, channelTitle, videoId, description, publishedAt, queriedAt, kind, etag, regionCode, items_etag, channelId, qq))
                SQLconnection.commit()
        else:
            openlogfileHandle.write("Avoided saving a duplicate into SQL!" + " - " + videoId)
            openlogfileHandle.write("\n")
   
v = askTheUser()

if v == None:
    sys.exit()
    
begin_string = v[0]
end_of_month_string = v[1]
query_q = v[2]


connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', # deals with the exotic emojis
                             cursorclass=pymysql.cursors.DictCursor)

print ("\n\n")          
printDateNicely(datetime.datetime.now())

payload = {'key': config.GOOGLE_API_KEY, 
    'part': 'snippet', 
    'q': query_q,                                           # 'dog+training'
    'order' : 'date',                  # reverse chronological of creation
    'type':'video',
  #  'videoCaption':'closedCaption',    # includes captions. 
    'maxResults':50}    


# videoCaption 	string
# The videoCaption parameter indicates whether the API should filter video search results based on 
# whether they have captions. If you specify a value for this parameter, 
# you must also set the type parameter's value to video
# Acceptable values are:

# any – Do not filter results based on caption availability.
# closedCaption – Only include videos that have captions.
# none – Only include videos that do not have captions.
# complete documentation here: https://developers.google.com/youtube/v3/docs/search/list


counter = 0
#begin_string = '2017-02-01T00:00:00Z'
end_datetime = dateutil.parser.parse(begin_string).replace(tzinfo=None)
#end_of_month_string = '2017-03-01T00:00:00Z' 
end_of_month_datetime = dateutil.parser.parse(end_of_month_string).replace(tzinfo=None)
while end_datetime < end_of_month_datetime:
    bs = begin_string     # to get it out of the loop
    begin_datetime = dateutil.parser.parse(begin_string).replace(tzinfo=None)
    end_datetime = begin_datetime + relativedelta(days=1)
    end_string = end_datetime.isoformat()
    es = end_string   # to get it out of the loop
    print ("\n")
    begin_datetime = end_datetime
    begin_string = begin_datetime.isoformat()

    print ("begin: ", zed(bs))
    print ("end: ", zed(es))
    f.write("\n")
    f.write("begin: " + zed(bs))
    f.write("\n")
    f.write("end: " + zed(es))
    f.write("\n")
        
    payload.update({'publishedAfter' : zed(bs)})
    payload.update({'publishedBefore': zed(es)})
    
    wr(1, payload, f)
    
    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
    time.sleep( 1/5 )
    statuscode = r.status_code

    # We have been retrieving for each day
    # ..however where a day contains multiple pages
    # it is necessary to have another loop of sorts
    # here which retrieves those pages within the one
    # day
    # more queries for the special case of multiple pages
    # within one day

    if statuscode == 200:
        time.sleep( 1/5 )        
        objects = r.json()

        if 'nextPageToken' not in list(objects):
            print ("NormalLengthDay") 
            storeMeInSQL(objects, query_q, connection, f)
            counter += 1
            daycount = 1
            
        elif 'nextPageToken' in list(objects):
            storeMeInSQL(objects, query_q, connection, f)  
            counter += 1          
            daycount = 1
            itemsEmpty = 0
            while 'nextPageToken' in list(objects):    
                NPT = objects['nextPageToken']
                payload.update({'pageToken': NPT})
                time.sleep( 1/5 )
                
                wr(2, payload, f)
                
                r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
                time.sleep( 1/5 )
                statuscode = r.status_code
                if statuscode == 200:
                    time.sleep( 1/5 ) 
                    objects = r.json()
                    storeMeInSQL(objects, query_q, connection, f)   
                    counter += 1                 
                    daycount += 1
                else:
                    print (bs, statuscode)
                time.sleep( 1/5 )
                wr(3, payload, f)
                if len(objects['items']) == 0:
                    itemsEmpty += 1
                if itemsEmpty > 3:
                    break
            payload.pop('pageToken')   
            # important! - now that this section is finished clean out that key from the dictionary!!!
            wr(4, payload, f)                  
        
        print(daycount, " pages of results today.")
        f.write(str(daycount) + " pages of results today.")
        wr(5, payload, f)
                   
    else:
        print ("statuscode : ", statuscode)

    time.sleep( 1/5 ) 


                        
print ('\n')
printDateNicely(datetime.datetime.now())
print (counter, " SQL-store operations in total.")

f.close()
connection.close()

