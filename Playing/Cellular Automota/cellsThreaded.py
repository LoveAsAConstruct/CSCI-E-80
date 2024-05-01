import pygame
import random
import math
import threading
class Board:
    def __init__(self, width, height, kill, live) -> None:
        self.width = width
        self.height = height
        self.kill = kill
        self.live = live
        self.size = None;
        self.container = []
        self.changed = []
        for x in range (0, width):
            self.container.append([])
            for y in range (0,height):
                self.container[x].append(random.choice([True,False]))
        for x in range (0, width):
            self.changed.append([])
            for y in range (0,height):
                self.changed[x].append(False)
                
    def prepare_draw(self, size):
        # A thread worker function to determine what needs to be drawn
        def draw_worker(x_start, x_end, draw_operations):
            for i in range(x_start, x_end):
                for j, cell in enumerate(self.container[i]):
                    if self.changed[i][j]:
                        color = (255, 255, 255) if cell else (0, 0, 0)
                        rect = pygame.Rect(i*size, j*size, size, size)
                        draw_operations.append((color, rect))
                        self.changed[i][j] = False

        self.size = size
        draw_operations = []
        threads = []

        # Determine the number of threads to use (e.g., number of processors)
        num_threads = 5000
        step = self.width // num_threads

        # Start threads
        for n in range(num_threads):
            x_start = n * step
            x_end = self.width if n == num_threads - 1 else (n + 1) * step
            thread = threading.Thread(target=draw_worker, args=(x_start, x_end, draw_operations))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        return draw_operations

    def draw(self, window, size):
        draw_operations = self.prepare_draw(size)
        for color, rect in draw_operations:
            pygame.draw.rect(window, color, rect)

    def count_neighboring_true(self, row_index, col_index):
        count = 0
        for i in range(row_index-1, row_index+2):
            for j in range(col_index-1, col_index+2):
                # Wrapping around for edge cases
                wrapped_i = i % self.width
                wrapped_j = j % self.height
                if self.container[wrapped_i][wrapped_j] and (wrapped_i != row_index or wrapped_j != col_index):
                    count += 1
        return count

    def screenToCell(self, screenPos):
        x = math.floor(screenPos[0]/self.size)
        y = math.floor(screenPos[1]/self.size)
        return (x, y)
    
    def toggle(self, screenPos):
        pos = self.screenToCell(screenPos)
        self.container[pos[0]][pos[1]] = not self.container[pos[0]][pos[1]]
        self.changed[pos[0]][pos[1]] = True
    
    def update(self):
        def worker(x_start, x_end, tempContainer):
            for i in range(x_start, x_end):
                for j in range(self.height):
                    tempContainer[i][j] = self.processCell(i, j, self.container[i][j])

        tempContainer = [[self.container[x][y] for y in range(self.height)] for x in range(self.width)]
        threads = []

        # Determine the number of threads to use (e.g., number of processors)
        num_threads = 4
        step = self.width // num_threads

        # Start threads
        for n in range(num_threads):
            x_start = n * step
            x_end = self.width if n == num_threads - 1 else (n + 1) * step
            thread = threading.Thread(target=worker, args=(x_start, x_end, tempContainer))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        self.container = tempContainer
                
    def processCell(self, i,j, cell):
        count = self.count_neighboring_true(i, j)
        count -= 1
        result = None
        if count in self.kill:
            result = False
        if count in self.live:
            result = True
        if result != None and result != cell:
            self.changed[i][j] = True
            return result
        else:
            return self.container[i][j]