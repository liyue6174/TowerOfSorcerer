class GameControl(object):
    def __init__(self, gm):
        self.gm = gm

    def update(self):
        self.gm.frame += 1
