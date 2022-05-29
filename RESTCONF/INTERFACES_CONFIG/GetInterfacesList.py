import requests
import json
from pprint import pprint


headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
module = "ietf-interfaces:interfaces"
requests.packages.urllib3.disable_warnings()

def get_interfaces_list(router):
    url = f"https://{router['ip']}:{router['port']}/restconf/data/{module}"
    response = requests.get(url,headers = headers, auth = (router["username"], router["password"]), verify=False).json()
    with open(f"INTERFACES_CONFIG/{router['name']}-interfaces-list-config.json", "w") as f:
        json.dump(response, f, indent=4)
