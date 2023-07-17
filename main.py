import pygame as pg
import sys
"""
Doom Fire
https://www.youtube.com/watch?v=6hE5sEh0pwI
"""

WIN_SIZE = WIDTH, HEIGHT = 1600, 900
STEPS_BETWEEN_COLORS = 4
COLORS = ['black', 'red', 'orange', 'yellow', 'white']

class DoomFire:
    def __init__(self, app):
        self.app = app
        self.palette = self.get_palette()

    def draw_palette(self):
        # display each color of this palette as a square 
        size = 90
        for i, color in enumerate(self.palette):
            pg.draw.rect(self.app.screen, color, (i * size, HEIGHT // 2, size - 5, size - 5))

    @staticmethod
    def get_palette():
        palette = [(0, 0, 0)]
        for i, color in enumerate(COLORS[:-1]):
            c1, c2 = color, COLORS[i + 1]
            for step in range(STEPS_BETWEEN_COLORS):
                # linear interpolation function
                c = pg.Color(c1).lerp(c2, (step + 0.5) / STEPS_BETWEEN_COLORS)
                palette.append(c)
        return palette

    def update(self):
        pass

    def draw(self):
        self.draw_palette()


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(size=WIN_SIZE)
        self.clock = pg.time.Clock()
        self.doom_fire = DoomFire(self)

    def update(self):
        self.doom_fire.update()
        self.clock.tick(60)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
    
    def draw(self):
        self.screen.fill('black')
        self.doom_fire.draw()
        pg.display.flip()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                self.update()
                self.draw()

if __name__ == '__main__':
    app = App()
    app.run()
