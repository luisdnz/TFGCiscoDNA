import requests
import json


headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
module = "Cisco-IOS-XE-native:native/router"
requests.packages.urllib3.disable_warnings()

def put_ospf_config(router):
    url = f"https://{router['ip']}:{router['port']}/restconf/data/{module}"
    with open(f"OSPF_CONFIG/{router['name']}-ospf-config.json", "r") as f:
        jsonstr = f.read()
    response = requests.put(url,headers = headers,data=jsonstr, auth = (router["username"], router["password"]), verify=False)
