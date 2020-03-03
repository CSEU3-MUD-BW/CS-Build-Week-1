from random import randint
from adventure.models import Room
from util.room_content import ROOMS


Room.objects.all().delete()


class MapWorld:
    def __init__(self):
        self.grid = []

    def map_creator(self):
        def grid_populator():
            grid = [[None] * 10 for x in range(10)]
            room_count = 0
            for row in range(len(grid)):
                for room in range(len(grid[row])):
                    grid[row][room] = Room(
                        title=ROOMS[room_count]['title'], description=ROOMS[room_count]['description'])
                    grid[row][room].save()
                    # room_count += 1
            return grid

        self.grid = grid_populator()
        for idx_y, row in enumerate(self.grid):
            for idx_x, room in enumerate(row):
                directions = ['n', 's', 'e', 'w']
                connected = False
                if idx_y - 1 < 0:
                    directions.remove('n')
                if idx_y + 1 > len(self.grid) - 1:
                    directions.remove('s')
                if idx_x - 1 < 0:
                    directions.remove('w')
                if idx_x + 1 > len(row) - 1:
                    directions.remove('e')
                while not connected:
                    for direction in directions:
                        neighbor = ''
                        if direction == 'n':
                            opposite = 's'
                            neighbor = self.grid[idx_y - 1][idx_x]
                        if direction == 'e':
                            opposite = 'w'
                            neighbor = self.grid[idx_y][idx_x + 1]
                        if direction == 'w':
                            opposite = 'e'
                            neighbor = self.grid[idx_y][idx_x - 1]
                        if direction == 's':
                            opposite = 'n'
                            neighbor = self.grid[idx_y + 1][idx_x]
                        connection_decider = randint(0, 1)
                        if connection_decider:
                            room.connectRooms(neighbor, direction)
                            neighbor.connectRooms(room, opposite)
                            connected = True
        return self.grid
