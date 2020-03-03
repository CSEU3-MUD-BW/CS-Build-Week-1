from util.create_world import MapWorld
from adventure.models import Player

world = MapWorld()
world_map = world.map_creator()

players = Player.objects.all()
for p in players:
    p.currentRoom = world_map[0][0].id
    p.save()
