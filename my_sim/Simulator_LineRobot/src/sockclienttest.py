# echo-client.py

import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65433  # The port used by the server
prev_sensor_data = None
sensor_data = None
prev_motor_drive_inputs = None
motor_drive_inputs = "0,1,0|0,0,1"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # tmp = True

    while True:
        s.sendall(motor_drive_inputs.encode())

        # print(f"Sent {motor_drive_inputs}")
        prev_motor_drive_inputs = motor_drive_inputs

        prev_sensor_data = sensor_data
        sensor_data = s.recv(1024)

        print(f"Recieved {sensor_data}")

        # if(sensor_data.decode() == '1,0'):
        #     motor_drive_inputs = "100,0,1|0,0,1"
        # if(sensor_data.decode() == '1,1'):
        #     motor_drive_inputs = "0,0,1|0,0,1"
