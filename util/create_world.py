from random import randint
from adventure.models import Player, Room
import tracery
from tracery.modifiers import base_english
from room_content import ROOMS

Room.objects.all().delete()

basicRoomFeatures = 'panel,light,cable'


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


grid = map_creator()
anchor_room = grid[0][0]

players = Player.objects.all()

for p in players:
    p.currentRoom = anchor_room.id
    p.save()
