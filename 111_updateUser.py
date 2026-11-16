
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
password = '1Qaz2Wsx'
fqdn = '198.18.133.3'
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

def add_device_to_user(userid, new_device_name):
    try:
        user_info = axl.getUser(
            userid=userid,
            returnedTags={'associatedDevices': {'device': ''}}
        )
        
        current_devices = []
        assoc = user_info['return']['user'].get('associatedDevices')
        if assoc and assoc.get('device'):
            current_devices = list(assoc['device'])

        if new_device_name not in current_devices:
            current_devices.append(new_device_name)

            resp = axl.updateUser(
                userid=userid,
                associatedDevices={
                    'device': current_devices
                }
            )
            print(f"{userid} güncellendi. UUID: {resp['return']}")
        else:
            print(f"{new_device_name} zaten {userid} kullanıcısına tanımlı.")

    except Fault as f:
        print(f"AXL Hatası ({userid}): {f}")
        show_history()
