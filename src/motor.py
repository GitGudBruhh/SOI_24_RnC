import numpy as np

from setupdata import MOTOR_MAX_RPM
from setupdata import WHEEL_RADIUS

class Motor:
    duty_cycle = 0
    rpm = 0
    wheel_speed = 0
    wheel_angular_speed = 0
    in1 = False
    in2 = False

    def __init__(self, position: int, d_cycle: int, IN1_PIN_val: bool, IN2_PIN_val: bool):
        self._rpm : int = 0
        self.position = position # LEFT = 0, RIGHT = 1
        self.write_motor_pins(d_cycle, IN1_PIN_val, IN2_PIN_val)

    def set_direction_pin_vals(self, IN1_PIN_val: bool, IN2_PIN_val: bool):
        self.in1 = IN1_PIN_val
        self.in2 = IN2_PIN_val

        if(self.in1 == self.in2):
            self.direction = 0
        elif(self.in1):
            if(self.position == 0):
                self.direction = -1
            else:
                self.direction = 1
        elif(self.in2):
            if(self.position == 0):
                self.direction = 1
            else:
                self.direction = -1

    def set_duty_cycle(self, d_cycle: int):
        # 0 -> 255 :: 0 -> MOTOR_MAX_RPM :: 0T -> 100%T
        self.duty_cycle = d_cycle
        self.rpm = (self.direction * d_cycle * MOTOR_MAX_RPM)/255
        self.wheel_angular_speed = self.rpm * 2 * np.pi / 60 # in rad/s
        self.wheel_speed = self.wheel_angular_speed * WHEEL_RADIUS # in px/s

    def write_motor_pins(self, d_cycle: int, IN1_PIN_val: bool, IN2_PIN_val: bool):
        self.set_direction_pin_vals(IN1_PIN_val, IN2_PIN_val)
        self.set_duty_cycle(d_cycle)