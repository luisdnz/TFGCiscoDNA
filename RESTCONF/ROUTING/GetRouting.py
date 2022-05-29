import requests
import json
from pprint import pprint


headers = {
    "Accept" : "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
module = "ietf-routing:routing-state"
requests.packages.urllib3.disable_warnings()

def get_routing(router):
    url = f"https://{router['ip']}:{router['port']}/restconf/data/{module}"
    response = requests.get(url,headers = headers, auth = (router["username"], router["password"]), verify=False).json()
    with open(f"ROUTING/{router['name']}-routing.json", "w") as f:
        json.dump(response, f, indent=4)
    routing_instances = response['ietf-routing:routing-state']['routing-instance']
    print(f"Tabla de rutas de {router['name']}")
    for instance in routing_instances:
        if instance['type'] == 'ietf-routing:default-routing-instance':
            routes = instance['ribs']['rib'][0]['routes']['route']
            for route in routes:
                network = route['destination-prefix']
                protocol = route['source-protocol']
                metric = route['metric']
                via = route['next-hop']['next-hop-address']
                interface = route['next-hop']['outgoing-interface']
                if protocol == "ietf-ospf:ospfv2":
                    print(f"Ruta a {network} asignada por OSPF via {via} [{metric}] por la interfaz {interface}")
                else:
                    print(f"Ruta a {network} conectada de forma directa por la interfaz {interface}")
            print("\n")



