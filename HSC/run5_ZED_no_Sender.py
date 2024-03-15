import os 
import Jetson.GPIO as GPIO

import subprocess
import multiprocessing
from multiprocessing import Process, Value
import serial
#%%
def reset_ttyacm0(port='/dev/ttyACM0', baudrate=9600, timeout=1):
    try:
        # Open the serial port
        ser = serial.Serial(port, baudrate, timeout=timeout)

        # Send a break signal to reset the device
        ser.send_break(duration=0.25)

        # Close the serial port
        ser.close()

        print(f"Reset {port} successful.")

    except serial.SerialException as e:
        print(f"Error: {e}")

#%%
# Pin numbering
Jetson_Ready_pin = 7
Recording_pin = 11
RaspberryPi_Pin = 13
Toggle_switch = 15

GPIO.setmode(GPIO.BOARD)

GPIO.setup(Jetson_Ready_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(Recording_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RaspberryPi_Pin, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(Toggle_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

current_directory = os.getcwd()
shell_script_name = "run_cltool.sh"
shell_script_path = os.path.join(current_directory, shell_script_name)

exit_flag = Value('b', False)  # Shared flag to signal process termination
bash_process = None

#%%  closing a cltool module

import psutil

def close_serial_connection(port):
    try:
        ser = serial.Serial(port)
        ser.close()
        print(f"Serial connection on {port} closed successfully.")
    except serial.SerialException as e:
        print(f"Error closing serial connection on {port}: {e}")


# Function to find and terminate processes using the given serial port
def terminate_processes_using_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if f"{port}" in ' '.join(proc.info['cmdline']):
            print(f"Terminating process {proc.info['pid']} using {port}")
            proc.terminate()



# Replace 'ttyACM0' with your actual TTY device path
tty_device = '/dev/ttyACM0'
#tty_device_Radio = '/dev/ttyACM1'

#%%  cltool bash script run in a seperate subprocess Guided by a  multiprocessing for parallel control
def run_bash_script(exit_flag):
    while not exit_flag.value:
        subprocess.run(["bash", shell_script_path])

#%%  Toggle switch action code 
def record(channel):
    global bash_process
    global Sender_Code
    
    if GPIO.input(Toggle_switch) == GPIO.HIGH:
        # Create ZED code sub process
        ZED_Code = multiprocessing.Process(target=lambda: exec(open("Tracking_ZED.py").read()))
        if not bash_process or not bash_process.is_alive():
            print("Recording data")
            GPIO.output(Recording_pin, GPIO.HIGH)
            GPIO.output(RaspberryPi_Pin, GPIO.HIGH)
            exit_flag.value = False
            bash_process = Process(target=run_bash_script, args=(exit_flag,))
            bash_process.start()
            print("Process started")
            
            # Run the Radio sender code 
            ZED_Code.start()
    else:
        
#        terminate_processes_using_port(tty_device_Radio)
        
        if bash_process and bash_process.is_alive():
            print("Terminating recording")
            GPIO.output(Jetson_Ready_pin, GPIO.LOW)
            GPIO.output(Recording_pin, GPIO.LOW)
            GPIO.output(RaspberryPi_Pin, GPIO.LOW)
           

            exit_flag.value = True
#            if bash_process.is_alive():
            terminate_processes_using_port(tty_device)

              # Close the serial connection
            close_serial_connection(tty_device)
            GPIO.output(Jetson_Ready_pin, GPIO.HIGH)
#            else:
#                print("Process terminated successfully")
#                GPIO.output(Jetson_Ready_pin, GPIO.HIGH)
            
            # Reset the process to allow it to be recreated when the toggle switch is turned on again
            bash_process = None
            exit_flag.value = False

try:
    GPIO.add_event_detect(Toggle_switch, GPIO.BOTH, callback=record)
    while True:
        pass

except KeyboardInterrupt:
    
    
    GPIO.output(Jetson_Ready_pin, GPIO.LOW)
    GPIO.output(Recording_pin, GPIO.LOW)
    GPIO.output(RaspberryPi_Pin, GPIO.LOW)
    GPIO.cleanup()
