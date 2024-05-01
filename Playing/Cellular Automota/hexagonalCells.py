import pygame
import random
import math

class HexagonalBoard:
    def __init__(self, width, height, kill, live) -> None:
        self.width = width
        self.height = height
        self.kill = kill
        self.live = live
        self.size = None
        self.container = []
        self.changed = []

        # Initialize the board with random True/False values
        for x in range(width):
            self.container.append([])
            for y in range(height):
                self.container[x].append(random.choice([True, False]))

        for x in range(width):
            self.changed.append([])
            for y in range(height):
                self.changed[x].append(False)

        
    def draw(self, window, size):
        self.size = size
        # Calculate vertical and horizontal distances based on hexagon size
        vertical_distance = size * math.sqrt(3)
        horizontal_distance = size * 3/2

        for i, row in enumerate(self.container):
            for j, cell in enumerate(row):
                if self.changed[i][j]:
                    color = (0, 0, 0) if cell else (255, 255, 255)
                    # Calculate the center position for the hexagon
                    x = j * horizontal_distance
                    y = i * vertical_distance
                    # Apply an offset for every other column
                    if j % 2 == 1:
                        y += vertical_distance / 2
                    
                    # Round positions to avoid rendering cracks due to floating-point precision issues
                    x = round(x)
                    y = round(y)

                    self.draw_hexagon(window, (x, y), size, color)
                    self.changed[i][j] = False

    def draw_hexagon(self, surface, center, size, color):
        # Calculate the vertices of the flat-topped hexagon
        points = []
        for i in range(6):
            # Start at 30 degrees for a flat-topped hexagon
            angle_deg = 60 * i + 30
            angle_rad = math.radians(angle_deg)
            point = (center[0] + size * math.cos(angle_rad),
                    center[1] + size * math.sin(angle_rad))
            points.append(point)
        pygame.draw.polygon(surface, color, points)

    def count_neighboring_true(self, row_index, col_index):
        count = 0
        # Offsets for the six neighbors of a hexagon
        neighbor_offsets = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
        if row_index % 2 == 1:
            neighbor_offsets = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1)]

        for dx, dy in neighbor_offsets:
            wrapped_i = (row_index + dx) % self.width
            wrapped_j = (col_index + dy) % self.height
            if self.container[wrapped_i][wrapped_j]:
                count += 1

        return count

    def screenToCell(self, screenPos):
        x, y = screenPos
        row = int(x / (self.size * 3/4))
        col = int((y - (row % 2) * self.size / 2) / self.size)
        return (row, col)

    def toggle(self, screenPos):
        pos = self.screenToCell(screenPos)
        self.container[pos[0]][pos[1]] = not self.container[pos[0]][pos[1]]
        self.changed[pos[0]][pos[1]] = True

    def update(self):
        tempContainer = [[self.container[x][y] for y in range(self.height)] for x in range(self.width)]
        for i, row in enumerate(self.container):
            for j, cell in enumerate(row):
                tempContainer[i][j] = self.processCell(i, j, cell)
        self.container = tempContainer

    def processCell(self, i, j, cell):
        count = self.count_neighboring_true(i, j)
        result = cell
        if cell and count in self.kill:
            result = False
        elif not cell and count in self.live:
            result = True
        if result != cell:
            self.changed[i][j] = True
        return result
