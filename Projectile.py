import pygame
from load_image import load_image
from SpriteGroups import projectile_group, all_sprites, enemy_group
import math


class Stone(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, damage):
        super().__init__(projectile_group, all_sprites)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.speed = 2
        self.damage = damage
        self.radius = 15
        self.animation_frames = []
        for i in range(1, 6):
            frame = load_image(f"{i}.png", ["PNG", "projectiles", "stone"])
            self.animation_frames.append(frame)
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.x, self.y = self.rect.x, self.rect.y = start_pos
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.2

    def update(self):
        x_diff = self.end_pos[0] - self.rect.x
        y_diff = self.end_pos[1] - self.rect.y
        distance = ((x_diff ** 2) + (y_diff ** 2)) ** 0.5
        if distance != 0:
            x_vel = x_diff / distance * self.speed
            y_vel = y_diff / distance * self.speed
            self.x += x_vel
            self.y += y_vel
            self.rect.x, self.rect.y = self.x, self.y
        if distance < self.speed:
            for i in enemy_group:
                e_x, e_y = i.get_pos()
                t_x, t_y = self.x, self.y
                if math.sqrt(abs(t_x - e_x) ** 2 + abs(t_y - e_y) ** 2) <= self.radius:
                    i.get_damage(self.damage)
            self.animation_timer += 1 / 60
            if self.animation_timer > self.animation_speed:
                self.animation_timer = 0
                self.animation_index += 1
                if self.animation_index >= len(self.animation_frames):
                    self.destroy()
                else:
                    self.image = self.animation_frames[self.animation_index]

    def destroy(self):
        projectile_group.remove(self)
        all_sprites.remove(self)
        self.kill()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, start_pos, enemy, damage, speed=3):
        super().__init__(projectile_group, all_sprites)
        self.start_pos = start_pos
        self.damage = damage
        self.speed = speed
        self.enemy = enemy
        self.image = load_image("arrow.png", ["PNG", "projectiles"])
        self.rect = self.image.get_rect()
        x_diff = self.enemy.rect.x - start_pos[0]
        y_diff = self.enemy.rect.y - start_pos[1]
        angle = -math.degrees(math.atan2(y_diff, x_diff))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.x, self.y = self.rect.x, self.rect.y = start_pos

    def update(self):
        x_diff = self.enemy.rect.x - self.rect.x
        y_diff = self.enemy.rect.y - self.rect.y
        distance = ((x_diff ** 2) + (y_diff ** 2)) ** 0.5
        if distance != 0:
            x_vel = x_diff / distance * self.speed
            y_vel = y_diff / distance * self.speed
            self.x += x_vel
            self.y += y_vel
            self.rect.x, self.rect.y = self.x, self.y
        if distance < self.speed:
            try:
                self.enemy.get_damage(self.damage)
            except NameError:
                pass
            self.destroy()

    def destroy(self):
        projectile_group.remove(self)
        all_sprites.remove(self)
        self.kill()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1000, 500
    screen = pygame.display.set_mode(size)

    running = True
    test = Stone((100, 100), (400, 300), 15)
    while running:
        screen.fill("black")
        for stone in projectile_group:
            stone.update()
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()


