from load_image import load_image
import os
import pygame
import pygame_menu


def main_menu(best_score, surface):
    response = {"map": 1, "difficulty": 1}
    #pygame.init()
    #surface = pygame.display.set_mode((800, 800))
    image = load_image("bg_main.jpg", ["PNG"])

    def set_difficulty(value, difficulty):
        response["difficulty"] = difficulty

    def set_map(value, map):
        response["map"] = map

    def start_the_game():
        pass
        #тут старт



    menu = pygame_menu.Menu('Tower Defence', 800, 800,
                            theme=pygame_menu.themes.THEME_GREEN)

    menu.add.button('Играть', start_the_game)
    menu.add.label(f"Вас лучший счет: {best_score}")
    menu.add.selector('Сложность :', [('Easy', 1), ('Middle', 2), ('Hard', 3)],
                      onchange=set_difficulty)
    menu.add.selector('Карта :', [('Карта 1', 1), ('Карта 2', 2), ('Карта 3', 3)], onchange=set_map)
    menu.add.button('Выйти', pygame_menu.events.EXIT)

    menu.mainloop(surface)
def lose_menu(score, best_score, surface):
    response = {"map": 1, "difficulty": 1}
    #pygame.init()
    #surface = pygame.display.set_mode((800, 800))
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


def pause_menu(screen):
    img = pygame.image.load(os.path.join("data", "tmp", "pause.png")).convert()
    img.set_alpha(50)
    pygame.image.save(img, os.path.join("data", "tmp", "pause.png"))
    myimage = pygame_menu.baseimage.BaseImage(
        image_path=os.path.join("data", "tmp", "pause.png"),
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY)
    mytheme = pygame_menu.themes.THEME_DARK.copy()
    mytheme.background_color = myimage

    def continue_game():
        return "continue"

    def restart_game():
        return "restart"

    menu = pygame_menu.Menu(width=600, height=500,
                            theme=mytheme, title="Paused", onclose=continue_game)
    menu.add.button("Продолжить", pygame_menu.events.CLOSE)
    menu.add.button("Начать заново", restart_game)
    menu.add.button("Выйти", pygame_menu.events.EXIT)
    menu.mainloop(screen)
