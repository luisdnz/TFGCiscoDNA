from INTERFACES_CONFIG.GetInterfacesList import get_interfaces_list
from INTERFACES_CONFIG.PutInterfacesList import put_interfaces_list
from OSPF_CONFIG.GetOspfConfig import get_ospf_config
from OSPF_CONFIG.PutOspfConfig import put_ospf_config
from DHCP_CONFIG.PutDhcpConfig import put_dhcp_config
from DHCP_CONFIG.GetDhcpConfig import get_dhcp_config
from DHCP_DATA.GetDhcpData import get_dhcp_data
from RUNNING_CONFIG.GetRunningConfig import get_running_config
from NAT_CONFIG.GetNatConfig import get_nat_config
from NAT_CONFIG.PutNatConfig import put_nat_config
from NAT_DATA.GetNatData import get_nat_data
from INTERFACE_DATA.GetInterfaceData import get_interfaces_data
r1 = {
    'name':'R1',
    'ip':'10.10.20.1',
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

#for router in routers:
#    get_interfaces_data(router)
#get_interfaces_list(r1)
 #   put_interfaces_list(router)
    #get_ospf_config(router)
  #  put_ospf_config(router)
#get_running_config(r1)
    #get_running_config(router)
#get_nat_data(r1)
#put_nat_config(r1)
#get_dhcp_data(r5)
#get_dhcp_config(r5)
put_dhcp_config(r5)
