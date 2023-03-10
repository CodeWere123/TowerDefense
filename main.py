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
    game_map = response
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
            for tower_id in towers:
                if event.type == TOWER_SHOOT_BASE_EVENT_ID + tower_id:
                    towers[tower_id].shoot()
        tiles_group.draw(game_screen)
        enemy_group.draw(game_screen)
        tower_group.draw(game_screen)
        projectile_group.draw(game_screen)
        ui_group.draw(game_screen)
        game_screen.blit(game.all_gold_text, (540, 395))
        game_screen.blit(game.heart_text, (535, 435))
        game_screen.blit(game.score_text, (0, 0))
        game_screen.blit(game.wave_time_text, (0, 470))
        if game.do_render_tower_gold:
            game_screen.blit(game.archer_gold, (540, 130))
            game_screen.blit(game.stone_gold, (540, 190))
            game_screen.blit(game.wizard_gold, (540, 250))
            game_screen.blit(game.mine_gold, (540, 310))
        if game.do_render_upgrade_gold:
            game_screen.blit(game.upgrade_gold, (540, 130))
        if game.game_is_over:
            with open(os.path.join("data", "save", "highscores.txt"), "r+") as f:
                lines = list(f.readlines())
                if game_map["map"] == "td_jungle.txt":
                    lines[0] = str(game.score) + "\n"
                if game_map["map"] == "td_jungle2.txt":
                    lines[1] = str(game.score) + "\n"
                if game_map["map"] == "td_jungle3.txt":
                    lines[2] = str(game.score) + "\n"
                f.truncate(0)
                f.seek(0)
                f.writelines(lines)
            lose_menu(game.score, 1, main_menu_screen)
        pygame.display.flip()
        if clock.tick(FPS):
            enemy_group.update()
            projectile_group.update()


def main_menu(surface):
    f = open(os.path.join("data", "save", "highscores.txt"))
    highscores = list(map(str.strip, f.readlines()))
    highscores = {"td_jungle.txt": highscores[0], "td_jungle2.txt": highscores[1],
                  "td_jungle3.txt": highscores[2]}
    f.close()
    main_menu_screen = pygame.display.set_mode((800, 800))
    response = {"map": "td_jungle.txt", "difficulty": 1}
    image = load_image("bg_main.jpg", ["PNG"])

    def set_difficulty(value, difficulty):
        response["difficulty"] = difficulty

    def set_map(value, map):
        response["map"] = map
        label.set_title(f"?????? ???????????? ????????: {highscores[response['map']]}")

    def start_the_game():
        start_game_screen(response)



    menu = pygame_menu.Menu('Tower Defence', 800, 800,
                            theme=pygame_menu.themes.THEME_GREEN)

    menu.add.button('????????????', start_the_game)
    label = menu.add.label(f"?????? ???????????? ????????: {highscores[response['map']]}")
    menu.add.selector('?????????????????? :', [('Easy', 1), ('Middle', 2), ('Hard', 3)],
                      onchange=set_difficulty)
    menu.add.selector('?????????? :', [('?????????? 1', "td_jungle.txt"), ('?????????? 2', "td_jungle2.txt"),
                                  ('?????????? 3', "td_jungle3.txt")],
                      onchange=set_map)
    menu.add.button('??????????', pygame_menu.events.EXIT)

    menu.mainloop(surface)


def lose_menu(score, best_score, surface):
    surface = pygame.display.set_mode((800, 800))
    response = {"map": 1, "difficulty": 1}
    image = load_image("bg_main.jpg", ["PNG"])

    def to_menu():
        main_menu(surface)

    menu = pygame_menu.Menu('???? ??????????????????', 800, 800,
                            theme=pygame_menu.themes.THEME_ORANGE)
    if best_score > score:
        menu.add.label(f"?????? ?????????????? ????????: {score}")
        menu.add.label(f"?????? ???? ?????????????? ???? ??????????????: {best_score - score}")
    else:
        menu.add.label(f"???? ?????????????????? ?????????? ????????????: {score}")
        menu.add.label(f"???????????? ???????????? ?????? ?????????????? ???? : {score - best_score}")
    menu.add.button('?? ?????????????? ????????', to_menu)
    menu.add.button('??????????', pygame_menu.events.EXIT)

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
        game.destroy()
        main_menu(main_menu_screen)

    def restart_game():
        game.restart()
        menu.close()

    menu = pygame_menu.Menu(width=600, height=500,
                            theme=mytheme, title="Paused", onclose=pygame_menu.events.CLOSE)
    menu.add.button("????????????????????", pygame_menu.events.CLOSE)
    menu.add.button("???????????? ????????????", restart_game)
    menu.add.button("??????????", exit_to_main_menu)
    menu.mainloop(screen)


TILE_SIZE = 50
FPS = 60

pygame.init()
clock = pygame.time.Clock()
main_menu_screen = pygame.display.set_mode((800, 800))
main_menu(main_menu_screen)