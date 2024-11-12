import time
import threading

def simulate_wifi_and_lte():
    wifi_connected = True  # Start with WiFi connected

    while True:
        if wifi_connected:
            print("WiFi is connected")
            time.sleep(10)  # Stay connected to WiFi for 10 seconds
            print("WiFi connection is lost")
            print("Switching to LTE Module")
            
            # Simulate connecting to the LTE module
            time.sleep(2)  # Short delay for LTE connection simulation
            print("3G/4G LTE Module connected successfully")

            # Switch to LTE for the next cycle
            wifi_connected = False
            time.sleep(10)  # Stay with LTE for 10 seconds

        else:
            print("WiFi connection established")
            wifi_connected = True
            time.sleep(10)  # Stay connected to WiFi for another 10 seconds

def main():
    print("Starting script")
    # Start the WiFi and LTE simulation in a separate thread
    monitor_thread = threading.Thread(target=simulate_wifi_and_lte)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Keep the main thread running
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
