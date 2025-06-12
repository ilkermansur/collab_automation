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

def get_blf (device_name):

    try:
        get_phone_blf_infos = axl.getPhone (name = device_name, returnedTags={'name':'',
                                                                                    'model':'',
                                                                                    'busyLampFields': {
                                                                                        'busyLampField': {
                                                                                            'blfDest':'',
                                                                                            'blfDirn':'',
                                                                                            'routePartition':'',
                                                                                            'label': '',
                                                                                            'index': '',
                                                                                            'associatedBlfSdFeatures':{
                                                                                                'feature': ''
                                                                                            }
                                                                                    }
                                                                                    }})
        
        print(get_phone_blf_infos['return']['phone']['busyLampFields']['busyLampField'])
        
    except Fault as f:
        print (f)


def clone_blfdials(old_device_name, new_device_name):

    try:
        get_phone_blf_infos = axl.getPhone (name = old_device_name, returnedTags={'name':'',
                                                                                    'model':'',
                                                                                    'busyLampFields': {
                                                                                        'busyLampField': {
                                                                                            'blfDest':'',
                                                                                            'blfDirn':'',
                                                                                            'routePartition':'',
                                                                                            'label': '',
                                                                                            'index': '',
                                                                                            'associatedBlfSdFeatures':{
                                                                                                'feature': ''
                                                                                            }
                                                                                    }
                                                                                    }})
        
        get_phone_blf = get_phone_blf_infos['return']['phone']['busyLampFields']['busyLampField']

        axl.updatePhone(name=new_device_name, busyLampFields= {'busyLampField' : get_phone_blf})

    except Fault as f:
        print (f)

clone_blfdials(old_device_name='SEP04EB40B9542C', new_device_name='SEP111122223333')
