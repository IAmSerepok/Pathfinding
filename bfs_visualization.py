import pygame as pg

from random import random
from collections import deque
from math import floor

from typing import Tuple, List


class App:
    """Класс для визуализации алгоритма поиска в ширину (BFS) на сетке.

    Attributes:
        columns (int): Количество колонок в сетке.
        rows (int): Количество строк в сетке.
        tile_size (int): Размер одной клетки в пикселях.
        ways (List[Tuple[int, int]]): Направления движения.
        grid (List[List[int]]): Двумерный массив, представляющий сетку (0 - проходимая клетка, 1 - стена).
        graph (Dict[Tuple[int, int], List[Tuple[int, int]]]): Граф смежности для проходимых клеток.
        start (Tuple[int, int]): Начальная позиция для BFS.
        queue (deque): Очередь для алгоритма BFS.
        visited (Dict[Tuple[int, int], List[Tuple[int, int]]]): Посещенные клетки и их родители.
        cur_node (Tuple[int, int]): Текущая обрабатываемая клетка.
        time (int): Счетчик времени для управления скоростью анимации.
        delay (int): Задержка между шагами алгоритма.
        started (bool): Флаг начала алгоритма.
        running (bool): Флаг паузы/продолжения алгоритма.
    """

    def __init__(self, columns: int = 50, rows: int = 30, tile_size: int = 15) -> None:
        """Инициализирует приложение для визуализации BFS.

        Args:
            columns (int): Количество колонок в сетке.
            rows (int): Количество строк в сетке.
            tile_size (int): Размер клетки в пикселях.
        """
        self.columns, self.rows = columns, rows
        self.tile_size = tile_size

        # Направления движения (вверх, влево, вправо, вниз)
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1]

        pg.init()
        self.sc = pg.display.set_mode([self.columns * self.tile_size, 
                                      self.rows * self.tile_size])
        self.clock = pg.time.Clock()

        # Генерация случайной сетки (30% стен)
        self.grid = [[1 if random() < 0.3 else 0 
                     for _ in range(self.columns)] 
                     for _ in range(self.rows)]

        # Построение графа смежности
        self.graph = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.__get_next_nodes(x, y)

        # Инициализация переменных для BFS
        self.start = (-1, -1)
        self.queue = deque([self.start])
        self.visited = {self.start: None}
        self.cur_node = self.start

        self.time, self.delay = 0, 1
        self.started, self.running = False, True

    def __get_rect(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """Возвращает координаты и размер прямоугольника для отрисовки клетки.
        
        Args:
            x (int): Координата x клетки.
            y (int): Координата y клетки.
            
        Returns:
            rect (Typle[int, int, int, int]): Кортеж для pg.Rect.
        """
        return (x * self.tile_size + 1, y * self.tile_size + 1, 
                self.tile_size - 2, self.tile_size - 2)

    def __check_next_node(self, x: int, y: int) -> bool:
        """Проверяет, является ли клетка проходимой и находится в пределах сетки.
        
        Args:
            x (int): Координата x клетки.
            y (int): Координата y клетки.
            
        Returns:
            is_passable (bool): True если клетка проходима и в пределах сетки, иначе False.
        """
        return (0 <= x < self.columns and 
                0 <= y < self.rows and 
                not self.grid[y][x])

    def __get_next_nodes(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Возвращает список соседних проходимых клеток.
        
        Args:
            x (int): Координата x текущей клетки.
            y (int): Координата y текущей клетки.
            
        Returns:
            passable_neighbours (List[Tuple[int, int]]): Список кортежей (x, y) соседних проходимых клеток.
        """
        return [(x + dx, y + dy) for dx, dy in self.ways 
                if self.__check_next_node(x + dx, y + dy)]

    def __get_cords(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Конвертирует координаты мыши в координаты клетки сетки.
        
        Args:
            pos (Tuple[int, int]): Координат мыши.
            
        Returns:
            cell_coords (Tuple[int, int]): Координат клетки.
        """
        x, y = pos
        return floor(x / self.tile_size), floor(y / self.tile_size)

    def run(self):
        """Основной цикл приложения, обрабатывающий события и отрисовку."""
        while True:
            # Очистка экрана
            self.sc.fill(pg.Color('black'))
            
            # Отрисовка стен
            [[pg.draw.rect(self.sc, pg.Color('darkorange'), 
              self.__get_rect(x, y), border_radius=self.tile_size // 5)
              for x, col in enumerate(row) if col] 
              for y, row in enumerate(self.grid)]
            
            # Отрисовка посещенных клеток и очереди
            [pg.draw.rect(self.sc, pg.Color('forestgreen'), self.__get_rect(x, y)) 
             for x, y in self.visited]
            [pg.draw.rect(self.sc, pg.Color('darkslategray'), self.__get_rect(x, y)) 
             for x, y in self.queue]

            # Логика BFS
            if self.time % self.delay == 0 and self.started and self.running:
                if self.queue:
                    self.cur_node = self.queue.popleft()
                    next_nodes = self.graph.get(self.cur_node, [])
                    for next_node in next_nodes:
                        if next_node not in self.visited:
                            self.queue.append(next_node)
                            self.visited[next_node] = self.cur_node

            # Отрисовка пути
            path_head, path_segment = self.cur_node, self.cur_node
            while path_segment and path_segment in self.visited:
                pg.draw.rect(self.sc, pg.Color('white'), 
                            self.__get_rect(*path_segment), 
                            border_radius=self.tile_size // 5)
                path_segment = self.visited[path_segment]
            
            # Отрисовка стартовой и текущей клеток
            if self.start != (-1, -1):
                pg.draw.rect(self.sc, pg.Color('blue'), 
                            self.__get_rect(*self.start), 
                            border_radius=self.tile_size // 5)
            pg.draw.rect(self.sc, pg.Color('magenta'), 
                        self.__get_rect(*path_head), 
                        border_radius=self.tile_size // 5)

            # Обработка событий
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if not self.started and event.button == 1:  # ЛКМ
                        x, y = self.__get_cords(event.pos)
                        if (x, y) in self.graph:
                            self.start = self.cur_node = (x, y)
                            self.queue = deque([self.start])
                            self.visited = {self.start: None}
                            self.started = True
                    elif self.started and event.button == 3:  # ПКМ
                        self.running = not self.running

            pg.display.flip()
            self.time += 1
            self.clock.tick(60)


if __name__ == "__main__":
    app = App()
    app.run()
