from requests import Session
from zeep import Client
from zeep.transports import Transport
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from lxml import etree
from requests.auth import HTTPBasicAuth

disable_warnings(InsecureRequestWarning)

username = 'axl_user'
password = 'Aa123456'
fqdn = '192.168.85.90'
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


#####################################################################################################################

def list_group_phone (device_name = '%'):
    """
    The function `list_group_phone` retrieves a list of phones based on a search criteria and then
    checks the associated end user for each phone.
    
    :param device_name: The `list_group_phone` function seems to be querying a list of phones based on
    the provided `device_name` parameter. It then iterates through the list of phones and calls the
    `check_associated_enduser` function for each phone, defaults to % (optional)
    """

    try:

        all_phone = axl.listPhone(searchCriteria={'name':device_name}, returnedTags={'name':''})

        list_phone = all_phone['return']['phone']

        for phone in list_phone:
            device_name = phone['name']
            check_associated_enduser(device_name)

    except Fault as f:
        print (f)
        show_history()

#####################################################################################################################

def check_associated_enduser(device_name):
    """
    This Python function checks if a phone is associated with an end user and prints the user ID if it
    is, otherwise it prints a message indicating that the phone is not associated with any user.
    
    :param device_name: It looks like the code snippet you provided is a Python function that checks the
    associated end user of a phone based on the phone's name. The function uses the `axl.getPhone`
    method to retrieve information about the phone, specifically the associated end user
    """
    try:

        get_phone = axl.getPhone (name=device_name, returnedTags = 
                                {'lines': {
                                    'line': {
                                        'associatedEndusers': {
                                            'enduser':{
                                                'userId':''
                                            }
                                        }
                                    }
                                }
                            }
                        )

        associated_enduser = get_phone['return']['phone']['lines']['line'][0]['associatedEndusers']

        if associated_enduser != None:

            associated_enduser = get_phone['return']['phone']['lines']['line'][0]['associatedEndusers']['enduser'][0]['userId']
            print (f'{associated_enduser} kullanıcısı ile  {device_name} ilişkilendirilmiş')

        else:
            print ('*****************************************************************************')
            print (f'{device_name} herhangi bir kullanıcısı ile ilişkilendirilmemiş')
            
            userid, pattern = get_owner_user_id_and_pattern(device_name)

            update_associated_user(device_name=device_name, userid=userid, pattern = pattern)
    
    except Fault as f:
        print (f)
        show_history()

#####################################################################################################################

def get_owner_user_id_and_pattern(device_name):

    get_phone = axl.getPhone (name=device_name, returnedTags = {
                                                            'name':'',
                                                            'ownerUserName':'',
                                                            'lines' : {
                                                                'line' : [{
                                                                    'index' : 1,
                                                                    'dirn' : {
                                                                        'pattern' : ''
                                                                    }
                                                            }]
                                                            }
                                                            }
                                                            )
    userid = get_phone ['return']['phone']['ownerUserName']['_value_1']
    pattern = get_phone ['return']['phone']['lines']['line'][0]['dirn']['pattern']

    return userid, pattern

#####################################################################################################################


def update_associated_user(device_name, pattern, userid):
    try:
        update_phone = axl.updatePhone(
            name=device_name,
            lines={
                'line': [
                    {
                        'index': 1,
                        'dirn': {
                            'pattern': pattern,
                            'routePartitionName': 'pt_a'
                        },
                        'associatedEndusers': {
                            'enduser': [   # Küçük harf ve dizi (liste) olarak tanımlandı.
                                {
                                    'userId': userid
                                }
                            ]
                        }
                    }
                ]
            }
        )
        print("Telefon güncellemesi başarılı!")
    except Exception as e:
        print("Bir hata oluştu:", e)
        show_history()


list_group_phone(device_name='%')
