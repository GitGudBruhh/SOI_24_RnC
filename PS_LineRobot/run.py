import numpy as np
import time

def create_rot_matrix(angle: float):
    return np.array([[np.cos(angle), np.sin(angle)],
                    [-np.sin(angle), np.cos(angle)]])

class Robot:
    length = None
    width = None
    corner_angle = None
    half_diag_length = None

    current_pos = None
    current_speed = None
    current_angular_velocity = None
    sensor_vals = None

    angle = None
    direction_unit_vec = None

    corners = None
    corner_offsets = None

    def __init__(self, dimensions: tuple, start_pos: tuple, angle: float):
        self.width = dimensions[0]
        self.length = dimensions[1]
        self.current_speed = 0
        self.current_angular_velocity = 0
        self.corner_angle = np.arctan(self.width/self.length)
        self.half_diag_length = np.linalg.norm([self.width/2, self.length/2])

        self.current_pos = np.array(start_pos, dtype='float64')
        self.angle = angle

        self.direction_unit_vec = create_rot_matrix(angle) @ np.array([1, 0])

        corner_0_offset = create_rot_matrix(angle + self.corner_angle) @ (self.half_diag_length * np.array([0, 1]))
        corner_1_offset = create_rot_matrix(angle - self.corner_angle) @ (self.half_diag_length * np.array([0, 1]))
        self.corner_offsets = np.array([corner_0_offset, corner_1_offset])

        self.corners = np.zeros((4, 2))
        self.corners[0] = self.current_pos + self.corner_offsets[0]
        self.corners[1] = self.current_pos + self.corner_offsets[1]
        self.corners[2] = self.current_pos - self.corner_offsets[0]
        self.corners[3] = self.current_pos - self.corner_offsets[1]

        ################################################
        #      Direction unit vector                   #
        #        X                                     #
        #        |                                     #
        #        |                                     #
        #   X,---|---,X Corner Offsets                 #
        #    |\  |  /|                                 #
        #    | \ | / |                                 #
        #    |  \|/  |                                 #
        #    |   O   |  Length                         #
        #    |  pos  |                                 #
        #    |       |                 ^ Y             #
        #    |       |                 |               #
        #    `-------'                 |               #
        #      Width                   '-----> X       #
        ################################################


    # Helper functions
    # DO NOT TOUCH THESE
    def rotate(self, rot_angle: float):
        self.direction_unit_vec = create_rot_matrix(rot_angle) @ self.direction_unit_vec
        self.corner_offsets[0] = create_rot_matrix(rot_angle) @ self.corner_offsets[0]
        self.corner_offsets[1] = create_rot_matrix(rot_angle) @ self.corner_offsets[1]

        self.corners[0] = self.current_pos + self.corner_offsets[0]
        self.corners[1] = self.current_pos + self.corner_offsets[1]
        self.corners[2] = self.current_pos - self.corner_offsets[0]
        self.corners[3] = self.current_pos - self.corner_offsets[1]

    def move(self, displacement: float):
        self.current_pos += displacement
        for idx in range(4):
            self.corners[idx] += displacement

    # Access functions
    # You only ever have to use these functions to update the robots condition
    def update_angle(self, time_elapsed: float):
        self.rotate(self.current_angular_velocity * time_elapsed)

    def update_pos(self, time_elapsed: float):
        displacement = self.direction_unit_vec * self.current_speed * time_elapsed
        self.move(displacement)

    def get_speed(self):
        return self.current_speed

    def get_ang_vel(self):
        return self.current_angular_velocity

    def get_sensor_vals(self):
        return self.sensor_val

    def set_speed(self, speed: float):
        self.current_speed = speed

    def set_ang_vel(self, ang_vel: float):
        self.current_angular_velocity = ang_vel

########################################################################################################
# Pygame implementation of environment
# Create map as string
# Can get map from files as string

map = '''O#####O######
O#####O######
O#OOOOOOOO###
OOO######O###
O####S##GO###
'''

# Convert string to rows of strings for easier iteration and position access
map_array = map.split('\n')
#########################################################################################################
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
strip_width = 30

# Determine the start pos of maze
start_pos = (0, 0)
for row in map_array:
    if 'S' in row:
        start_pos = np.array([row.index('S'), map_array.index(row)])
        print(start_pos)

#This variable is used because pygame draws by default starting from the top left corner
path_offset = np.array([strip_width/2 - 2, strip_width/2]) #Used once to center the robot onto the path at the start

# Create the robot object (Dimensions, start position, Direction facing (Standard unit circle))
my_rob = Robot((40, 40), strip_width*start_pos + path_offset, np.pi/2)
my_rob.set_speed(0)
my_rob.set_ang_vel(-np.pi)

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Roboto', 30)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
running = True

# Load the sprite for wheels
rob_image = pygame.image.load('black.jpg')
rob_image = pygame.transform.scale(rob_image, (5, 5))

# Variables used to keep track of ticks
time_start = 0
time_end = 0
while running:
    time_start = time_end
    time_end = pygame.time.get_ticks()
    text_surface = my_font.render(str(pygame.time.get_ticks()), False, (0, 0, 0)) # Surface used to print time onto screen

    # Update the position and angle of robot each time interval
    my_rob.update_pos((time_end - time_start)/1000)
    my_rob.update_angle((time_end - time_start)/1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255)) #Fill background as white

    # Choosing j, i (position of maze block) and filling it in if it's a strip
    for j in range(len(map_array)):
        row = map_array[j]
        for i in range(len(row)):
            block_pos = (i*strip_width, j*strip_width) #Get block position
            if row[i] == 'O':
                pygame.draw.rect(screen, (100, 100, 100), block_pos + (strip_width, strip_width)) #Draw the path at block_pos
            elif row[i] == 'S':
                pygame.draw.rect(screen, (200, 200, 0), block_pos + (strip_width, strip_width))
            elif row[i] == 'G':
                pygame.draw.rect(screen, (0, 200, 0), block_pos + (strip_width, strip_width))

    # Draw the four corners and an additional front for the robot for easier visibility
    screen.blit(rob_image, my_rob.corners[0])
    screen.blit(rob_image, my_rob.corners[1])
    screen.blit(rob_image, my_rob.corners[2])
    screen.blit(rob_image, my_rob.corners[3])
    screen.blit(rob_image, my_rob.current_pos)
    screen.blit(rob_image, my_rob.current_pos + 30*my_rob.direction_unit_vec)
    screen.blit(text_surface, (500,0))
    pygame.display.flip()

pygame.quit()
