# http://stackoverflow.com/questions/16742381/how-to-convert-youtube-api-duration-to-seconds

import isodate
import config
import pymysql.cursors
        
connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', # deals with the exotic emojis
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    while ytDuration != None:
        sql = "SELECT duration, durationSeconds, id FROM statistics WHERE durationSeconds IS NULL;"
        cursor.execute(sql)
        ytDuration = cursor.fetchone()    
        seconds = int(isodate.parse_duration(ytDuration['duration']).total_seconds())
        DBid = ytDuration['id']
        cursor.execute("UPDATE youtubeProjectDB.statistics SET durationSeconds=%d WHERE id=%d;" % (seconds, DBid))
        connection.commit()
connection.close()

# Note - runs perfectly but ends with the following error:
# TypeError: 'NoneType' object is not subscriptable 