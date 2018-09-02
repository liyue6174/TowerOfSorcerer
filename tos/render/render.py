class Render(object):
    def __init__(self, gm):
        self.gm = gm
        self.size = 64

    def init(self):
        from . import get_path
        import pygame
        pygame.init()
        pygame.key.set_repeat(50, 50)
        pygame.display.set_caption('TOS')
        self.screen = pygame.display.set_mode((18 * self.size, 13 * self.size))
        self.font = {
            30: pygame.font.Font(get_path('res') + "/notosans.ttc", 30),
            35: pygame.font.Font(get_path('res') + "/notosans.ttc", 35),
            40: pygame.font.Font(get_path('res') + "/notosans.ttc", 40),
        }
        self.clock = pygame.time.Clock()

    def display(self):
        import pygame
        self.clock.tick(30)
        self.screen.fill((0, 0, 0))
        self.draw_background()
        if self.gm.show_attr_book_page:
            self.draw_enemy_info()
        elif self.gm.show_portal_page:
            self.draw_portal_info()
        else:
            self.draw_map()
            self.draw_hero()
            self.draw_attack_ani()
            if self.gm.open_shop_number is not None:
                self.draw_shop()
        pygame.display.update()

    def draw_background(self):
        from .image_background import img_background, cfg_other
        from .image_base import cfg_base
        self.screen.blit(img_background, (0, 0))
        self.draw_font(40, self.gm.hero.level, 255, 80)
        self.draw_font(35, self.gm.hero.hp, 295, 136)
        self.draw_font(35, self.gm.hero.power, 295, 181)
        self.draw_font(35, self.gm.hero.defense, 295, 226)
        self.draw_font(35, self.gm.hero.gold, 295, 271)
        self.draw_font(35, self.gm.hero.exp, 295, 316)
        self.draw_font(35, self.gm.hero.key_count[110], 255, 383)
        self.draw_font(35, self.gm.hero.key_count[112], 255, 447)
        self.draw_font(35, self.gm.hero.key_count[114], 255, 511)
        self.draw_font(35, self.gm.cur_level, 192, 629, mode=1)
        if self.gm.hero_has_attr_book:
            self.screen.blit(cfg_base[140], (64, 565))
            self.screen.blit(cfg_other['key_L'], (108, 609))
        if self.gm.hero_has_portal:
            self.screen.blit(cfg_base[141], (128, 565))
            self.screen.blit(cfg_other['key_F'], (172, 609))
            if self.gm.cur_level == 21:
                self.screen.blit(cfg_other['ban'], (128, 565))
        if self.gm.hero_has_cross:
            self.screen.blit(cfg_base[147], (192, 565))
            self.screen.blit(cfg_other['key_C'], (236, 609))
        if self.gm.hero_has_grail:
            self.screen.blit(cfg_base[143], (256, 565))
            self.screen.blit(cfg_other['key_G'], (300, 609))

    def draw_map(self):
        from .image_base import cfg_base
        from .image_enemy import cfg_enemy
        map = self.gm.map[self.gm.cur_level]
        for i in range(11):
            for j in range(11):
                cfg = (cfg_base if map[i][j] < 200 else cfg_enemy)[map[i][j]]
                img = cfg[self.gm.frame // 8 % 2] if type(cfg) == type([]) else cfg
                self.screen.blit(img, ((i + 6) * self.size, (j + 1) * self.size))

    def draw_hero(self):
        from .image_hero import cfg_hero
        hero = self.gm.hero
        delta_frame = self.gm.frame - hero.state_frame
        state = delta_frame if delta_frame < 2 else 0
        img = cfg_hero[hero.direction][state]
        self.screen.blit(img, ((hero.pos_x + 6) * self.size, (hero.pos_y + 1) * self.size))

    def draw_attack_ani(self):
        delta = self.gm.frame - self.gm.attack_ani[0]
        if delta < 5:
            from .image_background import cfg_other
            img, (x, y) = cfg_other['attack_ani'][delta], self.gm.attack_ani[1]
            self.screen.blit(img, ((x + 6) * self.size, (y + 1) * self.size))

    def draw_shop(self):
        from .image_background import cfg_shop_bg
        from .image_base import cfg_base
        if self.gm.open_shop_number in {126, 127}:
            self.screen.blit(cfg_shop_bg[self.gm.open_shop_number], (541, 285))
            self.screen.blit(cfg_base[self.gm.open_shop_number], (568, 330))
        else:
            self.screen.blit(cfg_shop_bg[self.gm.open_shop_number], (541, 221))
            self.screen.blit(cfg_base[self.gm.open_shop_number][self.gm.frame // 8 % 2], (568, 266))
        if self.gm.open_shop_number == 126:
            self.draw_font(35, 500, 775, 300, condition=self.gm.hero.gold >= 500)
        elif self.gm.open_shop_number == 127:
            self.draw_font(35, 500, 775, 300, condition=self.gm.hero.exp >= 500)
        elif self.gm.open_shop_number == 153:
            self.draw_font(35, 100, 872, 371, condition=self.gm.hero.exp >= 100)
            self.draw_font(35, 30, 872, 426, condition=self.gm.hero.exp >= 30)
            self.draw_font(35, 30, 872, 481, condition=self.gm.hero.exp >= 30)
        elif self.gm.open_shop_number == 154:
            self.draw_font(35, 270, 872, 371, condition=self.gm.hero.exp >= 270)
            self.draw_font(35, 95, 877, 426, condition=self.gm.hero.exp >= 95)
            self.draw_font(35, 95, 877, 481, condition=self.gm.hero.exp >= 95)
        elif self.gm.open_shop_number == 155:
            self.draw_font(35, 10, 887, 371, condition=self.gm.hero.gold >= 10)
            self.draw_font(35, 50, 887, 426, condition=self.gm.hero.gold >= 50)
            self.draw_font(35, 100, 895, 481, condition=self.gm.hero.gold >= 100)
        elif self.gm.open_shop_number == 156:
            self.draw_font(35, 1, 698, 371, condition=self.gm.hero.key_count[110] > 0)
            self.draw_font(35, 1, 688, 426, condition=self.gm.hero.key_count[112] > 0)
            self.draw_font(35, 1, 688, 481, condition=self.gm.hero.key_count[114] > 0)
        elif self.gm.open_shop_number == 160:
            self.draw_font(35, 25, 855, 235, condition=self.gm.hero.gold >= 25)
        elif self.gm.open_shop_number == 161:
            self.draw_font(35, 100, 862, 235, condition=self.gm.hero.gold >= 100)

    def draw_enemy_info(self):
        from .image_background import cfg_other
        from .image_enemy import cfg_enemy, cfg_name
        from tos.config.cfg_enemy import attr_enemy
        for k, number in enumerate(self.gm.cur_level_enemy_index_set):
            enemy_info = attr_enemy[number]
            self.screen.blit(cfg_other['enemy_attr_bg'], (400, k * 86 + 80))
            self.screen.blit(cfg_enemy[number][self.gm.frame // 8 % 2], (403, k * 86 + 83))
            self.screen.blit(cfg_name[number], (547, k * 86 + 82))
            self.draw_font(30, enemy_info['power'], 791, k * 86 + 77, mode=1)
            self.draw_font(30, enemy_info['gold'], 989, k * 86 + 77, mode=2)
            self.draw_font(30, enemy_info['exp'], 1002, k * 86 + 77, mode=0)
            self.draw_font(30, enemy_info['hp'], 611, k * 86 + 113, mode=1)
            self.draw_font(30, enemy_info['defense'], 791, k * 86 + 113, mode=1)
            loss_hp = self.gm.get_loss_hp(number)
            if loss_hp < 0:
                self.screen.blit(cfg_other['can_not_attack'], (920, k * 86 + 114))
            else:
                self.draw_font(30, loss_hp, 996, k * 86 + 113, mode=1, condition=loss_hp < self.gm.hero.hp)

    def draw_portal_info(self):
        from .image_background import cfg_other
        self.screen.blit(cfg_other['portal_bg'], (400, 80))
        for i in range(self.gm.max_level + 1):
            pos_x, pos_y = 430 + i // 7 * 220, 250 + i % 7 * 70
            self.screen.blit(cfg_other['portal_level'], (pos_x, pos_y))
            self.draw_font(35, chr(ord('A') + i), pos_x + 20, pos_y - 5, mode=1)
            self.draw_font(35, i, pos_x + 106, pos_y - 5, mode=1)

    def draw_font(self, size, info, x, y, mode=2, condition=None):  # mode: 0_left, 1_center, 2_right
        color = {None: (255, 255, 255), True: (0, 255, 0), False: (255, 0, 0)}[condition]
        image = self.font[size].render(str(info), True, color)
        if mode == 1:
            x -= image.get_width() * 0.5
        elif mode == 2:
            x -= image.get_width()
        self.screen.blit(image, (x, y))
