
from INTERFACES_CONFIG.GetInterfacesList import get_interfaces_list
from OSPF_DATA.GetOspfData import get_ospf_data
from OSPF_CONFIG.GetOspfConfig import get_ospf_config
from INTERFACE_DATA.GetInterfaceData import get_interfaces_data 
from NAT_CONFIG.GetNatConfig import get_nat_config
from NAT_DATA.GetNatData import get_nat_data
from DHCP_CONFIG.GetDhcpConfig import get_dhcp_config
from DHCP_DATA.GetDhcpData import get_dhcp_data
#from ACL.GetAclConfig import *
from RESOURCES import *
from ROUTING.GetRouting import get_routing

import networkx as nx
import matplotlib.pyplot as plt
import json
import pprint

from tkinter import * 
from tkinter import ttk

r1 = {
    'name':'R1',
    'ip':'10.10.20.1',
    'port':'443',
    'username':'cisco',
    'password':'cisco',
    'id' : "1.1.1.1"
}


r2 = {
    'name':'R2',
    'ip':'10.10.20.2',
    'port':'443',
    'username':'cisco',
    'password':'cisco',
    'id' : "2.2.2.2"
}


r3 = {
    'name':'R3',
    'ip':'10.10.20.3',
    'port':'443',
    'username':'cisco',
    'password':'cisco',
    'id' : "3.3.3.3"
}

r4 = {
    'name':'R4',
    'ip':'10.10.20.4',
    'port':'443',
    'username':'cisco',
    'password':'cisco',
    'id' : "4.4.4.4"
}


r5 = {
    'name':'R5',
    'ip':'10.10.20.5',
    'port':'443',
    'username':'cisco',
    'password':'cisco',
    'id' : "5.5.5.5"
}

routers = [r1,r2,r3,r4,r5]
lsa_names  = {}

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

def transpose_2nlist(l):
    l2 = []
    for columna in range(len(l[0])):
        aux = []
        for fila in range(len(l)):
            aux.append(l[fila][columna])
        l2.append(tuple(aux))
    return l2





class Table: 
    def __init__(self,root,data,n_rows,n_columns): 
        for i in range(n_rows): 
            for j in range(len(data[i])): 
                  
                self.e = Entry(root, width=22, fg='blue', 
                               font=('Arial',16,'bold')) 
                  
                self.e.grid(row=i, column=j) 
                self.e.insert(END, data[i][j]) 
        

  
 
    
   


