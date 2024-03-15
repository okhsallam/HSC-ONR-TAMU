import serial
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
# Terminate processes using the serial port
terminate_processes_using_port(tty_device)

# Close the serial connection
close_serial_connection(tty_device)
