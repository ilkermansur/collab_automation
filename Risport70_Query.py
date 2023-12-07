"""
__author__   = ilker MANSUR imansur@btegitim.com
__purpose__  = Check agents and route call to alternate anoncement
__version__  = 1.0

"""

# Import Library
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
import schedule
from netmiko import ConnectHandler
import time

# Credential for CUCM AXL Application user
axlusername = 'axladmin'
axlpassword = '1Qaz2Wsx'
fqdn = '192.168.80.100'

# Credential for CUBE SSH
username = 'axladmin'
password = '1Qaz2Wsx'
host = '192.168.80.100'

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(axlusername, axlpassword)
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
wsdl = f'https://{fqdn}:8443/realtimeservice2/services/RISService70?wsdl'
  
disable_warnings(InsecureRequestWarning)

client = Client(wsdl=wsdl, transport=transport,plugins=[history])
service = client.create_service('{http://schemas.cisco.com/ast/soap}RisBinding',
                                f'https://{fqdn}:8443/realtimeservice2/services/RISService70')


cube_info = {'device_type' : 'cisco_xe',
             'host' : host,
             'username' : username,
             'password' : password}


def check_agent ():

    jabber_devices = ['CSFagent01','CSFAgent02']
    status_list = []


    for device in jabber_devices:

        cm_selection_criteria = {
        'MaxReturnedDevices': '1000',
        'DeviceClass': 'Any',
        'Model': '255', # any model
        'Status': 'Any',
        'NodeName': '',
        'SelectBy': 'Name',
        'SelectItems': {
            'item': device
        },
        'Protocol': 'Any',
        'DownloadStatus': 'Any'
    }

        try:
            phone_query_response = service.selectCmDevice(StateInfo='', CmSelectionCriteria=cm_selection_criteria)
            status = phone_query_response['SelectCmDeviceResult']['CmNodes']['item'][0]['CmDevices']['item'][0]['LinesStatus']['item'][0]
            status_list.append(status['Status'])

        except Fault as f:
            print (f)

    if 'Registered' in status_list:
        print ('herşey ok')
 
    else :
        alternate_anons_enable()
        with open ('event_log.txt', 'a') as f:
            f.write (time.asctime())
            f.write(status)
            f.write ('alternative announcement has been activated')


schedule.every(5).seconds.do(check_agent)

def alternate_anons_enable ():
    config_set = ['dial-peer voice 1111', 'no shutdown']
    cube_connect = ConnectHandler(**cube_info)
    cube_connect.send_config_set(config_set)
    
def alternate_anons_disable ():
    config_set = ['dial-peer voice 1111', 'shutdown']
    cube_connect = ConnectHandler(**cube_info)
    cube_connect.send_config_set(config_set)
"""
while True:
    schedule.run_pending()
    time.sleep(1)
"""

check_agent()