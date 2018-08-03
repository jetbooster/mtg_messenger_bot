import re
from difflib import SequenceMatcher

def slugify(name):
    return "".join(x for x in name if x.isalnum())


class LukesCards():
    def __init__(self):
        self.ITERATOR = -1
        self.cards = [
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
    def getNextCard(self):
        self.ITERATOR += 1
        index = self.ITERATOR % len(self.cards)
        return cards[index]



def nicknames(name):
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
        return nicks[name.lower()]
    except KeyError:
        return name


def properNames(corseMatch, name):
    # Can probably improve this so it returns the proper capitalisations
    # for now standardise as lowercase
    corseMatchLower = [l.lower() for l in corseMatch]
    if name in corseMatchLower:
        # if there is an exact full match, return it
        return [name]
    # Prioritise cardnames which contain the search-word surrounded by word boundries
    wordBoundaryPriorityRegex = re.compile(".*\\b{}\\b.*".format(name))
    boundryMatch = [m.group(0) for l in corseMatchLower for m in [wordBoundaryPriorityRegex.search(l)] if m]
    if boundryMatch:
        corseMatchLower = boundryMatch #filter results which did not pass the word boundary filter
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
