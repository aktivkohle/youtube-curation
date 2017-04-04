# http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
# http://www.saltycrane.com/blog/2008/09/how-get-stdout-and-stderr-using-python-subprocess-module/
insertionErrors= 0
from subprocess import Popen, PIPE, STDOUT
from subprocess import run as subprRun
import sys
from parseSubtitles import getVtt
import os
import glob
import config
from datetime import datetime
import time
import pymysql.cursors
import html

def clean_directory():    
    files = glob.glob('./youtube-dl-output/*')
    print ("Deleting..")
    for f in files:
        print (f)
        os.remove(f)
        
def printDateNicely(timestamp):
    reg_format_date = timestamp.strftime("%d %B %Y %I:%M:%S %p")
    return reg_format_date

def readFile(fname):
    with open(fname, 'r') as myfile:
        data=myfile.read()
        return data
    
def youtubeComplains(message):
    m = str(message)
    if ("ERROR" in m) and ("YouTube said" in m):
        return True
    elif ("doesn\'t have subtitles" in m):
        return True
    elif ("This video is unavailable" in m):
        return True
    else:
        return False

def loadIntoSql(VI, CT, CF, L, CFF, SQLCursor, SQLconnection):
    queryMethod = 'youtube-dl'
    queriedAt = printDateNicely(datetime.now())
    captionsText = CT
    wordCount = None
    captionsFile = CF
    captionsFileFormat = CFF
    language = L
    videoId = VI

    try:
        sql = "INSERT INTO captions (videoId, captionsText,wordCount, captionsFile, language, captionsFileFormat, queryMethod, queriedAt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        if 'en' in language or 'de' in language:
        	CT = html.unescape(CT)
        SQLCursor.execute(sql, (videoId, captionsText, wordCount, captionsFile, language, captionsFileFormat, queryMethod, queriedAt))   
        SQLconnection.commit() # better here or every 10 
        print(".", end="")
    except:
        print("\n", "Oops!",sys.exc_info()[0],"insertion error occured with videoId", videoId)
        if insertionErrors > 5:
            sys.exit()            
        insertionErrors += 1
        

path = './youtube-dl-output'
PATH = './youtube-dl-output/'

ytdl_version = subprRun(['youtube-dl', '--version'], stdout=PIPE, cwd=path).stdout.decode('utf-8') 
print ("Using youtube-dl version : ", ytdl_version)
        
connection = pymysql.connect(host='localhost',
                             user='root',
                             password=config.MYSQL_SERVER_PASSWORD,
                             db='youtubeProjectDB',
                             charset='utf8mb4', # deals with the exotic emojis
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor1:
    sql = "SELECT DISTINCT(videoId) FROM search_api WHERE videoId NOT IN (SELECT videoId FROM captions WHERE queryMethod = 'youtube-dl') AND videoId NOT IN (SELECT DISTINCT(videoId) FROM statistics WHERE durationSeconds < 10) AND videoId NOT IN (SELECT videoId FROM NOcaptions);"
    cursor1.execute(sql)
    videoIdsDicts = cursor1.fetchall()

videoIds = [d.get('videoId') for d in videoIdsDicts]

time.sleep(2) 

# Try just the first 5 first for testing purposes:
# Comment this out for serious use!
# videoIds = videoIds[:100]

print (len(videoIds), " relevant videoIds found.")

with connection.cursor() as cursor2:
    for videoId in videoIds:
        time.sleep(0.3) 
        youURL = "https://www.youtube.com/watch?v="
        testVid = youURL + videoId
        cmd = 'youtube-dl '+'--all-subs '+'--skip-download '+'--output'+'='+videoId + ' ' +testVid
        result = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=path)
        errorMessage = ""
        youtubeComplained = False
        for line in result.stdout:
            line = line.rstrip()
            errorMessage += str(line) + "\n" 
            if youtubeComplains(line):
                youtubeComplained = True
        if youtubeComplained:            
            queriedAt = printDateNicely(datetime.now())
            sql3 = "INSERT INTO NOcaptions (videoId, queriedAt, errorMessage) VALUES (%s,%s,%s)"
            cursor2.execute(sql3, (videoId, queriedAt, errorMessage))
            connection.commit()    
            print ("Error message saved to DB!")
        # check for saved files and if they exist do something with them
        dirContents = os.listdir(path)
        if len(dirContents) > 0:
            if len(dirContents) > 1:
                print ("More than 1 captions file!! Actually there were ",  len(dirContents), " !")
            for file in dirContents:
                print (file.split("."))
                n, lang, subFormat = file.split(".")
                # Be careful!! n can contain a different videoId for the same video!!!

                if subFormat == 'vtt':
                    print ("Captions received in .vtt format.")
                    # do something
                    loadIntoSql(videoId, getVtt(PATH+file), readFile(PATH+file), lang, ("."+subFormat), cursor2, connection)

                elif subFormat == 'srt':
                    print ("Captions received in .srt format.")
                    # do something

                elif subFormat == 'ass':
                    print ("Captions received in .ass format. (don't laugh..)")
                    # do something

                # call a big function which processes the file
            clean_directory() # important line or will polute DB!!

print (insertionErrors, " insertion errors in total.")
connection.close()
