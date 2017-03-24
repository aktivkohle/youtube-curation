# http://stackoverflow.com/questions/14061195/how-to-get-transcript-in-youtube-api-v3 
# http://video.google.com/timedtext?lang={LANG}&v={VIDEOID}
import config
import requests
import untangle
from datetime import datetime
import time
import pymysql.cursors
import sys

def printDateNicely(timestamp):
    reg_format_date = timestamp.strftime("%d %B %Y %I:%M:%S %p")
    return reg_format_date

connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', # deals with the exotic emojis
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor1:
    sql = "SELECT DISTINCT(videoId) FROM search_api WHERE videoID NOT IN (SELECT videoId FROM captions);"
    cursor1.execute(sql)
    videoIdsDicts = cursor1.fetchall()

videoIds = [d.get('videoId') for d in videoIdsDicts]

# Try just the first 10 first:
videoIds = videoIds[:100]

time.sleep(2) 

with connection.cursor() as cursor2:
    for videoId in videoIds:
        time.sleep(0.3) 
        

        #videoId = 'xthIqXnHL_8'

        language = "en"

        payload = {'lang':language, 
                   'v':videoId} 

        queryMethod = 'http://video.google.com/timedtext'

        r = requests.get(queryMethod, params=payload)

        subTitle_xml = r.text
        if len(subTitle_xml) > 5:
            print(".", end="") # so you know it's alive and looping
            obj = untangle.parse(subTitle_xml)
            a = obj.transcript.text

            # https://github.com/stchris/untangle/issues/14
            # b = a[5]
            # b._name
            # b._attributes

            justText = []

            for line in obj.transcript.text:
                justText.append(line.cdata)    

            jt = ""
            for line in obj.transcript.text:
                jt += line.cdata + " "  # need a space at the end of line or words crushed together!

            # write an xml file
            xmlfilename = videoId + 'Captions' + '.xml'
            f =  open(xmlfilename, "w")
            f.write(subTitle_xml)
            f.close()

            ## write an text file
            textfilename = videoId + 'Captions' + '.txt'
            f =  open(textfilename, "w")
            f.write(jt)
            f.close()

            queriedAt = printDateNicely(datetime.now())

            captionsText = jt
            captionsXML = subTitle_xml
            try:
                sql = "INSERT INTO captions (videoId, captionsText, captionsXML, language, queryMethod, queriedAt) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor2.execute(sql, (videoId, captionsText, captionsXML, language, queryMethod, queriedAt))   
            except:
                print("Oops!",sys.exc_info()[0],"occured with videoId", videoId)
        else:
            print("X", end="") # looping but not so healthy
            
connection.commit() 
#connection.rollback()
connection.close()   