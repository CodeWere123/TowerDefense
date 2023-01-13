import math
import pygame
from load_image import load_image

enemy_images = {
    'enemy1': load_image("enemy1.png", ["PNG", "enemy"]),
    'enemy2': load_image("enemy2.png", ["PNG", "enemy"])

}


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, speed, damage, etype, im, path, start, difficulty):
        super().__init__()
        self.health = round(health * (1 + (difficulty - 1) * 0.5))
        self.speed = round(speed * (1 + (difficulty - 1) * 0.1))
        self.damage = math.floor(damage * (1 + (difficulty - 1) * 0.5))
        self.etype = etype
        self.path = path
        self.x = start[0]
        self.y = start[1]
        self.current_path_part = 0
        self.image = enemy_images[im]

    def update(self):
        part_x, part_y = path_part = self.path[self.current_path_part]
        difference = (part_x - self.x, part_y - self.y)
        self.x -= int(bool(difference[0])) * self.speed
        self.y -= int(bool(difference[1])) * self.speed
        if (part_x - self.x, part_y - self.y) != difference:
            self.x, self.y = part_x, part_y
            self.current_path_part += 1

    def get_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            del self
