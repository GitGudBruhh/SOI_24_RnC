import numpy as np
import env

#Design a robot 
#Here I am taking a two wheeled robot with the motors at the centre --> easy rotation
class LineFollower:
    length = None
    width = None

    wheel_radius = 0.0
    wheel_circumference = 0.0
    max_motor_speed = None

    current_left_motor_speed = 0
    current_right_motor_speed = 0

    current_linear_velocity = 0
    current_angular_velocity = 0

    no_of_rotations = 0

    current_position = np.zeros((1,2))
    current_orientation = np.zeros((1,2)) # {0,1} for north, {1,0} east {-1,0 } west and {0,-1} for south
    def __init__(self,dimensions, wheel_radius, max_motor_speed , start_coordinates,start_orientation) -> None :
        self.length = dimensions[0]
        self.width = dimensions[1]

        self.max_motor_speed = max_motor_speed 
        self.wheel_radius = wheel_radius
        self.wheel_circumference = 2*(22.0/7)*wheel_radius
        current_position = start_coordinates
        current_orientation = start_orientation

    def calc_robot_speed(self):
        if self.current_left_motor_speed + self.current_right_motor_speed == 0:
            self.current_linear_velocity = 0
            self.current_angular_velocity = (self.current_left_motor_speed*self.wheel_circumference)/self.wheel_radius
        elif self.current_left_motor_speed == self.current_right_motor_speed:
            self.current_linear_velocity = self.current_left_motor_speed*self.wheel_circumference
        else:
            print("Havent Done Yet =_=")

        
    def get_motor_speed(self) -> None:
        self.current_left_motor_speed = 10 #env.get_left_motor_speed() The values that need to be got from the environment
        self.current_right_motor_speed = 10#env.get_right_motor_speed()
    
    def rotate_cw(self, motor_speed):

        #define physics 
        env.set_left_motor_speed(motor_speed)
        env.set_right_motor_speed(-motor_speed)
        self.get_motor_speed()

    

    def rotate_ccw(self,motor_speed):
        #define physics 
        env.set_left_motor_speed(-motor_speed)
        env.set_right_motor_speed(motor_speed)
        self.get_motor_speed()

    def calculate_position(self):
        
        distance_travelled = self.no_of_rotations*self.wheel_radius
        self.current_position += distance_travelled*self.current_orientation

    def calculate_orientation(self,angle):
        theta = np.radians(angle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c,-s),(s,c)))
        self.current_orientation = np.dot(self.current_orientation,R)
    
    





