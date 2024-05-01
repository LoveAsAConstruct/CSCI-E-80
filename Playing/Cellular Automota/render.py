import pygame
import numpy as np
import cv2
from cells import Board
# Initialize Pygame
pygame.init()

# Define your parameters (e.g., CELLDIMENSIONS, growthParameter, lifeParameter, etc.)
# Initialize your board or whatever you're rendering (assuming it's called 'board')

# Set up Pygame window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

CELLDIMENSIONS = (5000, 5000,1)

# Set up variables
paused = False
step = 0
frame_count = 0
frames = []

running = True 
paused = False
board = Board(CELLDIMENSIONS[0], CELLDIMENSIONS[1], [4], [1,2])
growthParameter = [[4], [2,3]]
lifeParameter = [[1,4], [3]]
step = 0
# Main loop
while step < 500:
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

    window.fill((0, 0, 0))  # Clear the screen with black
    board.draw(window, CELLDIMENSIONS[2])
    if not paused:
        board.update()

    # Update and draw agents with mouse interaction
    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pressed:
        board.toggle(mouse_pos)
        # board.draw(window, CELLDIMENSIONS[2])

    # Convert pygame surface to numpy array
    frame = pygame.surfarray.array3d(window)
    frame = np.rot90(frame)  # Rotate frame
    frames.append(frame)

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 frames per second

# Convert frames list to video using OpenCV
height, width, _ = frames[0].shape
video_path = '/Users/isaiahmurray/Documents/CSCI E-80/Playing/Cellular Automota/output2.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(video_path, fourcc, 60, (width, height))

for frame in frames:
    video_writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

video_writer.release()

# Quit Pygame
pygame.quit()
