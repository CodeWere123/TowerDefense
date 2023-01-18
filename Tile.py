import pygame
from load_image import load_image
from SpriteGroups import tiles_group, all_sprites

# Картинки
tile_images = {
    'r': load_image('road_5.png', ["PNG", "road"]),
    'l':  load_image('land_1.png', ["PNG", "land"])
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_size):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)
