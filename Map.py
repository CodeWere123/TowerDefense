import os
from Tile import Tile


class Map:
    def __init__(self, filename):
        self.map_data = self.load_map(filename)
        self.map_filename = self.map_data[0]
        self.map_name = self.map_data[1]
        self.height = int(self.map_data[2])
        self.width = int(self.map_data[3])
        self.start_tile = [int(x) for x in self.map_data[4]]
        self.tile_size = int(self.map_data[5])
        self.level_map = self.map_data[6]
        self.tiles = []
        self.paths = self.generate_path(*self.start_tile)
        self.generate_level()

    # Файл карты примера находится в data/maps/ , а тут код превращает txt в что-то человеческое
    @staticmethod
    def load_map(filename):
        filename = os.path.join("data", "maps", filename)
        with open(filename, 'r') as mapFile:
            mapFile = mapFile.readlines()
            info = list(mapFile)[0].split(";")
            level_map = [line.strip().split(";") for line in list(mapFile)[1:]]
        map_filename = info[0]
        map_name = info[1]
        h, w = info[2:4]
        start_tile = info[4:6]
        tile_size = info[6]
        return [map_filename, map_name, h, w, start_tile, tile_size, level_map]
    
    # Это функция работает наполовину
    def generate_level(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = Tile(self.level_map[y][x], x, y, self.tile_size)
                self.tiles.append(tile)

    def generate_path(self, start_x, start_y, exclude_list=None):
        if exclude_list is None:
            exclude_list = []
        paths = []
        exclude_list.append((start_x, start_y))
        neighbours = self.get_valid_neighbours(start_x, start_y, exclude_list)
        if not neighbours:
            return [exclude_list]
        for nx, ny in neighbours:
            paths += self.generate_path(nx, ny, exclude_list)
        return paths

    @staticmethod
    def tile_to_screen(tile_x, tile_y, tile_size):
        screen_x = tile_x * tile_size + tile_size / 2
        screen_y = tile_y * tile_size + tile_size / 2
        return screen_x, screen_y

    def get_valid_neighbours(self, x, y, exclude_list):
        neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        valid_neighbours = []
        for nx, ny in neighbours:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.level_map[ny][nx] == 'road_5' and (nx, ny) not in exclude_list:
                    valid_neighbours.append((nx, ny))
        return valid_neighbours

    def get_start_or_end_coords(self, tile_x, tile_y):
        screen_x, screen_y = self.tile_to_screen(tile_x, tile_y, self.tile_size)
        if tile_x == 0:
            screen_x -= self.tile_size / 2
        elif tile_x == self.width - 1:
            screen_x += self.tile_size / 2
        elif tile_y == 0:
            screen_y -= self.tile_size / 2
        elif tile_y == self.height - 1:
            screen_y += self.tile_size / 2
        return screen_x, screen_y

    def paths_to_screen_coordinates(self, paths_list):
        screen_paths = []
        for path in paths_list:
            screen_path = [self.get_start_or_end_coords(path[0][0], path[0][1])]
            for tile_x, tile_y in path:
                screen_x, screen_y = self.tile_to_screen(tile_x, tile_y, self.tile_size)
                screen_path.append((screen_x, screen_y))
            screen_path.append(self.get_start_or_end_coords(path[-1][0], path[-1][1]))
            screen_paths.append(screen_path)
        return screen_paths
