
from OSPF_DATA.GetOspfData import get_ospf_data
from ROUTING import GetRouting
import networkx as nx
import matplotlib.pyplot as plt
import json
import pprint

from tkinter import * 

r1 = {
    'name':'R1',
    'ip':'10.10.20.100',
    'port':'443',
    'username':'cisco',
    'password':'cisco'
}


r2 = {
    'name':'R2',
    'ip':'10.10.20.2',
    'port':'443',
    'username':'cisco',
    'password':'cisco'
}


r3 = {
    'name':'R3',
    'ip':'10.10.20.3',
    'port':'443',
    'username':'cisco',
    'password':'cisco'
}

r4 = {
    'name':'R4',
    'ip':'10.10.20.4',
    'port':'443',
    'username':'cisco',
    'password':'cisco'
}


r5 = {
    'name':'R5',
    'ip':'10.10.20.5',
    'port':'443',
    'username':'cisco',
    'password':'cisco'
}

routers = [r1,r2,r3,r4,r5]


def plot_spf_tree(router):
    G = nx.Graph()
    G.add_node(r1['name'])
    edge_labels = {}
    
    with open(f"ROUTING/{router['name']}-routing.json", "r") as f:
        routingjson = json.loads(f.read())
    
    routes = routingjson["ietf-routing:routing-state"]["routing-instance"][0]["ribs"]["rib"][0]["routes"]["route"]
    pprint.pprint(routes)

    for route in routes:
        if not "/32" in route["destination-prefix"]:
            dest = route["destination-prefix"]
            interface = route["next-hop"]["outgoing-interface"]
            if "ietf-ospf:ospfv2" == route["source-protocol"]:
                protocol = "O"
                nhop = route["next-hop"]["next-hop-address"]
                metric = route["metric"]
                
            else:
                protocol = "D"
                G.add_node(dest)
                G.add_edge(r1['name'],dest)
                edge_labels[(r1['name'],dest)] = (interface,protocol)

    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, with_labels=True, edgelist=list(G.edges()), node_size=600)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.show()

    
def plot_spf_tree2(router):
    G = nx.Graph()
    G.add_node(r1['name'])
    edge_labels = {}
    
    with open(f"ROUTING/{router['name']}-routing.json", "r") as f:
        routingjson = json.loads(f.read())
    
    routes = routingjson["ietf-routing:routing-state"]["routing-instance"][0]["ribs"]["rib"][0]["routes"]["route"]
    pprint.pprint(routes)

    #Adding directly connected nodes
    for route in routes:
        if not "/32" in route["destination-prefix"]:
            dest = route["destination-prefix"]
            interface = route["next-hop"]["outgoing-interface"]
            if "ietf-routing:direct" == route["source-protocol"]:
                protocol = "D"
                G.add_node(dest)
                G.add_edge(r1['name'],dest)
                edge_labels[(r1['name'],dest)] = (interface,protocol)               

    #Adding indirectly connected nodes
    for route in routes:
        if not "/32" in route["destination-prefix"]:
            dest = route["destination-prefix"]
            interface = route["next-hop"]["outgoing-interface"]
            if "ietf-ospf:ospfv2" == route["source-protocol"]:
                protocol = "D"
                G.add_node(dest)
                G.add_edge(r1['name'],dest)
                edge_labels[(r1['name'],dest)] = (interface,protocol)
    pos = nx.spring_layout(G)
    nx.draw(G, pos=pos, with_labels=True, edgelist=list(G.edges()), node_size=600)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.show()



gui = Tk()
gui.title("Restconf Client")
gui.size=(1080,720)
root = gui.grid()
gui.mainloop()