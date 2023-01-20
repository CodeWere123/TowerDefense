import pygame

# Это для того чтобы классы не импортировали из мэина, который импортирует из этих классов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
tower_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
ui_button_group = pygame.sprite.Group()
ui_group = pygame.sprite.Group()
