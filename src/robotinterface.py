import socket
import copy

from setupdata import (
    HOST,
    PORT1,
    PORT2,
    LOGLEVEL)

import setupdata

def motor_drive_inputs_receiver():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT1))
        s.listen()
        conn, addr = s.accept()
        
        setupdata.is_receiver_active = True

        with conn:
            print(f"[SIM] reciever(): Connected by {addr}")
            
            prev_string_data = None
            while True:
                if(setupdata.simulation_complete):
                    data = conn.recv(32)
                    conn.sendall("SIM_COMPLETE".encode())
                    break

                data = conn.recv(32)

                string_data = data.decode('ascii')
                
                signals = string_data.split('|')

                for idx in range(len(signals)):
                    signals[idx] = signals[idx].split(',')
                    signals[idx][0] = int(signals[idx][0])
                    signals[idx][1] = bool(int(signals[idx][1]))
                    signals[idx][2] = bool(int(signals[idx][2]))

                setupdata.signal_list = copy.deepcopy(signals[0:2])
                
                conn.send("MOTOR_INP_RECV_ACK".encode())
                
                if LOGLEVEL[0] == 0:
                    pass
                
                elif LOGLEVEL[0] == 1:
                    if(not prev_string_data == string_data):
                        print(f"[SIM] receiver(): Recieved {string_data}")
                        prev_string_data = string_data

                elif LOGLEVEL[0] == 2:
                    print(f"[SIM] receiver(): Recieved {string_data}")
                
                elif LOGLEVEL[0] == 3:
                    print(f"[SIM] receiver(): Recieved {string_data}")
                    print(f"[SIM] receiver(): Sent MOTOR_INP_RECV_ACK")

            conn.close()
        s.close()

def sensor_vals_sender():

    prev_data = b''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT2))
        s.listen()
        conn, addr = s.accept()
        
        setupdata.is_sender_active = True
        prev_data = None
        
        with conn:
            print(f"[SIM] sender(): Connected by {addr}")
            while True:                
                if(setupdata.simulation_complete):
                    completion_ack = conn.recv(32)
                    conn.send("SIM_COMPLETE".encode())
                    break


                request = conn.recv(32)
                
                
                if(request.decode() == "SENSOR_DATA_REQ"):
                    current_data = b'SENSOR_DATA_UNAVAIL'
                    
                    if(not setupdata.my_rob == None and not setupdata.screen == None):
                        sensor_vals = copy.copy(setupdata.my_rob.sensor_vals)
                        sensor_vals[0] = str(int(sensor_vals[0]))
                        sensor_vals[1] = str(int(sensor_vals[1]))
                        sensor_vals[2] = str(int(sensor_vals[2]))
                        sensor_vals[3] = str(int(sensor_vals[3]))

                        current_data = (','.join(sensor_vals)).encode()
                        
                    conn.send(current_data)
                
                    if LOGLEVEL[1] == 0:
                        pass
                    elif LOGLEVEL[1] == 1:
                        if(not current_data == prev_data):
                            prev_data = current_data

                            print(f"[SIM] sender(): Sent {current_data}")
                            

                    elif LOGLEVEL[1] == 2:
                        print(f"[SIM] sender(): Recieved request {request}")
                        print(f"[SIM] sender(): Sent {current_data}")
            
            conn.close()
        s.close()
