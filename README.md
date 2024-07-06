# What is this?

This is a mini-robot simulator made using pygame for the Robotics + Coding clubs' problem statement Circuit Chase, SOI 2024, IIT Dharwad.

# Requirements

- A machine (bare metal/virtual machine) capable of handling at least 4 threads at a time.
- 2GB of RAM
- Python 3.9 or above

# Usage

## Setup 

Execute these commands on your command line to setup the simulator.

1. Clone the repository and change directory.
```
$ git clone https://github.com/GitGudBruhh/SOI_24_RnC
$ cd SOI_24_RnC
```

2. Create a python virtual environment for installing the required packages for the simulator.
```
$ python -m venv soi24venv
$ source soi24venv/bin/activate
```

3. Install the required packages in the virtual environment.
```
(soi24venv)$ pip install -r requirements.txt
```

4. Using the virtual environment as source run the simulator in `src/`.
```
(soi24venv)$ cd src/
(soi24venv)$ python mazeimagegen.py
(soi24venv)$ python start.py
```

The simulator server is now waiting for the connection to be established at localhost, `127.0.0.1`, ports `65432` and `65433`.
The port `65432` corresponds to the socket where the simulator receives the motor drive input signals.
The port `65433` corresponds to the socket from which the simulator sends the sensor data.

This design decision was taken to allow for asynchronous and independent communication for sending and recieving data.
The participant's code must connect to the server, acting as a client. An example code for Python is provided in the repository.

To test the simulator functionality, open up a new termninal in `src/` and run
```
$ python yourLogicClient.py
```

The simulator now runs and you can view it in the pygame window. Logs are written on to the standard output on the terminal.

## Customizing the Robot

The `setupdata.py` file contains constants related to the robot's dimensions and the maze setup. These can be modified before the simulation. The logging level for the standard output can also be set in the same file.

- The `WHEEL_POS_RATIO` is the ratio between the distance of the wheel's centre from the front, and the length of the robot. Here, PX*/W.
- The `PATH_SENSOR_POS_RATIO` is the ratio of distance of a path sensor to its closest front corner, and the width of the robot. Here, (s1-X)/W. Note that the ratio must always be less than 0.5
- The robot's dimensions can be customized (length and width)
- The line strip width can be customized if one wants to generate custom mazes.
- The wheel's specifications (Motor's max RPM, wheel radius, acceleration, angular acceleration) can also be changed
				- Logging levels, with higher number corresponding to more information being logged.
- NOTE: In the simulation, 1mm = 1px

```
        ################################
        #          ,---Path sensors	   #
        #          v                   #
        #   X,-s1-s2-,X*               #
        #    |       |                 #
        #    |       |  Length         #
        #    |       |                 #
        #    |   O   |                 #
        #   █|       |█                #
        #   █|       |█ P              #
        #   █|       |█                #
        #    `-------'                 #
        #      Width                   #
        ################################
```

## Generating custom mazes

The maze background is generated before running the simulator.

The `mazemap.py` file contains the `maze` (multiline-string) variable which you can edit.

Each non empty character in the string corresponds to a square chunk of side length defined in `setupdata.py` (`STRIP_WIDTH`). If the player wants to define custom mazes, the `mazeimagegen.py` script is used to generate the background image of the new maze. 

The S character corresponds to the start position in the maze. Please note that there should be **exactly one** start position S in the maze.

The mazes given were made using https://asciiflow.com

If you wish to make your own maze using characters available on your keyboard, you can do so by adding the characters into the `CHARSET` string in `setupdata.py` as comma separated values. By default, the `O` character also acts as a maze block.

For example:
```
# Suppose you have defined such a maze in mazemap.py
maze = '''

  SOOOOOOOOOOOOOOOOOOOOOOOOOOO   
                             O   
							 O   
							 O   
							 O   

'''
```

Running `python mazeimagegen.py` creates the background image `maze.png`.

Then, running the simulator opens up a window with the custom maze.
Be sure to give sufficient space padding in the left, right, top and bottom of the mazes to generate a background usable by the simulator.

## Communication Protocol
Data is exchanged as a string of signals with

* the client (player) updating the pulse width (`0 - 255`), `IN1` and `IN2` (Boolean) signals at port `65432`, and

* the client requesting the server for the sensor data at port `65433`.

Each update to the motor drive signals is met with an acknowledgement,`MOTOR_INP_RECV_ACK`, from the server. Once the player closes the simulator window, the server waits for a client message and then sends back a `SIM_COMPLETE` message, closing the connection.

In the sensor data channel, the client is required to send a `SENSOR_DATA_REQ` message to the server to fetch the sensor data. Under normal working conditions, the server will respond with the sensor data string. However, if the simulator has not been completely set up, the server responds with a `SENSOR_DATA_UNAVAIL` message. Similar to the motor drive inputs channel, once the simulator window is closed, the server waits for a message from the client, and then sends back `SIM_COMPLETE` message.

Note: It is recommended that the client use the `SIM_COMPLETE` messages to detect the end of simulation instead of directly interacting with the simulator's files.

The overall working of the simulator, and the communication protocol is provided in `FLOWCHART.txt`.

The client is to decode the recieved data into an ascii string, split at the delimiter `','` (comma), and use the sensor data provided to update the signals for the motor drive according to their algorithm. The motor drive signals string is split for the two wheels using the delimiter `'|'` (vertical bar). For each motor, the input is given as `DutyCycle,IN1,IN2`.							

# Examples


Note: The examples given use multithreading to communicate with the sockets parallelly.

Python:
Suppose the left wheel is to be rotated at its maximum speed anticlockwise, and the right wheel is to be set to zero speed. That is, the duty cycle is to be set at 100% (255) for the left wheel and 0% (0) for the right wheel. To rotate the left wheel anticlockwise (forward motion of wheel), `IN1` is to be set to a logic LOW, and `IN2` is to be set to a logic HIGH.

The string data is required to be converted to a bytes object before transmission:
```
>>> motor_drive_inp = b"255,0,1|0,0,0"
>>> type(motor_drive_inp)
<class 'bytes'>
```

This bytes object is to be sent across the socket to the simulator, which will update the wheel's data accordingly.

```
>>> sim_socket.sendall(motor_drive_inp)
```

Similarly, the recieved sensor values might look as follows:
```
>>> sensor_vals = conn.recv(32)
>>> print(sensor_vals)
b'1,1,0,0,0'
```

The middle two sensor values are path sensors, while the other two are the corner sensors used for turn logic.

An example `yourLogicClient.py` is given in the `src/` directory for the player's reference.

# Bugs? Need help?

Open an issue on this repo or feel free to contact us at codingclub@iitdh.ac.in, robotics@iitdh.ac.in, or 220010005@iitdh.ac.in



