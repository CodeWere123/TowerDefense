import pygame
from load_image import load_image
from SpriteGroups import projectile_group, all_sprites
import sys


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, damage, speed):
        """
        :param pos: позиция
        :param id: айди, уникален для каждого места башни, нужен для снарядов
        :param ttype: тип башни для модели
        :param health: хп
        :param damage: урон, для снарядов
        """
        super().__init__(projectile_group, all_sprites)
        self.ANIMATION = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]

        self.image = load_image("1.png", ["PNG", "stone1"])
        self.rect = self.image.get_rect()
        self.x, self.y = self.rect.x, self.rect.y = pos
        self.delay = 400
        self.tick = 0 # тики, я хз как это сделать подругому, оно работает
        self.speed = speed
        self.damage = damage
        self.i_index = 0
        self.target_x, self.target_y = target_pos

    def move(self):
        if abs(self.target_x - self.rect.x) + abs(self.target_y - self.rect.y) < 5:
            self.tick += 1
            if self.i_index == 0:
                self.i_index += 1
        if self.i_index == 0:
            if self.rect.x < self.target_x:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
            if self.rect.y < self.target_y:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
        else:
            if self.tick > self.delay:
                self.tick = 0
                self.i_index += 1
                if self.i_index < 5:
                    self.image = load_image(f"{self.ANIMATION[self.i_index]}", ["PNG", "stone1"])
                else:
                    projectile_group.remove(self)
                    self.kill()

            else:
                self.tick += 1


# if __name__ == '__main__':
#    pygame.init()
#    size = width, height = 1000, 500
#    screen = pygame.display.set_mode(size)
#
#    running = True
#    test = Projectail((100, 100), (400, 300), 1, 1)
#    while running:
#        screen.fill("black")
#        for stone in projectile_group:
#            stone.move()
#        all_sprites.draw(screen)
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                running = False
#        pygame.display.flip()
#    pygame.quit()


