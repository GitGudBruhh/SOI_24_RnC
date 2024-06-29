import socket
import threading
import time

from setupdata import HOST, PORT1, PORT2

poll_time = 0.025
motor_drive_inputs = "100,0,1|100,1,0"
sensor_data = None
SIM_RUNNING = None

def motor_drive_inputs_sender():
    global poll_time
    global motor_drive_inputs
    global SIM_RUNNING
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT1))
        
        prev_motor_drive_inputs = None

        while True:
            time.sleep(poll_time)
            s.sendall(motor_drive_inputs.encode())
            
            #print(f"[PLYR] sender(): Sent {motor_drive_inputs}")
            prev_motor_drive_inputs = motor_drive_inputs
            
            acknowledgement = s.recv(32)
            #print(f"[PLYR] sender(): Acknowledgement recieved {acknowledgement}")
            
            if(acknowledgement.decode() == "SIM_COMPLETE"):
                SIM_RUNNING = False
                s.close()
                return


def sensor_vals_reciever():
    global poll_time
    global sensor_data
    global SIM_RUNNING
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT2))
        
        prev_sensor_data = None

        while True:
            
            prev_sensor_data = sensor_data
            time.sleep(poll_time)
            s.send("SENSOR_DATA_REQ".encode())
            
            sensor_data = s.recv(32)
            
            if(sensor_data.decode() == "SIM_COMPLETE"):
                SIM_RUNNING = False
                s.close()
                return

            #print(f"[PLYR] receiver(): Recieved {sensor_data}")
            s.send("SENSOR_DATA_RECV_ACK".encode())
            #print(f"[PLYR] receiver(): Sent SENSOR_DATA_RECV_ACK")
            
def logic():
    global motor_drive_inputs
    global sensor_data
    global SIM_RUNNING
    
    prev_sensor_data = None
    SIM_RUNNING = True
    
    while SIM_RUNNING:
        if(not prev_sensor_data == sensor_data):
            prev_sensor_data = sensor_data
            if(sensor_data == b'1,0'):
                motor_drive_inputs = "255,0,1|88,1,0"
                time.sleep(1.222222)
                motor_drive_inputs = "100,0,1|100,1,0"
            #     motor_drive_inputs = "100,0,1|0,0,0"
            #     time.sleep(2.045)
            #     motor_drive_inputs = "255,0,1|255,1,0"
            # elif(sensor_data == b'0,1' or sensor_data == b'0,0'):
            #     motor_drive_inputs = "10,0,1|10,1,0"
            #     time.sleep(3.6)
            #     motor_drive_inputs = "0,0,0|100,1,0"
            #     time.sleep(2.045)
            #     motor_drive_inputs = "255,0,1|255,1,0"
            # elif(sensor_data == b'1,1'):
            #     motor_drive_inputs = "255,0,1|255,1,0"
    

t1 = threading.Thread(name='socket_worker_s',
                      target=motor_drive_inputs_sender)
t2 = threading.Thread(name='socket_worker_r',
                      target=sensor_vals_reciever)
t3 = threading.Thread(name='robot_logic',
                      target=logic)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

exit()

