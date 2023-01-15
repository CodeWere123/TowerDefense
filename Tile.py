import pygame
from load_image import load_image
from SpriteGroups import tiles_group, all_sprites

# Картинки
tile_images = {
    'road_1': load_image('road_1.png', ["PNG", "road"]),
    'road_2': load_image('road_2.png', ["PNG", "road"]),
    'road_3': load_image('road_3.png', ["PNG", "road"]),
    'road_4': load_image('road_4.png', ["PNG", "road"]),
    'road_5': load_image('road_5.png', ["PNG", "road"]),
    'road_6': load_image('road_6.png', ["PNG", "road"]),
    'road_7': load_image('road_7.png', ["PNG", "road"]),
    'road_8': load_image('road_8.png', ["PNG", "road"]),
    'road_9': load_image('road_9.png', ["PNG", "road"]),
    'road_10': load_image('road_10.png', ["PNG", "road"]),
    'road_11': load_image('road_11.png', ["PNG", "road"]),
    'road_12': load_image('road_12.png', ["PNG", "road"]),
    'road_13': load_image('road_13.png', ["PNG", "road"]),
    'land_1':  load_image('land_1.png', ["PNG", "land"])
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_size):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)
