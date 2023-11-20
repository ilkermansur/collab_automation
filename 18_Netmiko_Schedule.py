from netmiko import ConnectHandler
import schedule
import time


device = { 'device_type' : "cisco_xe",
                  'host' : '192.168.80.254',
              'username' : 'cisco',
              'password' : 'cisco1',
                  'port' : 22 # Default
}

def check_device_config():
    try:
        # Establish an SSH connection to the device
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()  # Enter enable mode if required
            # Send a command and retrieve the output (e.g., show running-config)
            output = net_connect.send_command('show running-config')
            print(output)  # You might want to log this instead of printing
    except Exception as e:
        print("Failed to connect to the device:", e)

# Schedule the check_device_config function to run every 30 minutes
schedule.every(30).minutes.do(check_device_config)

while True:
    schedule.run_pending()
    time.sleep(1)

