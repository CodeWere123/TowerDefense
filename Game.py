import pygame
import math
import random
from Map import Map
from Enemy import Enemy
from UserEvents import NEW_WAVE_EVENT_ID, ENEMY_SPAWN_INTERVAL_EVENT_ID, ONE_SECOND_EVENT_ID

ENEMIES_DATA = [
    [20, 1, 1, "land", "goblin", 1],
    [50, 2, 2, "air", "minion", 3]
]


class Game:
    def __init__(self, map_file, difficulty):
        self.health = 20
        self.coins = 300
        self.game_map = Map(map_file)
        self.difficulty = difficulty
        self.wave = 1
        self.current_enemies = []
        self.wave_time = 5
        pygame.time.set_timer(ONE_SECOND_EVENT_ID, 1000)
        pygame.time.set_timer(NEW_WAVE_EVENT_ID, 5000)
        pygame.time.set_timer(ENEMY_SPAWN_INTERVAL_EVENT_ID, 0)

    def new_wave(self):
        number_of_enemies = self.wave * (math.floor(math.log10(self.wave)) + 1) +\
                            2 * (math.floor(math.log2(self.wave)) + 1)
        enemies = []
        while number_of_enemies > 0:
            weights = [x[-1] for x in ENEMIES_DATA if x[-1] <= number_of_enemies]
            weights = [x / sum(weights) for x in weights]
            enemy_data = random.choices([x for x in ENEMIES_DATA if x[-1] <= number_of_enemies],
                                        weights=weights)[0]
            enemies.append(enemy_data[:-1])
            number_of_enemies -= enemy_data[-1]
        self.current_enemies = enemies
        pygame.time.set_timer(ENEMY_SPAWN_INTERVAL_EVENT_ID, 300)
        self.wave += 1

    def next_enemy(self):
        enemy_data = self.current_enemies.pop()
        Enemy(*enemy_data, self.game_map.paths_to_screen_coordinates(
            self.game_map.paths), self.difficulty, self)
        if len(self.current_enemies) == 0:
            pygame.time.set_timer(ENEMY_SPAWN_INTERVAL_EVENT_ID, 0)

    def next_wave_time(self):
        self.wave_time -= 1
        if self.wave_time == 0:
            self.wave_time = 5

    def get_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.game_over()

    def game_over(self):
        pass
