from netmiko import ConnectHandler
import schedule
import time

netConnect = ConnectHandler (
    device_type = "cisco_xe",
           host = '192.168.80.254',
       username = 'cisco',
       password = 'cisco1',
           port = 22 # Default
)


output = netConnect.send_command('sh cube calls all')
calls = int(output.splitlines()[13].split(sep=' ')[4])
print (calls)





