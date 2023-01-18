import pygame
import math
import random
from Map import Map
from Enemy import Enemy
from UserEvents import NEW_WAVE_EVENT_ID, ENEMY_SPAWN_INTERVAL_EVENT_ID

ENEMIES_DATA = [
    [20, 1, 1, "land", "enemy1.png", 1],
    [50, 2, 1, "air", "enemy2.png", 3]
]


class Game:
    def __init__(self, map_file, difficulty):
        self.health = 20
        self.coins = 300
        self.game_map = Map(map_file)
        self.difficulty = difficulty
        self.wave = 1
        pygame.time.set_timer(NEW_WAVE_EVENT_ID, 30000)

    def new_wave(self):
        number_of_enemies = self.wave * (math.floor(math.log10(self.wave)) + 1) +\
                            2 * (math.floor(math.log2(self.wave)) + 1)
        enemies = []
        while number_of_enemies > 0:
            weights = [x[-1] for x in ENEMIES_DATA]
            weights = [x / sum(weights) for x in weights]
            enemy_data = random.choices(ENEMIES_DATA, weights=weights)[0][:-1]
            enemies.append(Enemy(*enemy_data, self.game_map.paths_to_screen_coordinates(
                self.game_map.paths), self.difficulty, self))
        pygame.time.set_timer(ENEMY_SPAWN_INTERVAL_EVENT_ID, 300)

    def get_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.game_over()

    def game_over(self):
        pass
