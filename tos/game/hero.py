class Hero(object):
    def __init__(self, gm):
        self.gm = gm
        self.level = 1
        self.hp = 1000
        self.power = 10
        self.defense = 10
        self.gold = 0
        self.exp = 0
        self.key_count = {110: 0, 112: 0, 114: 0}

        self.pos_x = 5
        self.pos_y = 9
        self.state_frame = -5
        self.direction = 'DOWN'

    def move_to(self, pos_x, pos_y, direction):
        self.state_frame = self.gm.frame
        self.direction = direction
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update_hp(self, value):
        self.hp += value

    def update_power(self, value):
        self.power += value

    def update_defense(self, value):
        self.defense += value

    def update_gold(self, value):
        self.gold += value

    def update_exp(self, value):
        self.exp += value

    def update_key_count(self, key, value):
        self.key_count[key] += value
