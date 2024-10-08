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
        if not is_wifi_connected():
            print("WiFi connection lost. Switching to LTE...")
            connect_to_lte()
            time.sleep(10)
        else:
            print("WiFi is connected.")
            time.sleep(CHECK_INTERVAL)

def main():
    while True:
        print("Starting script")
        # Starting the WiFi monitoring in a separate thread
        monitor_thread = threading.Thread(target=monitor_wifi_and_switch_to_lte)
        monitor_thread.daemon = True
        monitor_thread.start()
        time.sleep(2)

if __name__ == '__main__':
    main()