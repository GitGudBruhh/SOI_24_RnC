# CONSTANTS

# --------------------------------------------------------------------------------
# SCALE: 1cm = 10px
# --------------------------------------------------------------------------------

MOTOR_MAX_RPM = 60 # in rpm, which is 120pi rad/min, which is 2pi rad/s, which corresponds to 15.7 cm/s
WHEEL_RADIUS = 25 #in px, 2.5 in cm
ACCELERATION = 1 # pixel per tick^2
ANGULAR_ACCELERATION = 0.1 # per tick^2

SCREEN_WIDTH = 800#1400
SCREEN_HEIGHT = 600 #780
STRIP_WIDTH =  15 #1.5cm
WHEEL_POS_RATIO = 0.7
PATH_SENSOR_POS_RATIO = 0.3
ROBOT_WIDTH = 80 #8cm
ROBOT_LENGTH = 120 #12cm

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT1 = 65432
PORT2 = 65433

MAZE_CHARSET = '─,│,┐,┘,└,┌,┬,┤,┴,├,┼,O'
MAZE_FILE_NAME = 'maze.png'
LOGLEVEL = (0, 0) # Tuple: (MOTOR_DRIVE_CHANNEL: 0 - 3, SENSOR_DATA_CHANNEL: 0 - 2)

# GLOBAL VARIABLES, PARTICIPANTS DO NOT TOUCH THESE

global signal_list
global my_rob
global screen
global simulation_complete
global is_sender_active
global is_receiver_active

signal_list = [[0, False, False], [0, False, False]]
my_rob = None
screen = None
simulation_complete = False
is_sender_active = False
is_receiver_active = False
ROBOT_IMAGE = None