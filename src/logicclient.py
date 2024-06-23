import socket
import threading

from setupdata import HOST, PORT1, PORT2

def sender():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT1))
        
        prev_motor_drive_inputs = None
        motor_drive_inputs = "255,0,1|255,1,0"

        while True:
            s.sendall(motor_drive_inputs.encode())
            
            print(f"[PLYR] sender(): Sent {motor_drive_inputs}")
            prev_motor_drive_inputs = motor_drive_inputs
            
            acknowledgement = s.recv(1024)
            print(f"[PLYR] sender(): Acknowledgement recieved {acknowledgement}")
            
            if(acknowledgement.decode() == "SIM_COMPLETE"):
                s.close()
                return


def reciever():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT2))
        
        prev_sensor_data = None
        sensor_data = None

        while True:
            prev_sensor_data = sensor_data
            sensor_data = s.recv(1024)
            
            if(sensor_data.decode() == "SIM_COMPLETE"):
                s.close()
                return

            print(f"[PLYR] receiver(): Recieved {sensor_data}")
            s.send("SENSOR_DATA_RECV_ACK".encode())
            print(f"[PLYR] receiver(): Sent SENSOR_DATA_RECV_ACK")

t1 = threading.Thread(name='socket_worker_s',
                      target=sender)
t2 = threading.Thread(name='socket_worker_r',
                      target=reciever)

t1.start()
t2.start()

t1.join()
t2.join()

exit()

