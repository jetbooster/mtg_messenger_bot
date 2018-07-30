# -*- coding: UTF-8 -*-

import re
import json
from requests import get
from difflib import SequenceMatcher

from fbchat import Client
from fbchat.models import Message

YOUR_FACEBOOK_USERNAME = ""
YOUR_FACEBOOK_PASSWORD = ""

LUKE_ITERATOR = 0

with open('credentials.txt') as fyl:
    YOUR_FACEBOOK_USERNAME = fyl.readline().strip()
    YOUR_FACEBOOK_PASSWORD = fyl.readline().strip()


# Main regex for detecting bot call. [[content]]
MainRegex = re.compile(r"(?<=\[\[)(.*?)(?=\]\])")


def mtgJson(name):
    try:
        apinames = json.loads(get("http://mtgapi.samus.nl/cardjson/{}".format(name)).text)
        return apinames
    except:
        print("samus.nl api call error")
        return False



def LukesCards(LUKE_ITERATOR):
    cards = [
        'Birthing Pod',
        'Gitaxian Probe',
        'Stoneforge Mystic',
        'Treasure Cruise',
        'Dig Through Time',
        'Ancient Den',
        'Blazing Shoal',
        'Chrome Mox',
        'Cloudpost',
        'Dark Depths',
        'Deathrite Shaman',
        'Dread Return',
        'Eye of Ugin',
        'Glimpse of Nature',
        'Golgari Grave-Troll',
        'Great Furnace',
        'Green Sun\'s Zenith',
        'Hypergenesis',
        'Mental Misstep',
        'Ponder',
        'Preordain',
        'Punishing Fire',
        'Rite of Flame',
        'Seat of the Synod',
        'Second Sunrise',
        'Seething Song',
        'Sensei\'s Divining Top',
        'Skullclamp',
        'Splinter Twin',
        'Summer Bloom',
        'Tree of Tales',
        'Umezawa\'s Jitte',
        'Vault of Whispers',
    ]
    index = LUKE_ITERATOR % len(cards)
    return (cards[index],LUKE_ITERATOR)



def nicknames(name, LUKE_ITERATOR):
    if name.lower() == 'luke':
        LUKE_ITERATOR += 1
        return LukesCards(LUKE_ITERATOR)
    try:
        nicks = {"bob": "Dark Confidant",
                 "gary": "Gray Merchant of Asphodel",
                 "sad robot": "Solemn Simulacrum",
                 "jens": "Solemn Simulacrum",
                 "bolt": "Lightning Bolt",
                 "path": "Path to Exile",
                 "snappy": "Snapcaster Mage",
                 "tiago chan": "Snapcaster Mage",
                 "goyf": "Tarmogoyf",
                 "taylor swift": "Monastery Swiftspear",
                 "mom": "Mother of Runes",
                 "bfm": "B.F.M. (Big Furry Monster)",
                 "i can't even": "Void Winnower",
                 "durdle turtle": "Meandering Towershell",
                 "tim": "Prodigal Sorcerer",
                 "ernie": "Ernham Djinn",
                 "wog": "Wrath of God",
                 "finkel": "Shadowmage Infiltrator",
                 "jon finkel": "Shadowmage Infiltrator",
                 "titi": "Thing in the Ice",
                 "chris pikula": "Meddling Mage",
                 "superman": "Morphling",
                 "gitgud frog": "The Gitrog Monster",
                 "poyser": "Doomed Traveler",
                 "bourne": "Look at me I'm the DCI",
                 "ged": "Grimgrin",
                 "simoon": "Omniscience",
                 "lyndon": "Rakdos, Lord",
                 "ben": "Narset, Enlightened",
                 "josh": "Sowing Salt",
                 "chris": "capsize",
                 "robinson": "Derevi",
                 "merrison": "General Tazri",
                 "science": "Enter the Infinite",
                 "skittles": "Skithiryx",
                 "baby jace": "Jace, Vryn",
                 "lotv": "Liliana of the Veil",
                 "jarvis": "Reclusive Artificer"
                 }
        return (nicks[name.lower()], LUKE_ITERATOR)
    except KeyError:
        return name


def properNames(corseMatch, name):
    # Can probably improve this so it returns the proper capitalisations
    # for now standardise as lowercase
    corseMatchLower = [l.lower() for l in corseMatch]
    NamePriorityRegex = re.compile("^{}(([,])|( of )|( the )).*".format(name.lower()))
    shortnames = [m.group(0) for l in corseMatchLower for m in [NamePriorityRegex.search(l)] if m]
    if shortnames:
        return shortnames
    else:
        return corseMatchLower


def sequenceMatch(closeMatch, name):
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
        return False


def cardFetch(name):
    corseMatch = mtgJson(name)
    closeMatch = properNames(corseMatch, name)
    fineMatch = sequenceMatch(closeMatch, name)
    print(corseMatch)
    print(closeMatch)
    print(fineMatch)
    print("Entered name:{}, Best Match:{}".format(name, fineMatch))
    imageUrl = scryfall(fineMatch)
    if imageUrl:
        return {'imageurl': imageUrl, 'name': name}
    else:
        # If we get here either something went wrong or there as simply no cards with those names
        return False

# Subclass fbchat.Client and override required methods


class MtgBot(Client):
    def __init__(self, username,password):
        super().__init__(username,password)
        self.LUKE_ITERATOR = -1

    def _uploadImage(self, image_path, data, mimetype):
        # mimetype seems a but flakey, force it to be image/jpeg
        return super(MtgBot, self)._uploadImage(image_path, data, "image/jpeg")

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        matchList = MainRegex.findall(message_object.text)
        # Have I been called? if not, do nothing.
        if 'mtgbot:' in message_object.text:
            return
        if len(matchList) != 0:
            for name in matchList:
                alteredName,self.LUKE_ITERATOR = nicknames(name, self.LUKE_ITERATOR)
                if alteredName != name:
                    imageUrl = scryfall(alteredName)
                    if imageUrl:
                        cardData = {'imageurl': imageUrl, 'name': name}
                else:
                    cardData = cardFetch(alteredName)
                if cardData:
                    # if cardData exists, at least one card was found! fire away!
                    # obviously, no gurantee it will be the card you wanted!
                    self.sendRemoteImage(cardData['imageurl'], message=Message(
                        text='mtgbot: {}'.format(cardData['name'])), thread_id=thread_id, thread_type=thread_type)
                else:
                    self.send(message=Message(text='mtgbot: No card found for {}'.format(
                        name)), thread_id=thread_id, thread_type=thread_type)


client = MtgBot(YOUR_FACEBOOK_USERNAME, YOUR_FACEBOOK_PASSWORD)
client.listen()
