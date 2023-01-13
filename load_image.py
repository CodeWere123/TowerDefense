import os
import sys
import pygame


def load_image(name, added=None, colorkey=None):
    if added is None:
        added = []
    fullname = os.path.join('data', *added, name)
    if not os.path.isfile(fullname):
        print(f"File '{fullname}' not found")
        sys.exit()
    image = pygame.image.load(fullname)
    return image