class ClientGUI(Frame):
    
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args,**kwargs)
        self.parent = master
        self.grid()
        self.createWidgets()
        self.IConfBut=None
        self.DDataBut=None
        self.NConfBut=None
        self.IDataBut=None
        self.OConfBut=None
        self.ODataBut=None
        self.NDataBut=None
        self.DConfBut=None
        self.LIBut=None
        self.LDBut=None
        self.RBut = None
    
    def createWidgets(self):
        self.R1Button = Button(self, font=("Arial", 12), fg='Black', text="R1", highlightbackground='red', command=lambda: self.display_unique_options("R1"))
        self.R1Button.config(height=2,width=10)
        self.R1Button.grid(row=1, column=0, sticky="nsew")

        self.R2Button = Button(self, font=("Arial", 12), fg='Black', text="R2", highlightbackground='red', command=lambda: self.display_options("R2"))
        self.R2Button.config(height=2,width=10)
        self.R2Button.grid(row=2, column=0, sticky="nsew")

        self.R3Button = Button(self, font=("Arial", 12), fg='Black', text="R3", highlightbackground='red', command=lambda: self.display_options("R3"))
        self.R3Button.config(height=2,width=10)
        self.R3Button.grid(row=3, column=0, sticky="nsew")

        self.R4Button = Button(self, font=("Arial", 12), fg='Black', text="R4", highlightbackground='red', command=lambda: self.display_options("R4"))
        self.R4Button.config(height=2,width=10)
        self.R4Button.grid(row=4, column=0, sticky="nsew")

        self.R5Button = Button(self, font=("Arial", 12), fg='Black', text="R5", highlightbackground='red', command=lambda: self.display_unique_options("R5"))
        self.R5Button.config(height=2,width=10)
        self.R5Button.grid(row=5, column=0, sticky="nsew")

        self.AButton = Button(self, font=("Arial", 12), fg='Black', text="All", highlightbackground='red', command=lambda: self.display_options("All"))
        self.AButton.config(height=2,width=10)
        self.AButton.grid(row=6, column=0, sticky="nsew")

        self.TButton = Button(self, font=("Arial", 12), fg='Black', text="Listeners", highlightbackground='red', command=lambda: self.display_listener_options())
        self.TButton.config(height=2,width=10)
        self.TButton.grid(row=7, column=0, sticky="nsew")

    def deleteWidgets(self):
            if self.IConfBut != None:
                self.IConfBut.destroy()
                self.IConfBut=None
            if self.DDataBut != None:
                self.DDataBut.destroy()
                self.DDataBut=None
            if self.NConfBut != None:
                self.NConfBut.destroy()
                self.NConfBut=None
            if self.IDataBut != None:
                self.IDataBut.destroy()
                self.IDataBut=None
            if self.OConfBut != None:
                self.OConfBut.destroy()
                self.OConfBut=None
            if self.ODataBut != None:
                self.ODataBut.destroy()
                self.ODataBut=None
            if self.NDataBut != None:
                self.NDataBut.destroy()
                self.NDataBut=None
            if self.DConfBut != None:
                self.DConfBut.destroy()
                self.DConfBut=None
            if self.LIBut != None:
                self.LIBut.destroy()
                self.LIBut=None
            if self.LDBut != None:
                self.LDBut.destroy()
                self.LDBut=None
            if self.RBut != None:
                self.RBut.destroy()
                self.RBut = None
            


    def display_unique_options(self,r):
        self.deleteWidgets()
        self.IConfBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} Interfaces Config", highlightbackground='red', command=lambda: self.display_interface_config(r))
        self.IConfBut.config(height=2,width=15)
        self.IConfBut.grid(row=1, column=1, sticky="nsew")

        if r == "R5":
            self.DConfBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} DHCP Config", highlightbackground='red', command=lambda: self.display_dhcp_config(r))
            self.DConfBut.config(height=2,width=15)
            self.DConfBut.grid(row=2, column=1, sticky="nsew")

            self.DDataBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} DHCP Data", highlightbackground='red', command=lambda: self.display_dhcp_data(r))
            self.DDataBut.config(height=2,width=15)
            self.DDataBut.grid(row=2, column=2, sticky="nsew")

        if r == "R1":
            self.NConfBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} NAT Config", highlightbackground='red', command=lambda: self.display_nat_config(r))
            self.NConfBut.config(height=2,width=15)
            self.NConfBut.grid(row=2, column=1, sticky="nsew")
            self.NDataBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} NAT Data", highlightbackground='red', command=lambda: self.display_nat_data(r))
            self.NDataBut.config(height=2,width=15)
            self.NDataBut.grid(row=2, column=2, sticky="nsew")

        self.OConfBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} OSPF Config", highlightbackground='red', command=lambda: self.display_ospf_config(r))
        self.OConfBut.config(height=2,width=15)
        self.OConfBut.grid(row=3, column=1, sticky="nsew")

        self.IDataBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} Interfaces Data", highlightbackground='red', command=lambda: self.display_interf_data(r))
        self.IDataBut.config(height=2,width=15)
        self.IDataBut.grid(row=1, column=2, sticky="nsew")

        self.ODataBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} OSPF Data", highlightbackground='red', command=lambda: self.display_ospf_data(r))
        self.ODataBut.config(height=2,width=15)
        self.ODataBut.grid(row=3, column=2, sticky="nsew")

        self.RBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} Routing", highlightbackground='red', command=lambda: self.display_routing(r))
        self.RBut.config(height=2,width=15)
        self.RBut.grid(row=4, column=1, sticky="nsew")

    def display_options(self, r):
        self.deleteWidgets()
        self.IConfBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} Interfaces Config", highlightbackground='red', command=lambda: self.display_interface_config(r))
        self.IConfBut.config(height=2,width=15)
        self.IConfBut.grid(row=1, column=1, sticky="nsew")
       
        self.OConfBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} OSPF Config", highlightbackground='red', command=lambda: self.display_ospf_config(r))
        self.OConfBut.config(height=2,width=15)
        self.OConfBut.grid(row=2, column=1, sticky="nsew")

        self.IDataBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} Interfaces Data", highlightbackground='red', command=lambda: self.display_interf_data(r))
        self.IDataBut.config(height=2,width=15)
        self.IDataBut.grid(row=1, column=2, sticky="nsew")

        self.ODataBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} OSPF Data", highlightbackground='red', command=lambda: self.display_ospf_data(r))
        self.ODataBut.config(height=2,width=15)
        self.ODataBut.grid(row=2, column=2, sticky="nsew")

        if r!="All":
            self.RBut = Button(self,font=("Arial", 12), fg='Black', text=f"{r} Routing", highlightbackground='red', command=lambda: self.display_routing(r))
            self.RBut.config(height=2,width=15)
            self.RBut.grid(row=3, column=1, sticky="nsew")



    def display_listener_options(self):
        self.deleteWidgets()
        self.LIBut = Button(self,font=("Arial", 12), fg='Black', text=f"Listener Interfaces", highlightbackground='red', command=lambda: self.display_listener_interf())
        self.LIBut.config(height=2,width=15)
        self.LIBut.grid(row=1, column=1, sticky="nsew")

        self.LDBut = Button(self,font=("Arial", 12), fg='Black', text=f"Listener DHCP Pools", highlightbackground='red', command=lambda: self.display_interface_config(r))
        self.LDBut.config(height=2,width=15)
        self.LDBut.grid(row=1, column=2, sticky="nsew")
        

    def display_listener_interf(self):
        root = Tk()
        text = Text(root,width=60,height = 2)
        text.pack()
        text.insert(INSERT,"Interface GigabitEthernet4 in R1 went from Up/Up to Down")

    
    def display_interface_config(self, r):
        if r!="All": 
            for router in routers:
                if r == router['name']:
                    get_interfaces_list(router)
                    with open(f"INTERFACES_CONFIG/{router['name']}-interfaces-list-config.json", "r") as f:
                        json_i = json.loads(f.read())
                    
                    data = [("Interface", "Status", "IPv4", "Netmask", "IPv6", "Netmask")]
                    for interface in json_i["ietf-interfaces:interfaces"]["interface"]:
                        name = interface['name']
                        status = "Up/Up" if interface['enabled']==1 else "Down"
                        ipv4 = "Not Set"
                        maskv4 = "Not Set"
                        ipv6 = "Not Set"
                        maskv6 = "Not Set"
                        if len(interface["ietf-ip:ipv4"])>0:
                            ipv4 = interface["ietf-ip:ipv4"]["address"][0]['ip']
                            maskv4 = interface["ietf-ip:ipv4"]["address"][0]['netmask']
                        if len(interface["ietf-ip:ipv6"])>0:
                            ipv6 = interface["ietf-ip:ipv6"]["address"][0]['ip']
                            maskv6 = interface["ietf-ip:ipv6"]["address"][0]['netmask']
                        interf = (name, status, ipv4, maskv4, ipv6, maskv6)
                        data.append(interf)
                    self.tp = Toplevel()
                    self.tp.title('All Router Interfaces')
                    self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in data[0]])
                    self.tree.config(show='headings')
                    self.tree.grid(row=0, column=0)
                    for i in range(len(data)):
                        self.tree.insert('',index = i, values=data[i])
        else:
            cabecera = ("Router","Interface", "Status", "IPv4", "Netmask", "IPv6", "Netmask")
            data = [("Router","Interface", "Status", "IPv4", "Netmask", "IPv6", "Netmask")]
            for router in routers:
                get_interfaces_list(router)
                with open(f"INTERFACES_CONFIG/{router['name']}-interfaces-list-config.json", "r") as f:
                    json_i = json.loads(f.read())
                    
                
                for interface in json_i["ietf-interfaces:interfaces"]["interface"]:
                    name = interface['name']
                    status = "Up/Up" if interface['enabled']==1 else "Down"
                    ipv4 = "Not Set"
                    maskv4 = "Not Set"
                    ipv6 = "Not Set"
                    maskv6 = "Not Set"
                    if len(interface["ietf-ip:ipv4"])>0:
                        ipv4 = interface["ietf-ip:ipv4"]["address"][0]['ip']
                        maskv4 = interface["ietf-ip:ipv4"]["address"][0]['netmask']
                    if len(interface["ietf-ip:ipv6"])>0:
                        ipv6 = interface["ietf-ip:ipv6"]["address"][0]['ip']
                        maskv6 = interface["ietf-ip:ipv6"]["address"][0]['netmask']
                    interf = (router['name'],name, status, ipv4, maskv4, ipv6, maskv6)
                    data.append(interf)
                data.append(cabecera)
            self.tp = Toplevel()
            self.tp.title('All Router Interfaces')
            self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in cabecera])
            self.tree.config(show='headings')
            self.tree.grid(row=0, column=0)
            for i in range(len(data)):
                self.tree.insert('',index = i, values=data[i])
    
    def display_dhcp_config(self, r):
        if r!="All":    
            for router in routers:
                if r == router['name']:
                    get_dhcp_config(router)
                    with open(f"DHCP_CONFIG/{router['name']}-dhcp-config.json", "r") as f:
                        json_d = json.loads(f.read())
                    dict_p = {}
                    pools = [("Pool", "Default Router", "DNS Server", "Domain Name", "Network", "Mask")]
                    for pool in json_d["Cisco-IOS-XE-native:dhcp"]["Cisco-IOS-XE-dhcp:pool"]:
                        name = pool["id"]
                        def_r = pool["default-router"]["default-router-list"][0]
                        dns = pool["dns-server"]["dns-server-list"][0]
                        d_name = pool["domain-name"]
                        ip = pool["network"]["primary-network"]["number"]
                        mask = pool["network"]["primary-network"]["mask"]
                        pools.append((name,def_r,dns,d_name,ip,mask))
                        dict_p[ip]=[name]
                    for pool in json_d["Cisco-IOS-XE-native:dhcp"]["Cisco-IOS-XE-dhcp:excluded-address"]["low-address-list"]:
                        for key in dict_p.keys():
                            if pool["low-address"][0:9] in key:
                                lista_excluded = dict_p[key]
                                lista_excluded.append(pool["low-address"])
                                dict_p[key] = lista_excluded
                    
                    for pool in json_d["Cisco-IOS-XE-native:dhcp"]["Cisco-IOS-XE-dhcp:excluded-address"]["low-high-address-list"]:
                        for key in dict_p.keys():
                            if pool["low-address"][0:9] in key:
                                lista_excluded = dict_p[key]
                                lista_excluded.append(pool["low-address"] + " - " + pool["high-address"])
                                dict_p[key] = lista_excluded
                    pools.append(("Excluded Addresses"))
                    for key in dict_p.keys():
                        pools.append((dict_p[key]))
                    self.tp = Toplevel()
                    self.tp.title('All Router Interfaces')
                    self.tree = ttk.Treeview(self.tp, height=len(pools), columns=[f"#{n}" for n in pools[0]])
                    self.tree.config(show='headings')
                    self.tree.grid(row=0, column=0)
                    for i in range(len(pools)):
                        self.tree.insert('',index = i, values=pools[i])
        else:
            for router in routers:
                    get_dhcp_config(router)
                    with open(f"DHCP_CONFIG/{router['name']}-dhcp-config.json", "r") as f:
                        json_d = json.loads(f.read())
                    dict_p = {}
                    pools = [(router["name"],"Pool", "Default Router", "DNS Server", "Domain Name", "Network", "Mask")]
                    for pool in json_d["Cisco-IOS-XE-native:dhcp"]["Cisco-IOS-XE-dhcp:pool"]:
                        name = pool["id"]
                        def_r = pool["default-router"]["default-router-list"][0]
                        dns = pool["dns-server"]["dns-server-list"][0]
                        d_name = pool["domain-name"]
                        ip = pool["network"]["primary-network"]["number"]
                        mask = pool["network"]["primary-network"]["mask"]
                        pools.append((name,def_r,dns,d_name,ip,mask))
                        dict_p[ip]=[name]

                    for pool in json_d["Cisco-IOS-XE-native:dhcp"]["Cisco-IOS-XE-dhcp:excluded-address"]["low-address-list"]:
                        for key in dict_p.keys():
                            if pool["low-address"][0:9] in key:
                                lista_excluded = dict_p[key]
                                lista_excluded.append(pool["low-address"])
                                dict_p[key] = lista_excluded
                    
                    for pool in json_d["Cisco-IOS-XE-native:dhcp"]["Cisco-IOS-XE-dhcp:excluded-address"]["low-high-address-list"]:
                        for key in dict_p.keys():
                            if pool["low-address"][0:9] in key:
                                lista_excluded = dict_p[key]
                                lista_excluded.append(pool["low-address"] + " - " + pool["high-address"])
                                dict_p[key] = lista_excluded
                    pools.append((router["Name"],"Excluded-Addresses"))
                    for key in dict_p.keys():
                        pools.append((dict_p[key]))
            self.tp = Toplevel()
            self.tp.title('All Router Interfaces')
            self.tree = ttk.Treeview(self.tp, height=len(pools), columns=[f"#{n}" for n in pools[0]])
            self.tree.config(show='headings')
            self.tree.grid(row=0, column=0)
            for i in range(len(pools)):
                self.tree.insert('',index = i, values=pools[i])
            

    def display_nat_config(self, r):
        for router in routers:
            if r == router['name']:
                get_nat_config(router)
                with open(f"NAT_CONFIG/{router['name']}-nat-config.json", "r") as f:
                    json_n = json.loads(f.read())
                
                data = [("Inside/Outside", "Static/Dynamic", "Local IP", "Global IP")]
                for nat in json_n["Cisco-IOS-XE-nat:nat"]["inside"]["source"]["static"]["nat-static-transport-list"]:
                    inside = "Inside" if len(json_n["Cisco-IOS-XE-nat:nat"]["inside"])>0 else "Outside"
                    static = "Static" if len(json_n["Cisco-IOS-XE-nat:nat"]["inside"]["source"]["static"])>0 else "Dynamic"
                    local = nat["local-ip"]
                    glob = nat["global-ip"]
                    nat_inf = (inside, static, local, glob)
                    data.append(nat_inf)
                self.tp = Toplevel()
                self.tp.title('All Router Interfaces')
                self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in data[0]])
                self.tree.config(show='headings')
                self.tree.grid(row=0, column=0)
                for i in range(len(data)):
                    self.tree.insert('',index = i, values=data[i])

    def display_ospf_config(self, r):
        if r != "All": 
            for router in routers:
                if r == router['name']:
                    get_ospf_config(router)
                    with open(f"OSPF_CONFIG/{router['name']}-ospf-config.json", "r") as f:
                        json_o = json.loads(f.read())
                    
                    data = [("Router", "Process ID", "Router ID", "Network", "Wildcard", "Area")]
                    for ospf in json_o["Cisco-IOS-XE-native:router"]["Cisco-IOS-XE-ospf:router-ospf"]["ospf"]["process-id"]:
                        pid = ospf["id"]
                        net = ospf["network"][0]["ip"]
                        wc = ospf["network"][0]["wildcard"]
                        area = ospf["network"][0]["area"]
                        rid = ospf["router-id"]
                        ospf_c = (r, pid, rid, net, wc,area)
                        data.append(ospf_c)
                    self.tp = Toplevel()
                    self.tp.title('All Router Interfaces')
                    self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in data[0]])
                    self.tree.config(show='headings')
                    self.tree.grid(row=0, column=0)
                    for i in range(len(data)):
                        self.tree.insert('',index = i, values=data[i])
        else:
                cabecera=("Router", "Process ID", "Router ID", "Network", "Wildcard", "Area")
                data = [cabecera]
                for router in routers:
                    get_ospf_config(router)
                    print(router["name"])
                    with open(f"OSPF_CONFIG/{router['name']}-ospf-config.json", "r") as f:
                        json_o = json.loads(f.read())
                    for ospf in json_o["Cisco-IOS-XE-native:router"]["Cisco-IOS-XE-ospf:router-ospf"]["ospf"]["process-id"]:
                        pid = ospf["id"]
                        net = ospf["network"][0]["ip"]
                        wc = ospf["network"][0]["wildcard"]
                        area = ospf["network"][0]["area"]
                        rid = ospf["router-id"]
                        ospf_c = (router["name"], pid, rid, net, wc,area)
                        data.append(ospf_c)                  
                self.tp = Toplevel()
                self.tp.title('All Router Interfaces')
                self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in data[0]])
                self.tree.config(show='headings')
                self.tree.grid(row=0, column=0)
                for i in range(len(data)):
                    self.tree.insert('',index = i, values=data[i])

    
    def display_interf_data(self, r):
        if r!="All":
            for router in routers:
                if r == router['name']:
                    get_interfaces_data(router)
                    with open(f"INTERFACE_DATA/{router['name']}-interfaces-stats.json", "r") as f:
                        json_o = json.loads(f.read())
                    
                    intf_names = [r]
                    for intf in json_o["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
                        intf_names.append(intf["name"])
                    
                    data = [tuple(intf_names)]

                    ip_l = ["IP"]
                    mask_l = ["Mask"]
                    duplex = ["Duplex Mode"]
                    speed = ["Speed"]
                    in_acl = ["Input ACL"]
                    out_acl = ["Output ACL"]
                    inpckts = ["In Packets"]
                    outpckts = ["Out Packets"]
                    indisc = ["In Discarded"]
                    outdisc = ["Out Discarded"]
                    inerr = ["In Errors"]
                    outerr = ["Out Errors"]
                    for intf in json_o["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
                        ip_l.append(intf["ipv4"])
                        mask_l.append(intf["ipv4-subnet-mask"])
                        duplex.append(intf["ether-state"]["negotiated-duplex-mode"])
                        speed.append(intf["ether-state"]["negotiated-port-speed"])
                        in_acl.append(intf["input-security-acl"])
                        out_acl.append(intf["output-security-acl"])
                        inpckts.append(intf["statistics"]["in-unicast-pkts"])
                        outpckts.append(intf["statistics"]["in-unicast-pkts"])
                        indisc.append(intf["statistics"]["in-discards"])
                        outdisc.append(intf["statistics"]["out-discards"])
                        inerr.append(intf["statistics"]["in-errors"])
                        outerr.append(intf["statistics"]["out-errors"])

                    data.append(tuple(ip_l))
                    data.append(tuple(mask_l))
                    data.append(tuple(duplex))
                    data.append(tuple(speed))
                    data.append(tuple(in_acl))
                    data.append(tuple(out_acl))
                    data.append(tuple(inpckts))
                    data.append(tuple(outpckts))
                    data.append(tuple(indisc))
                    data.append(tuple(outdisc))
                    data.append(tuple(inerr))
                    data.append(tuple(outerr))
                    self.tp = Toplevel()
                    self.tp.title('All Router Interfaces')
                    self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in data[0]])
                    self.tree.config(show='headings')
                    self.tree.grid(row=0, column=0)
                    for i in range(len(data)):
                        self.tree.insert('',index = i, values=data[i])
        else:
            data=[]
            for router in routers:
                intf_names = [router["name"]]
                get_interfaces_data(router)
                with open(f"INTERFACE_DATA/{router['name']}-interfaces-stats.json", "r") as f:
                    json_o = json.loads(f.read())
                
                
                for intf in json_o["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
                    intf_names.append(intf["name"])
                
                data.append(tuple(intf_names))

                ip_l = ["IP"]
                mask_l = ["Mask"]
                duplex = ["Duplex Mode"]
                speed = ["Speed"]
                in_acl = ["Input ACL"]
                out_acl = ["Output ACL"]
                inpckts = ["In Packets"]
                outpckts = ["Out Packets"]
                indisc = ["In Discarded"]
                outdisc = ["Out Discarded"]
                inerr = ["In Errors"]
                outerr = ["Out Errors"]
                for intf in json_o["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]:
                    ip_l.append(intf["ipv4"])
                    mask_l.append(intf["ipv4-subnet-mask"])
                    duplex.append(intf["ether-state"]["negotiated-duplex-mode"])
                    speed.append(intf["ether-state"]["negotiated-port-speed"])
                    in_acl.append(intf["input-security-acl"])
                    out_acl.append(intf["output-security-acl"])
                    inpckts.append(intf["statistics"]["in-unicast-pkts"])
                    outpckts.append(intf["statistics"]["in-unicast-pkts"])
                    indisc.append(intf["statistics"]["in-discards"])
                    outdisc.append(intf["statistics"]["out-discards"])
                    inerr.append(intf["statistics"]["in-errors"])
                    outerr.append(intf["statistics"]["out-errors"])

                data.append(tuple(ip_l))
                data.append(tuple(mask_l))
                data.append(tuple(duplex))
                data.append(tuple(speed))
                data.append(tuple(in_acl))
                data.append(tuple(out_acl))
                data.append(tuple(inpckts))
                data.append(tuple(outpckts))
                data.append(tuple(indisc))
                data.append(tuple(outdisc))
                data.append(tuple(inerr))
                data.append(tuple(outerr))
            self.tp = Toplevel()
            self.tp.title('All Router Interfaces')
            self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in data[0]])
            self.tree.config(show='headings')
            self.tree.grid(row=0, column=0)
            for i in range(len(data)):
                self.tree.insert('',index = i, values=data[i])

    def display_dhcp_data(self, r):
        for router in routers:
            if r == router['name']:
                get_dhcp_data(router)
                with open(f"DHCP_DATA/{router['name']}-dhcp-oper-data.json", "r") as f:
                    json_o = json.loads(f.read())
                                
                data = [("Pool", "DHCP Client IP","Client ID","Conn Type", "Expires", "State")]
                for dato in json_o["Cisco-IOS-XE-dhcp-oper:dhcpv4-server-oper"]:
                    pool = dato["pool-name"]
                    ip=dato["client-ip"]
                    cid = dato["client-id"]
                    ct = "Ethernet" if dato["client-id-type"]=="dhcp-htype-ethernet" else dato["client-id-type"]
                    expi = dato["expiration"]["time"][0:10] + " " + dato["expiration"]["time"][11:19] + " GMT+0"
                    state ="Active" if dato["state"] == "dhcp-server-binding-state-active" else "Not Active"
                    data.append((pool,ip,cid,ct,expi,state))
                self.tp = Toplevel()
                self.tp.title('All Router Interfaces')
                self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in data[0]])
                self.tree.config(show='headings')
                self.tree.grid(row=0, column=0)
                for i in range(len(data)):
                    self.tree.insert('',index = i, values=data[i])

    def display_nat_data(self,r):
        for router in routers:
            if r == router['name']:
                get_nat_data(router)
                with open(f"NAT_DATA/{router['name']}-nat-data.json", "r") as f:
                    json_o = json.loads(f.read())
                data = [("NAT STATISTICS","","","","","","","",""),("Entries", "Statics","Insides","Outsides","Hits", "Misses","Entry Timeouts", "Packets Punted", "Frag Packet Count")]
                dato = json_o["Cisco-IOS-XE-nat-oper:nat-data"]["ip-nat-statistics"]
                entries=dato["entries"]
                statics = dato["statics"]
                insides = dato["insides"]
                outsides = dato["outsides"]
                hits = dato["hits"]
                misses = dato["misses"]
                ento = dato["entry-timeouts"]
                punt = dato["packets-punted"]
                frag = dato["frag-pak-count"]
                data.append((entries,statics,insides,outsides,hits,misses,ento,punt,frag))
                d_t = transpose_2nlist(data)
                t2 = ("TRANSLATIONS", "","","","","")
                d_t.append(t2)
                data2 = ("Outside Local", "Inside Local", "Outside Global", "Inside Global","Protocol", "Count")
                d_t.append(data2)
                if "ip-nat-translation" in json_o["Cisco-IOS-XE-nat-oper:nat-data"].keys():
                    dict_cuenta = {}
                    dict_trans = {}
                    for trans in json_o["Cisco-IOS-XE-nat-oper:nat-data"]["ip-nat-translation"]:
                        dict_cuenta[trans["outside-local-addr"]] = 0 if trans["outside-local-addr"] not in dict_cuenta.keys() else dict_cuenta[trans["outside-local-addr"]] + 1
                        ol = trans["outside-local-addr"] +":"+ str(trans["outside-local-port"])
                        il = trans["inside-local-addr"] +":"+ str(trans["inside-local-port"])
                        og = trans["outside-global-addr"] +":"+ str(trans["outside-global-port"])
                        ig = trans["inside-global-addr"] +":"+ str(trans["inside-global-port"])
                        p = trans["protocol"]
                        dict_trans[trans["outside-local-addr"]] = [ol,il,og,ig,p]
                    res = []
                    for key in dict_cuenta.keys():
                        res = dict_trans[key]
                        res.append(dict_cuenta[key])
                        d_t.append(tuple(res)) 
                self.tp = Toplevel()
                self.tp.title('All Router Interfaces')
                self.tree = ttk.Treeview(self.tp, height=len(d_t), columns=[f"#{n}" for n in d_t[-1]])
                self.tree.config(show='headings')
                self.tree.grid(row=0, column=0)
                for i in range(len(d_t)):
                    self.tree.insert('',index = i, values=d_t[i])

    def display_ospf_data(self,r):
        if r!="All":
            if len(lsa_names.keys())==0:  
                for router in routers:
                    get_ospf_data(router)
                    with open(f"OSPF_DATA/{router['name']}-ospf.json", "r") as f:
                        json_o = json.loads(f.read())
                    lsaid = json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"][0]["router-id"]
                    lsa_names[lsaid] = router['name'] + "(" + router['id'] + ")"
                f.close()
                print(lsa_names)
            if len(lsa_names.keys())>0:
                for router in routers:
                    if r == router['name']:
                        get_ospf_data(router)
            
            with open(f"OSPF_DATA/{r}-ospf.json", "r") as f:
                json_o = json.loads(f.read())
                
            data = [("Area","Neighbor ID", "Cost", "State", "Address", "Interface")]
            area = json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"][0]["ospf-area"][0]["area-id"]
            for neighbor in json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"][0]["ospf-area"][0]["ospf-interface"]:
                if "ospf-neighbor" in neighbor.keys():
                    nid = neighbor["ospf-neighbor"][0]["neighbor-id"]
                    cost = neighbor["cost"]
                    state = neighbor["state"]
                    addr = neighbor["ospf-neighbor"][0]["address"] 
                    interf = neighbor["name"]
                    data.append((area,nid,cost,state,addr,interf))
                
            data.append((f"{r} Link States Database","","","",""))
            data.append(("Link ID","ADV Router", "LSA Type", "Age", "Seq | Checksum", "Link Count"))
            for dato in json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospfv2-instance"][0]["ospfv2-area"][0]["ospfv2-lsdb-area"]:
                if "router-lsa" in dato.keys():
                    lid = lsa_names[dato["lsa-id"]]
                    adv = lsa_names[dato["advertising-router"]]
                    tp = dato["lsa-type"]
                    age = dato["lsa-age"]
                    seq = str(dato["lsa-seq-number"]) + " | " + str(dato["lsa-checksum"])
                    lc = dato["router-lsa"]["router-lsa-number-links"]
                    data.append((lid,adv,tp,age,seq,lc))
            self.tp = Toplevel()
            self.tp.title('All Router Interfaces')
            self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in data[0]])
            self.tree.config(show='headings')
            self.tree.grid(row=0, column=0)
            for i in range(len(data)):
                self.tree.insert('',index = i, values=data[i])
        else:   
                data = []
                for router in routers:
                    get_ospf_data(router)
                    with open(f"OSPF_DATA/{router['name']}-ospf.json", "r") as f:
                        json_o = json.loads(f.read())
                    lsaid = json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"][0]["router-id"]
                    lsa_names[lsaid] = router['name'] + "(" + router['id'] + ")"
                f.close()
                for router in routers:
                    with open(f"OSPF_DATA/{router['name']}-ospf.json", "r") as f:
                        json_o = json.loads(f.read())
                        
                    data.append((router["name"],"Area","Neighbor ID", "Cost", "State", "Address", "Interface"))
                    area = json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"][0]["ospf-area"][0]["area-id"]
                    for neighbor in json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"][0]["ospf-area"][0]["ospf-interface"]:
                        if "ospf-neighbor" in neighbor.keys():
                            nid = neighbor["ospf-neighbor"][0]["neighbor-id"]
                            cost = neighbor["cost"]
                            state = neighbor["state"]
                            addr = neighbor["ospf-neighbor"][0]["address"] 
                            interf = neighbor["name"]
                            data.append(("",area,nid,cost,state,addr,interf))
                    print(lsa_names)
                    data.append((f"{router['name']} Link States Database","","","",""))
                    data.append(("Link ID","ADV Router", "LSA Type", "Age", "Seq | Checksum", "Link Count"))
                    for dato in json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospfv2-instance"][0]["ospfv2-area"][0]["ospfv2-lsdb-area"]:
                        if "router-lsa" in dato.keys():
                            print(dato["lsa-id"])
                            lid = lsa_names[dato["lsa-id"]]
                            adv = lsa_names[dato["advertising-router"]]
                            tp = dato["lsa-type"]
                            age = dato["lsa-age"]
                            seq = str(dato["lsa-seq-number"]) + " | " + str(dato["lsa-checksum"])
                            lc = dato["router-lsa"]["router-lsa-number-links"]
                            data.append((lid,adv,tp,age,seq,lc))
                self.tp = Toplevel()
                self.tp.title('All Router Interfaces')
                self.tree = ttk.Treeview(self.tp, height=len(data), columns=[f"#{n}" for n in data[0]])
                self.tree.config(show='headings')
                self.tree.grid(row=0, column=0)
                for i in range(len(data)):
                    self.tree.insert('',index = i, values=data[i])
    
        
    


gui = Tk()
gui.title("Restconf Client")
gui.geometry("720x480")
root = ClientGUI(gui).grid()
gui.mainloop()