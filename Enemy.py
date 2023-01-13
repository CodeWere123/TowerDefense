import math
import pygame
from load_image import load_image

# Картинки врагов, пока что просто квадраты разных цветов
enemy_images = {
    'enemy1': load_image("enemy1.png", ["PNG", "enemy"]),
    'enemy2': load_image("enemy2.png", ["PNG", "enemy"])

}


class Enemy(pygame.sprite.Sprite):
    # здоровье, скорость, урон (когда проходят до конца), тип врага (земля, воздух), путь (от начальной координаты, до конечной, все по центрам тайлов),
    # референс к картинке, путь, начальные коорды, сложность в виде целого числа от 1 до 3
    def __init__(self, health, speed, damage, etype, im, path, start, difficulty):
        super().__init__()
        self.health = round(health * (1 + (difficulty - 1) * 0.5))
        self.speed = round(speed * (1 + (difficulty - 1) * 0.1))
        self.damage = math.floor(damage * (1 + (difficulty - 1) * 0.5))
        self.etype = etype
        self.path = path
        self.x = start[0]
        self.y = start[1]
        # К какому тайлу происходит передвижение
        self.current_path_part = 0
        self.image = enemy_images[im]

    def update(self):
        # куда перемещаемся
        part_x, part_y = path_part = self.path[self.current_path_part]
        # кортеж разниц потому что мне лень писать ифы
        difference = (part_x - self.x, part_y - self.y)
        # отнимается потому что коорды идут сверху слева, а бул для того чтобы от разницы осталось только направление
        self.x -= int(bool(difference[0])) * self.speed
        self.y -= int(bool(difference[1])) * self.speed
        # если зашел за центр тайла к которому идешь, то поставить позицию на центр тайла и сменить фокус на следующий тайл
        if (part_x - self.x, part_y - self.y) != difference:
            self.x, self.y = part_x, part_y
            self.current_path_part += 1

    # тут я думаю все понятно
    def get_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            del self
