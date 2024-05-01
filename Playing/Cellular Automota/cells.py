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
                
    def draw(self, window, size):
        self.size = size
        for i,row in enumerate(self.container):
            for j,cell in enumerate(row):
                if self.changed[i][j]:
                    color = (0,0,0)
                    if cell:
                        color = (255,255,255)
                    pygame.draw.rect(window, color, pygame.Rect(i*size,j*size,size,size))
                    self.changed[i][j] = False

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
        threads = []
        tempContainer = []
        for x in range (0, self.width):
            tempContainer.append([])
            for y in range (0,self.height):
                tempContainer[x].append(self.container[x][y])
        for i,row in enumerate(self.container):
            for j,cell in enumerate(row):
                tempContainer[i][j] = self.processCell(i,j, cell)
                """
                if len(threads) > 1:
                    for thread in threads:
                        thread.start()
                    for thread in threads:
                        thread.join()
                    threads = []
                threads.append(threading.Thread(target=self.processCell, args=(i,j)))  
                """                
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