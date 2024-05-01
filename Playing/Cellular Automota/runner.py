import pygame
from cellsThreaded import Board
CELLDIMENSIONS = (1000, 1000,1)
WIDTH = int(CELLDIMENSIONS[0] * CELLDIMENSIONS[2])
HEIGHT = int(CELLDIMENSIONS[1] * CELLDIMENSIONS[2])

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()

# Window configuration
window_size = (WIDTH, HEIGHT)  # Width, Height
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Agent Simulation")

# Set the background color
background_color = (100, 100, 100)  # RGB for black

running = True 
paused = False
board = Board(CELLDIMENSIONS[0], CELLDIMENSIONS[1], [4], [1,2])
growthParameter = [[4], [2,3]]
lifeParameter = [[1,4], [3]]
step = 0
while running:
    step += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
    if step % 50 == 0:
        board.kill = growthParameter[0]
        board.live = growthParameter[1]
    if (step + 25) % 50 == 0:
        board.kill = lifeParameter[0]
        board.live = lifeParameter[1]
    #window.fill((0, 0, 0))  # Clear the screen with black
    board.draw(window, CELLDIMENSIONS[2])
    if not paused:
        board.update()
    # Update and draw agents with mouse interaction
    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pressed:
        board.toggle(mouse_pos)
        #board.draw(window, CELLDIMENSIONS[2])
    pygame.display.flip()  # Update the display
    clock.tick(10)  # Limit the frame rate to 60 frames per second

pygame.quit()