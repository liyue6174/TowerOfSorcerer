from . import load, get2, get_name

img = load('enemy.png')

cfg_enemy = {
    200: get2(img, 0),  # 绿头怪
    201: get2(img, 1),  # 红头怪
    202: get2(img, 2),  # 青头怪
    203: get2(img, 3),  # 怪王
    204: get2(img, 4),  # 骷髅人
    205: get2(img, 5),  # 骷髅士兵
    206: get2(img, 6),  # 骷髅队长
    207: get2(img, 7),  # 小蝙蝠
    208: get2(img, 8),  # 大蝙蝠
    209: get2(img, 9),  # 红蝙蝠
    210: get2(img, 10),  # 初级法师
    211: get2(img, 11),  # 高级法师
    212: get2(img, 12),  # 麻衣法师
    213: get2(img, 13),  # 红衣法师
    214: get2(img, 14),  # 兽面人
    215: get2(img, 15),  # 兽面武士
    216: get2(img, 16),  # 石头怪人
    217: get2(img, 17),  # 初级卫兵
    218: get2(img, 18),  # 冥卫兵
    219: get2(img, 19),  # 高级卫兵
    220: get2(img, 20),  # 双手剑士
    221: get2(img, 21),  # 影子战士
    222: get2(img, 22),  # 冥队长
    223: get2(img, 23),  # 冥战士
    224: get2(img, 24),  # 金卫士
    225: get2(img, 25),  # 金队长
    226: get2(img, 26),  # 白衣武士
    227: get2(img, 27),  # 红衣魔王(16层)
    228: get2(img, 27),  # 红衣魔王(19层)
    229: get2(img, 28),  # 灵武士
    230: get2(img, 29),  # 灵法师
    231: get2(img, 30),  # 冥灵魔王(19层)
    232: get2(img, 30),  # 冥灵魔王(21层)
}

cfg_name = {
    200: get_name(img, 0),  # 绿头怪
    201: get_name(img, 1),  # 红头怪
    202: get_name(img, 2),  # 青头怪
    203: get_name(img, 3),  # 怪王
    204: get_name(img, 4),  # 骷髅人
    205: get_name(img, 5),  # 骷髅士兵
    206: get_name(img, 6),  # 骷髅队长
    207: get_name(img, 7),  # 小蝙蝠
    208: get_name(img, 8),  # 大蝙蝠
    209: get_name(img, 9),  # 红蝙蝠
    210: get_name(img, 10),  # 初级法师
    211: get_name(img, 11),  # 高级法师
    212: get_name(img, 12),  # 麻衣法师
    213: get_name(img, 13),  # 红衣法师
    214: get_name(img, 14),  # 兽面人
    215: get_name(img, 15),  # 兽面武士
    216: get_name(img, 16),  # 石头怪人
    217: get_name(img, 17),  # 初级卫兵
    218: get_name(img, 18),  # 冥卫兵
    219: get_name(img, 19),  # 高级卫兵
    220: get_name(img, 20),  # 双手剑士
    221: get_name(img, 21),  # 影子战士
    222: get_name(img, 22),  # 冥队长
    223: get_name(img, 23),  # 冥战士
    224: get_name(img, 24),  # 金卫士
    225: get_name(img, 25),  # 金队长
    226: get_name(img, 26),  # 白衣武士
    227: get_name(img, 27),  # 红衣魔王(16层)
    228: get_name(img, 27),  # 红衣魔王(19层)
    229: get_name(img, 28),  # 灵武士
    230: get_name(img, 29),  # 灵法师
    231: get_name(img, 30),  # 冥灵魔王(19层)
    232: get_name(img, 30),  # 冥灵魔王(21层)
}
