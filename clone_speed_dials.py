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


def clone_speed_dials(old_phone_device_name, new_phone_device_name):

    try:
        get_phone_info = axl.getPhone (name = old_phone_device_name, returnedTags={'name':'',
                                                                                   'model':'',
                                                                                   'speeddials':{'speeddial':[{
                                                                                       'dirn':'',
                                                                                       'label':'',
                                                                                       'index':''
                                                                                       }]}})

        get_speeddials = get_phone_info['return']['phone']['speeddials']['speeddial']

        axl.updatePhone(name=new_phone_device_name, speeddials= {'speeddial' :get_speeddials})

    except Fault as f:
        print (f)

clone_speed_dials(old_phone_device_name='SEP04EB40B9542C', new_phone_device_name='SEP111122223333')
