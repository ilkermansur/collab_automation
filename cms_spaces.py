import requests
import urllib3
import xmltodict

urllib3.disable_warnings()

# CMS API'ye bağlanacak bilgiler
cms_url = "https://cms1.dcloud.cisco.com:445/api/v1/"
username = "apiuser"
password = "dCloud123!"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
space_name_list = []

def get_all_spaces(limit=20):
    offset = 0
    total_space = 0

    params = {'offset': offset, 'limit': limit}

    response = requests.get(url=cms_url + '/cospaces/',
                            auth=requests.auth.HTTPBasicAuth(username, password),
                            headers=headers,
                            params=params,
                            verify=False)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:

        data = xmltodict.parse(response.content)
        total_space_int =  (int(data['coSpaces']['@total']))
        loop = (total_space_int // 20) + 1

    i = 0

    while i < loop:
            
        params = {'offset': offset, 'limit': limit}
        response = requests.get(url=cms_url + '/cospaces/',
                                auth=requests.auth.HTTPBasicAuth(username, password),
                                headers=headers,
                                params=params,
                                verify=False)

        data = xmltodict.parse(response.content)
        
        data_list = data['coSpaces']['coSpace']
        for space in data_list :
            space_name_list.append(space['name'])
        i += 1
        offset += 20

    print (space_name_list)
    print (len(space_name_list))

# Example usage to get all spaces
get_all_spaces()
