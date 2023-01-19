import pygame
from load_image import load_image
from SpriteGroups import tower_group, all_sprites
import logging
from get_target import get_target, get_random
from Projectile import Projectail
from SpriteGroups import enemy_group
import random

class Tower_default(pygame.sprite.Sprite):
    tower_id = 0

    def __init__(self, pos, tower_type, damage, kd):
        """
        :param pos: позиция
        :param id: айди, уникален для каждого места башни, нужен для снарядов
        :param ttype: тип башни для модели
        :param health: хп
        :param damage: урон, для снарядов
        """
        super().__init__(tower_group, all_sprites)
        self.x, self.y = pos
        self.kd = kd
        self.tower_type = tower_type
        self.damage = damage
        self.tower_id = self.set_tower_id
        self.image = load_image("mortira.png", ["PNG", "towers"])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        logging.info(f"Башня типа: {tower_type} c айди {self.tower_id}, создана на координатах {pos}")

    def get_pos(self):
        return self.x, self.y

    def upgrade(self, pos):
        self.damage += 10 #ТУТ нз САМ СМОТРИ ПО БАЛАНСУ

    def shot(self):
        pygame.time.set_timer(self.tower_id, self.kd)
        target = get_target((self.x, self.y))
        if target:
            Projectail((self.x, self.y), (target.x, target.y), 10, 1)

    def destroy(self):
        logging.info(f"[log]: Башня типа: {self.tower_type} c айди {self.tower_id} уничтожена на "
                     f"координатах {self.x, self.y}")
        tower_group.remove(self)
        all_sprites.remove(self)
        self.kill()

    @classmethod
    def set_tower_id(cls):
        tower_id = cls.tower_id
        cls.tower_id += 1
        return tower_id

class Tower_killer(pygame.sprite.Sprite):
    tower_id = 0

    def __init__(self, pos, damage, kd):
        """
        :param pos: позиция
        :param id: айди, уникален для каждого места башни, нужен для снарядов
        :param ttype: тип башни для модели
        :param health: хп
        :param damage: урон, для снарядов
        """
        super().__init__(tower_group, all_sprites)
        self.x, self.y = pos
        self.kd = kd

        self.damage = damage
        self.tower_id = self.set_tower_id
        self.image = load_image("killer.png", ["PNG", "towers"])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


    def get_pos(self):
        return self.x, self.y

    def upgrade(self, pos):
        self.kd -= 10 #ТУТ нз САМ СМОТРИ ПО БАЛАНСУ

    def shot(self):
        pygame.time.set_timer(self.tower_id, self.kd)

        target = random.choice(enemy_group)
        if target:
            enemy_group.remove(target)
            all_sprites.remove(target)

    def destroy(self):
        tower_group.remove(self)
        all_sprites.remove(self)
        self.kill()

    @classmethod
    def set_tower_id(cls):
        tower_id = cls.tower_id
        cls.tower_id += 51
        return tower_id

class golden_cave(pygame.sprite.Sprite):
    tower_id = 0

    def __init__(self, pos, kd):
        """
        :param pos: позиция
        :param id: айди, уникален для каждого места башни, нужен для снарядов
        :param ttype: тип башни для модели
        :param health: хп
        :param damage: урон, для снарядов
        """
        super().__init__(tower_group, all_sprites)
        self.x, self.y = pos
        self.kd = kd
        self.tower_id = self.set_tower_id
        self.image = load_image("mining.png", ["PNG", "towers"])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


    def get_pos(self):
        return self.x, self.y

    def upgrade(self, pos):
        pygame.time.set_timer(self.tower_id, self.kd)
        self.kd -= 10 #ТУТ нз САМ СМОТРИ ПО БАЛАНСУ

    def shot(self):
        pygame.time.set_timer(self.tower_id, self.kd)
        #экономики нет!

    def destroy(self):
        tower_group.remove(self)
        all_sprites.remove(self)
        self.kill()

    @classmethod
    def set_tower_id(cls):
        tower_id = cls.tower_id
        cls.tower_id += 51
        return tower_id

class archer(pygame.sprite.Sprite):
    tower_id = 0

    def __init__(self, pos, tower_type, damage, kd):
        """
        :param pos: позиция
        :param id: айди, уникален для каждого места башни, нужен для снарядов
        :param ttype: тип башни для модели
        :param health: хп
        :param damage: урон, для снарядов
        """
        super().__init__(tower_group, all_sprites)
        self.x, self.y = pos
        self.kd = kd
        self.tower_type = tower_type
        self.damage = damage
        self.tower_id = self.set_tower_id
        self.image = load_image("archer.png", ["PNG", "towers"])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        logging.info(f"Башня типа: {tower_type} c айди {self.tower_id}, создана на координатах {pos}")

    def get_pos(self):
        return self.x, self.y

    def upgrade(self, pos):
        self.kd -= 10 #ТУТ нз САМ СМОТРИ ПО БАЛАНСУ

    def shot(self):
        pygame.time.set_timer(self.tower_id, self.kd)
        #тут логика не прописана!

    def destroy(self):
        logging.info(f"[log]: Башня типа: {self.tower_type} c айди {self.tower_id} уничтожена на "
                     f"координатах {self.x, self.y}")
        tower_group.remove(self)
        all_sprites.remove(self)
        self.kill()

    @classmethod
    def set_tower_id(cls):
        tower_id = cls.tower_id
        cls.tower_id += 51
        return tower_id