import pygame
import math
import random
from Map import Map
from Enemy import Enemy
from UserEvents import NEW_WAVE_EVENT_ID, ENEMY_SPAWN_INTERVAL_EVENT_ID, ONE_SECOND_EVENT_ID
from SpriteGroups import ui_button_group, all_sprites, enemy_group, tower_group, projectile_group
from Towers import Tower, StoneTower, ArcherTower, WizardTower, GoldMine
from UI import UIElement, UIButton

ENEMIES_DATA = [
    [20, 0.5, 1, "land", "goblin", 1],
    [50, 1, 2, "air", "minion", 10],
    [200, 0.25, 4, "land", "golem", 30]
]

ARCHER_PRICE = 150
STONE_PRICE = 300
WIZARD_PRICE = 200
MINE_PRICE = 100


class Game:
    def __init__(self, map_file, difficulty):
        self.health = 20
        self.game_map = Map(map_file)
        self.difficulty = difficulty
        self.wave = 1
        self.gold = 300000
        self.current_enemies = []
        self.wave_time = 30
        self.tile_state = 0
        self.last_tile = []
        self.board = self.game_map.generate_board()
        self.do_render_tower_gold = False
        self.do_render_upgrade_gold = False
        self.setup_ui()
        pygame.time.set_timer(ONE_SECOND_EVENT_ID, 1000)
        pygame.time.set_timer(NEW_WAVE_EVENT_ID, 30000)
        pygame.time.set_timer(ENEMY_SPAWN_INTERVAL_EVENT_ID, 0)

    def setup_ui(self):
        self.ui_side_menu = UIElement("sidemenu.png", (500, 0))
        self.ui_pause_button = UIElement("pause.png", (525, 20))
        self.ui_heart = UIElement("heart.png", (525, 430))
        self.ui_coin = UIElement("coin.png", (510, 390))
        self.font = pygame.font.Font(None, 20)
        self.all_gold_text = self.font.render(self.readable_number(self.gold), True, (0, 0, 0))
        self.archer_gold = self.font.render(str(ARCHER_PRICE), True, (0, 0, 0))
        self.stone_gold = self.font.render(str(STONE_PRICE), True, (0, 0, 0))
        self.wizard_gold = self.font.render(str(WIZARD_PRICE), True, (0, 0, 0))
        self.mine_gold = self.font.render(str(MINE_PRICE), True, (0, 0, 0))
        self.upgrade_gold = None
        self.heart_font = pygame.font.Font(None, 36)
        self.heart_text = self.heart_font.render(str(self.health), True, (255, 255, 255))

    def new_wave(self):
        number_of_enemies = self.wave * (math.floor(math.log10(self.wave)) + 1) +\
                            2 * (math.floor(math.log2(self.wave)) + 1)
        enemies = []
        while number_of_enemies > 0:
            weights = [x[-1] for x in ENEMIES_DATA if x[-1] <= number_of_enemies]
            weights = [x / sum(weights) for x in weights]
            enemy_data = random.choices([x for x in ENEMIES_DATA if x[-1] <= number_of_enemies],
                                        weights=weights)[0]
            enemies.append(enemy_data)
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
            self.wave_time = 30

    def get_damage(self, damage):
        self.health -= damage
        self.heart_text = self.heart_font.render(str(self.health), True, (255, 255, 255))
        if self.health < 0:
            self.game_over()

    def add_gold(self, gold):
        self.gold += gold
        self.all_gold_text = self.font.render(self.readable_number(self.gold), True, (0, 0, 0))

    def game_over(self):
        pass

    def register_click(self, mouse_pos):
        tile = self.get_cell(mouse_pos)
        return self.on_click(tile, mouse_pos)

    def on_click(self, tile, mouse_pos):
        if self.ui_pause_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            return "pause"
        if self.tile_state == 0:
            try:
                tile_contents = self.board[tile[1]][tile[0]]
            except TypeError:
                tile_contents = "+"
            if tile_contents == "-":
                UIButton("archer_tower", (525, 80))
                UIButton("stone_tower", (525, 140))
                UIButton("wizard_tower", (525, 200))
                UIButton("gold_mine", (525, 260))
                self.tile_state = 1
                self.do_render_tower_gold = True
                self.last_tile = tile
            elif isinstance(tile_contents, Tower):
                UIButton("upgrade", (525, 80))
                UIButton("destroy", (525, 140))
                self.tile_state = 1
                self.upgrade_gold = self.font.render(self.readable_number(
                    tile_contents.get_upgrade_price()), True, (0, 0, 0))
                self.do_render_upgrade_gold = True
                self.last_tile = tile
        else:
            button = None
            for sprite in ui_button_group:
                if sprite.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    button = sprite
            if button is not None:
                button_type = button.button_type
                coords = self.game_map.tile_to_screen(*self.last_tile, self.game_map.tile_size,
                                                      False)
                if button_type == "archer_tower" and self.gold >= 150:
                    self.board[self.last_tile[1]][self.last_tile[0]] = ArcherTower(
                        coords, 1000, self, ARCHER_PRICE)
                    self.add_gold(-ARCHER_PRICE)
                elif button_type == "stone_tower" and self.gold >= 300:
                    self.board[self.last_tile[1]][self.last_tile[0]] = StoneTower(
                        coords, 2000, self, STONE_PRICE)
                    self.add_gold(-STONE_PRICE)
                elif button_type == "wizard_tower" and self.gold >= 200:
                    self.board[self.last_tile[1]][self.last_tile[0]] = WizardTower(
                        coords, 30000, self, WIZARD_PRICE)
                    self.add_gold(-WIZARD_PRICE)
                elif button_type == "gold_mine" and self.gold >= 100:
                    self.board[self.last_tile[1]][self.last_tile[0]] = GoldMine(
                        coords, 3000, self, MINE_PRICE)
                    self.add_gold(-MINE_PRICE)
                elif button_type == "upgrade":
                    if self.board[self.last_tile[1]][self.last_tile[0]].get_upgrade_price() == \
                            "NaN":
                        pass
                    elif self.gold >= \
                            self.board[self.last_tile[1]][self.last_tile[0]].get_upgrade_price():
                        self.add_gold(-self.board[self.last_tile[1]][
                            self.last_tile[0]].get_upgrade_price())
                        self.board[self.last_tile[1]][self.last_tile[0]].upgrade()
                elif button_type == "destroy":
                    self.board[self.last_tile[1]][self.last_tile[0]].destroy()
                    self.board[self.last_tile[1]][self.last_tile[0]] = "-"
                self.last_tile = []
            for i in ui_button_group:
                i.destroy()
            self.do_render_tower_gold = False
            self.do_render_upgrade_gold = False
            self.tile_state = 0
        return False

    def get_cell(self, mouse_pos):
        column = mouse_pos[0] // self.game_map.tile_size
        row = mouse_pos[1] // self.game_map.tile_size
        if not (0 <= column < self.game_map.width and 0 <= row < self.game_map.height):
            return None
        return column, row

    @staticmethod
    def find_sprite(sprites, x, y):
        for sprite in sprites:
            rect = sprite.rect
            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                return sprite
        return None

    @staticmethod
    def readable_number(num):
        if type(num) is str:
            return num
        if num >= 1000000:
            return '{:.1f}M'.format(num / 1000000)
        elif num >= 1000:
            return '{:.1f}K'.format(num / 1000)
        else:
            return str(num)

    def restart(self):
        for i in enemy_group:
            enemy_group.remove(i)
            all_sprites.remove(i)
            i.kill()
        for i in tower_group:
            tower_group.remove(i)
            all_sprites.remove(i)
            i.kill()
        for i in projectile_group:
            projectile_group.remove(i)
            all_sprites.remove(i)
            i.kill()
        self.health = 20
        self.wave = 1
        self.gold = 300
        self.board = self.game_map.generate_board()
        self.current_enemies = []
        self.wave_time = 30
        self.tile_state = 0
        self.last_tile = []
        self.do_render_tower_gold = False
        self.do_render_upgrade_gold = False
        pygame.time.set_timer(ONE_SECOND_EVENT_ID, 1000)
        pygame.time.set_timer(NEW_WAVE_EVENT_ID, 30000)
        pygame.time.set_timer(ENEMY_SPAWN_INTERVAL_EVENT_ID, 0)