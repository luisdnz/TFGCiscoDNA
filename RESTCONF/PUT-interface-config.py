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
interface = "interface=GigabitEthernet3"
url = f"https://{distr_rt_1['ip']}:{distr_rt_1['port']}/restconf/data/{module}/{interface}"
payload = {
    "ietf-interfaces:interface":
    {    
        'name' : 'GigabitEthernet3',
        'type' : 'iana-if-type:ethernetCsmacd',
        'description': 'Interfaz creada con Python a traves de RestCONF',
        'enabled' : 'true',
        'ietf-ip:ipv4' : {
            'address' : [
                            {
                            'ip' : '172.16.252.53',
                            'netmask' : '255.255.255.252'
                            }
                        ]
                    },
                'ietf-ip:ipv6' : {}
            }
}

requests.packages.urllib3.disable_warnings()
response = requests.put(url,headers = headers,data=json.dumps(payload), auth = (distr_rt_1["username"], distr_rt_1["password"]), verify=False)
print(response.text)