# What is this?

This is a mini-robot simulator made using pygame for the Robotics + Coding clubs' problem statement Circuit Chase, SOI 2024, IIT Dharwad.

# Usage

Execute these commands on your command line to setup the simulator.

## Setup 

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
(soi24venv)$ python start.py
```

The simulator server is now waiting for the connection to be established at localhost, `127.0.0.1`, ports `65432` and `65433`.
The port `65432` corresponds to the socket where the simulator receives the motor drive input signals.
The port `65433` corresponds to the socket from which the simulator sends the sensor data.

This design decision was taken to allow for asynchronous and independent communication for sending and recieving data.
The participant's code must connect to the server, acting as a client. Examples codes for Python and C are provided in the repository.

To test the socket functionality, open up a new termninal in `src/` and run
```
$ python logicclient.py
```

The simulator now runs and you can view it in the pygame window. Logs are written on to the standard output on the terminal.

The `setupdata.py` file contains constants related to the robot's dimensions and the maze setup. These can be modified before the simulation. The logging level for the standard output can also be set in the same file. The constants used in the testing phase are provided in the `setupdata.default` file.

The `mazemap.py` file contains the `maze` (multiline-string) variable. Each non empty character in the string corresponds to a square chunk of side length defined in `setupdata.py` (`STRIP_WIDTH`). If the player wants to define custom mazes, the `mazeimagegen.py` script is used to generate the background image of the new maze. The S and G characters in the maze are the start and goal positions respectively. Please note that there can be **only one** start position S.
```
        ################################
        #          ,---Path sensors	 		  #
        #          v                   #
        #   X,-s1-s2-,X*               #
        #    |       |                 #
        #    |       |  Length         #
        #    |       |                 #
        #    |   O   |                 #
        #   █|       |█                #
        #   █|       |█                #
        #   █|       |█                #
        #    `-------'                 #
        #      Width                   #
        ################################
```

The mazes are made using https://asciiflow.com

If you wish to make your own maze using characters available on your keyboard, you can do so by adding the characters into the `CHARSET` string in `setupdata.py` as comma separated values. By default, the `O` character also acts as a maze block.

Note: In the simulation, 1mm = 1px

Note: The `PATH_SENSOR_POS_RATIO` is the ratio of distance of a path sensor to its closer front corner to the distance of it from the farther front corner.	Here, (s1-X)/(X*-s1). Note that the ratio must always be less than 0.5

Note: The `WHEEL_POS_RATIO` is the ratio of the distances of the wheel's centre from the front and back corners respectively. 

Note: The examples given use multithreading to communicate with the sockets parallelly.

## Protocol
Data is exchanged as a string of signals with

* the client (player) updating the pulse width (`0 - 255`), `IN1` and `IN2` (Boolean) signals at port `65432`, and

* the client requesting the server for the sensor data at port `65433`.

Each update to the motor drive signals is met with an acknowledgement,`MOTOR_INP_RECV_ACK`, from the server. Once the player closes the simulator window, the server waits for a client message and then sends back a `SIM_COMPLETE` message, closing the connection.

In the sensor data channel, the client is required to send a `SENSOR_DATA_REQ` message to the server to fetch the sensor data. Under normal working conditions, the server will respond with the sensor data string. However, if the simulator has not been completely set up, the server responds with a `SENSOR_DATA_UNAVAIL` message. Similar to the motor drive inputs channel, once the simulator window is closed, the server waits for a message from the client, and then sends back `SIM_COMPLETE` message.

Note: It is recommended that the player use the `SIM_COMPLETE` messages to detect the end of simulation instead of directly interacting with the simulator's files.

The overall working of the simulator, and the communication protocol is provided in `FLOWCHART.txt`.

The client is to decode the recieved data into an ascii string, split at the delimiter `','` (comma), and use the sensor data provided to update the signals for the motor drive according to their algorithm. The motor drive signals string is split for the two wheels using the delimiter `'|'` (vertical bar). For each motor, the input is given as `PWM,IN1,IN2`.

## Examples
Python:
Suppose the left wheel is to be rotated at its maximum speed anticlockwise, and the right wheel is to be set to zero speed. That is, the pulse width is to be set at 100% (255) for the left wheel and 0% (0) for the right wheel. To rotate the left wheel anticlockwise (forward motion of wheel), `IN1` is to be set to a logic LOW, and `IN2` is to be set to a logic HIGH.

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

# Bugs? Need help?

Open an issue on this repo or feel free to contact us at codingclub@iitdh.ac.in or 220010005@iitdh.ac.in


