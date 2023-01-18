import math
import pygame
import random
from load_image import load_image
from SpriteGroups import enemy_group, all_sprites

# Картинки врагов, пока что просто квадраты разных цветов
enemy_images = {
    'enemy1': load_image("enemy1.png", ["PNG", "enemy"]),
    'enemy2': load_image("enemy2.png", ["PNG", "enemy"])

}


class Enemy(pygame.sprite.Sprite):
    # здоровье, скорость, урон (когда проходят до конца), тип врага (земля, воздух), путь (от начальной координаты, до конечной, все по центрам тайлов),
    # референс к картинке, путь, начальные коорды, сложность в виде целого числа от 1 до 3
    def __init__(self, health, speed, damage, enemy_type, image, paths, difficulty, game):
        super().__init__(enemy_group, all_sprites)
        self.health = round(health * (1 + (difficulty - 1) * 0.5))
        self.speed = round(speed * (1 + (difficulty - 1) * 0.1))
        self.damage = math.floor(damage * (1 + (difficulty - 1) * 0.5))
        self.enemy_type = enemy_type
        self.path = random.choice(paths)
        print(self.path)
        self.image = enemy_images[image]
        self.rect = self.image.get_rect()
        self.x, self.y = self.rect.x, self.rect.y = self.path[0]
        # К какому тайлу происходит передвижение
        self.current_path_part = 1
        self.game = game

    def update(self):
        # куда перемещаемся
        part_x, part_y = path_part = self.path[self.current_path_part]
        # кортеж разниц потому что мне лень писать ифы
        difference = (part_x - self.x, part_y - self.y)
        bool_difference = (bool(part_x - self.x), bool(part_y - self.y))
        # отнимается потому что коорды идут сверху слева, а бул для того чтобы от разницы осталось только направление
        if difference[0] != 0:
            self.x += int(difference[0] / abs(difference[0])) * self.speed
        if difference[1] != 0:
            self.y += int(difference[1] / abs(difference[1])) * self.speed
        # если зашел за центр тайла к которому идешь, то поставить позицию на центр тайла и сменить фокус на следующий тайл
        if (bool(part_x - self.x), bool(part_y - self.y)) != bool_difference:
            self.x, self.y = part_x, part_y
            self.current_path_part += 1
            if self.current_path_part == len(self.path):
                self.game.get_damage(self.damage)
                self.kill()
        self.rect.x, self.rect.y = self.x, self.y

    # тут я думаю все понятно
    def get_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.kill()
