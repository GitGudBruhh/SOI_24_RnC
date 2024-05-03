import numpy as np
import scipy

def create_rot_matrix(angle: float):
    return np.array([[np.cos(angle), np.sin(angle)], 
                    [-np.sin(angle), np.cos(angle)]])
    
class Robot:
    length = None
    width = None
    corner_angle = None
    half_diag_length = None
    
    current_pos = None
    
    angle = None
    direction_unit_vec = None
    
    corners = None
    corner_offsets = None

    def __init__(self, dimensions: tuple, start_pos: list, angle: float):
        self.width = dimensions[0]
        self.length = dimensions[1]
        self.corner_angle = np.arcsin(width/length)
        self.half_diag_length = np.linalg.norm([width/2, length/2])
        
        self.current_pos = np.array(start_pos)
        self.angle = angle
        
        self.direction_unit_vec = create_rot_matrix(angle) @ np.array([0, 1])
        
        corner_0_offset = create_rot_matrix(angle + corner_angle) @ (half_diag_length * np.array([0, 1]))
        corner_1_offset = create_rot_matrix(angle - corner_angle) @ (half_diag_length * np.array([0, 1]))
        self.corner_offsets = np.array([corner_0_offset, corner_1_offset])
        self.corners = [current_pos + cor]
        
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
        #    |       |                                 #
        #    |       |                 ^ Y             #
        #    |       |                 |               #
        #    `-------'                 |               #
        #      Width                   '-----> X       #
        ################################################

    def rotate(rot_angle: float):
        self.direction_unit_vec = create_rot_matrix(rot_angle) @ self.direction_unit_vec
        self.corner_offsets[0] = create_rot_matrix(rot_angle) @ self.corner_offsets[0]
        self.corner_offsets[1] = create_rot_matrix(rot_angle) @ self.corner_offsets[1]

        corners[0] = current_pos + corner_offsets[0]
        corners[1] = current_pos + corner_offsets[1]
        corners[2] = current_pos - corner_offsets[0]
        corners[3] = current_pos - corner_offsets[1]
        
