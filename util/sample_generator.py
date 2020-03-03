from random import randint
from room_content import generate_room_content

ROOMS = generate_room_content(100)


class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y

    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)

    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 10
        self.height = 10

    def generate_rooms(self, size_x, size_y, num_rooms):
        def grid_populator():
            """This generates a 2D array for the grid system and populates it"""
            # Create a 2D array containing 10 inner lists and 10 items in each
            grid = [[None] * 10 for x in range(10)]
            room_count = 0
            # Create a 2D array containing 10 inner lists and 10 items in each"""
            for row, _ in enumerate(grid):
                for room in range(len(grid[row])):
                    grid[row][room] = Room(id=room_count,
                                           name=ROOMS[room_count]['title'], description=ROOMS[room_count]['description'], y=row, x=room)
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
                                room.connect_rooms(neighbor, direction)
                                neighbor.connect_rooms(room, opposite)
                                connected = True
            return grid

        self.grid = map_creator()

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 44
width = 8
height = 7
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(
    f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
