from mazemap import *
import pygame
import numpy as np
from setupdata import STRIP_WIDTH, MAZE_CHARSET

max_len = -1
strip_width = STRIP_WIDTH


for row in maze_array:
    if max_len < len(row):
        max_len = len(row)

SCREEN_WIDTH = max_len * strip_width  # 1400
SCREEN_HEIGHT = len(maze_array) * strip_width  # 780

running = True

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

running = True

block_size = (strip_width, strip_width)
screen_midpoint = np.array([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])

screen.fill((200, 200, 200))

for j in range(len(maze_array)):
    print(j)
    row = maze_array[j]

    for i in range(len(row)):
        # block_offset_from_rob = np.array([i*strip_width, j*strip_width])
        # block_pos =  tuple(screen_midpoint) #Get block position ON SCREEN
        block_pos = (i*strip_width, j*strip_width)

        if (block_pos[0] > SCREEN_WIDTH):
            continue
        if (block_pos[1] > SCREEN_HEIGHT):
            continue

        if (row[i] in MAZE_CHARSET):
            pygame.draw.rect(screen, (0, 0, 0), block_pos +
                             block_size)  # Draw the path at block_pos
        elif row[i] == 'S':
            pygame.draw.rect(screen, (200, 200, 0), block_pos +
                             block_size)  # Draw start state
        elif row[i] == 'G':
            pygame.draw.rect(screen, (0, 200, 0), block_pos +
                             block_size)  # Draw goal state

pygame.display.flip()
pygame.image.save(screen, "map.png")

pygame.quit()
