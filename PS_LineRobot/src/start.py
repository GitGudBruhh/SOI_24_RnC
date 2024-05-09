import numpy as np
import pygame
from robot import *
from robotdata import *
from mazemap import *

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1200
strip_width = 15 #1.5cm

ROBOT_WIDTH = 100 #10cm
ROBOT_LENGTH = 120 #12cm
##########################
# SCALE: 1cm = 10px
##########################

# Determine the start pos
start_pos = (0, 0)
for row in map_array:
    if 'S' in row:
        start_pos = np.array([row.index('S'), map_array.index(row)])
        print(start_pos)

# Temp variable Used once to center the robot onto the path at the start
path_offset = np.array([strip_width/2 - 2, strip_width/2])

# Create the robot object (Dimensions, start position, Direction facing)
my_rob = Robot((ROBOT_LENGTH, ROBOT_WIDTH), strip_width*start_pos + path_offset, np.pi/2)
robot_interface = RobotData(0, 0)

# Initialize the pygame objects and screen
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Roboto', 30)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
running = True

rob_image = pygame.image.load('black.jpg')

rob_image_point = pygame.transform.scale(rob_image, (3, 3))
rob_image_wheel = pygame.transform.scale(rob_image, (5, 5))

# Time start and time end keep track of time elapsed in a loop
# Used for rendering time onto screen
# Also used for movement of robot
time_start = 0
time_end = 0
while running:
    time_start = time_end
    time_end = pygame.time.get_ticks()
    text_surface = my_font.render(str(pygame.time.get_ticks()), False, (0, 0, 0))

    my_rob.set_speed(robot_interface.get_speed())
    my_rob.set_ang_vel(robot_interface.get_ang_vel())
    my_rob.update_pos((time_end - time_start)/1000)
    my_rob.update_angle((time_end - time_start)/1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255)) #Fill background

    # Choosing j, i (position of block) and filling it in if it's a strip
    for j in range(len(map_array)):
        row = map_array[j]
        for i in range(len(row)):
            block_pos = (i*strip_width, j*strip_width) #Get block position
            if(row[i] in '─,│,┐,┘,└,┌,┬,┤,┴,├,┼'):
                pygame.draw.rect(screen, (100, 100, 100), block_pos + (strip_width, strip_width)) # Draw the path at block_pos
            elif row[i] == 'S':
                pygame.draw.rect(screen, (200, 200, 0), block_pos + (strip_width, strip_width)) # Draw start state
            elif row[i] == 'G':
                pygame.draw.rect(screen, (0, 200, 0), block_pos + (strip_width, strip_width)) # Draw goal state

    # TWO WHEELED ROBOT
    screen.blit(rob_image_point, my_rob.corners[0])
    screen.blit(rob_image_point, my_rob.corners[1])
    screen.blit(rob_image_point, my_rob.corners[2])
    screen.blit(rob_image_point, my_rob.corners[3])

    screen.blit(rob_image_wheel, my_rob.wheel_pos[0])
    screen.blit(rob_image_wheel, my_rob.wheel_pos[1])

    screen.blit(rob_image_point, my_rob.current_pos)
    screen.blit(rob_image_wheel, my_rob.current_pos + 30*my_rob.direction_unit_vec)
    screen.blit(text_surface, (500,0))
    pygame.display.flip()

pygame.quit()
