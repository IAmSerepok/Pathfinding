import pygame as pg

from random import random
from collections import deque

from typing import Tuple, List


class App:
    """Класс для визуализации алгоритма поиска пути на базе поиска в ширину (BFS) на 2D сетке.

    Attributes:
        columns (int): Количество колонок в сетке.
        rows (int): Количество строк в сетке.
        tile_size (int): Размер одной клетки в пикселях.
        ways (List[Tuple[int, int]]): Направления движения (соседи по вертикали/горизонтали).
        grid (List[List[int]]): 2D массив, представляющий карту (0 - свободно, 1 - препятствие).
        graph (Dict[Tuple[int, int], List[Tuple[int, int]]]): Граф смежности для свободных клеток.
        start (Tuple[int, int]): Стартовая позиция для BFS.
        goal (Tuple[int, int]): Целевая позиция.
        queue (deque): Очередь для алгоритма BFS.
        visited (Dict[Tuple[int, int], Tuple[int, int]]): Посещенные клетки и их родители.
    """

    def __init__(self, columns: int = 50, rows: int = 30, tile_size: int = 15) -> None:
        """Инициализирует приложение с заданными параметрами сетки.

        Args:
            columns (int): Ширина сетки в клетках.
            rows (int): Высота сетки в клетках.
            tile_size (int): Размер клетки в пикселях.
        """
        self.columns, self.rows = columns, rows
        self.tile_size = tile_size
        
        # Возможные направления движения (вверх, влево, вправо, вниз)
        self.ways = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        # Инициализация pygame
        pg.init()
        self.sc = pg.display.set_mode([self.columns * self.tile_size, 
                                      self.rows * self.tile_size])
        self.clock = pg.time.Clock()

        # Генерация случайной карты (20% препятствий)
        self.grid = [[1 if random() < 0.2 else 0 
                     for _ in range(self.columns)] 
                     for _ in range(self.rows)]

        # Построение графа смежности
        self.graph = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:  # Если клетка свободна
                    self.graph[(x, y)] = self.__get_next_nodes(x, y)

        # Начальные параметры BFS
        self.start = (0, 0)
        self.goal = self.start
        self.queue = deque([self.start])
        self.visited = {self.start: None}

    def __get_rect(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """Возвращает параметры прямоугольника для отрисовки клетки.
        
        Args:
            x (int): x координата клетки.
            y (int): y координата клетки.
            
        Returns:
            rect (Typle[int, int, int, int]): Кортеж для pg.Rect.
        """
        return (x * self.tile_size + 1, 
                y * self.tile_size + 1, 
                self.tile_size - 2, 
                self.tile_size - 2)

    def __get_center(self, x: int, y: int) -> Tuple[float, float]:
        """Возвращает центр клетки для отрисовки пути.
        
        Args:
            x (int): x координата клетки.
            y (int): y координата клетки.
            
        Returns:
            center_coords (Tuple[int, int]): Координаты центра клетки в пикселях.
        """
        return ((x + 0.5) * self.tile_size, 
                (y + 0.5) * self.tile_size)

    def __check_next_node(self, x: int, y: int) -> bool:
        """Проверяет, доступна ли клетка для перемещения.
        
        Args:
            x: X-координата клетки.
            y: Y-координата клетки.
            
        Returns:
            is_passable (bool): True если клетка проходима и в пределах сетки, иначе False.
        """
        return (0 <= x < self.columns and 
                0 <= y < self.rows and 
                not self.grid[y][x])

    def __get_next_nodes(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Возвращает список доступных соседних клеток.
        
        Args:
            x (int): x координата текущей клетки.
            y (int): y координата текущей клетки.
            
        Returns:
            passable_neighbours (List[Tuple[int, int]]): Список кортежей (x, y) соседних проходимых клеток.
        """
        return [(x + dx, y + dy) for dx, dy in self.ways 
                if self.__check_next_node(x + dx, y + dy)]

    def __get_click_mouse_pos(self) -> Tuple[int, int]:
        """Обрабатывает позицию клика мыши и возвращает координаты клетки.
        
        Returns:
            click_coords (Tuple[int, int]): Координаты (x, y) клетки, по которой кликнули.
        """
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.tile_size, y // self.tile_size
        pg.draw.rect(self.sc, pg.Color('red'), self.__get_rect(grid_x, grid_y))
        return grid_x, grid_y

    def __bfs(self) -> None:
        """Выполняет поиск в ширину (BFS) от стартовой до целевой точки."""
        self.queue = deque([self.start])
        self.visited = {self.start: None}

        while self.queue:
            cur_node = self.queue.popleft()
            if cur_node == self.goal:
                break

            for next_node in self.graph.get(cur_node, []):
                if next_node not in self.visited:
                    self.queue.append(next_node)
                    self.visited[next_node] = cur_node

    def run(self) -> None:
        """Основной цикл приложения, обрабатывающий отрисовку и события."""
        while True:
            # Очистка экрана
            self.sc.fill(pg.Color('black'))
            
            # Выполнение BFS
            self.__bfs()
            
            # Отрисовка сетки
            for y, row in enumerate(self.grid):
                for x, col in enumerate(row):
                    if col:  # Препятствия
                        pg.draw.rect(self.sc, (255, 115, 0), 
                                    self.__get_rect(x, y), 
                                    border_radius=self.tile_size // 5)
            
            # Отрисовка посещенных клеток и очереди
            for x, y in self.visited:
                pg.draw.rect(self.sc, pg.Color('forestgreen'), self.__get_rect(x, y))
            for x, y in self.queue:
                pg.draw.rect(self.sc, pg.Color('darkslategray'), self.__get_rect(x, y))

            # Отрисовка пути
            path_head = path_segment = self.goal
            while path_segment and path_segment in self.visited:
                pg.draw.circle(self.sc, pg.Color('white'), 
                              self.__get_center(*path_segment), 
                              self.tile_size // 4)
                path_segment = self.visited[path_segment]
            
            # Отрисовка старта и цели
            pg.draw.rect(self.sc, pg.Color('blue'), 
                        self.__get_rect(*self.start), 
                        border_radius=self.tile_size // 5)
            pg.draw.rect(self.sc, pg.Color('magenta'), 
                        self.__get_rect(*path_head), 
                        border_radius=self.tile_size // 5)

            # Обработка событий
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    try:
                        x, y = self.__get_click_mouse_pos()
                        if not self.grid[y][x]:  # Если клетка свободна
                            if event.button == 1:  # ЛКМ - установка цели
                                self.goal = (x, y)
                            elif event.button == 3:  # ПКМ - установка старта
                                self.start = (x, y)
                    except IndexError:
                        pass  # Клик за пределами сетки

            pg.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    app = App()
    app.run()
