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

def tweet(e):
    print e.title
    try:
        title = e.title.split(', ')
        tweet_str = title[0] + ' earthquake hits ' + title[3] + ' on ' + title[1] + ', ' + title[2]
    except:
        log(time.strftime("%c") + ": Warning - title not formatted properly")
        tweet_str = title[0]
        
    print tweet_str
    config = json.load(open('./config.json'))
    
    # try:
    twitter = Twython(
        config['twitter']['app_key'],
        config['twitter']['app_secret'],
        config['twitter']['oauth_token'],
        config['twitter']['oauth_token_secret'])

    twitter.update_status(status=tweet_str)
    # except:
    #     log(time.strftime("%c") + ": Error - failed to send tweet")

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
        
