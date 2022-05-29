import json


with open("OSPF/prueba-ospf.json", "r") as f:
    jsonstr = json.loads(f.read())


ospf_instance = jsonstr['Cisco-IOS-XE-ospf-oper:ospf-oper-data']['ospf-state']['ospf-instance']
router_id = ospf_instance[0]['process-id']
area = ospf_instance[0]['ospf-area'][0]['area-id']
neighbours = ospf_instance[0]['ospf-area'][0]['ospf-interface']

for neighbour in neighbours:
    if('ospf-neighbor' in neighbour.keys()):
        interface = neighbour['name']
        cost = neighbour['cost']
        neighbor_id = neighbour['ospf-neighbor'][0]['neighbor-id']
        neigbor_add = neighbour['ospf-neighbor'][0]['address']
        print(f"Vecino: {neighbor_id} con direccion {neigbor_add} por la interfaz {interface} con coste {cost}.")
        