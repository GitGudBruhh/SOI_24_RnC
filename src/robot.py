import numpy as np
import pygame

from setupdata import WHEEL_POS_RATIO, PATH_SENSOR_RATIO

def create_rot_matrix(angle: float):
    return np.array([[np.cos(angle), np.sin(angle)],
                    [-np.sin(angle), np.cos(angle)]])

class Robot:
    length = None
    width = None
    corner_angle = None
    half_diag_length = None

    current_pos = None
    current_speed = 0
    current_angular_velocity = 0
    sensor_vals = [0, 0, 0, 0]
    centre_of_rot = None

    angle = None
    direction_unit_vec = None

    corners = None
    corner_offsets = None

    dist_travelled = 0

    def __init__(self, dimensions: tuple, start_pos: tuple, angle: float):
        self.width = dimensions[1]
        self.length = dimensions[0]

        self.corner_angle = np.arctan(self.width/self.length) #TThis is the angle b/w direction vector and centre->corner vector
        self.half_diag_length = np.linalg.norm([self.width/2, self.length/2]) #Half diagonal length is useful in calculations

        self.current_pos = np.array(start_pos, dtype='float64')
        self.angle = angle

        self.direction_unit_vec = create_rot_matrix(angle) @ np.array([1, 0])

        corner_0_offset = create_rot_matrix(angle + self.corner_angle) @ (self.half_diag_length * np.array([1, 0]))
        corner_1_offset = create_rot_matrix(angle - self.corner_angle) @ (self.half_diag_length * np.array([1, 0]))
        self.corner_offsets = np.array([corner_0_offset, corner_1_offset])

        self.corners = np.zeros((4, 2))
        self.corners[0] = self.current_pos + self.corner_offsets[0]
        self.corners[1] = self.current_pos + self.corner_offsets[1]
        self.corners[2] = self.current_pos - self.corner_offsets[0]
        self.corners[3] = self.current_pos - self.corner_offsets[1]

        self.wheel_pos = np.zeros((2, 2))

        # WHEELS AT MIDDLE
        # self.wheel_pos[0] = (self.corners[0] + self.corners[3])/2
        # self.wheel_pos[1] = (self.corners[1] + self.corners[2])/2
        # WHEELS AT MIDDLE

        # WHEELS AT BACK CORNERS
        # self.wheel_pos[0] = self.corners[3]
        # self.wheel_pos[1] = self.corners[2]
        # WHEELS AT BACK CORNERS
        
        # WHEELS AT SOME PLACE IN BETWEEN
        self.wheel_pos[0] = (1 - WHEEL_POS_RATIO) * self.corners[0] + WHEEL_POS_RATIO * self.corners[3]
        self.wheel_pos[1] = (1 - WHEEL_POS_RATIO) * self.corners[1] + WHEEL_POS_RATIO * self.corners[2]
        # WHEELS AT BACK CORNERS

        ################################################
        #   Direction unit vector (init. dir = pi/2)   #
        #        D                                     #
        #        |                                     #
        #        |                                     #
        #   X,---|---,X Corner Offsets (O -> X)        #
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
        # TODO!!!!! USE CENTRE_OF_ROT TO CHANGE

        r_matrix = create_rot_matrix(rot_angle)

        for idx in range(4):
            self.corners[idx] = r_matrix @ (self.corners[idx] - self.centre_of_rot) + self.centre_of_rot

        for idx in range(2):
            self.wheel_pos[idx] = r_matrix @ (self.wheel_pos[idx] - self.centre_of_rot) + self.centre_of_rot

        self.current_pos = r_matrix @ (self.current_pos - self.centre_of_rot) + self.centre_of_rot

        self.corner_offsets[0] = self.corners[0] - self.current_pos
        self.corner_offsets[1] = self.corners[1] - self.current_pos

        tmp = (self.corners[0] + self.corners[1])/2 - self.current_pos
        self.direction_unit_vec = tmp/np.linalg.norm(tmp)

    def move(self, displacement: float):
        self.current_pos += displacement
        for idx in range(4):
            self.corners[idx] += displacement

        self.wheel_pos[0] += displacement
        self.wheel_pos[1] += displacement

    # Emulator functions
    # You only ever have to use these functions to update the robots condition inside the emulator
    # The function parameters are taken from the robot interface
    # The robot interface preprocesses the data to provide speed values
    # DO NOT LET PARTICIPANTS DIRECTLY ACCESS THESE

    def update_pos(self, time_elapsed: float, radius_of_rot_div_w):
        if(not radius_of_rot_div_w == 'INF'):
            wheel_mid = (self.wheel_pos[0] + self.wheel_pos[1])/2
            self.centre_of_rot =  wheel_mid + radius_of_rot_div_w * 2 * (self.wheel_pos[0] - wheel_mid) # WARNING IS IT WITH RESPECT TO 1 OR 0
            self.rotate(self.current_angular_velocity * time_elapsed)
            self.dist_travelled += (self.current_angular_velocity * time_elapsed) * radius_of_rot_div_w * self.width
        else:
            self.centre_of_rot = 'INF'
            displacement = self.direction_unit_vec * self.current_speed * time_elapsed
            self.move(displacement)
            self.dist_travelled += np.linalg.norm(displacement)

    def set_speed(self, speed: float):
        self.current_speed = speed

    def set_ang_vel(self, ang_vel: float):
        self.current_angular_velocity = ang_vel

    def get_sensor_vals(self, screen: pygame.surface.Surface, corners_on_screen):
        '''
        reads the IR sensor and return a list
        SHOULD BE USED BEFORE DRAWING THE ROBOT ON SCREEN


        sensor_vals[0] -> left sensor
        sensor_vals[1] -> right sensor
        (assuming corners[0] is front left corner)

        '''
        
        
        colour0 = screen.get_at((int(corners_on_screen[0][0]), int(corners_on_screen[0][1])))
        colour0_gs = (colour0[0] + colour0[1] + colour0[2]) / 3
        
        colour3 = screen.get_at((int(corners_on_screen[1][0]), int(corners_on_screen[1][1])))
        colour3_gs = (colour3[0] + colour3[1] + colour3[2]) / 3
        
        colour1 = screen.get_at((int( (1 - PATH_SENSOR_RATIO)*corners_on_screen[0][0] + PATH_SENSOR_RATIO*corners_on_screen[1][0] ) , 
                                 int( (1 - PATH_SENSOR_RATIO)*corners_on_screen[0][1] + PATH_SENSOR_RATIO*corners_on_screen[1][1] )))
        colour1_gs = (colour1[0] + colour1[1] + colour1[2]) / 3
        
        colour2 = screen.get_at((int( PATH_SENSOR_RATIO*corners_on_screen[0][0] + (1 - PATH_SENSOR_RATIO)*corners_on_screen[1][0] ) , 
                                 int( PATH_SENSOR_RATIO*corners_on_screen[0][1] + (1 - PATH_SENSOR_RATIO)*corners_on_screen[1][1] )))
        colour2_gs = (colour2[0] + colour2[1] + colour2[2]) / 3
        
        if (colour0_gs < 150):
            self.sensor_vals[0] = 0
        else:
            self.sensor_vals[0] = 1
        if (colour3_gs < 150):
            self.sensor_vals[3] = 0
        else:
            self.sensor_vals[3] = 1
        if (colour1_gs < 150):
            self.sensor_vals[1] = 0
        else:
            self.sensor_vals[1] = 1
        if (colour2_gs < 150):
            self.sensor_vals[2] = 0
        else:
            self.sensor_vals[2] = 1
        
        return self.sensor_vals
