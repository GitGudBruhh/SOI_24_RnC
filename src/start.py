import numpy as np
import pygame
import threading
import socket
import time
from drawutils import *

from setupdata import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STRIP_WIDTH,
    ROBOT_LENGTH, ROBOT_WIDTH, INIT_ANGLE,
    MAZE_FILE_NAME)

import setupdata

from robot import Robot
from robotmotion import RobotMotion
from mazemap import maze_array
from robotinterface import motor_drive_inputs_receiver, sensor_vals_sender

def begin_simulation():    
# --------------------------------------------------------------------------------
# Initialize the pygame objects and screen
# --------------------------------------------------------------------------------
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('', 22)
    setupdata.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    map_image = pygame.image.load(MAZE_FILE_NAME).convert()
    
    screen_midpoint = np.array([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])
    
    # Variable used to add to corner offsets array to get 4 corners array
    corners_on_screen_midpoint_base = np.array([screen_midpoint]*4)
    
    # time.sleep(1)
    
# --------------------------------------------------------------------------------
# Determine the start pos
# --------------------------------------------------------------------------------
    start_pos: np.ndarray
    
    is_start_pos_found = False
    for row in maze_array:
        if 'S' in row:
            start_pos = np.array([row.index('S'), maze_array.index(row)])
            print(f"[SIM] Robot starts at {start_pos}")
            
            if(not is_start_pos_found):
                is_start_pos_found = True
            else:
                print(f"[SIM] Multiple start positions found")
                return
            
    if not is_start_pos_found:
        print(f"[SIM] Start position has not been provided")
        return

    # Temp variable used once to center the robot onto the path at the start
    offset_center_to_path = np.array([STRIP_WIDTH/2, STRIP_WIDTH/2])

# --------------------------------------------------------------------------------
# Create the robot object (Dimensions, start position, Direction facing)
# --------------------------------------------------------------------------------
    
    base_image = pygame.image.load('robot.jpg')
    base_image = pygame.transform.scale(base_image, (ROBOT_WIDTH, ROBOT_LENGTH))
    
    setupdata.my_rob = Robot((ROBOT_LENGTH, ROBOT_WIDTH),
                   STRIP_WIDTH*start_pos + offset_center_to_path, INIT_ANGLE)
    robot_motion = RobotMotion(setupdata.signal_list, (ROBOT_LENGTH, ROBOT_WIDTH))
    
    print("[SIM] Waiting for client to connect...")
    while(not setupdata.is_sender_active and not setupdata.is_receiver_active):
        time.sleep(0.5)
    
    init_time = pygame.time.get_ticks()
    print(f"[SIM] Simulation began at time {init_time}")

    clock = pygame.time.Clock()
    running = True
    
    while running:

        setupdata.screen.fill((255, 255, 255))  # Fill background

        elapsed_time = clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                setupdata.simulation_complete = True

    # --------------------------------------------------------------------------------
    # 1.
    # Drawing the map and writing data on screen
    # --------------------------------------------------------------------------------

        setupdata.screen.blit(map_image, screen_midpoint - setupdata.my_rob.current_pos)

        text_surface = my_font.render(
            "Time elapsed: " + str(pygame.time.get_ticks()), False, (0, 0, 0))
        setupdata.screen.blit(text_surface, (SCREEN_WIDTH/12, 0))
        txt_s = my_font.render(
            "Speed: " + str(int(setupdata.my_rob.current_speed)), False, (0, 0, 0))
        setupdata.screen.blit(txt_s, (SCREEN_WIDTH/3, 0))
        txt_s = my_font.render(
            "Dist: " + str(int(setupdata.my_rob.dist_travelled)), False, (0, 0, 0))
        setupdata.screen.blit(txt_s, (SCREEN_WIDTH/2, 0))
        txt_s = my_font.render(
            "Sensor vals: " + str(setupdata.my_rob.sensor_vals), False, (0, 0, 0))
        setupdata.screen.blit(txt_s, (6*SCREEN_WIDTH/8, 0))
        
    # --------------------------------------------------------------------------------
    # 2.
    # Updating signals and sensor values (DO NOT CHANGE THE ORDER OF DRAWING)
    # --------------------------------------------------------------------------------


        robot_motion.update_signals(tuple(setupdata.signal_list))
        robot_motion.accel_decel(elapsed_time)

        robot_corners_on_screen = corners_on_screen_midpoint_base + setupdata.my_rob.corner_offsets

        setupdata.my_rob.get_sensor_vals(setupdata.screen, robot_corners_on_screen)

        # !!!!!!!!!!!!!!!!!
        # DO NOT TOUCH THIS
        # !!!!!!!!!!!!!!!!!
        setupdata.my_rob.set_speed(robot_motion.get_speed())
        setupdata.my_rob.set_ang_vel(robot_motion.get_ang_vel())
        setupdata.my_rob.update_pos(elapsed_time/1000,
                          robot_motion.radius_of_rotation_div_w)
        # !!!!!!!!!!!!!!!!!
        # DO NOT TOUCH THIS 
        # !!!!!!!!!!!!!!!!! 
    
    # --------------------------------------------------------------------------------
    # 3.
    # Drawing the robot and its sensors
    # --------------------------------------------------------------------------------
    
        setupdata.ROBOT_IMAGE = pygame.transform.rotozoom(base_image, setupdata.my_rob.angle * 180/np.pi - 90, 1)

        draw_robot(setupdata.screen, robot_corners_on_screen, setupdata.my_rob.direction_unit_vec)

        # if (type(setupdata.my_rob.centre_of_rot) == np.ndarray):
        #     pygame.draw.circle(
        #         setupdata.screen, (255, 0, 255), setupdata.my_rob.centre_of_rot - setupdata.my_rob.current_pos + screen_midpoint, 3)

        sensor_colors = [(50, 50, 50), (50, 50, 50), (50, 50, 50), (50, 50, 50), (50, 50, 50)]
        if (setupdata.my_rob.sensor_vals[0] == 1):
            sensor_colors[0] = (255, 255, 0)
        if (setupdata.my_rob.sensor_vals[1] == 1):
            sensor_colors[1] = (255, 255, 0)
        if (setupdata.my_rob.sensor_vals[2] == 1):
            sensor_colors[2] = (255, 255, 0)
        if (setupdata.my_rob.sensor_vals[3] == 1):
            sensor_colors[3] = (255, 255, 0)
        if (setupdata.my_rob.sensor_vals[4] == 1):
            sensor_colors[4] = (255, 255, 0)
            
        draw_sensors(setupdata.screen, sensor_colors, robot_corners_on_screen, setupdata.my_rob.direction_unit_vec)

    # --------------------------------------------------------------------------------
    # 4.
    # Flipping the display to make it visible to player
    # --------------------------------------------------------------------------------
    
        pygame.display.flip()

        pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')
            
        clock.tick(60)

    pygame.quit()
    return

t3 = threading.Thread(name='simulator', 
                      target=begin_simulation)
t1 = threading.Thread(name='motor_drive_inputs_receiver',
                      target=motor_drive_inputs_receiver)
t2 = threading.Thread(name='sensor_vals_sender',
                      target=sensor_vals_sender)

t3.start()
t1.start()
t2.start()

t3.join()
t1.join()
t2.join()

exit()
