import serial
import time 
import os 
import numpy as np
import Jetson.GPIO as GPIO
import sys
#%%
GPIO.setmode(GPIO.BOARD)

Toggle_switch = 15
GPIO.setup(Toggle_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#%%
com_port = '/dev/ttyACM1'

ser = serial.Serial(port=com_port, baudrate=9600, timeout=1)

#%% Get the message  

def get_message(): 
    Path  =  'IS_logs'
    # Get the last directory
    directories = [d for d in os.listdir(Path) if os.path.isdir(os.path.join(Path, d))]
    directories = sorted(directories)
    all_files = os.listdir(Path + '/' + directories[-1])
    # Filter files with the specified ending
    target_files = [file for file in all_files if file.endswith('0001_DID_INS_1.csv')]


    target_file_path = os.path.join(target_files[0])

    # Open the file and read the last line
    with open(Path + '/' + directories[-1]+'/'+target_file_path, 'r') as file:
        last_line = file.readlines()[-2]
        last_line =last_line.strip().split(',')

    Lat  = last_line[3]
    Lon = last_line[4]
    Heading =  last_line[11]
    u = last_line[13]
    v = last_line[14]
    U = str(np.sqrt(float(u)**2 + float(v)**2))
    # message =  [Lat, Lon,Heading, u,v]
    message =  Lat+   ','+Lon+','+Heading+','+ U
    # Encode the message to bytes
    message = bytes(message, 'utf-8')
    return message
#%%
try:
    while True:
        time.sleep(2)
        ser.write(get_message())
        print(GPIO.input(Toggle_switch))
        if GPIO.input(Toggle_switch) == GPIO.LOW:
            ser.close()
            break

except KeyboardInterrupt:
    # Close the COM port on keyboard interrupt (Ctrl+C)
    ser.close()
    print("COM port closed.")
    
#except GPIO.input(Toggle_switch) == GPIO.LOW:
#     print('hello')
#     ser.close()
#     sys.exit(1)
    









