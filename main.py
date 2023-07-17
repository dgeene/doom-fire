import pygame as pg
import sys
from pygame import gfxdraw
from random import randint
"""
Doom Fire
https://www.youtube.com/watch?v=6hE5sEh0pwI
"""

WIN_SIZE = WIDTH, HEIGHT = 1600, 900
STEPS_BETWEEN_COLORS = 9
COLORS = ['black', 'red', 'orange', 'yellow', 'white']
PIXEL_SIZE = 4

FIRE_REPS = 4
FIRE_WIDTH = WIDTH // (PIXEL_SIZE * FIRE_REPS)
FIRE_HEIGHT = HEIGHT // PIXEL_SIZE

class DoomFire:
    def __init__(self, app):
        self.app = app
        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        # create a surface for fire repetition
        self.fire_surf = pg.Surface([PIXEL_SIZE * FIRE_WIDTH, HEIGHT])

    def do_fire(self):
        """
        """
        for x in range(FIRE_WIDTH):
            for y in range(1, FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    rnd = randint(0, 3) # makes the fire effect somewhat
                    # using modulo prevents us from going outside index range
                    self.fire_array[y - 1][(x - rnd + 1) % FIRE_WIDTH] = color_index - rnd % 2
                else:
                    """
                    if a 0 color index has reached some particle. flame has gone out.
                    so spread black particles upwards
                    """
                    self.fire_array[y - 1][x] = 0

    def draw_fire(self):
        """
        The 0 index does not interest us because it will be black
        """
        self.fire_surf.fill('black')
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palette[color_index]
                    # draw fire particles
                    gfxdraw.box(self.fire_surf, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE,
                                                  PIXEL_SIZE), color)
        for i in range(FIRE_REPS):
            self.app.screen.blit(self.fire_surf, (self.fire_surf.get_width() * i, 0))

    def get_fire_array(self):
        """Create a 2d array for our fire

        Assign the last color value of the palette to the elements of the last row
        """
        fire_array = [[0 for i in range(FIRE_WIDTH)] for j in range(FIRE_HEIGHT)]
        for i in range(FIRE_WIDTH):
            fire_array[FIRE_HEIGHT - 1][i] = len(self.palette) - 1
        return fire_array

    def draw_palette(self):
        """display each color of this palette as a square
        """
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
        self.do_fire()

    def draw(self):
        #self.draw_palette()
        self.draw_fire()


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
