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

i = 0

def check_calls ():
    global i
    output = netConnect.send_command('sh cube calls all')
    number_of_calls =(output.splitlines()[13])

    calls_int = int(number_of_calls.split(sep= ' ')[4])

    if calls_int > 50 :
        print ("There ara more then 50 calls")
        i = 0
    elif calls_int > 100 :
        print ("There ara more then 100 calls")
        i = 0
    elif calls_int == 0 :
        print ("There is no call")
        i += 1
        print (i)
        if i ==3 :
            print ("Maybe there is a problem")



schedule.every(5).seconds.do(check_calls)

while True:
    schedule.run_pending()
    time.sleep(1)






