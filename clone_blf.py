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
import pandas as pd
import time

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

######################################## READ INFO from EXCEL ########################################      
df = pd.read_excel("blf_device_infos.xlsx")

device_list = df["device_name"].dropna().values.tolist()
new_device_list = df["new_device_name"].dropna().values.tolist()

blf_couple = zip (device_list, new_device_list)

tasinan_blf = 0
boyle_bir_kaynak_cihaz_yok = 0
kaynak_cihazda_blf_yok = 0

########################################### PHONE BLF INFO ###########################################

def phone_blf_info (device_name):

    global kaynak_cihazda_blf_yok, boyle_bir_kaynak_cihaz_yok

    try:
        get_phone_blf_infos = axl.getPhone (name = device_name)
        
        if get_phone_blf_infos['return']['phone']['busyLampFields']:
            blf_info = get_phone_blf_infos['return']['phone']['busyLampFields']['busyLampField']
            return blf_info
        else:
            with open ("process_log.txt", "a") as f:
                log = f"there is no blf on {device_name}\n"
                kaynak_cihazda_blf_yok += 1
                print (sayac())
                f.write(log)

                return get_phone_blf_infos['return']['phone']['busyLampFields']
    except Fault as f:
        with open ("process_log.txt", "a") as f:
            f.write (f"The specified {device_name} was not found\n")
            boyle_bir_kaynak_cihaz_yok += 1
            print (sayac())

            return None


########################################### CLONE PHONE BLF ###########################################

def clone_blf_info(device_name, new_device_name):
    global tasinan_blf
    try:
        blf_list = phone_blf_info(device_name)
        if blf_list:
            axl.updatePhone(name=new_device_name, busyLampFields= {'busyLampField' : blf_list})
            tasinan_blf += 1
            print (sayac())

            with open ("process_log.txt", "a") as f:
                number_of_blf = len(blf_list)
                log = f" {number_of_blf} adet blf {device_name} den {new_device_name} e taşındı.\n"
                f.write(log)

    except Fault as f:
        print (f)

################################################# SAYAC #################################################

def sayac ():
    sayac = f"tasinan_blf_sayisi : {tasinan_blf} - alinan_hata : {boyle_bir_kaynak_cihaz_yok} - Bu cihazda blf yok : {kaynak_cihazda_blf_yok}"
    return sayac
################################################# USAGE #################################################

for device_name, new_device_name in blf_couple:

    clone_blf_info(device_name=device_name, new_device_name=new_device_name)
    time.sleep(2)

print ("islem bitti \n", sayac())