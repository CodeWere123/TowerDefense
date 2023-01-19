import pygame
from load_image import load_image
from SpriteGroups import tower_group, all_sprites
import logging
from get_target import get_target
from Projectile import Projectail


class Tower(pygame.sprite.Sprite):
    tower_id = 0

    def __init__(self, pos, tower_type, damage):
        """
        :param pos: позиция
        :param id: айди, уникален для каждого места башни, нужен для снарядов
        :param ttype: тип башни для модели
        :param health: хп
        :param damage: урон, для снарядов
        """
        super().__init__(tower_group, all_sprites)
        self.x, self.y = pos
        self.tower_type = tower_type
        self.damage = damage
        self.tower_id = self.set_tower_id
        self.image = load_image("default.png", ["PNG", "towers"])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        logging.info(f"Башня типа: {tower_type} c айди {self.tower_id}, создана на координатах {pos}")

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, pos):
        self.x, self.y = pos

    def shot(self):
        target = get_target((self.x, self.y))
        if target:
            Projectail((self.x, self.y), (target.x, target.y), 10, 1)

    def destroy(self):
        logging.info(f"[log]: Башня типа: {self.tower_type} c айди {self.tower_id} уничтожена на "
                     f"координатах {self.x, self.y}")

    @classmethod
    def set_tower_id(cls):
        tower_id = cls.tower_id
        cls.tower_id += 1
        return tower_id
