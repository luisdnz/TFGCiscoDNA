import requests
import json
from pprint import pprint


headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
module = "Cisco-IOS-XE-interfaces-oper:interfaces"
requests.packages.urllib3.disable_warnings()

def get_interfaces_data(router):
    url = f"https://{router['ip']}:{router['port']}/restconf/data/{module}"
    response = requests.get(url,headers = headers, auth = (router["username"], router["password"]), verify=False).json()
    with open(f"INTERFACE_DATA/{router['name']}-interfaces-stats.json", "w") as f:
        json.dump(response, f, indent=4)