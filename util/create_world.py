from random import randint
from adventure.models import Player, Room
import tracery
from tracery.modifiers import base_english

Room.objects.all().delete()

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
    'featureAdjective': ['smoking', 'broken', 'flashing', 'beeping', 'oversized', 'odd-looking', 'unfamiliar', 'sharp', 'hot', 'regular'],

    'adverb': ['suspiciously', 'strangely', 'worryingly', 'puzzlingly', 'suprisingly', 'curiously'],
    'setTitleType': ['#roomAdjective.capitalize#', '#adverb.capitalize# #roomAdjective.capitalize#'],
    'title': '#setTitleType# #roomName.capitalize#',

    'setFeatureType': ['#feature#', '#featureAdjective# #feature#'],
    'description': [
        # Note: ~tildes~, here, make it possible to scrape features (items) from the room string.
        'You see ~#setFeatureType.a#~.',
        'You see ~#setFeatureType.a#~. And right next to it, ~#setFeatureType.a#~!',
        'You bend over, and spot several ~#setFeatureType.s#~.',
        'You hear a sound behind you and turn around. At your feet is ~#setFeatureType.a#~.',
        'You smell something strange. Following your nose, you find ~#setFeatureType.a#~ and some ~#setFeatureType.s#~.',
        'You peek round the door. There\'s nothing in the room but ~#setFeatureType.a#~.',
        'On the wall you see ~#setFeatureType.a#~. And on the ceiling, ~#setFeatureType.a#~.'
    ],

    'origin': '#[#setRoomName#]title#: #description#'
}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)


def scrapeItems(description):
    items = []

    scraping = False
    item = ''
    for i in range(len(description)):
        if description[i] == "~":
            if not scraping:
                scraping = True
            else:
                items.append(item)
                item = ''
                scraping = False

        if scraping and description[i] != "~":
            item += description[i]

    return items


def removeTildes(description):
    output = ""

    for i in range(len(description)):
        if description[i] != "~":
            output += description[i]

    return output


def generate_room_content(n=100):
    rooms = []
    for _ in range(n):
        roomString = grammar.flatten('#origin#')
        splitRoomString = roomString.split(": ")

        rooms.append({
            'title': splitRoomString[0],
            'description': removeTildes(splitRoomString[1]),
            'items': scrapeItems(splitRoomString[1])
        })

    return rooms


ROOMS = generate_room_content(100)
print(ROOMS)


def grid_populator():
    grid = [[None] * 10 for x in range(10)]
    room_count = 0
    for row, _ in enumerate(grid):
        for room in range(len(grid[row])):
            grid[row][room] = Room(
                title=ROOMS[room_count]['title'],
                description=ROOMS[room_count]['description'], y=row, x=room)
            grid[row][room].save()
            room_count += 1 if room_count < 100 else 0
    return grid


def map_creator():
    grid = grid_populator()
    for idx_y, row in enumerate(grid):
        for idx_x, room in enumerate(row):
            directions = ['n', 's', 'e', 'w']
            connected = False
            if idx_y - 1 < 0:
                directions.remove('n')
            if idx_y + 1 > len(grid) - 1:
                directions.remove('s')
            if idx_x - 1 < 0:
                directions.remove('w')
            if idx_x + 1 > len(row) - 1:
                directions.remove('e')
            while not connected:
                for direction in directions:
                    neighbor = ''
                    opposite = ''
                    if direction == 'n':
                        opposite = 's'
                        neighbor = grid[idx_y - 1][idx_x]
                    if direction == 'e':
                        opposite = 'w'
                        neighbor = grid[idx_y][idx_x + 1]
                    if direction == 'w':
                        opposite = 'e'
                        neighbor = grid[idx_y][idx_x - 1]
                    if direction == 's':
                        opposite = 'n'
                        neighbor = grid[idx_y + 1][idx_x]
                    connection_decider = randint(0, 1)
                    if connection_decider:
                        room.connectRooms(neighbor, direction)
                        neighbor.connectRooms(room, opposite)
                        connected = True
    return grid


GRID = map_creator()
ANCHOR_ROOM = GRID[0][0]

PLAYERS = Player.objects.all()
for p in PLAYERS:
    p.currentRoom = ANCHOR_ROOM.id
    p.save()
