from netmiko import ConnectHandler
import json

netConnect = ConnectHandler (
    device_type = "cisco_xe",
           host = '192.168.80.254',
       username = 'cisco',
       password = 'cisco1',
           port = 22 # Default
)

config_lines = [
    'conf t',
    'inter Gi 2',
    'description configured_by_python',
]

config = netConnect.send_config_set(config_lines)

output = netConnect.send_command ('show interface description', use_textfsm= True)
print(json.dumps(output, indent = 4))


