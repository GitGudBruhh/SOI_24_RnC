import numpy as np
import pygame
from robot import *
from robotinterface import *
from mazemap import *

SCREEN_WIDTH = 1600#1400
SCREEN_HEIGHT = 1200 #780
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
signal_list = [[100, False, True], [100, True, False]]
robot_interface = RobotInterface(signal_list, (ROBOT_LENGTH, ROBOT_WIDTH))

# Initialize the pygame objects and screen
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Roboto', 30)

clock = pygame.time.Clock()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
running = True

while running:

    screen.fill((200, 200, 200)) #Fill background

    elapsed_time = clock.get_time()

    ######################################################################################################################
    # 1.
    # Drawing the path on screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Choosing j, i (position of block) and filling it in if it's a strip
    for j in range(len(map_array)):
        row = map_array[j]
        for i in range(len(row)):
            block_pos = (i*strip_width, j*strip_width) #Get block position
            if(row[i] in '─,│,┐,┘,└,┌,┬,┤,┴,├,┼'):
                pygame.draw.rect(screen, (0, 0, 0), block_pos + (strip_width, strip_width)) # Draw the path at block_pos
            elif row[i] == 'S':
                pygame.draw.rect(screen, (200, 200, 0), block_pos + (strip_width, strip_width)) # Draw start state
            elif row[i] == 'G':
                pygame.draw.rect(screen, (0, 200, 0), block_pos + (strip_width, strip_width)) # Draw goal state

    my_rob.get_sensor_vals(screen)

    text_surface = my_font.render("Time elapsed: " + str(pygame.time.get_ticks()), False, (0, 0, 0))
    screen.blit(text_surface, (300,0))
    txt_s = my_font.render("Speed: " + str(my_rob.current_speed), False, (0, 0, 0))
    screen.blit(txt_s, (600,0))
    txt_s = my_font.render("Angular velocity: " + str(my_rob.current_angular_velocity), False, (0, 0, 0))
    screen.blit(txt_s, (800,0))
    txt_s = my_font.render("Sensor vals: " + str(my_rob.sensor_vals), False, (0, 0, 0))
    screen.blit(txt_s, (1100,0))

    ########################################################################################################################
    # 2.
    # Updating signals and sensor values (DO NOT CHANGE THE DRAW ORDER)

    ##################################################
    # !!!!!TODO!!!!!
    # signal_list = getSignalsFromFileOrSharedMemory()
    ##################################################

    robot_interface.update_signals(tuple(signal_list))
    robot_interface.accel_decel(elapsed_time)

    # !!!!!!!!!!!!!!!!! ####################################################################
    # DO NOT TOUCH THIS ####################################################################
    my_rob.set_speed(robot_interface.get_speed())                                        ###
    my_rob.set_ang_vel(robot_interface.get_ang_vel())                                    ###
    # my_rob.update_pos(elapsed_time/1000)                                                 ###
    # my_rob.update_angle(elapsed_time/1000, robot_interface.radius_of_rotation_div_w)     ###
    my_rob.update_pos(elapsed_time/1000, robot_interface.radius_of_rotation_div_w)
    # DO NOT TOUCH THIS ####################################################################
    # !!!!!!!!!!!!!!!!! ####################################################################

    # DEBUG ####################################################
    my_rob.get_sensor_vals(screen)
    if(my_rob.sensor_vals[0] == 0 and my_rob.sensor_vals[1] == 0):
        signal_list = [[255, False, True], [255, False, True]]
    # END DEBUG #################################################

    ########################################################################################################################
    # 3.
    # Drawing the robot pulygon and wheels
    pygame.draw.polygon(screen, (0, 100, 10), my_rob.corners, width=0)
    for c_idx in range(4):
        if c_idx < 2:
            pygame.draw.circle(screen, (255, 255, 0), my_rob.corners[c_idx], 5)
        else:
            pygame.draw.circle(screen, (0, 0, 0), my_rob.corners[c_idx], 5)

    pygame.draw.circle(screen, (0, 0, 0), my_rob.wheel_pos[0], 5)
    pygame.draw.circle(screen, (0, 0, 0, 0), my_rob.wheel_pos[1], 5)
    pygame.draw.circle(screen, (255, 0, 0), my_rob.current_pos, 3)
    pygame.draw.circle(screen, (0, 0, 0), my_rob.current_pos + 30*my_rob.direction_unit_vec, 3)
    if(type(my_rob.centre_of_rot) == np.ndarray):
        pygame.draw.circle(screen, (255, 0, 0), my_rob.centre_of_rot, 3)
    pygame.display.flip()

    pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')
    clock.tick(60)

pygame.quit()
