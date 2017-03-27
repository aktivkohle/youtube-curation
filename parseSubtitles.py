# the words "subtitles" and "captions" are used interchangeably

import re

def getVtt(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content] 

    p = re.compile('\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}')

    pureText = ""
    pay_attention = False
    for line in content:
        if p.match(line) != None:
            pay_attention = True   # gets past the metadata in the first few lines
        if pay_attention:
            #do whatever you want
            #print (line)
            if p.match(line) != None:
                pass
            elif line == '':
                pass
            else:
                pureText += line + " "    
    return pureText

# references:
# http://stackoverflow.com/questions/3277503/how-do-i-read-a-file-line-by-line-into-a-list
# http://stackoverflow.com/questions/11665582/regex-for-timestamp 
# http://stackoverflow.com/questions/27805919/how-to-only-read-lines-in-a-text-file-after-a-certain-string-using-python

