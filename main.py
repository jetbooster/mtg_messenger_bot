# -*- coding: UTF-8 -*-

import re
import os
import sys
import json
from requests import get
from difflib import SequenceMatcher

from fbchat import log, Client
from fbchat.models import *

YOUR_FACEBOOK_EMAIL = "YOUR EMAIL HERE"

if "MTG_BOT_PASSWORD" in os.environ:
    YOUR_FACEBOOK_PASSWORD = os.environ.get('MTG_BOT_PASSWORD')
else:
    print("Set your password using environment variables! `MTG_BOT_PASSWORD=password python main.py` no space around '='")
    sys.exit(1)


# Main regex for detecting bot call. [[content]]
MainRegex = re.compile(r"(?<=\[\[)(.*?)(?=\]\])")

# regex for detecting short names, which should take precedence over 'blahblah of {name}'


def mtgJson(name):
    try:
        apinames = json.loads(get("http://mtgapi.samus.nl/cardjson/{}".format(name)).text)
        return apinames
    except:
        print("samus.nl api call error")
        return False

def properNames(corseMatch,name):
    # Can probably improve this so it returns the proper capitalisations
    # for now standardise as lowercase
    corseMatchLower = [l.lower() for l in corseMatch]
    NamePriorityRegex = re.compile("^{}(([,])|( of )|( the )).*".format(name.lower()))
    shortnames = [m.group(0) for l in corseMatchLower for m in [NamePriorityRegex.search(l)] if m]
    if shortnames:
        return shortnames
    else:
        return corseMatchLower

def sequenceMatch(closeMatch,name):
    score = 0
    best = ""
    for i in closeMatch:
        newscore = SequenceMatcher(None, name.lower(), i.lower()).ratio()
        if newscore > score:
            best = i
            score = newscore
    return best

def scryfall(name):
    try:
        scryfall = json.loads(get("https://api.scryfall.com/cards/search?q={}".format(name)).text)
        # get the normal sized image, strip query param
        return scryfall['data'][0]['image_uris']['normal'].split("?")[0]
    except:
        print("scryfall api call error")
        raise
        return False

def cardFetch(name):
    corseMatch = mtgJson(name)
    closeMatch = properNames(corseMatch,name)
    fineMatch = sequenceMatch(closeMatch,name)
    print("Entered name:{}, Best Match:{}".format(name,fineMatch))
    imageUrl = scryfall(fineMatch)
    if imageUrl:
        return {'imageurl':imageUrl,'name':name}
    else:
        # If we get here either something went wrong or there as simply no cards with those names
        return False

# Subclass fbchat.Client and override required methods
class MtgBot(Client):
    def _uploadImage(self,image_path, data, mimetype):
        #mimetype seems a but flakey, force it to be image/jpeg
        return super(MtgBot,self)._uploadImage(image_path, data, "image/jpeg")

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        matchList = MainRegex.findall(message_object.text)
        # Have I been called? if not, do nothing.
        if len(matchList) != 0:
            for name in matchList:
                cardData = cardFetch(name)
                if cardData:
                    # if cardData exists, at least one card was found! fire away!
                    #obviously, no gurantee it will be the card you wanted!
                    self.sendRemoteImage(cardData['imageurl'],message=Message(text='mtgbot: '+cardData['name']), thread_id=thread_id, thread_type=thread_type)


client = MtgBot(YOUR_FACEBOOK_EMAIL, YOUR_FACEBOOK_PASSWORD)
client.listen()
