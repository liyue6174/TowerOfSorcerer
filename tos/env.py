import pickle


class Env(object):
    def __init__(self):
        self.init()

    def init(self):
        from tos.game.game_manager import GameManager
        from tos.game.game_control import GameControl
        import importlib

        self.gm = GameManager()
        self.gc = GameControl(self.gm)
        for level in range(22):
            self.gm.init(importlib.import_module('tos.config.level.level%d' % level).data)
        self.init_data = pickle.dumps(self.gm)
        self.temp_data = None
        self.render = None

    def display(self, visible):
        if visible:
            from tos.render.render import Render
            self.render = Render(self.gm)
            self.render.init()
        elif self.render is not None:
            self.render.end()
            self.render = None

    def save(self):
        self.temp_data = pickle.dumps(self.gm)

    def load(self):
        if self.temp_data is not None:
            self.gm = pickle.loads(self.temp_data)
            self.gc.gm = self.gm
            if self.render is not None:
                self.render.gm = self.gm

    def reset(self):
        self.gm = pickle.loads(self.init_data)
        self.gc.gm = self.gm
        if self.render is not None:
            self.render.gm = self.gm
        self.temp_data = None

    def quit(self):
        exit()

    def handle_events(self):
        if self.render is not None:
            import pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if self.gm.show_portal_page:
                        self.gm.handle_hero_portal(event.key - pygame.K_a)
                    elif self.gm.show_attr_book_page:
                        self.gm.handle_hero_attr_book(event.key - pygame.K_l)
                    elif self.gm.hero_has_portal and event.key == pygame.K_f:
                        self.gm.handle_hero_portal(-1)
                    elif self.gm.hero_has_attr_book and event.key == pygame.K_l:
                        self.gm.handle_hero_attr_book(-1)
                    elif self.gm.hero_has_cross and event.key == pygame.K_c:
                        self.gm.handle_hero_cross()
                    elif self.gm.hero_has_grail and event.key == pygame.K_g:
                        self.gm.handle_hero_grail()
                    elif self.gm.open_shop_number is not None:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_0]:
                            self.gm.handle_shop_event(
                                {
                                    pygame.K_1: 1,
                                    pygame.K_2: 2,
                                    pygame.K_3: 3,
                                    pygame.K_0: 0,
                                }[event.key]
                            )
                    elif event.key in [pygame.K_a, pygame.K_q, pygame.K_r, pygame.K_s]:
                        {
                            pygame.K_a: self.load,
                            pygame.K_q: self.quit,
                            pygame.K_r: self.reset,
                            pygame.K_s: self.save,
                        }[event.key]()
                    elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        self.gm.handle_move(
                            {
                                pygame.K_UP: 'UP',
                                pygame.K_DOWN: 'DOWN',
                                pygame.K_LEFT: 'LEFT',
                                pygame.K_RIGHT: 'RIGHT',
                            }[event.key]
                        )


if __name__ == '__main__':
    env = Env()
    env.display(True)

    while True:
        env.handle_events()
        env.gc.update()
        if env.render is not None:
            env.render.display()
