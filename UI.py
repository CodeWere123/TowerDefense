import pygame
from SpriteGroups import ui_group, ui_button_group, all_sprites
from load_image import load_image

button_images = {
    "upgrade": load_image("upgrade.png", ["PNG", "UIButtons"]),
    "destroy": load_image("destroy.png", ["PNG", "UIButtons"]),
    "stone_tower": load_image("stone_tower.png", ["PNG", "UIButtons"]),
    "archer_tower": load_image("archer_tower.png", ["PNG", "UIButtons"]),
    "wizard_tower": load_image("wizard_tower.png", ["PNG", "UIButtons"]),
    "gold_mine": load_image("gold_mine.png", ["PNG", "UIButtons"])
}


class UIButton(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__(ui_group, ui_button_group, all_sprites)
        self.button_type = image
        self.image = button_images[image]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def destroy(self):
        ui_button_group.remove(self)
        ui_group.remove(self)
        all_sprites.remove(self)
        self.kill()


class UIElement(pygame.sprite.Sprite):
    def __init__(self, ui_image, pos):
        super().__init__(ui_group, all_sprites)
        self.image = load_image(ui_image, ["PNG", "UI"])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def destroy(self):
        ui_group.remove(self)
        all_sprites.remove(self)
        self.kill()
