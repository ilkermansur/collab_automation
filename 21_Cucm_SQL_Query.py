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

username = 'axl2user'
password = '1Qaz2Wsx'
fqdn = '192.168.91.32'
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


sql_query = """
select de.name as device_profile_name,de.ndescription as description,nu.dnorpattern as directory_number_1,ru.name as route_pattern_1 from device de inner join devicenumplanmap dvm on de.pkid=dvm.fkdevice inner join numplan nu on nu.pkid=dvm.fknumplan inner join routepartition ru on nu.fkroutepartition=ru.pkid where nu.dnorpattern!=''  and de.name not like '%\_%' and de.name not like '%\-%' and de.name not like '% %' and len(nu.dnorpattern)=4 and len(de.name) in (4,6,7,8)
"""

def show_history():
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))  

try:
    result = client.service.executeSQLQuery(sql=sql_query)
    print (result)
    for row in result['return'].row:
        # Her bir satırdaki XML öğelerini açma ve içeriklerine erişme
        for element in row:
            element_name = element.tag
            element_content = element.text
            print(f"{element_name}: {element_content}")
        print()  # Her sıradan sonra bir boş satır ekleyin
except Exception as e:
    print("SQL sorgusu başarısız oldu. Hata:", e)
