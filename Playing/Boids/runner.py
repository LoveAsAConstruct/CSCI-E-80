import pygame
import sys
import random
import math
from tools import *
from boidAgent import Agent;


WIDTH = 800
HEIGHT = 800
CELLSIZE = 25
# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()


# Number of agents
num_agents = 100

# Initialize a list to hold all agents
agents = [Agent((random.uniform(0, 800), random.uniform(0, 800)), (random.uniform(-2,2), random.uniform(-2,2))) for _ in range(num_agents)]

# Window configuration
window_size = (WIDTH, WIDTH)  # Width, Height
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Agent Simulation")

# Set the background color
background_color = (100, 100, 100)  # RGB for black
def posToCell(x):
    pos = math.floor(x/CELLSIZE)
    if(pos < 0):
        return 0
    if(pos > WIDTH/CELLSIZE):
        return math.floor(x/CELLSIZE)
    return pos


# Initialize containers grid
containers = [[[] for _ in range(math.floor(HEIGHT/CELLSIZE) + 1)] for _ in range(math.floor(WIDTH/CELLSIZE) + 1)]



def get_adjacent_indices(x, y):
    """Get indices of adjacent cells including diagonals, ensuring they are within bounds."""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    max_x, max_y = len(containers), len(containers[0])
    adjacent_indices = [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < max_x and 0 <= y + dy < max_y]
    return adjacent_indices

# Initialize Pygame and create a window
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()  # For controlling the frame rate

running = True
paused = False;
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            paused = not paused

    window.fill((0, 0, 0))  # Clear the screen with black

    # Update and draw agents with mouse interaction
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    
    # Assign agents to containers based on their positions
    containers = [[[] for _ in range(math.floor(HEIGHT/CELLSIZE) + 1)] for _ in range(math.floor(WIDTH/CELLSIZE) + 1)]
    # Define container dimensions
    container_width = len(containers)
    container_height = len(containers[0]) if container_width > 0 else 0  # Assuming all rows have the same length

    for agent in agents:
        x, y = (posToCell(agent.position[0]),posToCell(agent.position[1]))
        # Check if agent is within container bounds
        if 0 <= x < container_width and 0 <= y < container_height:
            containers[x][y].append(agent)
        else:
            print("Agent is out of bounds and cannot be appended to the container.")
    for x in range(len(containers)):
        for y in range(len(containers[x])):
            # Collect all agents from the current cell and adjacent cells
            agents_to_update = [agent for agent in containers[x][y]]
            for ax, ay in get_adjacent_indices(x, y):
                agents_to_update.extend(containers[ax][ay])
                
            
            # Update and draw each agent in the current cell
            for agent in containers[x][y]:
                if not paused:
                    agent.update(agents_to_update,window)
                agent.draw(window)
                
                # Mouse interaction for agent velocity modification
                scalar = (100 - math.dist(mouse_pos, agent.position))/100
                if mouse_pressed[0] and math.dist(mouse_pos, agent.position) < 100:  # Left mouse button
                    agent.velocity = tadd(tmult(tnrml(tsub(agent.position,mouse_pos)),(scalar,scalar)),agent.velocity)
                elif mouse_pressed[2] and math.dist(mouse_pos, agent.position) < 100:  # Right mouse button
                    agent.velocity = tadd(tmult(tnrml(tsub(mouse_pos,agent.position)),(1-scalar,1-scalar)),agent.velocity)

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 frames per second

pygame.quit()