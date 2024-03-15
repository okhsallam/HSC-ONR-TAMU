import os
import serial
from ublox_gps import UbloxGps

port = serial.Serial('/dev/ttyACM2', baudrate=9600, timeout=1)
gps = UbloxGps(port)

#%%
import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

Toggle_switch = 15
GPIO.setup(Toggle_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#%%  Create a results folder 
folder_name = "RTK_GNSS"
# Check if the folder exists
if not os.path.exists(folder_name):
    # Create the folder if it doesn't exist
    os.makedirs(folder_name)

import os

def create_next_available_textfile(base_name):
    index = 1
    while True:
        file_name = f"{base_name}_{index}.txt"
        if not os.path.exists(file_name):
            file  = open(file_name, "a") 
            break
        index += 1
        
    return file

# Specify the base name for the text files
base_name =folder_name + "/RTK_GNSS"

# Call the function to create the next available text file
file = create_next_available_textfile(base_name)
    
#%% 
#def run():

try:
    print("Listening for UBX Messages")
    while True:
        try:
#                print(gps.stream_nmea())
            file.write(gps.stream_nmea())
            if GPIO.input(Toggle_switch) == GPIO.LOW:
                port.close()
                break
        
        except (ValueError, IOError) as err:
            print(err)
            
            
        except KeyboardInterrupt:
            # Close the COM port on keyboard interrupt (Ctrl+C)
            port.close()
            print("COM port closed.")

finally:
    port.close()


#if __name__ == '__main__':
#    run()
    
    