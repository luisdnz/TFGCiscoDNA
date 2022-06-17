
from threading import Thread
import time
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
from PIL import Image,ImageTk
from tkinter import Tk, PhotoImage, Label

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
dhcppools = {
    "Pool1" : [],
    "Pool2" : [],
    "Pool3" : []
}



def transpose_2nlist(l):
    l2 = []
    for columna in range(len(l[0])):
        aux = []
        for fila in range(len(l)):
            aux.append(l[fila][columna])
        l2.append(tuple(aux))
    return l2


   


class ClientGUI(Frame):
    
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args,**kwargs)
        self.parent = master
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

    def display_options(self, r):
        self.deleteWidgets()
        
        self.NConfBut = Button(font=("Arial", 8), fg='Black', text=f"{r} NAT Config", highlightbackground='red', command=lambda: self.display_nat_config(r))
        self.NConfBut.config(height=1,width=15)
        
        self.NDataBut = Button(font=("Arial", 8), fg='Black', text=f"{r} NAT Data", highlightbackground='red', command=lambda: self.display_nat_data(r))
        self.NDataBut.config(height=1,width=15)
        
        self.IConfBut = Button(font=("Arial", 8), fg='Black', text=f"{r} Interfaces Config", highlightbackground='red', command=lambda: self.display_interface_config(r))
        self.IConfBut.config(height=1,width=15)
        
        self.OConfBut = Button(font=("Arial", 8), fg='Black', text=f"{r} OSPF Config", highlightbackground='red', command=lambda: self.display_ospf_config(r))
        self.OConfBut.config(height=1,width=15)
        
        self.IDataBut = Button(font=("Arial", 8), fg='Black', text=f"{r} Interfaces Data", highlightbackground='red', command=lambda: self.display_interf_data(r))
        self.IDataBut.config(height=1,width=15)
        
        self.ODataBut = Button(font=("Arial", 8), fg='Black', text=f"{r} OSPF Data", highlightbackground='red', command=lambda: self.display_ospf_data(r))
        self.ODataBut.config(height=1,width=15)

        self.DConfBut = Button(font=("Arial", 8), fg='Black', text=f"{r} DHCP Config", highlightbackground='red', command=lambda: self.display_dhcp_config(r))
        self.DConfBut.config(height=1,width=15)

        self.DDataBut = Button(font=("Arial", 8), fg='Black', text=f"{r} DHCP Data", highlightbackground='red', command=lambda: self.display_dhcp_data(r))
        self.DDataBut.config(height=1,width=15)

        self.RBut = Button(font=("Arial", 8), fg='Black', text=f"{r} Routing Graph", highlightbackground='red', command=lambda: self.plot_spf_tree2(r))
        self.RBut.config(height=1,width=15)

        if r=="R1":
            self.IConfBut.place(x=111,y=221)
            self.IDataBut.place(x=111,y=244)
            self.OConfBut.place(x=111,y=267)
            self.ODataBut.place(x=111,y=290)
            self.NConfBut.place(x=111,y=313)
            self.NDataBut.place(x=111,y=336)
            self.RBut.place(x=111,y=359)
        elif r=="R2":
            self.IConfBut.place(x=113,y=438)
            self.IDataBut.place(x=113,y=461)
            self.OConfBut.place(x=113,y=483)
            self.ODataBut.place(x=113,y=506)
            self.RBut.place(x=113,y=529)
        elif r=="R3":
            self.IConfBut.place(x=684,y=438)
            self.IDataBut.place(x=684,y=461)
            self.OConfBut.place(x=684,y=483)
            self.ODataBut.place(x=684,y=506)
            self.RBut.place(x=684,y=529)
        elif r=="R4":
            self.IConfBut.place(x=684,y=221)
            self.IDataBut.place(x=684,y=244)
            self.OConfBut.place(x=684,y=267)
            self.ODataBut.place(x=684,y=290)
            self.RBut.place(x=684,y=313)
        elif r=="R5":
            self.IConfBut.place(x=320,y=21)
            self.IDataBut.place(x=320,y=44)
            self.OConfBut.place(x=320,y=67)
            self.ODataBut.place(x=320,y=90)
            self.DConfBut.place(x=320,y=113)
            self.DDataBut.place(x=320,y=136)
            self.RBut.place(x=320,y=159)
        elif r=="All":
            self.IConfBut.place(x=110,y=20)
            self.IDataBut.place(x=110,y=43)
            self.OConfBut.place(x=110,y=66)
            self.ODataBut.place(x=110,y=89)
        


    def display_listener_options(self):
        self.deleteWidgets()
        self.LIBut = Button(font=("Arial", 8), fg='Black', text=f"Listener Interfaces", highlightbackground='red', command=lambda: self.display_listener_interf())
        self.LIBut.config(height=1,width=15)
        self.LIBut.place(x=700,y=20)

        self.LDBut = Button(font=("Arial", 8), fg='Black', text=f"Listener DHCP Pools", highlightbackground='red', command=lambda: self.display_listener_dhcp())
        self.LDBut.config(height=1,width=15)
        self.LDBut.place(x=700,y=43)
        
    def display_listener_interf(self):
        t = Thread(target=self.listen)
        t.start()
    
    def display_listener_dhcp(self):
        t = Thread(target=self.listen2)
        t.start()

    def listen(self):
        root = self.master
        child_w = Toplevel(root)
        child_w.geometry("500x360")
        child_w.title("Interfaces Listener Says: ")
        while True:
            for router in routers:
                get_interfaces_list(router)
            for router in routers:
                self.check_changes(router, child_w)
            time.sleep(15)
            
    def check_changes(self, router, child_w):
        with open(f"INTERFACES_CONFIG/{router['name']}-interfaces-list-config.json", "r") as f:
            jsn = json.loads(f.read())
        for interface in jsn["ietf-interfaces:interfaces"]["interface"]:
            if interface["enabled"] == False:
                idr = router["name"]
                interf = interface["name"]
                text = Text(child_w,width=60,height = 2)
                text.pack()
                hour, min, secs = map(int, time.strftime("%H %M %S").split())
                text.insert(INSERT,f" {hour}:{min}:{secs} - Interface {interf} in {idr} went from Up/Up to Down")
    
    def listen2(self):
        root = self.master
        child_w = Toplevel(root)
        child_w.geometry("500x360")
        child_w.title("DHCP Listener Says: ")
        while True:
            get_dhcp_data(r5)
            get_dhcp_config(r5)
            self.check_changes2(child_w)
            time.sleep(15)
    
    def check_changes2(self, child_w):
        with open(f"DHCP_CONFIG/R5-dhcp-config.json", "r") as f:
            jsn = json.loads(f.read())
        for ex_add in jsn["Cisco-IOS-XE-native:dhcp"]["Cisco-IOS-XE-dhcp:excluded-address"]["low-address-list"]:
            if "192.168.1." in ex_add["low-address"]:
                if not ex_add["low-address"] in dhcppools["Pool1"]:
                    dhcppools["Pool1"].append(ex_add["low-address"])
            elif "192.168.2." in ex_add["low-address"]:
                if not ex_add["low-address"] in dhcppools["Pool2"]:
                    dhcppools["Pool2"].append(ex_add["low-address"])
            else:
                if not ex_add["low-address"] in dhcppools["Pool3"]:
                    dhcppools["Pool3"].append(ex_add["low-address"])
        for ex_add in jsn["Cisco-IOS-XE-native:dhcp"]["Cisco-IOS-XE-dhcp:excluded-address"]["low-high-address-list"]:
            low = ex_add["low-address"]
            high = ex_add["high-address"]
            low_int = int(low[10::])
            high_int = int(high[10::])
            for i in range(low_int,high_int+1):
                add = low[0:10] + str(i)
                if "192.168.1." in ex_add["low-address"]:
                    if not add in dhcppools["Pool1"]:
                        dhcppools["Pool1"].append(add)
                elif "192.168.2." in ex_add["low-address"]:
                    if not add in dhcppools["Pool2"]:
                        dhcppools["Pool2"].append(add)
                else:
                    if not add in dhcppools["Pool3"]:
                        dhcppools["Pool3"].append(add)
        with open(f"DHCP_DATA/R5-dhcp-oper-data.json", "r") as f:
            jsn = json.loads(f.read())
        for add in jsn["Cisco-IOS-XE-dhcp-oper:dhcpv4-server-oper"]:
            ip = add["client-ip"]
            pool = add["pool-name"]
            if not ip in dhcppools[pool]:
                dhcppools[pool].append(ip)
        for key in dhcppools.keys():
            if len(dhcppools[key])>=254:
                text = Text(child_w,width=60,height = 2)
                text.pack()
                hour, min, secs = map(int, time.strftime("%H %M %S").split())
                text.insert(INSERT,f"{hour}:{min}:{secs} - All IP addresses in {key} have been served")


    def plot_spf_tree2(self, r):
        router=None
        for rtr in routers:
            if rtr['name']==r:
                router=rtr
        G = nx.Graph()
        G.add_node(router['name'])
        colorlist=['yellow']
        edge_labels = {}
        nmap = {}
        interfmap={}
        get_routing(router)
        with open(f"ROUTING/{router['name']}-routing.json", "r") as f:
            routingjson = json.loads(f.read())
        
        routes = routingjson["ietf-routing:routing-state"]["routing-instance"][0]["ribs"]["rib"][0]["routes"]["route"]

        #Adding all neighbors and outgoing interfaces to the maps
        for route in routes:
            neigh = route["update-source"]
            interf = route["next-hop"]["outgoing-interface"]
            if neigh!="0.0.0.0":
                nmap[neigh] = route["next-hop"]["outgoing-interface"]
            if len(interf)>1:
                interfmap[interf]=(route["next-hop"]["next-hop-address"])
        #Adding all interfaces as nodes to the root
        for key in interfmap.keys():
            G.add_node(key)
            G.add_edge(key,router["name"])
            colorlist.append('green')
        #Adding all directly connected nets to interfaces
        for key in interfmap.keys():
            for route in routes:
                if route["source-protocol"] == "ietf-routing:direct" and key == route["next-hop"]["outgoing-interface"] and not "/32" in route["destination-prefix"]:
                    G.add_node(route["destination-prefix"])
                    G.add_edge(route["destination-prefix"], key)
                    colorlist.append('cyan')
        #Adding all neighbors as nodes to the interfaces
        for key in nmap.keys():
            intf = nmap[key]
            G.add_node(key)
            G.add_edge(key,intf)
            colorlist.append('blue')
        #Adding all networks routed by the neighbors
        for route in routes:
            net = route["destination-prefix"]
            neigh = route["update-source"]
            if not "/32" in net and neigh!="0.0.0.0":
                G.add_node(net)
                G.add_edge(net,neigh)
                colorlist.append('cyan')
        
        for route in routes:
            net = route["destination-prefix"]
            nhop = route["next-hop"]["next-hop-address"]
            if route["source-protocol"] == "ietf-routing:static":
                G.add_node(net)
                colorlist.append('orange')
                for rt in routes:
                    net2 = rt["destination-prefix"]
                    if nhop[0:3] in net2 and router["name"]=="R1" and len(rt["next-hop"]["outgoing-interface"])>1:
                        G.add_edge(net, rt["next-hop"]["outgoing-interface"])
                    elif rt["next-hop"]["next-hop-address"] == nhop and len(rt["next-hop"]["outgoing-interface"])>1:
                        G.add_edge(net, rt["next-hop"]["outgoing-interface"])
        
        pos = nx.spring_layout(G, seed=1734289231)
        nx.draw(G, node_color = colorlist, pos=pos, with_labels=True, edgelist=list(G.edges()), node_size=600)
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
        plt.axis('off')
        plt.show()
        
    
    
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
                    self.tree.tag_configure("cabecera", background='cyan', foreground="black")
                    self.tree.pack(side='left')
                    scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
                    scrollbar.pack(side='right', fill='y')
                    for i in range(len(data)):
                        if data[i]==data[0]:
                            self.tree.insert('',index = i, values=data[i], tags=("cabecera",))
                        else:
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
            self.tree.tag_configure("cabecera", background='cyan', foreground="black")
            self.tree.pack(side='left')
            scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
            scrollbar.pack(side='right', fill='y')
            for i in range(len(data)-1):
                if data[i]==data[0]:
                    self.tree.insert('',index = i, values=data[i], tags=("cabecera",))
                else:
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
                    self.tree.tag_configure("cabecera", background='cyan', foreground="black")
                    self.tree.pack(side='left')
                    scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
                    scrollbar.pack(side='right', fill='y')
                    for i in range(len(pools)):
                        if pools[i] == pools[0] or "Excluded Addresses" in pools[i]:
                            self.tree.insert('',index = i, values=pools[i], tags=("cabecera",))
                        else:
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
            self.tree.pack(side='left')
            scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
            scrollbar.pack(side='right', fill='y')
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
                self.tree.tag_configure("cabecera", background='cyan', foreground="black")
                self.tree.pack(side='left')
                scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
                scrollbar.pack(side='right', fill='y')
                for i in range(len(data)):
                    if data[i] == data[0]:
                        self.tree.insert('',index = i, values=data[i], tags=("cabecera",))
                    else:
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
                    self.tree.tag_configure("cabecera", background="cyan", foreground="black")
                    self.tree.pack(side='left')
                    scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
                    scrollbar.pack(side='right', fill='y')
                    for i in range(len(data)):
                        if data[i]==data[0]:
                            self.tree.insert('',index = i, values=data[i], tags=("cabecera",))
                        else:
                            self.tree.insert('',index = i, values=data[i])
        else:
                cabecera=("Router", "Process ID", "Router ID", "Network", "Wildcard", "Area")
                data = [cabecera]
                for router in routers:
                    get_ospf_config(router)
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
                self.tree.tag_configure('cabecera', background='cyan', foreground='black')
                self.tree.pack(side='left')
                scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
                scrollbar.pack(side='right', fill='y')
                for i in range(len(data)):
                    print(data[i])
                    print(cabecera)
                    if data[i] == cabecera:
                        self.tree.insert('',index = i, values=data[i], tags=('cabecera',))
                    else:
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
                    self.tree.tag_configure("cabecera", background="cyan", foreground="black")
                    self.tree.pack(side='left')
                    scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
                    scrollbar.pack(side='right', fill='y')
                    for i in range(len(data)):
                        if data[i]==data[0]:
                            self.tree.insert('',index = i, values=data[i], tags=("cabecera",))
                        else:
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
            self.tree.tag_configure("cabecera", background="cyan", foreground="black")
            self.tree.pack(side='left')
            scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
            scrollbar.pack(side='right', fill='y')
            self.tree.configure(yscrollcommand=scrollbar.set)
            for i in range(len(data)):
                if data[i][1:3]==data[0][1:3]:
                    self.tree.insert('',index = i, values=data[i], tags=("cabecera",))
                else:
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
                self.tree.tag_configure("cabecera", background="cyan", foreground="black")
                self.tree.pack(side='left')
                scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
                scrollbar.pack(side='right', fill='y')
                for i in range(len(data)):
                    if data[i]==data[0]:
                        self.tree.insert('',index = i, values=data[i], tags=("cabecera",))
                    else:
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
                self.tree.tag_configure("cabecera", background="cyan", foreground="black")
                self.tree.pack(side='left')
                scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
                scrollbar.pack(side='right', fill='y')
                for i in range(len(d_t)):
                    if d_t[i]==data2:
                        self.tree.insert('',index = i, values=d_t[i], tags=("cabecera",))
                    else:
                        self.tree.insert('',index = i, values=d_t[i])

    def display_ospf_data(self,r):
        if r!="All":
            if len(lsa_names.keys())==0:  
                for router in routers:
                    print(router["name"])
                    get_ospf_data(router)
                    with open(f"OSPF_DATA/{router['name']}-ospf.json", "r") as f:
                        json_o = json.loads(f.read())
                    lsaid = json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"][0]["router-id"]
                    lsa_names[lsaid] = router['name'] + "(" + router['id'] + ")"

                print(lsa_names)
            if len(lsa_names.keys())>0:
                for router in routers:
                    if r == router['name']:
                        get_ospf_data(router)
            with open(f"OSPF_DATA/{r}-ospf.json", "r") as f:
                json_o = json.loads(f.read())
            print("PASA4")
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
            cab2=("Link ID","ADV Router", "LSA Type", "Age", "Seq | Checksum", "Link Count")
            data.append(cab2)
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
            self.tree.tag_configure("cabecera", background="cyan", foreground="black")
            self.tree.pack(side='left')
            scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
            scrollbar.pack(side='right', fill='y')
            for i in range(len(data)):
                if data[i]==data[0] or data[i]==cab2:
                    self.tree.insert('',index = i, values=data[i], tags=("cabecera",))
                else:
                    self.tree.insert('',index = i, values=data[i])
        else:   
                data = []
                cab2 = ("Link ID","ADV Router", "LSA Type", "Age", "Seq | Checksum", "Link Count")
                for router in routers:
                    get_ospf_data(router)
                    print("PASA")
                    with open(f"OSPF_DATA/{router['name']}-ospf.json", "r") as f:
                        json_o = json.loads(f.read())
                    lsaid = json_o["Cisco-IOS-XE-ospf-oper:ospf-oper-data"]["ospf-state"]["ospf-instance"][0]["router-id"]
                    lsa_names[lsaid] = router['name'] + "(" + router['id'] + ")"
                f.close()
                print("PASA")
                for router in routers:
                    with open(f"OSPF_DATA/{router['name']}-ospf.json", "r") as f:
                        json_o = json.loads(f.read())
                    print("PASA")
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
                    data.append(cab2)
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
                self.tree.tag_configure("cabecera", background='cyan', foreground='black')
                self.tree.pack(side='left')
                scrollbar = ttk.Scrollbar(self.tp, orient='vertical', command=self.tree.yview)
                scrollbar.pack(side='right', fill='y')
                for i in range(len(data)):
                    if data[i][1::]==data[0][1::] or data[i]==cab2:
                        self.tree.insert('',index = i, values=data[i], tags=("cabecera",))  
                    else:
                        self.tree.insert('',index = i, values=data[i])




