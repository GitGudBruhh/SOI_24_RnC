import numpy as np
import time
import pygame

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
    sensor_vals = [0, 0]

    angle = None
    direction_unit_vec = None

    corners = None
    corner_offsets = None

    def __init__(self, dimensions: tuple, start_pos: tuple, angle: float):
        self.width = dimensions[1]
        self.length = dimensions[0]
        self.current_speed = 0
        self.current_angular_velocity = 0
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
        self.wheel_pos[0] = (self.corners[0] + self.corners[3])/2
        self.wheel_pos[1] = (self.corners[1] + self.corners[2])/2

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
        self.direction_unit_vec = create_rot_matrix(rot_angle) @ self.direction_unit_vec
        self.corner_offsets[0] = create_rot_matrix(rot_angle) @ self.corner_offsets[0]
        self.corner_offsets[1] = create_rot_matrix(rot_angle) @ self.corner_offsets[1]

        self.corners[0] = self.current_pos + self.corner_offsets[0]
        self.corners[1] = self.current_pos + self.corner_offsets[1]
        self.corners[2] = self.current_pos - self.corner_offsets[0]
        self.corners[3] = self.current_pos - self.corner_offsets[1]

        self.wheel_pos[0] = (self.corners[0] + self.corners[3])/2
        self.wheel_pos[1] = (self.corners[1] + self.corners[2])/2

    def move(self, displacement: float):
        self.current_pos += displacement
        for idx in range(4):
            self.corners[idx] += displacement

        self.wheel_pos[0] += displacement
        self.wheel_pos[1] += displacement

    # Access functions
    # You only ever have to use these functions to update the robots condition inside the emulator
    # DO NOT LET PARTICIPANTS DIRECTLY ACCESS THESE
    def update_angle(self, time_elapsed: float):
        self.rotate(self.current_angular_velocity * time_elapsed)

    def update_pos(self, time_elapsed: float):
        displacement = self.direction_unit_vec * self.current_speed * time_elapsed
        self.move(displacement)

    def set_speed(self, speed: float):
        self.current_speed = speed

    def set_ang_vel(self, ang_vel: float):
        self.current_angular_velocity = ang_vel

    def get_sensor_vals(self, screen: pygame.surface.Surface):
        '''
        reads the IR sensor and return a list
        SHOULD BE USED BEFORE UPDATING THE ROBOT ON SCREEN


        sensor_vals[0] -> left sensor
        sensor_vals[1] -> right sensor
        (assuming corners[0] is front left corner)

        '''
        colour1 = screen.get_at((int(self.corners[0][0]), int(self.corners[0][1])))
        colour1_gs = (colour1[0] + colour1[1] + colour1[2]) / 3
        colour2 = screen.get_at((int(self.corners[1][0]), int(self.corners[1][1])))
        colour2_gs = (colour2[0] + colour2[1] + colour2[2]) / 3
        if (colour1_gs < 150):
            self.sensor_vals[0] = 0
        else:
            self.sensor_vals[0] = 1
        if (colour2_gs < 150):
            self.sensor_vals[1] = 0
        else:
            self.sensor_vals[1] = 1

        #print(self.sensor_vals)

        return self.sensor_vals
