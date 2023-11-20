from netmiko import ConnectHandler
import json

netConnect = ConnectHandler (
    device_type = "cisco_xe",
           host = '192.168.80.254',
       username = 'cisco',
       password = 'cisco1',
           port = 22 # Default
)

output = netConnect.send_command('sh ip int brief', use_textfsm= True)

print(json.dumps(output, indent = 4))


