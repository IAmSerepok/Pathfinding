import pygame as pg
from random import random
from collections import deque


class App:
    def __init__(self):
        self.cols, self.rows = 35, 20
        self.tile_size = 30
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1]

        pg.init()
        self.sc = pg.display.set_mode([self.cols * self.tile_size, self.rows * self.tile_size])
        self.clock = pg.time.Clock()
        # grid
        self.grid = [[1 if random() < 0.2 else 0 for col in range(self.cols)] for row in range(self.rows)]
        # dict of adjacency lists
        self.graph = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

        # BFS settings
        self.start = (0, 0)
        self.goal = self.start
        self.queue = deque([self.start])
        self.visited = {self.start: None}

    def get_rect(self, x, y):
        return x * self.tile_size + 1, y * self.tile_size + 1, self.tile_size - 2, self.tile_size - 2

    def get_center(self, x, y):
        return (x + 0.5) * self.tile_size + 1, (y + 0.5) * self.tile_size + 1

    def check_next_node(self, x, y):
        return (0 <= x) and (x < self.cols) and (0 <= y) and (y < self.rows) and not self.grid[y][x]

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if self.check_next_node(x + dx, y + dy)]

    def get_click_mouse_pos(self):
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.tile_size, y // self.tile_size
        pg.draw.rect(self.sc, pg.Color('red'), self.get_rect(grid_x, grid_y))
        click = pg.mouse.get_pressed()
        return grid_x, grid_y

    def bfs(self):
        self.queue = deque([self.start])
        self.visited = {self.start: None}

        while self.queue:
            cur_node = self.queue.popleft()
            if cur_node == self.goal:
                break

            next_nodes = self.graph[cur_node]
            for next_node in next_nodes:
                if next_node not in self.visited:
                    self.queue.append(next_node)
                    self.visited[next_node] = cur_node

    def run(self):
        while True:
            # fill screen
            self.sc.fill(pg.Color('black'))
            self.bfs()
            # draw grid
            [[pg.draw.rect(self.sc, (255, 115, 0), self.get_rect(x, y), border_radius=self.tile_size // 5)
              for x, col in enumerate(row) if col] for y, row in enumerate(self.grid)]
            # draw BFS work
            [pg.draw.rect(self.sc, pg.Color('forestgreen'), self.get_rect(x, y)) for x, y in self.visited]
            [pg.draw.rect(self.sc, pg.Color('darkslategray'), self.get_rect(x, y)) for x, y in self.queue]

            # draw path
            path_head, path_segment = self.goal, self.goal
            while path_segment and path_segment in self.visited:
                pg.draw.circle(self.sc, pg.Color('white'), self.get_center(*path_segment), self.tile_size // 4)
                path_segment = self.visited[path_segment]
            pg.draw.rect(self.sc, pg.Color('blue'), self.get_rect(*self.start), border_radius=self.tile_size // 5)
            pg.draw.rect(self.sc, pg.Color('magenta'), self.get_rect(*path_head), border_radius=self.tile_size // 5)
            # pygame necessary lines
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = self.get_click_mouse_pos()
                    if event.button == 1:
                        if mouse_pos and not self.grid[mouse_pos[1]][mouse_pos[0]]:
                            self.goal = mouse_pos
                    elif event.button == 3:
                        if mouse_pos and not self.grid[mouse_pos[1]][mouse_pos[0]]:
                            self.start = mouse_pos

            pg.display.flip()
            self.clock.tick(30)


app = App()
app.run()
