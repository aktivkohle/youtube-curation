from time import sleep
from datetime import datetime

sleep(2)
print ( str(datetime.now()) )
sleep(1)

import searchAPIandLoad_ProductionVersion
print ( str(datetime.now()) )
sleep(60)

import PullIDsfromSQL_RetrieveLikesDislikes
print ( str(datetime.now()) )
sleep(60)

import captionsYoutube_dl_SQL
print ( str(datetime.now()) )

import wordCountColumn  
print ( str(datetime.now()) )
# the last program runs properly but doesn't end gracefully
# could be fixed with change in its loop fetchall instead of 
# fetchone 

