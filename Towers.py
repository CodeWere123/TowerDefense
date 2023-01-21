import pygame
from load_image import load_image
from SpriteGroups import tower_group, all_sprites
import math
from Projectile import Stone, Arrow
from SpriteGroups import enemy_group
from UserEvents import TOWER_SHOOT_BASE_EVENT_ID
import random

towers = dict()


class Tower(pygame.sprite.Sprite):
    tower_id = 0

    def __init__(self, pos, cooldown, game, filename, price):
        """
        :param pos: позиция
        :param cooldown: перезарядка
        """
        super().__init__(tower_group, all_sprites)
        self.x, self.y = pos
        self.tower_id = self.set_tower_id()
        self.cooldown = cooldown
        self.image = load_image(filename, ["PNG", "towers"])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.game = game
        self.price = price
        self.upgrade_price = self.price // 2
        pygame.time.set_timer(TOWER_SHOOT_BASE_EVENT_ID + self.tower_id, self.cooldown)
        towers[self.tower_id] = self

    def get_price(self):
        return self.price

    def get_upgrade_price(self):
        return self.upgrade_price

    def get_pos(self):
        return self.x, self.y

    def upgrade(self):
        pass

    def destroy(self):
        tower_group.remove(self)
        all_sprites.remove(self)
        pygame.time.set_timer(TOWER_SHOOT_BASE_EVENT_ID + self.tower_id, 0)
        try:
            towers.pop(self.tower_id)
        except KeyError:
            pass
        self.kill()

    def get_target(self):
        pass

    @classmethod
    def set_tower_id(cls):
        tower_id = cls.tower_id
        cls.tower_id += 1
        return tower_id


class StoneTower(Tower):
    def __init__(self, pos, cooldown, game, price):
        """
        :param pos: позиция
        :param cooldown: перезарядка
        """
        super().__init__(pos, cooldown, game, "stone_tower.png", price)
        self.damage = 15
        self.radius = 100

    def upgrade(self):
        self.damage += 5
        self.upgrade_price += 50

    def shoot(self):
        enemy = None
        max_path_part = 1
        for i in enemy_group:
            e_x, e_y = i.get_pos()
            t_x, t_y = self.x, self.y
            if math.sqrt(abs(t_x - e_x) ** 2 + abs(t_y - e_y) ** 2) <= self.radius:
                if i.current_path_part > max_path_part and i.enemy_type == "land":
                    max_path_part = i.current_path_part
                    enemy = i
        if enemy is not None:
            Stone((self.x, self.y), (enemy.x, enemy.y), self.damage)


class WizardTower(Tower):
    def __init__(self, pos, cooldown, game, price):
        """
        :param pos: позиция
        :param cooldown: перезарядка
        """
        super().__init__(pos, cooldown, game, "wizard_tower.png", price)
        self.upgrade_count = 0

    def upgrade(self):
        if self.upgrade_count < 9:
            self.cooldown -= 2000
            pygame.time.set_timer(TOWER_SHOOT_BASE_EVENT_ID + self.tower_id, self.cooldown)
            self.upgrade_count += 1
            self.upgrade_price += 75
        else:
            self.game.add_gold(self.upgrade_price)

    def get_upgrade_price(self):
        if self.upgrade_count < 9:
            return self.upgrade_price
        else:
            return "NaN"

    def shoot(self):
        if enemy_group:
            target = random.choices([x for x in enemy_group],
                                    weights=[0.9 if x.enemy_name == "golem" else 0.1 for x in
                                             enemy_group])[0]
            target.destroy()


class GoldMine(Tower):
    def __init__(self, pos, cooldown, game, price):
        """
        :param pos: позиция
        :param cooldown: перезарядка
        """
        super().__init__(pos, cooldown, game, "gold_mine.png", price)
        self.gold_rate = 5

    def upgrade(self):
        self.gold_rate += 2
        self.upgrade_price += 25

    def shoot(self):
        self.game.add_gold(self.gold_rate)


class ArcherTower(Tower):
    def __init__(self, pos, cooldown, game, price):
        """
        :param pos: позиция
        :param cooldown: перезарядка
        """
        super().__init__(pos, cooldown, game, "archer_tower.png", price)
        self.radius = 150
        self.damage = 10

    def upgrade(self):
        self.damage += 2
        self.upgrade_price += 25

    def shoot(self):
        enemy = None
        max_path_part = 1
        for i in enemy_group:
            e_x, e_y = i.get_pos()
            t_x, t_y = self.rect.x, self.rect.y
            if math.sqrt(abs(t_x - e_x) ** 2 + abs(t_y - e_y) ** 2) <= self.radius:
                if i.current_path_part > max_path_part:
                    max_path_part = i.current_path_part
                    enemy = i
        if enemy is not None:
            Arrow((self.x, self.y), enemy, self.damage)
