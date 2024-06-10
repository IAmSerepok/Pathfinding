import pygame as pg
from random import random
from collections import deque
from math import floor


class App:
    def __init__(self):
        self.columns, self.rows = 50, 30
        self.tile_size = 15
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1]

        pg.init()
        self.sc = pg.display.set_mode([self.columns * self.tile_size, self.rows * self.tile_size])
        self.clock = pg.time.Clock()
        # grid
        self.grid = [[1 if random() < 0.3 else 0 for col in range(self.columns)] for row in range(self.rows)]
        # dict of adjacency lists
        self.graph = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)
        # BFS settings
        self.start = (-1, -1)
        self.queue = deque([self.start])
        self.visited = {self.start: None}
        self.cur_node = self.start

        self.time, self.delay = 0, 1
        self.started, self.running = False, True

    def get_rect(self, x, y):
        return x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2, self.tile_size - 2

    def set_ways(self, ways):
        self.ways = ways

    def check_next_node(self, x, y):
        return bool((0 <= x) and (x < self.columns) and (0 <= y) and (y < self.rows) and not self.grid[y][x])

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if self.check_next_node(x + dx, y + dy)]

    def get_cords(self, pos):
        x, y = pos
        x = floor(x / self.tile_size)
        y = floor(y / self.tile_size)
        return x, y

    def run(self):
        while True:
            # fill screen
            self.sc.fill(pg.Color('black'))
            # draw grid
            [[pg.draw.rect(self.sc, pg.Color('darkorange'), self.get_rect(x, y), border_radius=self.tile_size // 5)
              for x, col in enumerate(row) if col] for y, row in enumerate(self.grid)]
            # draw BFS work
            [pg.draw.rect(self.sc, pg.Color('forestgreen'), self.get_rect(x, y)) for x, y in self.visited]
            [pg.draw.rect(self.sc, pg.Color('darkslategray'), self.get_rect(x, y)) for x, y in self.queue]

            if self.time % self.delay == 0 and self.started and self.running:
                # BFS logic
                if self.queue:
                    self.cur_node = self.queue.popleft()
                    next_nodes = self.graph[self.cur_node]
                    for next_node in next_nodes:
                        if next_node not in self.visited:
                            self.queue.append(next_node)
                            self.visited[next_node] = self.cur_node

            # draw path
            path_head, path_segment = self.cur_node, self.cur_node
            while path_segment:
                pg.draw.rect(self.sc, pg.Color('white'), self.get_rect(*path_segment), self.tile_size,
                             border_radius=self.tile_size // 5)
                path_segment = self.visited[path_segment]
            pg.draw.rect(self.sc, pg.Color('blue'), self.get_rect(*self.start), border_radius=self.tile_size // 5)
            pg.draw.rect(self.sc, pg.Color('magenta'), self.get_rect(*path_head), border_radius=self.tile_size // 5)
            # pygame necessary lines
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if not self.started and event.button == 1:
                        x, y = self.get_cords(event.pos)
                        if not self.grid[y][x]:
                            self.start = self.cur_node = (x, y)
                            self.queue = deque([self.start])
                            self.visited = {self.start: None}
                            self.cur_node = self.start
                            self.started = not self.started
                    elif self.started and event.button == 3:
                        self.running = not self.running

            pg.display.flip()
            self.time += 1
            self.clock.tick(60)


app = App()
app.run()
