# This class will be used by the participants to exchange data with the emulator
# The signal setter functions need to be changed to use the motor speed values
import pygame

MOTOR_MAX_SPEED = 60 #in rpm, which is 120pi rad/min, which is 2pi rad/s
WHEEL_RADIUS = 2.5 #in cm
class RobotData:
    '''
    - motor1speed: float IN
    - motor2speed: float IN
    - speed: float SIGNAL
    - ang_vel: float SIGNAL
    - sensor_values: [bool, bool] OUT
    '''
    def __init__(self, speed, ang_vel):
        self.current_speed = speed
        self.current_angular_velocity = ang_vel

    ############################################
    # DONT TOUCH THESE WHILE NOT DEBUGGING
    def set_speed(self, speed):
        self.speed = speed

    def set_ang_vel(self, ang_vel):
        self.ang_vel = ang_vel
    #############################################

    def get_speed(self):
        return self.current_speed

    def get_ang_vel(self):
        return self.current_angular_velocity
