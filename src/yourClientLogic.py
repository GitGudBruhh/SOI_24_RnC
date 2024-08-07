import socket
import threading
import time

from setupdata import HOST, PORT1, PORT2

# This is a test script used to check the functionality of the simulator
# Very very unpredictable and does not give similar results across runs due to timing
# issues commonly found in simulators. To avoid these, use a lower speed for the robot.

poll_time = 0
motor_drive_inputs = "100,0,1|105,1,0" # Set to add slight deviation in path and test path correction
sensor_data = None
SIM_RUNNING = None


def motor_drive_inputs_sender():
    global motor_drive_inputs
    global SIM_RUNNING
    
# --------------------------------------------------------------------------------
# Initialize the socket object
# --------------------------------------------------------------------------------
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT1))
        
        prev_motor_drive_inputs = None
        
    # --------------------------------------------------------------------------------
    # Setup the motor inputs send loop
    # --------------------------------------------------------------------------------

        while True:
            time.sleep(poll_time)
            s.sendall(motor_drive_inputs.encode())
            
            prev_motor_drive_inputs = motor_drive_inputs
            
        # --------------------------------------------------------------------------------
        # Receive the acknowledgement before proceeding
        # --------------------------------------------------------------------------------
            acknowledgement = s.recv(32)
            
        # --------------------------------------------------------------------------------
        # Break if simulation completes
        # --------------------------------------------------------------------------------
            if(acknowledgement.decode() == "SIM_COMPLETE"):
                SIM_RUNNING = False
                s.close()
                return


def sensor_vals_reciever():
    global sensor_data
    global SIM_RUNNING
    
# --------------------------------------------------------------------------------
# Initialize the socket object
# --------------------------------------------------------------------------------
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT2))
        
        prev_sensor_data = None

    # --------------------------------------------------------------------------------
    # Setup the sensor values reciever loop
    # --------------------------------------------------------------------------------
        while True:
            
            prev_sensor_data = sensor_data
            time.sleep(poll_time)
            
        # --------------------------------------------------------------------------------
        # Send the request to the interface
        # --------------------------------------------------------------------------------
            s.send("SENSOR_DATA_REQ".encode())
            
        # --------------------------------------------------------------------------------
        # Receive the sensor data into the global variable [used in logic()]
        # --------------------------------------------------------------------------------
            sensor_data = s.recv(32)
            
            if(sensor_data.decode() == "SIM_COMPLETE"):
                SIM_RUNNING = False
                s.close()
                return
            
def logic():
    global motor_drive_inputs
    global sensor_data
    global SIM_RUNNING
    
    prev_sensor_data = None
    sensor_values = None
    SIM_RUNNING = True
    
# --------------------------------------------------------------------------------
# Setup the logic loop
# --------------------------------------------------------------------------------
    while SIM_RUNNING:
        if(not prev_sensor_data == sensor_data):
            prev_sensor_data = sensor_data
            sensor_values = sensor_data.decode().split(',')
            
        # --------------------------------------------------------------------------------
        # Simple logic to ...
        # --------------------------------------------------------------------------------
            if(len(sensor_values) != 5):
                pass
            
            # Rotate right [this robot is biased toward right turn]
            elif(sensor_values[4] == '0'):
            # elif(sensor_values[0]  == '1' and sensor_values[4]  == '0'):
                motor_drive_inputs = "127,0,1|44,1,0"
                # print("RIGHT")
                time.sleep(1.22222)
                motor_drive_inputs = "127,0,1|127,1,0"
                
                
            # Rotate left
            elif(sensor_values[0]  == '0' and sensor_values[4]  == '1'):
                motor_drive_inputs = "44,0,1|127,1,0"
                # print("LEFT")
                time.sleep(1.22222)
                motor_drive_inputs = "127,0,1|127,1,0"
                
            # Detect and correct path deviation (right)
            elif(sensor_values[1]  == '0' and sensor_values[3]  == '1'):
                motor_drive_inputs = "20,0,1|25,1,0"
                # print("PATH CORRECT, MOVE LEFT")
                time.sleep(0.2)
                motor_drive_inputs = "127,0,1|127,1,0"
            
            # Detect and correct path deviation (left)
            elif(sensor_values[1]  == '1' and sensor_values[3]  == '0'):
                motor_drive_inputs = "25,0,1|20,1,0"
                # print("PATH CORRECT, MOVE RIGHT")
                time.sleep(0.2)
                motor_drive_inputs = "127,0,1|127,1,0"
                
            elif(sensor_values[0] == '1' and
                 sensor_values[1] == '1' and
                 sensor_values[2] == '1' and
                 sensor_values[3] == '1' and
                 sensor_values[4] == '1'):
                motor_drive_inputs = "0,0,0|0,0,0"
                # print("BACKTRACK")
                
    

t1 = threading.Thread(name='motor_drive_inputs_sender',
                      target=motor_drive_inputs_sender)
t2 = threading.Thread(name='sensor_vals_reciever',
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

