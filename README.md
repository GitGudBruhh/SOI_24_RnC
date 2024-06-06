# What is this?

This is a mini-robot simulator made using pygame for the Robotics + Coding clubs' problem statement Circuit Chase, SOI 2024, IIT Dharwad.

# Usage

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
(soi24venv)$ python start.py
```

The simulator server is now waiting for the connection to be established at localhost, `127.0.0.1`, ports `65432` and `65433`.
The port `65432` corresponds to the socket where the simulator receives the motor drive input signals.
The port `65433` corresponds to the socket from which the simulator sends the sensor output values.

This design decision was taken to allow for asynchronous and independent communication for sending and recieving data.
The participant's code must connect to the server, acting as a client. Examples codes for Python and C are provided in the repository.

To test the socket functionality, open up a new termninal in `src/` and run
```
$ python logicclient.py
```

The simulator now runs and you can view it in the pygame window. Logs are written on to the standard output on the terminal.
You can set the logging level in the `setupdata.py` file in range 0 - 4.

Note: The examples given use multithreading to communicate with the sockets parallelly.

Data is exchanged as a binary encoded string of signals with

* the client requiring to update the pulse width (`0 - 255`), `IN1` and `IN2` (Boolean) signals asynchronously (need not be updated every loop), and

* the server responding to the client with the sensor values in a specified interval (here, 0.5s, can be changed in robotinterface.py)

The client is to decode the recieved data into an ascii string, split at the delimiters `','` (comma) and `'|'` (vertical bar), and use the sensor values provided to update the signals for the robot according to their algorithm.


The overall working of the simulator is provided in `flowchart.txt`.

## Examples
Python:
Suppose the pulse width is to be set at 100% for the left wheel. To rotate it anticlockwise (forward motion of wheel), `IN1` is to be set to false, and `IN2` is to be set to true. Suppose the right wheel's speed is to be set to zero.

The binary encoded signal string in python will be:
```
>>> signal_string = b"255,0,1|0,0,0"
>>> type(signal_string)
<class 'bytes'>
```

This bytes object is to be sent across the socket to the simulator, which will update the wheel's data accordingly.

```
>>> sim_socket.sendall(signal_string) # sim_socket is the socket object
```

# Bugs? Need help?

Open an issue on this repo or feel free to contact us at codingclub@iitdh.ac.in or 220010005@iitdh.ac.in
