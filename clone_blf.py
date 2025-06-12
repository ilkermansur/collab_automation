from requests import Session
from zeep import Client
from zeep.transports import Transport
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from lxml import etree
from requests.auth import HTTPBasicAuth

disable_warnings(InsecureRequestWarning)

username = 'axluser'
password = '123456'
fqdn = '192.168.85.168'
address = 'https://{}:8443/axl/'.format(fqdn)
wsdl = 'AXLAPI.wsdl'
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
axl = client.create_service(binding, address)

def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))  

########################################### PHONE BLF INFO ###########################################

def phone_blf_info (device_name):
    try:

        get_phone_blf_infos = axl.getPhone (name = device_name)
        
        if get_phone_blf_infos['return']['phone']['busyLampFields'] != None:
            blf_info = get_phone_blf_infos['return']['phone']['busyLampFields']['busyLampField']
            return blf_info
        else: 
            with open ("process_log.txt", "a") as f:
                log = f"there is no blf on {device_name}\n"
                f.write(log)
                return get_phone_blf_infos['return']['phone']['busyLampFields']
    except Fault as f:
        print (f)

########################################### CLONE PHONE BLF ###########################################

def clone_blf_info(device_name, new_device_name):
    try:
        blf_list = phone_blf_info(device_name)
        if blf_list != None:
            axl.updatePhone(name=new_device_name, busyLampFields= {'busyLampField' : blf_list})

            with open ("process_log.txt", "a") as f:
                number_of_blf = len(blf_list)
                log = f" {number_of_blf} adet blf {device_name} den {new_device_name} e taşındı."
                f.write(log)

    except Fault as f:
        print (f)

################################################# USAGE #################################################

if __name__ == "__main__":

    clone_blf_info(device_name="SEP04EB40B9542C", new_device_name="SEP111122223333")
