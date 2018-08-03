# -*- coding: UTF-8 -*-

import re
import os

from fbchat import Client
from fbchat.models import Message

import utils
import services


# Subclass fbchat.Client and override required methods
class MtgBot(Client):
    def __init__(self, username, password):
        super().__init__(username,password)
        self.LukesCards = utils.LukesCards()
        self.MainRegex = re.compile(r"(?<=\[\[)(.*?)(?=\]\])")

    def _uploadImage(self, image_path, data, mimetype):
        # mimetype seems a but flakey, force it to be image/jpeg
        return super()._uploadImage(image_path, data, "image/jpeg")

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        matchList = self.MainRegex.findall(message_object.text)
        # Have I been called? if not, do nothing.
        if 'mtgbot:' in message_object.text:
            return
        if len(matchList) != 0:
            for name in matchList:
                if name.lower() == 'luke':
                    alteredName =  self.LukesCards.getNextCard()
                else:
                    alteredName = utils.nicknames(name)
                if alteredName != name:
                    # A nickname has been found, jump straight to scryfall
                    cardData = services.scryfall(alteredName)
                else:
                    cardData = services.cardFetch(alteredName)

                if cardData:
                    # if cardData exists, the best match was found! fire away!
                    # obviously, no gurantee it will be the card you wanted!
                    if cardData['dualfaced']:
                        #check in file cache
                        filename = services.buildDualFaced(cardData)
                        self.sendLocalImage('./cache/{}'.format(filename), message=Message(
                            text='mtgbot: {}'.format(cardData['name'])), thread_id=thread_id, thread_type=thread_type)

                    else:
                        self.sendRemoteImage(cardData['imageurls'][0], message=Message(
                            text='mtgbot: {}'.format(cardData['name'])), thread_id=thread_id, thread_type=thread_type)
                else:
                    self.send(message=Message(text='mtgbot: No card found for {}'.format(
                        name)), thread_id=thread_id, thread_type=thread_type)


if __name__ == "__main__":
    YOUR_FACEBOOK_USERNAME = ""
    YOUR_FACEBOOK_PASSWORD = ""

    with open('credentials.txt') as fyl:
        YOUR_FACEBOOK_USERNAME = fyl.readline().strip()
        YOUR_FACEBOOK_PASSWORD = fyl.readline().strip()

    if not 'cache' in os.listdir('.'):
        os.mkdir('./cache')
    client = MtgBot(YOUR_FACEBOOK_USERNAME, YOUR_FACEBOOK_PASSWORD)
    client.listen()
