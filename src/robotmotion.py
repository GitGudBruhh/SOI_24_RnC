import numpy as np
from setupdata import ACCELERATION
from setupdata import ANGULAR_ACCELERATION
from motor import Motor

class RobotMotion:
    '''
    - motor1speed: float IN
    - motor2speed: float IN
    - speed: float SIGNAL
    - ang_vel: float SIGNAL
    - sensor_values: [bool, bool] OUT
    '''
    is_decel = False
    is_accel = False
    new_speed = None
    current_speed = 0

    motors = None
    width = None
    length = None
    radius_of_rotation_div_w = None

    is_ang_decel = False
    is_ang_accel = False
    new_ang_vel = None
    current_angular_velocity = 0

    prev_signals = None

    def __init__(self, signals, dimensions: tuple[int]):
        m_left = Motor(0, signals[0][0], signals[0][1], signals[0][2])
        m_right = Motor(1, signals[1][0], signals[1][1], signals[1][2])
        self.motors = [m_left, m_right]
        self.width = dimensions[1]
        self.length = dimensions[0]
        self.prev_signals = signals

    ############################################
    # DONT TOUCH THESE WHILE NOT DEBUGGING
    def set_speed(self, speed: float):
        ############ !!!!!!!!!!! #####################
        if(self.current_speed <= speed):
            self.is_accel = True
            self.is_decel = False
            self.new_speed = speed
        else:
            self.is_accel = False
            self.is_decel = True
            self.new_speed = speed
        ############ !!!!!!!!!!! #####################

        # self.current_speed = speed

    def set_ang_vel(self, ang_vel: float):
        ########### !!!!!!!!!!! #####################
        if(self.current_angular_velocity <= ang_vel):
            self.is_ang_accel = True
            self.is_ang_decel = False
            self.new_ang_vel = ang_vel
        else:
            self.is_ang_accel = False
            self.is_ang_decel = True
            self.new_ang_vel = ang_vel
        ########### !!!!!!!!!!! #####################

        # self.current_angular_velocity = ang_vel

    def accel_decel(self, ticks_elapsed: int):
        if(self.is_accel):
            if(self.current_speed >= self.new_speed):
                self.current_speed = self.new_speed
                self.new_speed = None
                self.is_accel = False
                self.is_decel = False
                print("FIN_ACCEL")

            else:
                self.current_speed += ACCELERATION * ticks_elapsed
                print("IS_ACCEL")

        if(self.is_decel):
            if(self.current_speed <= self.new_speed):
                self.current_speed = self.new_speed
                self.new_speed = None
                self.is_decel = False
                self.is_accel = False
                print("FIN_DECEL")

            else:
                self.current_speed -= ACCELERATION * ticks_elapsed
                print("IS_DECEL")

        if(self.is_ang_accel):
            if(self.current_angular_velocity >= self.new_ang_vel):
                self.current_angular_velocity = self.new_ang_vel
                self.new_ang_vel = None
                self.is_ang_accel = False
                print("FIN_ANG_ACCEL")

            else:
                self.current_angular_velocity += ANGULAR_ACCELERATION * ticks_elapsed
                print("IS_ANG_ACCEL")

        if(self.is_ang_decel):
            if(self.current_angular_velocity <= self.new_ang_vel):
                self.current_angular_velocity = self.new_ang_vel
                self.new_ang_vel = None
                self.is_ang_decel = False
                print("FIN_ANG_DECEL")

            else:
                self.current_angular_velocity -= ANGULAR_ACCELERATION * ticks_elapsed
                print("IS_ANG_ACCEL")

        pass
    ############################################

    def update_signals(self, signals: tuple[int]):
        if(signals != self.prev_signals):
            self.motors[0].write_motor_pins(signals[0][0], signals[0][1], signals[0][2])
            self.motors[1].write_motor_pins(signals[1][0], signals[1][1], signals[1][2])
            self.set_speed((self.motors[0].wheel_speed + self.motors[1].wheel_speed)/2)
            self.set_ang_vel((self.motors[1].wheel_speed - self.motors[0].wheel_speed)/self.width)

            if(not (self.motors[1].wheel_angular_speed == self.motors[0].wheel_angular_speed)):
                self.radius_of_rotation_div_w = ((self.motors[1].wheel_angular_speed + self.motors[0].wheel_angular_speed)/(2*(self.motors[1].wheel_angular_speed - self.motors[0].wheel_angular_speed)))

            else:
                self.radius_of_rotation_div_w = 'INF'
            self.prev_signals = signals

    def get_speed(self):
        return self.current_speed

    def get_ang_vel(self):
        return self.current_angular_velocity
