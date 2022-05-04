import requests
import json
from pprint import pprint

distr_rt_1 = {
    "ip" : "10.10.20.183",
    "port": "443",
    "username":"cisco",
    "password":"cisco"    
}
headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
module = "ietf-interfaces:interfaces"
url = f"https://{distr_rt_1['ip']}:{distr_rt_1['port']}/restconf/data/{module}"


requests.packages.urllib3.disable_warnings()
response = requests.get(url,headers = headers, auth = (distr_rt_1["username"], distr_rt_1["password"]), verify=False).json()
pprint(response)
with open("RESTCONF/interfaces-list-config.json", "w") as f:
    json.dump(response, f, indent=4)


interfaces = response[module]['interface']
for interface in interfaces:
    if bool(interface['ietf-ip:ipv4']):
        print(f"{interface['name']} -- {interface['description']} -- {interface['ietf-ip:ipv4']['address'][0]['ip']}")