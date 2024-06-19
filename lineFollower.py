# echo-client.py

import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65434  # The port used by the server
prev_sensor_data = None
sensor_data = None
prev_motor_drive_inputs = None
motor_drive_inputs = "100,0,1|100,1,0"

def turn_right():
    vals = "100,0,1|100,0,1"
    s.sendall(vals.encode())
    print(f"Sent {vals}")
    time.sleep(1.025)
    s.sendall(motor_drive_inputs.encode())
    print(f"Sent {motor_drive_inputs}")
def turn_left():
    vals = "100,1,0|100,1,0"
    s.sendall(vals.encode())
    print(f"Sent {vals}")
    time.sleep(1.025)
    s.sendall(motor_drive_inputs.encode())
    print(f"Sent {motor_drive_inputs}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    change = False
    first = True
    time.sleep(2)
    #turn_right()
    
    while True:
        s.sendall(motor_drive_inputs.encode())
        
        # if change:
        #     change = False
        #     time.sleep(1)
        #     motor_drive_inputs = "100,0,1|100,1,0"
            

        print(f"Sent {motor_drive_inputs}")
        prev_motor_drive_inputs = motor_drive_inputs

        prev_sensor_data = sensor_data
        sensor_data = s.recv(1024)
        print("lsd=",len(sensor_data))
        if(len(sensor_data) > 3):
            sensor_data = sensor_data[-3::]
        print(f"Recieved {sensor_data}")
        
        if(sensor_data == b"1,0"):
            time.sleep(1.25)
            s.sendall("0,0,0|0,0,0".encode())
            print(f"Sent 0,0,0|0,0,0")
            time.sleep(1)
            turn_right()
            time.sleep(1)
        if(sensor_data == b"0,1"):
            time.sleep(1.25)
            s.sendall("0,0,0|0,0,0".encode())
            print(f"Sent 0,0,0|0,0,0")
            time.sleep(1)
            turn_left()
            time.sleep(1)
        if(sensor_data == b"0,0"):
            time.sleep(1.25)
            s.sendall("0,0,0|0,0,0".encode())
            print(f"Sent 0,0,0|0,0,0")
            time.sleep(1)
            turn_left()
            time.sleep(1)


        
