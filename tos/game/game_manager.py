from tos.config.cfg_enemy import attr_enemy
from tos.game.hero import Hero


class GameManager(object):
    def __init__(self):
        self.frame = 0
        self.map = []
        self.up_pos = []
        self.down_pos = []
        self.cur_level = 0
        self.max_level = 0
        self.cur_level_enemy_index_set = set()
        self.attack_ani = [-5, (0, 0)]
        self.hero = Hero(self)

        self.open_shop_number = None
        self.hero_has_attr_book = False  # 怪物信息手册(L使用)
        self.hero_has_portal = False  # 传送门(F使用)
        self.hero_has_cross = False  # 十字架(C使用)
        self.hero_has_grail = False  # 圣水瓶(G使用)
        self.show_attr_book_page = False
        self.show_portal_page = False

    def init(self, data):
        self.map.append(data['map'])
        self.up_pos.append(data['up_pos'])
        self.down_pos.append(data['down_pos'])

    def get_loss_hp(self, enemy_index):
        enemy = attr_enemy[enemy_index]
        power_hero = self.hero.power - enemy['defense']
        if power_hero > 0:
            power_enemy = enemy['power'] - self.hero.defense
            power_enemy = power_enemy if power_enemy > 0 else 0
            attack_count = (enemy['hp'] - 1) // power_hero
            loss_hp = power_enemy * attack_count
            loss_hp += enemy['quick_attack'] if 'quick_attack' in enemy else 0
            loss_hp += (self.hero.hp // enemy['quick_atk_ratio']) if 'quick_atk_ratio' in enemy else 0
            return loss_hp
        return -1

    # ---------------------------------------- handle ----------------------------------------
    def handle_move(self, direction):
        (next_x, next_y) = {  # next position
            'UP': (self.hero.pos_x, self.hero.pos_y - 1),
            'DOWN': (self.hero.pos_x, self.hero.pos_y + 1),
            'LEFT': (self.hero.pos_x - 1, self.hero.pos_y),
            'RIGHT': (self.hero.pos_x + 1, self.hero.pos_y),
        }[direction]
        if next_x < 0 or next_y < 0 or next_x > 10 or next_y > 10:  # out of range
            return
        number = self.map[self.cur_level][next_x][next_y]
        if number in {101, 102, 103, 117, 118, 162, 163}:  # impassable
            return
        if number < 200:  # not enemy
            if number == 100:  # floor
                self.hero.move_to(next_x, next_y, direction)
            elif number == 104:  # up stairs
                self.cur_level += 1
                if self.cur_level > self.max_level:  # update max_level
                    self.max_level = self.cur_level
                self.hero.move_to(*self.down_pos[self.cur_level], 'DOWN')
            elif number == 105:  # down stairs
                self.cur_level -= 1
                self.hero.move_to(*self.up_pos[self.cur_level], 'DOWN')
            elif number in {126, 127, 153, 154, 155, 156, 160, 161}:  # prop or shop event
                self.open_shop_number = number
            elif number in {111, 113, 115, 116, 150, 151, 152}:  # open the door or npc event
                if number in {111, 113, 115} and self.hero.key_count[number - 1] == 0:  # unable open
                    return
                if number in {111, 113, 115}:  # open the door
                    self.hero.update_key_count(number - 1, -1)
                elif number == 150:  # fairy event
                    self.hero.update_key_count(110, 1)
                    self.hero.update_key_count(112, 1)
                    self.hero.update_key_count(114, 1)
                elif number == 151:  # thief event
                    self.map[2][1][6] = 100
                    self.map[12][10][0] = 148
                elif number == 152:  # princess event
                    self.map[18][6][10] = 100
                self.map[self.cur_level][next_x][next_y] = 100
            else:  # get prop
                if number in {132, 133}:  # add up
                    self.hero.update_hp({132: 200, 133: 500}[number])
                elif number in {120, 122, 124, 128, 130}:  # add power
                    self.hero.update_power({120: 10, 122: 70, 124: 70, 128: 150, 130: 3}[number])
                elif number in {121, 123, 125, 129, 131}:  # add defense
                    self.hero.update_defense({121: 10, 123: 30, 125: 85, 129: 190, 131: 3}[number])
                elif number in {110, 112, 114}:  # add key
                    self.hero.key_count[number] += 1
                elif number == 140:  # enemy info reel
                    self.hero_has_attr_book = True
                elif number == 141:  # portal
                    self.hero_has_portal = True
                elif number == 142:  # gold coin
                    self.hero.update_gold(300)
                elif number == 143:  # grail
                    self.hero_has_grail = True
                elif number == 144:  # key box
                    self.hero.update_key_count(110, 1)
                    self.hero.update_key_count(112, 1)
                    self.hero.update_key_count(114, 1)
                elif number == 145:
                    self.hero.level += 1
                    self.hero.update_hp(1000)
                    self.hero.update_power(10)
                    self.hero.update_defense(10)
                elif number == 146:
                    self.hero.level += 3
                    self.hero.update_hp(3000)
                    self.hero.update_power(30)
                    self.hero.update_defense(30)
                elif number == 147:  # cross
                    self.hero_has_cross = True
                elif number == 148:  # gemstone hoe
                    self.map[18][5][9] = 100
                self.hero.move_to(next_x, next_y, direction)
                self.map[self.cur_level][next_x][next_y] = 100
        else:  # fighting with enemy
            loss_hp = self.get_loss_hp(number)
            if 0 <= loss_hp < self.hero.hp:
                enemy = attr_enemy[number]
                self.hero.update_hp(-loss_hp)
                self.hero.update_gold(enemy['gold'])
                self.hero.update_exp(enemy['exp'])
                self.hero.move_to(next_x, next_y, direction)
                self.attack_ani = [self.frame, (next_x, next_y)]
                self.map[self.cur_level][next_x][next_y] = 100

    def handle_shop_event(self, value):
        {
            126: self.handle_shop_126_event,
            127: self.handle_shop_127_event,
            153: self.handle_shop_153_event,
            154: self.handle_shop_154_event,
            155: self.handle_shop_155_event,
            156: self.handle_shop_156_event,
            160: self.handle_shop_160_event,
            161: self.handle_shop_161_event,
        }[self.open_shop_number](value)

    def handle_shop_126_event(self, value):
        '''处理15层仙剑逻辑'''
        if value == 0:
            self.open_shop_number = None
        elif value == 1 and self.hero.gold >= 500:
            self.hero.update_power(120)
            self.hero.update_gold(-500)
            self.map[15][4][3] = 100
            self.open_shop_number = None

    def handle_shop_127_event(self, value):
        '''处理15层仙盾逻辑'''
        if value == 0:
            self.open_shop_number = None
        elif value == 1 and self.hero.exp >= 500:
            self.hero.update_defense(120)
            self.hero.update_exp(-500)
            self.map[15][6][3] = 100
            self.open_shop_number = None

    def handle_shop_153_event(self, value):
        '''处理第5层白发老人的逻辑'''
        if value == 0:
            self.open_shop_number = None
        elif value == 1 and self.hero.exp >= 100:
            self.hero.update_exp(-100)
            self.hero.level += 1
            self.hero.update_hp(1000)
            self.hero.update_power(7)
            self.hero.update_defense(7)
        elif value == 2 and self.hero.exp >= 30:
            self.hero.update_exp(-30)
            self.hero.update_power(5)
        elif value == 3 and self.hero.exp >= 30:
            self.hero.update_exp(-30)
            self.hero.update_defense(5)

    def handle_shop_154_event(self, value):
        '''处理第13层白发老人的逻辑'''
        if value == 0:
            self.open_shop_number = None
        elif value == 1 and self.hero.exp >= 270:
            self.hero.update_exp(-270)
            self.hero.level += 3
            self.hero.update_hp(3000)
            self.hero.update_power(20)
            self.hero.update_defense(20)
        elif value == 2 and self.hero.exp >= 95:
            self.hero.update_exp(-95)
            self.hero.update_power(17)
        elif value == 3 and self.hero.exp >= 95:
            self.hero.update_exp(-95)
            self.hero.update_defense(17)

    def handle_shop_155_event(self, value):
        '''处理第5层红衣商人的逻辑'''
        if value == 0:
            self.open_shop_number = None
        elif value == 1 and self.hero.gold >= 10:
            self.hero.update_gold(-10)
            self.hero.key_count[110] += 1
        elif value == 2 and self.hero.gold >= 50:
            self.hero.update_gold(-50)
            self.hero.key_count[112] += 1
        elif value == 3 and self.hero.gold >= 100:
            self.hero.update_gold(-100)
            self.hero.key_count[114] += 1

    def handle_shop_156_event(self, value):
        '''处理第12层红衣商人的逻辑'''
        if value == 0:
            self.open_shop_number = None
        elif value == 1 and self.hero.key_count[110] > 0:
            self.hero.key_count[110] -= 1
            self.hero.update_gold(7)
        elif value == 2 and self.hero.key_count[112] > 0:
            self.hero.key_count[112] -= 1
            self.hero.update_gold(35)
        elif value == 3 and self.hero.key_count[114] > 0:
            self.hero.key_count[114] -= 1
            self.hero.update_gold(70)

    def handle_shop_160_event(self, value):
        '''处理第3层商店的逻辑'''
        if value == 0:
            self.open_shop_number = None
        elif value in [1, 2, 3] and self.hero.gold >= 25:
            self.hero.update_gold(-25)
            if value == 1:
                self.hero.update_hp(800)
            elif value == 2:
                self.hero.update_power(4)
            elif value == 3:
                self.hero.update_defense(4)

    def handle_shop_161_event(self, value):
        '''处理第11层商店的逻辑'''
        if value == 0:
            self.open_shop_number = None
        elif value in [1, 2, 3] and self.hero.gold >= 100:
            self.hero.update_gold(-100)
            if value == 1:
                self.hero.update_hp(4000)
            elif value == 2:
                self.hero.update_power(20)
            elif value == 3:
                self.hero.update_defense(20)

    def handle_hero_attr_book(self, value):
        '''处理使用圣光徽道具的逻辑'''
        if not self.show_attr_book_page and value == -1:
            self.cur_level_enemy_index_set.clear()
            for map_info in self.map[self.cur_level]:
                for number in map_info:
                    if number >= 200:
                        self.cur_level_enemy_index_set.add(number)
            self.show_attr_book_page = True
        elif self.show_attr_book_page and value == 0:
            self.show_attr_book_page = False

    def handle_hero_portal(self, value):
        '''处理使用传送门道具的逻辑'''
        if self.cur_level == 21:
            return
        if not self.show_portal_page and value == -1:
            self.show_portal_page = True
        elif self.show_portal_page and 0 <= value <= self.max_level:
            self.cur_level = value
            self.hero.move_to(*self.down_pos[self.cur_level], 'DOWN')
            self.show_portal_page = False

    def handle_hero_cross(self):
        '''处理使用十字架的逻辑'''
        self.hero.update_hp(self.hero.hp // 3)
        self.hero.update_power(self.hero.power // 3)
        self.hero.update_defense(self.hero.defense // 3)
        self.hero_has_cross = False

    def handle_hero_grail(self):
        '''处理使用圣水瓶的逻辑'''
        self.hero.update_hp(self.hero.hp)
        self.hero_has_grail = False
