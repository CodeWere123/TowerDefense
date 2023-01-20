import math
import pygame
import random
from load_image import load_image
from SpriteGroups import enemy_group, all_sprites

# Картинки врагов, пока что просто квадраты разных цветов
enemy_images = {
    'minion': load_image("minion.png", ["PNG", "enemy"]),
    'goblin': load_image("goblin.png", ["PNG", "enemy"]),
    'golem': load_image("golem.png", ["PNG", "enemy"])
}


class Enemy(pygame.sprite.Sprite):
    # здоровье, скорость, урон (когда проходят до конца), тип врага (земля, воздух), путь (от начальной координаты, до конечной, все по центрам тайлов),
    # референс к картинке, путь, начальные коорды, сложность в виде целого числа от 1 до 3
    def __init__(self, health, speed, damage, enemy_type, image, weight, paths, difficulty, game):
        super().__init__(enemy_group, all_sprites)
        self.health = round(health * (1 + (difficulty - 1) * 0.5))
        self.speed = speed * (1 + (difficulty - 1) * 0.1)
        self.damage = math.floor(damage * (1 + (difficulty - 1) * 0.5))
        self.enemy_type = enemy_type
        self.weight = weight
        self.path = random.choice(paths)
        self.image = enemy_images[image]
        self.enemy_name = image
        self.rect = self.image.get_rect()
        self.x, self.y = self.rect.x, self.rect.y = self.path[0]
        # К какому тайлу происходит передвижение
        self.current_path_part = 1
        self.game = game

    def update(self):
        # куда перемещаемся
        part_x, part_y = path_part = self.path[self.current_path_part]
        # кортеж разниц потому что мне лень писать ифы
        difference = (self.number_to_sign(part_x - self.x), self.number_to_sign(part_y - self.y))
        # отнимается потому что коорды идут сверху слева, а бул для того чтобы от разницы осталось только направление
        if difference[0] != 0:
            self.x += difference[0] * self.speed
        if difference[1] != 0:
            self.y += difference[1] * self.speed
        # если зашел за центр тайла к которому идешь, то поставить позицию на центр тайла и сменить фокус на следующий тайл
        if (self.number_to_sign(part_x - self.x), self.number_to_sign(part_y - self.y)) != difference:
            self.x, self.y = part_x, part_y
            self.current_path_part += 1
            if self.current_path_part == len(self.path) - 1:
                print("a")
                self.game.get_damage(self.damage)
                self.destroy()
        self.rect.x, self.rect.y = self.x, self.y

    def get_pos(self):
        return self.rect.x, self.rect.y

    @staticmethod
    def number_to_sign(num):
        if num > 0:
            return 1
        elif num == 0:
            return 0
        else:
            return -1

    # тут я думаю все понятно
    def get_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.game.add_gold(self.weight * 3)
            self.destroy()

    def destroy(self):
        enemy_group.remove(self)
        all_sprites.remove(self)
        self.kill()
