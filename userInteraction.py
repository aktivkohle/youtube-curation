import sys
from dateutil.relativedelta import relativedelta
import dateparser

def zed(ts):
    ending = ts[-1:]
    if ending == 'Z':
        return ts[:-1] + '.000Z'   
    else:
        return ts + '.000Z'


def askTheUser():
    input1 = input("\n\nPlease enter the month and year in of the period over which\nyou would like to run your query. Either two months seperated by\na 'to' like July2015 to Sept2015 or otherwise just \none month. You can write the whole month or the standard abbreviation. \nPlease write the whole year (4 digits)\n\n\n  -------> ")

    months = input1.split('to')
    if len(months) == 0:
        print ("no input detected")
        sys.exit()
    elif len(months) == 1:
        d = dateparser.date.DateDataParser(settings={'PREFER_DAY_OF_MONTH': 'first'}).get_date_data(months[0])['date_obj']
        D1 = d
        D2 = d + relativedelta(months=1)
        d_str1 = zed(D1.isoformat())
        d_str2 = zed(D2.isoformat())
        print ("\n")
        print (d_str1, 'to', d_str2)    

    elif len(months) == 2:
        d1 = dateparser.date.DateDataParser(settings={'PREFER_DAY_OF_MONTH': 'first'}).get_date_data(months[0])['date_obj']
        d2 = dateparser.date.DateDataParser(settings={'PREFER_DAY_OF_MONTH': 'last'}).get_date_data(months[1])['date_obj']
        d2 = d2 + relativedelta(days=1)
        d_str1 = zed(d1.isoformat())
        d_str2 = zed(d2.isoformat())
        print ("\n")
        print (d_str1, 'to', d_str2)
    else:
        print ("no input detected")
        sys.exit() 

    input2 = input("\n\n\nPlease enter the query term you would like to use. \nSeperate words with a plus sign (\"+\")\nPress ENTER for default search term of \"machine+learning\".\n\n\n\n  -------> ")
    if input2 == '':
        input2 = 'machine+learning'
    
    userResponses = (d_str1, d_str2, input2)
    
    input3 = input("\n\nOk thanks. About to run a query to the API and save the results to the DB.\n\n Requested search terms were:\n\n %s\t%s\t%s\n\n Type \"yes\" and press ENTER to proceed.\n\n\n\n  -------> " % userResponses)
    
    if input3 == "yes":
        return userResponses
    else:
        print ("Goodbye!")
        return None # then if askTheUser() = None in calling program
