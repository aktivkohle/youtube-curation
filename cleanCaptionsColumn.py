import config
import pymysql.cursors
import html
        
connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', # deals with the exotic emojis
                             cursorclass=pymysql.cursors.DictCursor)

updated = 0
print ('Updating the following ids: ')
with connection.cursor() as cursor:
        sql1 = "SELECT captionsText, id FROM captions WHERE language LIKE '%en%';"        
        cursor.execute(sql1)
        results = cursor.fetchall()    # fetchall is much more redundant than fetchone method in other scripts!!
        for row in results:
            DBid = row['id']
            ct = row['captionsText']
            cleaned = html.unescape(ct)                
            sql2 = "UPDATE `captions` SET `captionsText`=%s WHERE `id`=%s;"
            cursor.execute(sql2, (cleaned, DBid))
            connection.commit()
            updated += 1
            print(DBid, end=',')
connection.close()  
print ('\n')
print (updated, ' text fields cleaned.')

# 5111  text fields cleaned. 4 april 2017


