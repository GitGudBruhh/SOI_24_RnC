import numpy as np
import pygame
import threading
import socket
import time

from setupdata import (
    SCREEN_WIDTH, SCREEN_HEIGHT, STRIP_WIDTH, WHEEL_POS_RATIO,
    ROBOT_LENGTH, ROBOT_WIDTH, WHEEL_RADIUS)

import setupdata

from robot import Robot
from robotmotion import RobotMotion
from mazemap import maze_array
from robotinterface import motor_drive_inputs_receiver, sensor_vals_sender

##########################
# SCALE: 1cm = 10px
##########################

def begin_simulation():    
    # Initialize the pygame objects and screen
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('Roboto', 30)
    setupdata.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    map_image = pygame.image.load('map.png').convert()
    
    time.sleep(1)
    
    # Determine the start pos
    start_pos = (0, 0)
    s_count_checker = False
    for row in maze_array:
        if 'S' in row:
            start_pos = np.array([row.index('S'), maze_array.index(row)])
            print(f"[SIM] Robot starts at {start_pos}")
            
            if(not s_count_checker):
                s_count_checker = True
            else:
                print(f"[SIM] Multiple start positions found")
            
    if not s_count_checker:
        print(f"[SIM] Start position has not been provided")
        return

    # Temp variable used once to center the robot onto the path at the start
    path_offset = np.array([STRIP_WIDTH/2, STRIP_WIDTH/2])

    # Create the robot object (Dimensions, start position, Direction facing)
    setupdata.my_rob = Robot((ROBOT_LENGTH, ROBOT_WIDTH),
                   STRIP_WIDTH*start_pos + path_offset, 0)
    robot_motion = RobotMotion(setupdata.signal_list, (ROBOT_LENGTH, ROBOT_WIDTH))
    
    print("[SIM] Waiting for client to connect...")
    while(not setupdata.is_sender_active and not setupdata.is_receiver_active):
        pass
    
    init_time = pygame.time.get_ticks()
    print(f"[SIM] Simulation began at time {init_time}")

    clock = pygame.time.Clock()

    running = True

    block_size = (STRIP_WIDTH, STRIP_WIDTH)
    screen_midpoint = np.array([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])


    while running:

        setupdata.screen.fill((200, 200, 200))  # Fill background

        elapsed_time = clock.get_time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                setupdata.simulation_complete = True

        ####################################################################################################################

        # 1.
        # Drawing the map and data on screen

        setupdata.screen.blit(map_image, screen_midpoint - setupdata.my_rob.current_pos)

        text_surface = my_font.render(
            "Time elapsed: " + str(pygame.time.get_ticks()), False, (0, 0, 0))
        setupdata.screen.blit(text_surface, (300, 0))
        txt_s = my_font.render(
            "Speed: " + str(int(setupdata.my_rob.current_speed)), False, (0, 0, 0))
        setupdata.screen.blit(txt_s, (600, 0))
        txt_s = my_font.render(
            "Dist: " + str(int(setupdata.my_rob.dist_travelled)), False, (0, 0, 0))
        setupdata.screen.blit(txt_s, (800, 0))
        txt_s = my_font.render(
            "Sensor vals: " + str(setupdata.my_rob.sensor_vals), False, (0, 0, 0))
        setupdata.screen.blit(txt_s, (1100, 0))

        ####################################################################################################################

        # 2.
        # Updating signals and sensor values (DO NOT CHANGE THE DRAW ORDER)

        robot_motion.update_signals(tuple(setupdata.signal_list))
        robot_motion.accel_decel(elapsed_time)

        tmp = np.array([screen_midpoint, screen_midpoint])
        robot_corners_on_screen = list(
            tmp + setupdata.my_rob.corner_offsets) + list(tmp - setupdata.my_rob.corner_offsets)

        setupdata.my_rob.get_sensor_vals(setupdata.screen, robot_corners_on_screen)

        # !!!!!!!!!!!!!!!!! ####################################################################
        # DO NOT TOUCH THIS ####################################################################
        setupdata.my_rob.set_speed(robot_motion.get_speed())
        setupdata.my_rob.set_ang_vel(robot_motion.get_ang_vel())
        setupdata.my_rob.update_pos(elapsed_time/1000,
                          robot_motion.radius_of_rotation_div_w)
        # DO NOT TOUCH THIS ####################################################################
        # !!!!!!!!!!!!!!!!! ####################################################################

        ####################################################################################################################

        # 3.
        # Drawing the robot polygon and wheels
        perp_dir = (robot_corners_on_screen[1] - robot_corners_on_screen[0])/np.linalg.norm(
            (robot_corners_on_screen[1] - robot_corners_on_screen[0]))
        left_wheel_polygon = [(1 - WHEEL_POS_RATIO) * robot_corners_on_screen[0] + WHEEL_POS_RATIO * robot_corners_on_screen[3] + setupdata.my_rob.direction_unit_vec * WHEEL_RADIUS,
                              (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[0] + WHEEL_POS_RATIO * robot_corners_on_screen[3] + setupdata.my_rob.direction_unit_vec *WHEEL_RADIUS - perp_dir * 15,
                              (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[0] + WHEEL_POS_RATIO * robot_corners_on_screen[3] - setupdata.my_rob.direction_unit_vec *WHEEL_RADIUS - perp_dir * 15,
                              (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[0] + WHEEL_POS_RATIO * robot_corners_on_screen[3] - setupdata.my_rob.direction_unit_vec *WHEEL_RADIUS,
                              ]
        right_wheel_polygon = [(1 - WHEEL_POS_RATIO) * robot_corners_on_screen[1] + WHEEL_POS_RATIO * robot_corners_on_screen[2] + setupdata.my_rob.direction_unit_vec *WHEEL_RADIUS,
                               (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[1] + WHEEL_POS_RATIO * robot_corners_on_screen[2] + setupdata.my_rob.direction_unit_vec *WHEEL_RADIUS + perp_dir * 15,
                               (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[1] + WHEEL_POS_RATIO * robot_corners_on_screen[2] - setupdata.my_rob.direction_unit_vec *WHEEL_RADIUS + perp_dir * 15,
                               (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[1] + WHEEL_POS_RATIO * robot_corners_on_screen[2] - setupdata.my_rob.direction_unit_vec *WHEEL_RADIUS,
                               ]
        
        pygame.draw.polygon(setupdata.screen, (0, 150, 10), robot_corners_on_screen, width=0)
        pygame.draw.polygon(setupdata.screen, (50, 50, 50), robot_corners_on_screen, width=3)
        pygame.draw.polygon(setupdata.screen, (0, 0, 0), left_wheel_polygon, width=0)
        pygame.draw.polygon(setupdata.screen, (0, 0, 0), right_wheel_polygon, width=0)

        if (type(setupdata.my_rob.centre_of_rot) == np.ndarray):
            pygame.draw.circle(
                setupdata.screen, (255, 0, 255), setupdata.my_rob.centre_of_rot - setupdata.my_rob.current_pos + screen_midpoint, 3)

        sensor_colors = [(50, 50, 50), (50, 50, 50)]
        if (setupdata.my_rob.sensor_vals[0] == 1):
            sensor_colors[0] = (255, 255, 0)
        if (setupdata.my_rob.sensor_vals[1] == 1):
            sensor_colors[1] = (255, 255, 0)

        pygame.draw.circle(
            setupdata.screen, sensor_colors[0], robot_corners_on_screen[0], 5)
        pygame.draw.circle(
            setupdata.screen, sensor_colors[1], robot_corners_on_screen[1], 5)

        pygame.display.flip()

        pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')
            
        clock.tick(120)

        ####################################################################################################################

    pygame.quit()
    return

t3 = threading.Thread(name='simulator', 
                      target=begin_simulation)
t1 = threading.Thread(name='socket_worker_s',
                      target=motor_drive_inputs_receiver)
t2 = threading.Thread(name='socket_worker_r',
                      target=sensor_vals_sender)

t3.start()
t1.start()
t2.start()

t3.join()
t1.join()
t2.join()

exit()
