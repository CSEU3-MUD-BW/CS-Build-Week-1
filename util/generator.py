"""This is a module method to generate random integers."""
from random import randint
from adventure.models import Player, Room
from room_content_generator import generate_room_content

Room.objects.all().delete()

ROOMS = generate_room_content(100)


def grid_populator():
    """This generates a 2D array for the grid system and populates it"""
    # Create a 2D array containing 10 inner lists and 10 items in each
    grid = [[None] * 10 for x in range(10)]
    room_count = 0
    # Create a 2D array containing 10 inner lists and 10 items in each"""
    for row, _ in enumerate(grid):
        for room in range(len(grid[row])):
            grid[row][room] = Room(
                title=ROOMS[room_count]['title'], description=ROOMS[room_count]['description'], y=row, x=room)
            grid[row][room].save()
            room_count += 1 if room_count < 100 else 0
    return grid


def map_creator():
    """This generates the map by linking rooms via relevant cardinal points"""
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
                    neighbor, opposite = '', ''
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
