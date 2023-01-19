from SpriteGroups import enemy_group
import random

def get_target(tower_pos):
    if len(enemy_group) != 0:
        x, y = tower_pos
        best = ""
        min_alfa = 1000
        for enemy in enemy_group:
            alfa = abs(enemy.x - x) + abs(enemy.y - y)
            if alfa < min_alfa:
                min_alfa = alfa
                best = enemy
        return best
    return False

def get_random():
    if len(enemy_group) != 0:
        return random.choice(enemy_group)
    return False
    #тут ты хотел переделать с големы
