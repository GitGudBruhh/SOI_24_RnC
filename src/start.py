import numpy as np
import pygame
import threading
import socket
import time
from drawutils import *
import copy

from setupdata import (
    HOST,
    PORT1,
    PORT2,
    LOGLEVEL)

import setupdata

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
    drew_first = False
    
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
    
    init_time = pygame.time.get_ticks()
    print(f"[SIM] Simulation began at time {init_time}")

    clock = pygame.time.Clock()
    running = True
    
    setupdata.screen.fill((255, 255, 255))  # Fill background
    pygame.display.flip()
    
# --------------------------------------------------------------------------------
# Open receiver socket
# --------------------------------------------------------------------------------
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s1.bind((HOST, PORT1))
        s1.listen()
        conn1, addr1 = s1.accept()
        
    # --------------------------------------------------------------------------------
    # Set reciever active if client connects
    # --------------------------------------------------------------------------------
        setupdata.is_receiver_active = True
        print(f"[SIM] receiver(): Connected by {addr1}")

    # --------------------------------------------------------------------------------
    # Open sender socket
    # --------------------------------------------------------------------------------
        with conn1:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s2.bind((HOST, PORT2))
                s2.listen()
                conn2, addr2 = s2.accept()
                    
            # --------------------------------------------------------------------------------
            # Set sender active if client connects
            # --------------------------------------------------------------------------------
                setupdata.is_sender_active = True
                print(f"[SIM] sender(): Connected by {addr2}")
                prev_data = None
                
            # --------------------------------------------------------------------------------
            # Implement simulator logic here
            # --------------------------------------------------------------------------------
                with conn2:
                    while running:

                    # --------------------------------------------------------------------------------
                    # Receive, decode and convert the signals to a list
                    # --------------------------------------------------------------------------------
                        data = conn1.recv(32)

                        string_data = data.decode('ascii')
                        
                        signals = string_data.split('|')

                        for idx in range(len(signals)):
                            signals[idx] = signals[idx].split(',')
                            signals[idx][0] = int(signals[idx][0])
                            signals[idx][1] = bool(int(signals[idx][1]))
                            signals[idx][2] = bool(int(signals[idx][2]))
                    
                    # --------------------------------------------------------------------------------
                    # Update global signals used by simulator and send acknowledgement
                    # --------------------------------------------------------------------------------
                        setupdata.signal_list = copy.deepcopy(signals[0:2])
                        
                        conn1.send("MOTOR_INP_RECV_ACK".encode())
                        
                    # --------------------------------------------------------------------------------
                    # Print logs based on logging level
                    # --------------------------------------------------------------------------------
                        if LOGLEVEL[0] == 0:
                            pass
                        
                        elif LOGLEVEL[0] == 1:
                            if(not prev_string_data == string_data):
                                print(f"[SIM] receiver(): Recieved {string_data}")
                                prev_string_data = string_data

                        elif LOGLEVEL[0] == 2:
                            print(f"[SIM] receiver(): Recieved {string_data}")
                        
                        elif LOGLEVEL[0] == 3:
                            print(f"[SIM] receiver(): Recieved {string_data}")
                            print(f"[SIM] receiver(): Sent MOTOR_INP_RECV_ACK")
                        
            #########################################################################################################
            
                        if(setupdata.simulation_complete):
                            completion_ack = conn2.recv(32)
                            conn2.sendall("SIM_COMPLETE".encode())
                            setupdata.is_sender_active = False
                            break

                        request = conn2.recv(32)
                        
                    # --------------------------------------------------------------------------------
                    # Receive request and send current sensor values
                    # --------------------------------------------------------------------------------
                        if(request.decode() == "SENSOR_DATA_REQ"):
                            current_data = b'SENSOR_DATA_UNAVAIL'
                            
                            if(not setupdata.my_rob == None and not setupdata.screen == None):
                                sensor_vals = copy.copy(setupdata.my_rob.sensor_vals)
                                
                                for idx in range(len(sensor_vals)):
                                    sensor_vals[idx] = str(int(sensor_vals[idx]))

                                current_data = (','.join(sensor_vals)).encode()
                                
                            conn2.sendall(current_data)
                            
                    # --------------------------------------------------------------------------------
                    # Print logs based on logging level
                    # --------------------------------------------------------------------------------
                            if LOGLEVEL[1] == 0:
                                pass
                            elif LOGLEVEL[1] == 1:
                                if(not current_data == prev_data):
                                    prev_data = current_data

                                    print(f"[SIM] sender(): Sent {current_data}")
                                    

                            elif LOGLEVEL[1] == 2:
                                print(f"[SIM] sender(): Recieved request {request}")
                                print(f"[SIM] sender(): Sent {current_data}")
                
            #########################################################################################################

                        setupdata.screen.fill((255, 255, 255))  # Fill background

                        
                        elapsed_time = clock.get_time()
                        if(not drew_first):
                            elapsed_time = 0
                            drew_first = True

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
                            
                        draw_sensors(setupdata.screen, sensor_colors, robot_corners_on_screen)

                    # --------------------------------------------------------------------------------
                    # 4.
                    # Flipping the display to make it visible to player
                    # --------------------------------------------------------------------------------
                        pygame.display.flip()

                        pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')
                            
                        clock.tick(60)
                                
                    conn2.close()
                s2.close()
                
                data = conn1.recv(32)
                conn1.sendall("SIM_COMPLETE".encode())
                setupdata.is_receiver_active = False
                
                conn1.close()
            s1.close()

        pygame.quit()
        return

# t3 = threading.Thread(name='simulator', 
#                       target=begin_simulation)
# t1 = threading.Thread(name='motor_drive_inputs_receiver',
#                       target=motor_drive_inputs_receiver)
# t2 = threading.Thread(name='sensor_vals_sender',
#                       target=sensor_vals_sender)
# 
# t3.start()
# t1.start()
# t2.start()
# 
# t3.join()
# t1.join()
# t2.join()

begin_simulation()

exit()
