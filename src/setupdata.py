# CONSTANTS

MOTOR_MAX_RPM = 60 # in rpm, which is 120pi rad/min, which is 2pi rad/s, which corresponds to 15.7 cm/s
WHEEL_RADIUS = 25 #in px, 2.5 in cm
ACCELERATION = 5 # pixel per tick^2
ANGULAR_ACCELERATION = 0.1 # per tick^2

SCREEN_WIDTH = 1600#1400
SCREEN_HEIGHT = 1200 #780
STRIP_WIDTH =  15 #1.5cm
WHEEL_POS_RATIO = 0.7
ROBOT_WIDTH = 80 #8cm
ROBOT_LENGTH = 100 #12cm

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT1 = 65432
PORT2 = 65433

# GLOBAL VARIABLES

# def initialize():
global signal_list
global my_rob
global screen
global simulation_complete

signal_list = [[0, False, False], [0, False, False]]
my_rob = None
screen = None
simulation_complete = False
