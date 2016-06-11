#***************************************************
#
# Earthquake Tweeter
# Author: Ash Williams
#
# 1.Monitor earthquake data
# 2.If new earthquake detected, tweet it 
#
#***************************************************
import time
import json
import sys
from twython import Twython

global last_entry

def log(text):
   with open("./quake-tweeter.log", "a") as log:
        log.write(text + '\n') 
    
def initialize():
    global last_entry
    last_entry = "http://geonet.org.nz/quakes/2016p434709"
    
    log(time.strftime("%c") + ": Initialized")
    


def checkFeed():
    try:
        import feedparser
        d = feedparser.parse('http://www.geonet.org.nz/quakes/services/felt.rss')
        
        
        global last_entry, previous_entry
        if last_entry == d.entries[0].id:
            return False
        else:
            previous_entry = last_entry
            last_entry = d.entries[0].id
            log(time.strftime("%c") + ": Feed Updated - " + d.entries[0].id)
            return d
    except:
        log(time.strftime("%c") + ": Error - retrieving feed")
        return False

def convertMonthToNum(monthStr):
    if monthStr == 'Jan':
        month = 1
    elif monthStr == 'Feb':
        month = 2
    elif monthStr == 'Mar':
        month = 3
    elif monthStr == 'Apr':
        month = 4
    elif monthStr == 'May':
        month = 5
    elif monthStr == 'Jun':
        month = 6
    elif monthStr == 'Jul':
        month = 7
    elif monthStr == 'Aug':
        month = 8
    elif monthStr == 'Sep':
        month = 9
    elif monthStr == 'Oct':
        month = 10
    elif monthStr == 'Nov':
        month = 11
    elif monthStr == 'Dec':
        month = 12
    else:
        month = -1
    
    return month

def send_tweet(tweet_str):
    log(time.strftime("%c") + ": Tweeting: " + tweet_str)
    config = json.load(open('./config.json'))
    
    try:
        twitter = Twython(
            config['twitter']['app_key'],
            config['twitter']['app_secret'],
            config['twitter']['oauth_token'],
            config['twitter']['oauth_token_secret'])
    
        twitter.update_status(status=tweet_str)
    except:
        log(time.strftime("%c") + ": Error - failed to send tweet")

def tweet(e):
    # 
    # print e.title
    try:
        title = e.title.split(', ')
        
        import datetime as dt
        import os
        os.environ['TZ'] = 'NZ'
        time.tzset()
        current = time.strftime("%c").split()
        currentTime = current[3].split(':')
        year = int(current[4])
        month = convertMonthToNum(current[1])
        day = int(current[2])
        hour = int(currentTime[0])
        minute = int(currentTime[1])
        second = int(currentTime[2])
        # print year, month, day, hour, minute, second
        curr_date = dt.datetime(year,month,day,hour,minute,second)
        
        quake = title[2].split()
        quakeTime = quake[4].split(':')
        year = int(quake[2])
        month = convertMonthToNum(quake[0])
        day = int(quake[1])
        hour = int(quakeTime[0])
        
        if quake[5] == 'pm':
            hour += 12
            hour = hour % 24
        
        minute = int(quakeTime[1])
        second = int(quakeTime[2])
        # print year, month, day, hour, minute, second
        quake_date = dt.datetime(year,month,day,hour,minute,second)
        
        time_difference = (curr_date - quake_date).total_seconds()
        
        # print time_difference
        
        if time_difference <= 300:
            send_tweet(title[0] + ' earthquake hits ' + title[3] + ' on ' + title[1] + ', ' + title[2])
        else:
            log(time.strftime("%c") + ": Info - tweet not sent, too much time has passed. Secs: " + str(time_difference))
    
    except:
        print("Unexpected error:", sys.exc_info()[0])
        log(time.strftime("%c") + ": Warning - troubles formatting or the timing is off")

def main():
    initialize()
    
    while(True):
        d = checkFeed()
        if d != False:
            for e in d.entries:
                if e.id == previous_entry:
                    break
                else:
                    tweet(e)
        time.sleep(60)

if __name__ == '__main__':
    main()
        
