import os
from Tile import Tile


class Map:
    def __init__(self, filename):
        self.map_data = self.load_map(filename)
        self.map_filename = self.map_data[0]
        self.map_name = self.map_data[1]
        self.height = int(self.map_data[2])
        self.width = int(self.map_data[3])
        self.level_map = self.map_data[4]
        self.tiles = []
        self.path = []
        self.generate_level()

    def load_map(self, filename):
        filename = os.path.join("data", "maps", filename)
        with open(filename, 'r') as mapFile:
            mapFile = mapFile.readlines()
            info = list(mapFile)[0].split(";")
            level_map = [line.strip().split(";") for line in list(mapFile)[1:]]
        map_filename = info[0]
        map_name = info[1]
        h, w = info[2:]
        return [map_filename, map_name, h, w, level_map]

    def generate_level(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = Tile(self.level_map[y][x], x, y)
                self.tiles.append(tile)
                if self.level_map[y][x] == 'road_5':
                    self.path.append((x, y))
        start_x = self.path[0][0]
        start_y = self.path[0][1]
        if start_x == 0:
            self.path.insert(0, (start_x - 0.5, start_y))
        elif start_x == self.width - 1:
            self.path.insert(0, (start_x + 0.5, start_y))
        elif start_y == 0:
            self.path.insert(0, (start_x, start_y - 0.5))
        elif start_y == self.height - 1:
            self.path.insert(0, (start_x, start_y + 0.5))
        print(self.path)

