import pygame
import pygame_menu
import os
import sys
from load_image import load_image
from SpriteGroups import tower_group, enemy_group, tiles_group, ui_group, projectile_group
from Game import Game
from Towers import towers
from UserEvents import NEW_WAVE_EVENT_ID, ENEMY_SPAWN_INTERVAL_EVENT_ID, ONE_SECOND_EVENT_ID, TOWER_SHOOT_BASE_EVENT_ID


def start_game_screen(response):
    game = Game(response["map"], response["difficulty"])
    game_screen = pygame.display.set_mode((600, 500))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.image.save(game_screen, os.path.join("data", "tmp", "pause.png"))
                    pause_menu(game_screen, game)
            if event.type == pygame.MOUSEBUTTONDOWN:
                response = game.register_click(event.pos)
                if response == "pause":
                    pygame.image.save(game_screen, os.path.join("data", "tmp", "pause.png"))
                    pause_menu(game_screen, game)
            if event.type == NEW_WAVE_EVENT_ID:
                game.new_wave()
            if event.type == ENEMY_SPAWN_INTERVAL_EVENT_ID:
                game.next_enemy()
            if event.type == ONE_SECOND_EVENT_ID:
                game.next_wave_time()
                print(game.wave_time)
            for tower_id in towers:
                if event.type == TOWER_SHOOT_BASE_EVENT_ID + tower_id:
                    towers[tower_id].shoot()
        projectile_group.update()
        tiles_group.draw(game_screen)
        enemy_group.draw(game_screen)
        tower_group.draw(game_screen)
        projectile_group.draw(game_screen)
        ui_group.draw(game_screen)
        game_screen.blit(game.all_gold_text, (540, 395))
        game_screen.blit(game.heart_text, (535, 435))
        if game.do_render_tower_gold:
            game_screen.blit(game.archer_gold, (540, 130))
            game_screen.blit(game.stone_gold, (540, 190))
            game_screen.blit(game.wizard_gold, (540, 250))
            game_screen.blit(game.mine_gold, (540, 310))
        if game.do_render_upgrade_gold:
            game_screen.blit(game.upgrade_gold, (540, 130))
        pygame.display.flip()
        if clock.tick(FPS):
            enemy_group.update()


def main_menu(best_score, surface):
    main_menu_screen = pygame.display.set_mode((800, 800))
    response = {"map": "td_jungle.txt", "difficulty": 1}
    image = load_image("bg_main.jpg", ["PNG"])

    def set_difficulty(value, difficulty):
        response["difficulty"] = difficulty

    def set_map(value, map):
        response["map"] = map

    def start_the_game():
        start_game_screen(response)



    menu = pygame_menu.Menu('Tower Defence', 800, 800,
                            theme=pygame_menu.themes.THEME_GREEN)

    menu.add.button('Играть', start_the_game)
    menu.add.label(f"Вас лучший счет: {best_score}")
    menu.add.selector('Сложность :', [('Easy', 1), ('Middle', 2), ('Hard', 3)],
                      onchange=set_difficulty)
    menu.add.selector('Карта :', [('Карта 1', "td_jungle.txt"), ('Карта 2', "td_jungle2.txt"),
                                  ('Карта 3', "td_jungle3.txt")],
                      onchange=set_map)
    menu.add.button('Выйти', pygame_menu.events.EXIT)

    menu.mainloop(surface)


def lose_menu(score, best_score, surface):
    response = {"map": 1, "difficulty": 1}
    image = load_image("bg_main.jpg", ["PNG"])

    def to_menu():
        main_menu(best_score, surface)

    menu = pygame_menu.Menu('Вы проиграли', 800, 800,
                            theme=pygame_menu.themes.THEME_ORANGE)
    if best_score > score:
        menu.add.label(f"Ваш текущий счет: {score}")
        menu.add.label(f"Вам не хватило до рекорда: {best_score - score}")
    else:
        menu.add.label(f"Вы поставили новый рекорд: {score}")
        menu.add.label(f"Старый рекорд был обогнан на : {score - best_score}")
    menu.add.button('В главное меню', to_menu)
    menu.add.button('Выйти', pygame_menu.events.EXIT)

    menu.mainloop(surface)


def pause_menu(screen, game):
    img = pygame.image.load(os.path.join("data", "tmp", "pause.png")).convert()
    img.set_alpha(50)
    pygame.image.save(img, os.path.join("data", "tmp", "pause.png"))
    myimage = pygame_menu.baseimage.BaseImage(
        image_path=os.path.join("data", "tmp", "pause.png"),
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY)
    mytheme = pygame_menu.themes.THEME_DARK.copy()
    mytheme.background_color = myimage

    def exit_to_main_menu():
        main_menu(1, main_menu_screen)

    def restart_game():
        game.restart()
        menu.close()

    menu = pygame_menu.Menu(width=600, height=500,
                            theme=mytheme, title="Paused", onclose=pygame_menu.events.CLOSE)
    menu.add.button("Продолжить", pygame_menu.events.CLOSE)
    menu.add.button("Начать заново", restart_game)
    menu.add.button("Выйти", exit_to_main_menu)
    menu.mainloop(screen)


TILE_SIZE = 50
FPS = 60

pygame.init()
clock = pygame.time.Clock()
main_menu_screen = pygame.display.set_mode((800, 800))
main_menu(1, main_menu_screen)