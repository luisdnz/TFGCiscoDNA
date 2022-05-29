import requests
import json
from pprint import pprint


headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
module = "ietf-interfaces:interfaces"
requests.packages.urllib3.disable_warnings()

def put_interfaces_list(router):
    url = f"https://{router['ip']}:{router['port']}/restconf/data/{module}"
    with open(f"INTERFACES_CONFIG/{router['name']}-interfaces-list-config.json", "r") as f:
        jsonstr = f.read()
    response = requests.put(url,headers = headers,data=jsonstr, auth = (router["username"], router["password"]), verify=False)
