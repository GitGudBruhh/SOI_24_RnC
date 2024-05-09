# This class will be used by the participants to exchange data with the emulator
# The signal setter functions need to be changed to use the motor speed values

MOTOR_MAX_SPEED = 60 # in rpm, which is 120pi rad/min, which is 2pi rad/s
WHEEL_RADIUS = 2.5 #i n cm
ACCELERATION = 0.5 # per tick
class RobotData:
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

    def __init__(self, speed, ang_vel):
        self.current_speed = speed
        self.current_angular_velocity = ang_vel

    ############################################
    # DONT TOUCH THESE WHILE NOT DEBUGGING
    def set_speed(self, speed):
        if(self.current_speed <= speed):
            self.is_accel = True
            self.is_decel = False
            self.new_speed = speed
        else:
            self.is_accel = False
            self.is_decel = True
            self.new_speed = speed

    def accel_decel(self, ticks_elapsed):
        if(self.is_accel):
            if(self.current_speed >= self.new_speed):
                self.current_speed = self.new_speed
                self.new_speed = None
                self.is_accel = False
            else:
                self.current_speed += ACCELERATION * ticks_elapsed
        if(self.is_decel):
            if(self.current_speed <= self.new_speed):
                self.current_speed = self.new_speed
                self.new_speed = None
                self.is_decel = False
            else:
                self.current_speed += -ACCELERATION * ticks_elapsed


    def set_ang_vel(self, ang_vel):
        self.current_angular_velocity = ang_vel
    #############################################

    def get_speed(self):
        return self.current_speed

    def get_ang_vel(self):
        return self.current_angular_velocity
