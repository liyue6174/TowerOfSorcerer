from . import load, get_hero

img_hero = load('hero.png')

cfg_hero = {
    'UP': get_hero(img_hero, 3),
    'DOWN': get_hero(img_hero, 0),
    'LEFT': get_hero(img_hero, 1),
    'RIGHT': get_hero(img_hero, 2),
}
