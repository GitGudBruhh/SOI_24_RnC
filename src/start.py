import numpy as np
import pygame
import csv
import copy
import threading
import socket
import time

from robot import *
from robotinterface import *
from mazemap import *

SCREEN_WIDTH = 1600#1400
SCREEN_HEIGHT = 1200 #780
strip_width =  15 #1.5cm

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65433  # The port used by the server

ROBOT_WIDTH = 80 #8cm
ROBOT_LENGTH = 80 #8cm

signal_list = [[0, False, False], [0, False, False]]
my_rob = None
screen = None

SIMULATION_COMPLETE = False
##########################
# SCALE: 1cm = 10px
##########################

def socket_worker_sender(conn, addr):
    global signal_list
    global my_rob
    global screen
    global SIMULATION_COMPLETE

    with conn:
        print(f"Connected by {addr}")
        while True:

            if(SIMULATION_COMPLETE):
                conn.close()
                return

            data = conn.recv(1024)

            if not data:
                break

            string_data = data.decode('ascii')
            signals = string_data.split('|')

            for idx in range(len(signals)):
                signals[idx] = signals[idx].split(',')
                signals[idx][0] = int(signals[idx][0])
                signals[idx][1] = bool(int(signals[idx][1]))
                signals[idx][2] = bool(int(signals[idx][2]))

            signal_list = copy.deepcopy(signals[0:2])

def socket_worker_reciever():
    global my_rob
    global screen
    global SIMULATION_COMPLETE

    prev_data = b''

    with conn:
        while True:
            time.sleep(0.1)

            if(SIMULATION_COMPLETE):
                conn.close()
                return

            if(not my_rob == None and not screen == None):
                sensor_vals = copy.copy(my_rob.sensor_vals)
                sensor_vals[0] = str(int(sensor_vals[0]))
                sensor_vals[1] = str(int(sensor_vals[1]))

                current_data = (','.join(sensor_vals)).encode()

                if(not current_data == prev_data):
                    conn.sendall(current_data)
                    prev_data = current_data


def begin_simulation():
    # Determine the start pos
    start_pos = (0, 0)
    for row in map_array:
        if 'S' in row:
            start_pos = np.array([row.index('S'), map_array.index(row)])
            print(f"Robot starts at {start_pos}")

    # Temp variable Used once to center the robot onto the path at the start
    path_offset = np.array([strip_width/2, strip_width/2])

    global signal_list
    global my_rob
    global screen
    global SIMULATION_COMPLETE

    # Create the robot object (Dimensions, start position, Direction facing)
    my_rob = Robot((ROBOT_LENGTH, ROBOT_WIDTH), strip_width*start_pos + path_offset, 0)
    robot_interface = RobotInterface(signal_list, (ROBOT_LENGTH, ROBOT_WIDTH))

    # Initialize the pygame objects and screen
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('Roboto', 30)

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    map_image = pygame.image.load('map.png').convert()

    running = True

    block_size = (strip_width, strip_width)
    screen_midpoint = np.array([SCREEN_WIDTH/2, SCREEN_HEIGHT/2])

    while running:

        screen.fill((200, 200, 200)) #Fill background

        elapsed_time = clock.get_time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                SIMULATION_COMPLETE = True
                
        ####################################################################################################################

        # 1.
        # Drawing the map and data on screen
        
        screen.blit(map_image, screen_midpoint - my_rob.current_pos)

        text_surface = my_font.render("Time elapsed: " + str(pygame.time.get_ticks()), False, (0, 0, 0))
        screen.blit(text_surface, (300,0))
        txt_s = my_font.render("Speed: " + str(int(my_rob.current_speed)), False, (0, 0, 0))
        screen.blit(txt_s, (600,0))
        txt_s = my_font.render("Dist: " + str(int(my_rob.dist_travelled)), False, (0, 0, 0))
        screen.blit(txt_s, (800,0))
        txt_s = my_font.render("Sensor vals: " + str(my_rob.sensor_vals), False, (0, 0, 0))
        screen.blit(txt_s, (1100,0))

        ####################################################################################################################

        # 2.
        # Updating signals and sensor values (DO NOT CHANGE THE DRAW ORDER)

        robot_interface.update_signals(tuple(signal_list))
        robot_interface.accel_decel(elapsed_time)
        
        tmp = np.array([screen_midpoint, screen_midpoint])
        robot_corners_on_screen = list(tmp + my_rob.corner_offsets) + list(tmp - my_rob.corner_offsets)
        
        my_rob.get_sensor_vals(screen, robot_corners_on_screen)


        # !!!!!!!!!!!!!!!!! ####################################################################
        # DO NOT TOUCH THIS ####################################################################
        my_rob.set_speed(robot_interface.get_speed())                                        ###
        my_rob.set_ang_vel(robot_interface.get_ang_vel())                                    ###
        my_rob.update_pos(elapsed_time/1000, robot_interface.radius_of_rotation_div_w)       ###
        # DO NOT TOUCH THIS ####################################################################
        # !!!!!!!!!!!!!!!!! ####################################################################


        ####################################################################################################################

        # 3.
        # Drawing the robot polygon and wheels
        pygame.draw.polygon(screen, (0, 100, 10), robot_corners_on_screen, width=0)
        
#         for c_idx in range(4):
#             if c_idx < 2:
#                 pygame.draw.circle(screen, (255, 255, 0), my_rob.corners[c_idx], 5)
#             else:
#                 pygame.draw.circle(screen, (0, 0, 0), my_rob.corners[c_idx], 5)
#         
#         pygame.draw.circle(screen, (0, 0, 0), my_rob.wheel_pos[0], 8)
#         pygame.draw.circle(screen, (0, 0, 0, 0), my_rob.wheel_pos[1], 8)
#         pygame.draw.circle(screen, (255, 0, 0), my_rob.current_pos, 3)
#         pygame.draw.circle(screen, (0, 0, 0), my_rob.current_pos + 30*my_rob.direction_unit_vec, 3)

        if(type(my_rob.centre_of_rot) == np.ndarray):
            pygame.draw.circle(screen, (255, 0, 255), my_rob.centre_of_rot - my_rob.current_pos + screen_midpoint, 3)

        sensor_colors = [(50,50,50), (50,50,50)]
        if(my_rob.sensor_vals[0] == 1):
            sensor_colors[0] = (255, 255, 0)
        if(my_rob.sensor_vals[1] == 1):
            sensor_colors[1] = (255, 255, 0)
            
        pygame.draw.circle(screen, sensor_colors[0], robot_corners_on_screen[0], 5)
        pygame.draw.circle(screen, sensor_colors[1], robot_corners_on_screen[1], 5)


        pygame.display.flip()

        pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')
        clock.tick(120)

        ####################################################################################################################

    pygame.quit()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

t1 = threading.Thread(name = 'socket_worker_s', target = socket_worker_sender, args = (conn, addr))
t2 = threading.Thread(name = 'socket_worker_r', target = socket_worker_reciever)
t3 = threading.Thread(name = 'simulator', target = begin_simulation)

t1.start()
t2.start()
t3.start()

t3.join()
t1.join()
t2.join()

exit()
