import datetime

class SeparateTimeTrackers():
    
    def __init__(self, name): 
        print ("class initiated")
        self.__counter = 1   # more user friendly if starts at 1   
        self.__name = name   # stop someone seeing and changing the name variable once set.
        
    def timer(self):
        print (self.__name, self.__counter, datetime.datetime.now())
        self.__counter += 1
