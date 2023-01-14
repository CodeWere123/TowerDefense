import pygame
from load_image import load_image
from SpriteGroups import projectile_group, all_sprites


class Stone(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, damage, speed, projectile_id):
        """
        :param pos: От башни при инициации, текущая изменяемая позиция
        :param target_pos: Куда летит
        :param damage: От башни
        :param speed: Скорость
        :param id: Айдишник от башни, тот же
        """
        super().__init__(projectile_group, all_sprites)
        self.ANIMATION = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
        self.image = load_image("1.png", ["PNG", "stone1"])
        self.rect = self.image.get_rect()
        self.x, self.y = self.rect.x, self.rect.y = pos
        self.delay = 110
        self.projectile_id = projectile_id
        self.i_index = 1
        self.target_x, self.target_y = target_pos  # это константа, куда летит камень определяется заранее!

    def change_pos(self, coords):
        self.x, self.y = coords
        self.rect.x, self.rect.y = int(self.x), int(self.y)

    def destroy(self):
        self.i_index += 1
        if self.i_index < 5:
            pygame.time.set_timer(self.projectile_id, self.delay)
            self.image = load_image(f"{self.ANIMATION[self.i_index]}", ["PNG", "stone1"])
        else:
            projectile_group.remove(self)
            self.kill()