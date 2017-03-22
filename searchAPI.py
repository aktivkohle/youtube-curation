import requests
import config
import dateutil.parser
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import pprint
import pickle

logfileName = datetime.now().strftime("%d%B%Y%I:%M:%S%p") + '_Logfile.txt'
f = open(logfileName, 'w')

youtubeObjects = {}

def printDateNicely(timestamp):
    reg_format_date = timestamp.strftime("%d %B %Y %I:%M:%S %p")
    print(reg_format_date)

def storeMe(objts, ytDict):
    t = time.time()
    if (t not in list(ytDict)):
        ytDict.update({t:objts})
    else:
        print ("Oh no timestamp already in there :(")    

def wr(message, p, fi):    # to write to log file
    f.write(str(message))
    f.write('\n')
    q = dict(p)
    q['key'] = 'googleAPIkey'
    pprint.pprint(q, fi)
    f.write('\n')
    
def zed(ts):
    ending = ts[-1:]
    if ending == 'Z':
        return ts[:-1] + '.000Z'   
    else:
        return ts + '.000Z'
    
printDateNicely(datetime.now())

payload = {'key': config.GOOGLE_API_KEY, 
    'part': 'snippet', 
    'q': 'dog+training',     
    'order' : 'date',                  # reverse chronological of creation
    'type':'video',
    'videoCaption':'closedCaption',    # includes captions. 
    'maxResults':50}    


counter = 0
begin_string = '2017-02-01T00:00:00Z'
end_datetime = dateutil.parser.parse(begin_string).replace(tzinfo=None)
end_of_month_string = '2017-03-01T00:00:00Z' 
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
            storeMe(objects, youtubeObjects)

        elif 'nextPageToken' in list(objects):
            storeMe(objects, youtubeObjects)
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
                    storeMe(objects, youtubeObjects)
                    daycount += 1
                else:
                    print (bs, statuscode)
                time.sleep( 1/5 )
                wr(3, payload, f)
                if len(objects['items']) == 0:
                    itemsEmpty += 1
                if itemsEmpty > 3:
                    break
                    
            print(daycount, " pages of results today.")
            wr(4, payload, f)
            payload.pop('pageToken')  
            wr(5, payload, f)
            # Very importantly! 
            # now that this section is finished clean out that key from the dictionary!!!
                    
    else:
        print ("statuscode : ", statuscode)

    time.sleep( 1/5 ) 

    counter += 1
    if counter % 500 == 0:
        print (counter)
                        
print ('\n')
printDateNicely(datetime.now())

f.close()


# Pickle the 'data' dictionary using the highest protocol available.
with open('DogsOfFebruary2017.pickle', 'wb') as f:
    pickle.dump(youtubeObjects, f, pickle.HIGHEST_PROTOCOL)