gui = Tk()
gui.title("Restconf Client")
gui.geometry("912x597")
root = ClientGUI(gui)
#imagen = PhotoImage(file = "PRUEBA.png")
imagen = Image.open("PRUEBA.png")
img = imagen.resize((912,597)) 
my_img=ImageTk.PhotoImage(img)

background = Label(image = my_img, text = "Imagen S.O de fondo")
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)
ir1 = Image.open("router1.png")
ir1=ir1.resize((55,66))
ir1 = ImageTk.PhotoImage(ir1)
botonNuevo1 = Button(gui,image=ir1, compound="top", command= lambda: root.display_options("R1"))
botonNuevo1.place(x=48, y=220.5)
        

ir2 = Image.open("router2.png")
ir2 = ir2.resize((57,61))
ir2 = ImageTk.PhotoImage(ir2)
botonNuevo2 = Button(gui, image=ir2, compound="top", command= lambda: root.display_options("R2"))
botonNuevo2.place(x=48, y=487)


ir3 = Image.open("router3.png")
ir3 = ir3.resize((55,64))
ir3 = ImageTk.PhotoImage(ir3)
botonNuevo3 = Button(gui, image=ir3, compound="top", command= lambda: root.display_options("R3"))
botonNuevo3.place(x=786, y=484.5)


ir4 = Image.open("router4.png")
ir4 = ir4.resize((54,61))
ir4 = ImageTk.PhotoImage(ir4)
botonNuevo4 = Button(gui, image=ir4, compound="top", command= lambda: root.display_options("R4"))
botonNuevo4.place(x=785, y=224)


ir5 = Image.open("router5.png")
ir5 = ir5.resize((54,52))
ir5 = ImageTk.PhotoImage(ir5)
botonNuevo5 = Button(gui, image=ir5, compound="top", command= lambda: root.display_options("R5"))
botonNuevo5.place(x=418, y=22)

AButton = Button(gui, font=("Arial", 10), fg='Black', text="All", highlightbackground='red', command=lambda: root.display_options("All"))
AButton.config(height=1,width=10)
AButton.place(x=20,y=20)

TButton = Button(gui, font=("Arial", 10), fg='Black', text="Listeners", highlightbackground='red', command=lambda: root.display_listener_options())
TButton.config(height=1,width=10)
TButton.place(x=800,y=20)

gui.mainloop()

