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

        self.direction_unit_vec = create_rot_matrix(angle) @ np.array([0, 1])

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
