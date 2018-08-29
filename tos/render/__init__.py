def get_path(name):
    import os
    directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def load(name):
    import pygame
    return pygame.image.load(get_path('res') + '/' + name).convert_alpha()


def scale2x(img):
    import pygame
    return pygame.transform.scale2x(img)


def get_pos(img, x, y, width, height):
    import pygame
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(img, (0, 0), (x, y, width, height))
    return image


def get_name(img, number):
    return get_pos(img, 64, number * 32, 128, 32)


def get_hero(img, number):
    return [get(img, 0, number), get(img, 1, number), get(img, 2, number), get(img, 3, number)]


def get(img, x, y):
    return scale2x(get_pos(img, x * 32, y * 32, 32, 32))


def get2(img, number):
    return [get(img, 0, number), get(img, 1, number)]
