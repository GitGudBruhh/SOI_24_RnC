import numpy as np
import pygame
from robot import *
from robotdata import *
from mazemap import *

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1200
strip_width = 15 #1.5cm

ROBOT_WIDTH = 80 #8cm
ROBOT_LENGTH = 80 #8cm
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
path_offset = np.array([strip_width/2, strip_width/2])

# Create the robot object (Dimensions, start position, Direction facing)
my_rob = Robot((ROBOT_LENGTH, ROBOT_WIDTH), strip_width*start_pos + path_offset, np.pi/2)
robot_interface = RobotData(0, 10)

# Initialize the pygame objects and screen
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Roboto', 30)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
running = True

rob_image = pygame.image.load('black.jpg')

rob_image_point = pygame.transform.scale(rob_image, (3, 3))
rob_image_wheel = pygame.transform.scale(rob_image, (10, 50))

# Time start and time end keep track of time elapsed in a loop
# Used for rendering time onto screen
# Also used for movement of robot
time_start = 0
time_end = 0
while running:
    screen.fill((200, 200, 200)) #Fill background
    time_start = time_end
    time_end = pygame.time.get_ticks()

    text_surface = my_font.render("Time elapsed: " + str(pygame.time.get_ticks()), False, (0, 0, 0))
    screen.blit(text_surface, (300,0))
    txt_s = my_font.render("Speed: " + str(my_rob.current_speed), False, (0, 0, 0))
    screen.blit(txt_s, (600,0))
    txt_s = my_font.render("Angular velocity: " + str(my_rob.current_angular_velocity), False, (0, 0, 0))
    screen.blit(txt_s, (800,0))
    txt_s = my_font.render("Sensor vals: " + str(my_rob.sensor_vals), False, (0, 0, 0))
    screen.blit(txt_s, (1100,0))


    my_rob.set_speed(robot_interface.get_speed())
    my_rob.set_ang_vel(robot_interface.get_ang_vel())
    my_rob.update_pos((time_end - time_start)/1000)
    my_rob.update_angle((time_end - time_start)/1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # DEBUG ##################################################
    s_vals = my_rob.get_sensor_vals(screen)
    if(s_vals[0] == 0):
        if(robot_interface.get_ang_vel() == 10):
            robot_interface.set_ang_vel(0)

    robot_interface.accel_decel(time_end - time_start)
    # END DEBUG #################################################

    pygame.draw.polygon(screen, (0, 0, 255), my_rob.corners, width=3)
    for c_idx in range(4):
        if c_idx < 2:
            pygame.draw.circle(screen, (255, 255, 0), my_rob.corners[c_idx], 5)
        else:
            pygame.draw.circle(screen, (0, 0, 0), my_rob.corners[c_idx], 5)
    pygame.draw.circle(screen, (0, 0, 0), my_rob.wheel_pos[0], 5)
    pygame.draw.circle(screen, (0, 0, 0, 0), my_rob.wheel_pos[1], 5)
    pygame.draw.circle(screen, (255, 0, 0), my_rob.current_pos, 3)
    pygame.draw.circle(screen, (0, 0, 0), my_rob.current_pos + 30*my_rob.direction_unit_vec, 3)
    pygame.display.flip()

pygame.quit()
