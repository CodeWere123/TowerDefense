from load_image import load_image
import pygame
import pygame_menu


def main_menu(best_score,surface):
    response = {"map": 1, "difficulty": 1}
    #pygame.init()
    #surface = pygame.display.set_mode((800, 800))
    image = load_image("bg_main.jpg", ["PNG"])

    def set_difficulty(value, difficulty):
        response["difficulty"] = difficulty

    def set_map(value, map):
        response["map"] = map

    def start_the_game():
        #тут старт
        print(response)
        return response

    menu = pygame_menu.Menu('Tower defends', 800, 800,
                            theme=pygame_menu.themes.THEME_GREEN)

    menu.add.button('Играть', start_the_game)
    menu.add.label(f"Вас лучший счет: {best_score}")
    menu.add.selector('Сложность :', [('Hard', 1), ('Middle', 2), ('Easy', 3)], onchange=set_difficulty)
    menu.add.selector('Карта :', [('Карта 1', 1), ('Карта 2', 2), ('Карта 3', 3)], onchange=set_map)
    menu.add.button('Выйти', pygame_menu.events.EXIT)

    menu.mainloop(surface)
def lose_menu(score, best_score, surface):
    response = {"map": 1, "difficulty": 1}
    #pygame.init()
    #surface = pygame.display.set_mode((800, 800))
    image = load_image("bg_main.jpg", ["PNG"])

    def to_menu():
        main_menu(best_score)

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
