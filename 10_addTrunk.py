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
fqdn = '192.168.80.100'
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

try:

    addSipTrun_info = axl.addSipTrunk(sipTrunk = {

        'name' : 'Trunk_Test',
        'product' : 'SIP Trunk',
        'protocol' : 'SIP',
        'class' : 'Trunk',
        'protocolSide' : 'Network',
        'devicePoolName' : 'Default',
        'locationName' : 'Hub_None',
        'securityProfileName' : 'Non Secure SIP Trunk Profile',
        'sipProfileName' : 'Standard SIP Profile',
        'presenceGroupName' : 'Standard Presence group',
        'runOnEveryNode' : True,
        'destinations' : {
            'destination' : {
                'addressIpv4' : '192.168.1.1',
                'port' : '5060',
                'sortOrder' : '1'
            }
        } 
    })

except Fault as f:
    print (f)
