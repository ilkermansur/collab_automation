import requests
import urllib3

def traversal_zone_info (ip_addr,username, password):
    try:
        url = f"https://{ip_addr}/api/provisioning/controller/zone/traversalclient"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get (url, auth=(username, password), verify=False)
        trversal_info = response.json()
        return print (trversal_info)

    except requests.exceptions.RequestException as e:
        print (e)

def sysinfo (ip_addr,username,password):
    try:
        url = f"https://{ip_addr}/api/provisioning/sysinfo"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url=url,auth=(username,password),verify=False)
        sysinfo = response.json()
        return print (sysinfo)
    except requests.exceptions.RequestException as e:
        print (e)

def license (ip_addr,username,password):
    try:
        url = f"https://{ip_addr}/api/status/common/smartlicensing/licensing"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url=url,auth=(username,password),verify=False)
        license = response.json()
        return print (license)
    except requests.exceptions.RequestException as e:
        print (e)

def dns_info (ip_addr,username,password):
    try:
        
        url = f"https://{ip_addr}/api/v1/provisioning/common/dns/dnsserver"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url=url,auth=(username,password),verify=False)
        dns_info = response.json()
        print (dns_info)
    except requests.exceptions.RequestException as e:
        print (e)

def add_ntp (ip_addr,username,password,data_ntp):
    try:
        url = f"https://{ip_addr}/api/v1/provisioning/common/time/ntpserver"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(url=url,auth=(username,password),verify=False,json=data_ntp)
        print (response)
        return response.reason

    except requests.exceptions.RequestException as e:
        print (e)

def ntp_info (ip_addr,username,password):
    try:
        url = f"https://{ip_addr}/api/v1/provisioning/common/time/ntpserver"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url=url,auth=(username,password),verify=False)
        print (response.json())# 

    except requests.exceptions.RequestException as e:
        print (e)

"""
data_ntp = {
"index": 3,
"Address": "10.0.0.3",
"KeyId": 1,
"Hash": "sha1",
"Authentication": "disabled"
}

add_ntp("192.168.80.121","admin","admin",data_ntp)

"""
