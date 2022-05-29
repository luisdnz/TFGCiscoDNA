import requests
import json
from pprint import pprint

router = {
    "ip" : "10.10.20.2",
    "port": "443",
    "username":"cisco",
    "password":"cisco"    
}
headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
module = "Cisco-IOS-XE-native:native/router"
requests.packages.urllib3.disable_warnings()

def get_ospf_config(router):
    url = f"https://{router['ip']}:{router['port']}/restconf/data/{module}"
    response = requests.get(url,headers = headers, auth = (router["username"], router["password"]), verify=False).json()
    with open(f"OSPF_CONFIG/{router['name']}-ospf-config.json", "w") as f:
        json.dump(response, f, indent=4)
