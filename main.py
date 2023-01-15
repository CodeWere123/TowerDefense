import pygame
import sys
from Map import Map
from SpriteGroups import tower_group, enemy_group, tiles_group
from Enemy import Enemy


def game_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        tiles_group.draw(screen)
        enemy_group.draw(screen)
        tower_group.draw(screen)
        pygame.display.flip()
        if clock.tick(FPS):
            enemy_group.update()


TILE_SIZE = 50
FPS = 60

pygame.init()
size = WIDTH, HEIGHT = 500, 500
screen_start = pygame.display.set_mode(size)
clock = pygame.time.Clock()
jungle_map = Map("td_jungle.txt")
enemy = Enemy(1, 1, 1, 1, "enemy1", jungle_map.paths_to_screen_coordinates(jungle_map.paths), 1)
screen = pygame.display.set_mode((jungle_map.width * TILE_SIZE, jungle_map.height * TILE_SIZE))
game_screen()