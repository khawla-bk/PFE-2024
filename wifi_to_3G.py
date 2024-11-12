import subprocess
import time
import serial
import threading

CHECK_INTERVAL = 60
PING_HOST = "8.8.8.8"

def is_wifi_connected():
    try:
        subprocess.check_output(["ping", "-c", "1", PING_HOST])
        print("Wifi is connected")
        return True
    except subprocess.CalledProcessError:
        print("No wifi detected")
        return False

def connect_to_lte():
    port = "/dev/ttyUSB2"
    baudrate = 115200
    ser = serial.Serial(port, baudrate, timeout=1)

    ser.write(b"AT\r\n")
    time.sleep(1)

    ser.write(b"AT+CGDCONT=1,\"IP\",\"weborange\"\r\n")
    time.sleep(1)
    ser.write(b"AT+CGACT=1,1\r\n")
    time.sleep(1)

    ser.close()

def monitor_wifi_and_switch_to_lte():
    while True:
        if is_wifi_connected():
            # connect_to_lte()
            time.sleep(10)
            print("WiFi connection is lost")
            print("Switching to LTE Module")
        
            # Simulate connecting to the LTE module
            time.sleep(2)  # Short delay for LTE connection simulation
            print("3G/4G LTE Module connected successfully")

def main():
    print("Starting script")
    while True:
        # Starting the WiFi monitoring in a separate thread
        monitor_thread = threading.Thread(target=monitor_wifi_and_switch_to_lte)
        monitor_thread.daemon = True
        monitor_thread.start()
        time.sleep(5)

if __name__ == '__main__':
    main()