import requests
import json
from pprint import pprint


router = {
    "ip" : "10.10.20.1",
    "port": "443",
    "username":"cisco",
    "password":"cisco"    
}

headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
module = "Cisco-IOS-XE-acl-oper:access-lists"
requests.packages.urllib3.disable_warnings()

def put_interfaces_list(router):
    url = f"https://{router['ip']}:{router['port']}/restconf/data/{module}"
    with open(f"ACL/acl-data.json", "r") as f:
        jsonstr = f.read()
    response = requests.put(url,headers = headers,data=jsonstr, auth = (router["username"], router["password"]), verify=False)

put_interfaces_list(router)