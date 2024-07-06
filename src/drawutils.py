import numpy as np
import pygame
import random
from setupdata import WHEEL_POS_RATIO, WHEEL_RADIUS, PATH_SENSOR_POS_RATIO
import setupdata


def create_rectangle(perp_vector, dir_vector, center_point, rect_width, rect_height):
    return [center_point + rect_width/2 * (- perp_vector) + rect_height/2 * (dir_vector),
            center_point + rect_width/2 * (perp_vector) + rect_height/2 * (dir_vector),
            center_point + rect_width/2 * (perp_vector) + rect_height/2 * (- dir_vector),
            center_point + rect_width/2 * (- perp_vector) + rect_height/2 * (- dir_vector)
        ]

# def draw_wires(screen, lines):
#     for line in lines:
#         start_point, end_point, seed, color = line
#         random.seed(seed)
# 
#         direction_vector = end_point - start_point
#         direction_magnitude = np.linalg.norm(direction_vector)
#         direction_unit_vector = direction_vector / direction_magnitude
# 
#         num_points = 10
#         points = [start_point]
#         for i in range(1, num_points - 1):
#             offset = random.randint(-10, 10)
#             new_point = start_point + direction_unit_vector * (i / (num_points - 1) * direction_magnitude) + np.array([-direction_unit_vector[1], direction_unit_vector[0]]) * offset/2
#             points.append(tuple(new_point.astype(int)))
#         points.append(end_point)
# 
#         pygame.draw.lines(screen, color, False, points, 4)
        
def draw_robot(screen, robot_corners_on_screen, direction_unit_vec):
    
# --------------------------------------------------------------------------------
# Find the bounding rectangle for the robot
# Rotate the image to the robot's angle
# Overlay bounding rectangle of image on the bounding rectangle of robot
# --------------------------------------------------------------------------------
    perp_dir = (robot_corners_on_screen[1] - robot_corners_on_screen[0])/np.linalg.norm(
            (robot_corners_on_screen[1] - robot_corners_on_screen[0]))
    
    min_x = min(point[0] for point in robot_corners_on_screen)
    max_x = max(point[0] for point in robot_corners_on_screen)
    min_y = min(point[1] for point in robot_corners_on_screen)
    max_y = max(point[1] for point in robot_corners_on_screen)
    
    bounding_rect_width = max_x - min_x
    bounding_rect_height = max_y - min_y
    
    bounding_rect = pygame.Rect(min_x, min_y, bounding_rect_width, bounding_rect_height)
    
    image_bounding_rect = setupdata.ROBOT_IMAGE.get_rect()
    image_bounding_rect.x = bounding_rect.x
    image_bounding_rect.y = bounding_rect.y
    
# --------------------------------------------------------------------------------
# Find the wheel centre position
# Draw wheels
# --------------------------------------------------------------------------------
    
    left_wheel_polygon = [(1 - WHEEL_POS_RATIO) * robot_corners_on_screen[0] + WHEEL_POS_RATIO * robot_corners_on_screen[3] + direction_unit_vec * WHEEL_RADIUS + perp_dir * WHEEL_RADIUS/2,
                            (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[0] + WHEEL_POS_RATIO * robot_corners_on_screen[3] + direction_unit_vec * WHEEL_RADIUS - perp_dir * WHEEL_RADIUS/2,
                            (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[0] + WHEEL_POS_RATIO * robot_corners_on_screen[3] - direction_unit_vec * WHEEL_RADIUS - perp_dir * WHEEL_RADIUS/2,
                            (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[0] + WHEEL_POS_RATIO * robot_corners_on_screen[3] - direction_unit_vec * WHEEL_RADIUS + perp_dir * WHEEL_RADIUS/2,
                            ]
    right_wheel_polygon = [(1 - WHEEL_POS_RATIO) * robot_corners_on_screen[1] + WHEEL_POS_RATIO * robot_corners_on_screen[2] + direction_unit_vec * WHEEL_RADIUS - perp_dir * WHEEL_RADIUS/2,
                            (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[1] + WHEEL_POS_RATIO * robot_corners_on_screen[2] + direction_unit_vec * WHEEL_RADIUS + perp_dir * WHEEL_RADIUS/2,
                            (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[1] + WHEEL_POS_RATIO * robot_corners_on_screen[2] - direction_unit_vec * WHEEL_RADIUS + perp_dir * WHEEL_RADIUS/2,
                            (1 - WHEEL_POS_RATIO) * robot_corners_on_screen[1] + WHEEL_POS_RATIO * robot_corners_on_screen[2] - direction_unit_vec * WHEEL_RADIUS - perp_dir * WHEEL_RADIUS/2,
                            ]
    
    pygame.draw.polygon(screen, (0, 0, 0), left_wheel_polygon, width=0)
    pygame.draw.polygon(screen, (0, 0, 0), right_wheel_polygon, width=0)
    
    screen.blit(setupdata.ROBOT_IMAGE, image_bounding_rect)
    
def  draw_sensors(screen, sensor_colors, robot_corners_on_screen):
    
    # Drawing corner sensors
    pygame.draw.circle(
        screen, sensor_colors[0], robot_corners_on_screen[0], 3)
    pygame.draw.circle(
        screen, (0,0,0), robot_corners_on_screen[0], 4,width=1)
    
    pygame.draw.circle(
        screen, sensor_colors[4], robot_corners_on_screen[1], 3)
    pygame.draw.circle(
        screen, (0,0,0), robot_corners_on_screen[1], 4,width=1)
    
    # Drawing path sensors
    pygame.draw.circle(
        screen, sensor_colors[1], ( (1 - PATH_SENSOR_POS_RATIO)*robot_corners_on_screen[0] + PATH_SENSOR_POS_RATIO*robot_corners_on_screen[1]).astype(int) , 3)
    pygame.draw.circle(
        screen, (0,0,0), ( (1 - PATH_SENSOR_POS_RATIO)*robot_corners_on_screen[0] + PATH_SENSOR_POS_RATIO*robot_corners_on_screen[1]).astype(int), 4,width=1)
    
    pygame.draw.circle(
        screen, sensor_colors[3], ( PATH_SENSOR_POS_RATIO*robot_corners_on_screen[0] + (1 - PATH_SENSOR_POS_RATIO)*robot_corners_on_screen[1]).astype(int) , 3)
    pygame.draw.circle(
        screen, (0,0,0), ( PATH_SENSOR_POS_RATIO*robot_corners_on_screen[0] + (1 - PATH_SENSOR_POS_RATIO)*robot_corners_on_screen[1]).astype(int), 4,width=1)
    
    pygame.draw.circle(
        screen, sensor_colors[2], ( 0.5*robot_corners_on_screen[0] + 0.5*robot_corners_on_screen[1]).astype(int) , 3)
    pygame.draw.circle(
        screen, (0,0,0), ( 0.5*robot_corners_on_screen[0] + 0.5*robot_corners_on_screen[1]).astype(int), 4,width=1)
    