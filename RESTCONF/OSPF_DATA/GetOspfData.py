import requests
import json



headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
module = "Cisco-IOS-XE-ospf-oper:ospf-oper-data"
requests.packages.urllib3.disable_warnings()


def get_ospf_data(router):
    url = f"https://{router['ip']}:{router['port']}/restconf/data/{module}"
    response = requests.get(url,headers = headers, auth = (router["username"], router["password"]), verify=False).json()
    with open(f"OSPF_DATA/{router['name']}-ospf.json", "w") as f:
        json.dump(response, f, indent=4) 
