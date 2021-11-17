import pygame as pg
from collections import deque
from random import randrange


class Ant:
    def __init__(self, app, pos, color):
        self.app = app
        self.color = color
        self.x, self.y = pos
        self.increments = deque([(1, 0), (0, 1), (-1, 0), (0, -1)])

    def run(self):
        value = self.app.grid[self.y][self.x]
        self.app.grid[self.y][self.x] = not value

        SIZE = self.app.CELL_SIZE
        rect = self.x * SIZE, self.y * SIZE, SIZE - 1, SIZE - 1
        if value:
            pg.draw.rect(self.app.screen, (0, 0, 0), rect)
        else:
            pg.draw.rect(self.app.screen, self.color, rect)

        self.increments.rotate(1) if value else self.increments.rotate(-1)
        dx, dy = self.increments[0]
        self.x = (self.x + dx) % self.app.COLS
        self.y = (self.y + dy) % self.app.ROWS


class App:
    def __init__(self, WIDTH=1600, HEIGHT=900, CELL_SIZE=8, ANTS_COL=15, FPS=30):
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()

        self.CELL_SIZE = CELL_SIZE
        self.ROWS, self.COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
        self.grid = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]

        self.ants = [Ant(self, [randrange(self.COLS), randrange(self.ROWS)], self.get_color()) for _ in range(ANTS_COL)]

        self.pause = True
        self.FPS0 = FPS
        self.FPS = FPS

    @staticmethod
    def get_color():
        channel = lambda: randrange(100, 220)
        return channel(), channel(), channel()

    def run(self):
        while True:
            if not self.pause:
                [ant.run() for ant in self.ants]

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.pause = not self.pause
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.ants.append(Ant(self, [event.pos[0] // self.CELL_SIZE, event.pos[1] // self.CELL_SIZE],
                                             self.get_color()))
                    if event.button == 2:
                        self.FPS = self.FPS0
                    elif event.button == 4:
                        self.FPS *= 1.1
                    elif event.button == 5:
                        self.FPS = int(self.FPS / 1.1)

            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = App(1920, 1080, 3, 10, 120)
    app.run()
