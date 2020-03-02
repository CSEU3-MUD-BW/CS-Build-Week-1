import tracery
from tracery.modifiers import base_english

basicRoomFeatures = 'panel,light,cable'

rules = {
    'setRoomName': [
        f'[roomName:room][feature:{basicRoomFeatures}]',
        f'[roomName:corridor][feature:{basicRoomFeatures}]', 
        f'[roomName:medbay][feature:{basicRoomFeatures},medkit,empty bed]',
        f'[roomName:armoury][feature:{basicRoomFeatures},phaser,pistol,assault rifle,grenade,odd-looking gun]',
        f'[roomName:quarters][feature:{basicRoomFeatures},mirror,jewel,family photo]',
        f'[roomName:bridge][feature:{basicRoomFeatures},chair,flight computer]',
        f'[roomName:brig][feature:{basicRoomFeatures},force field,handcuff]',
        f'[roomName:passageway][feature:{basicRoomFeatures},communicator]',
        f'[roomName:laboratory][feature:{basicRoomFeatures},test tube,centrifuge,lazer]',
        f'[roomName:mess-hall][feature:{basicRoomFeatures},pot,pan,vegetable,fruit,plate,knife,fork,replicator]',
        f'[roomName:engine-room][feature:{basicRoomFeatures},pipe,reactor,green gelatinous puddle]',
    ],
    'roomAdjective': ['dark', 'smoky', 'dangerous-looking', 'messy', 'quiet', 'irradiated', 'full', 'empty', 'packed', 'stripped', 'ransacked'],
    'featureAdjective': ['smoking', 'broken', 'flashing', 'beeping', 'oversized', 'odd-looking', 'unfamiliar', 'sharp', 'hot'],

    'adverb': ['suspiciously', 'strangely', 'worryingly', 'puzzlingly', 'suprisingly', 'curiously'],
    'setTitleType': ['#roomAdjective.capitalize#', '#adverb.capitalize# #roomAdjective.capitalize#'],
    'title': '#setTitleType# #roomName.capitalize#',

    'setFeatureType': ['#feature#', '#featureAdjective# #feature#'],
    'description': [
        'You see ~#setFeatureType.a#~.', #Note: ~tildes~, here, make it possible to scrape features (items) from the room string.
        'You bend over, and spot several ~#setFeatureType.s#~.',
        'You hear a sound behind you and turn around. At your feet is ~#setFeatureType.a#~.'
    ],

    'origin': '#[#setRoomName#]title#: #description#'
    }

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)

# def scrapeItems(str):
#     for i in range(len(str)):
#         item = ''
        # scraping = 

rooms = []
for i in range(50):
    roomString = grammar.flatten('#origin#')
    splitRoomString = roomString.split(": ")

    rooms.append({
        'title': splitRoomString[0],
        'description': splitRoomString[1]
    })

print(rooms)