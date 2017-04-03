import config
import pymysql.cursors
import spacy
nlp = spacy.load('en')
        
connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', 
                             cursorclass=pymysql.cursors.DictCursor)

w = 1
with connection.cursor() as cursor:
        while w != None:
            sql = "SELECT captionsText, wordCount, id FROM captions WHERE wordCount IS NULL AND language LIKE '%en%';"
            cursor.execute(sql)
            w = cursor.fetchone()
            DBid = w['id']
            ct = w['captionsText']
            wc = len(nlp(ct))      
            cursor.execute("UPDATE youtubeProjectDB.captions SET wordCount=%d WHERE id=%d;" % (wc, DBid))
            connection.commit()
connection.close()
