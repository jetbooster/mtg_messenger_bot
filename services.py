import os
import json
import utils
from PIL import Image
from io import BytesIO
from requests import get

import utils

def scryfall(name):
    try:
        scryfall = json.loads(get("https://api.scryfall.com/cards/search?q={}".format(name)).text)
        # Prioritise full name match within results, otherwise first result.
        index = 0
        for card in scryfall['data']:
            if name == card['name']:
                index = scryfall['data'].index(card)

        if (scryfall['data'][index].get('card_faces')):
            card_face_urls = [card_face['image_uris']['normal'].split('?')[0] for card_face in scryfall['data'][index]['card_faces']]
            return ({
                'imageurls': card_face_urls,
                'name': scryfall['data'][index]['name'],
                'dualfaced': True
            })


        else:
            return ({
                'imageurls': [scryfall['data'][index]['image_uris']['normal'].split("?")[0]],
                'name': scryfall['data'][index]['name'],
                'dualfaced': False
            })
    except Exception as e:
        print("scryfall api call error")
        print(e)
        return False

def mtgJson(name):
    try:
        apinames = json.loads(get("http://mtgapi.samus.nl/cardjson/{}".format(name)).text)
        return apinames
    except:
        print("samus.nl api call error")
        return False

def cardFetch(name):
    corseMatch = mtgJson(name)
    closeMatch = utils.properNames(corseMatch, name)
    fineMatch = utils.sequenceMatch(closeMatch, name)
    print(corseMatch)
    print(closeMatch)
    print(fineMatch)
    print("Entered name:{}, Best Match:{}".format(name, fineMatch))
    return scryfall(fineMatch)

def buildDualFaced(cardData):
    cachedImages = os.listdir('cache')
    sluggedFileName = '{}.jpg'.format(utils.slugify(cardData['name']))
    if sluggedFileName in cachedImages:
        print("file in cache")
        return sluggedFileName
    else:
        print("file not in cache")
        imageRequests = map(get,cardData['imageurls'])
        images = [Image.open(img) for img in [BytesIO(image.content) for image in imageRequests]]
        widths, heights = zip(*(i.size for i in images))
        total_width = 976
        max_height = 680
        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0

        for im in images:
          new_im.paste(im, (x_offset,0))
          x_offset += im.size[0]
        new_im.save('./cache/{}'.format(sluggedFileName))
        return sluggedFileName
