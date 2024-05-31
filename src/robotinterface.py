import numpy as np

# This class will be used by the participants to exchange data with the emulator
# The signal setter functions need to be changed to use the motor speed values
# This class helps

MOTOR_MAX_RPM = 60 # in rpm, which is 120pi rad/min, which is 2pi rad/s, which corresponds to 15.7 cm/s
WHEEL_RADIUS = 25 #in px, 2.5 in cm
ACCELERATION = 5 # pixel per tick^2
ANGULAR_ACCELERATION = 0.1 # per tick^2

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

class RobotInterface:
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
