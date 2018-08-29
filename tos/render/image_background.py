from . import load, get_pos

img_background = load('background.png')
img_shop_bg = load('shop_bg.png')
img_other = load('other.png')

cfg_shop_bg = {
    126: get_pos(img_shop_bg, 0, 1161, 390, 262),
    127: get_pos(img_shop_bg, 387, 1161, 390, 262),
    153: get_pos(img_shop_bg, 0, 0, 390, 390),
    154: get_pos(img_shop_bg, 387, 0, 390, 390),
    155: get_pos(img_shop_bg, 0, 387, 390, 390),
    156: get_pos(img_shop_bg, 387, 387, 390, 390),
    160: get_pos(img_shop_bg, 0, 774, 390, 390),
    161: get_pos(img_shop_bg, 387, 774, 390, 390),
}

cfg_other = {
    'enemy_attr_bg': get_pos(img_other, 0, 0, 672, 70),
    'can_not_attack': get_pos(img_other, 175, 220, 155, 40),
    'portal_bg': get_pos(img_other, 0, 70, 672, 150),
    'portal_level': get_pos(img_other, 0, 220, 175, 40),
    'key_L': get_pos(img_other, 330, 220, 20, 20),
    'key_F': get_pos(img_other, 350, 220, 20, 20),
    'key_C': get_pos(img_other, 330, 240, 20, 20),
    'key_G': get_pos(img_other, 350, 240, 20, 20),
    'ban': get_pos(img_other, 320, 260, 64, 64),
    'attack_ani': [
        get_pos(img_other, 0, 260, 64, 64),
        get_pos(img_other, 64, 260, 64, 64),
        get_pos(img_other, 128, 260, 64, 64),
        get_pos(img_other, 192, 260, 64, 64),
        get_pos(img_other, 256, 260, 64, 64),
    ],
}
