import socket
import copy
import time

from setupdata import (
    HOST,
    PORT1,
    PORT2)

import setupdata

poll_time = 1

def socket_worker_receiver():
    # global signal_list
    # global simulation_complete
    global poll_time
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT1))
        s.listen()
        conn, addr = s.accept()
        
        setupdata.is_receiver_active = True

        with conn:
            print(f"[SIM] reciever(): Connected by {addr}")
            while True:
                time.sleep(poll_time)
                if(setupdata.simulation_complete):
                    data = conn.recv(1024)
                    conn.sendall("SIM_COMPLETE".encode())
                    conn.close()
                    # s.close()
                    return

                data = conn.recv(1024)

                string_data = data.decode('ascii')
                
                print(f"[SIM] receiver(): Recieved {string_data}")
                
                signals = string_data.split('|')

                for idx in range(len(signals)):
                    signals[idx] = signals[idx].split(',')
                    signals[idx][0] = int(signals[idx][0])
                    signals[idx][1] = bool(int(signals[idx][1]))
                    signals[idx][2] = bool(int(signals[idx][2]))

                setupdata.signal_list = copy.deepcopy(signals[0:2])
                
                conn.send("ROBOT_SIG_RECV_ACK".encode())
                print(f"[SIM] receiver(): Sent ROBOT_SIG_RECV_ACK")

def socket_worker_sender():
    # global my_rob
    # global screen
    # global simulation_complete
    global poll_time

    prev_data = b''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT2))
        s.listen()
        conn, addr = s.accept()
        
        setupdata.is_sender_active = True
        
        
        with conn:
            print(f"[SIM] sender(): Connected by {addr}")
            while True:
                time.sleep(poll_time)
                
                if(setupdata.simulation_complete):
                    conn.send("SIM_COMPLETE".encode())
                    conn.close()
                    # s.close()
                    return

                if(not setupdata.my_rob == None and not setupdata.screen == None):
                    sensor_vals = copy.copy(setupdata.my_rob.sensor_vals)
                    sensor_vals[0] = str(int(sensor_vals[0]))
                    sensor_vals[1] = str(int(sensor_vals[1]))

                    current_data = (','.join(sensor_vals)).encode()
                    
                    conn.send(current_data)
                    print(f"[SIM] sender(): Sent {current_data}")
                    
                    acknowledgement = conn.recv(1024)
                    print(f"[SIM] sender(): Acknowledgement recieved {acknowledgement}")
