from virl2_client import ClientLibrary


#Con esto nos conectamos a Cisco Modelling Labs.
#Los parametros suelen ser los mismos pero, si no se conecta, revisa los datos que te da el sandbox.
client = ClientLibrary(url="10.10.20.161", username="developer", password="C1sco12345", ssl_verify=False)
client.is_system_ready(wait=True)

#Con esto podemos crear un lab con el nombre que queramos.
#Si nos queremos unir a un lab ya creado usaríamos: client.join_existing_lab(labId)
lab = client.create_lab("Lab de prueba")

#Con esto vamos creando los nodos de la topología.
#El primer argumento es el nombre del nodo.
#El segundo argumento es la definicion del nodo, es decir, qué tipo de nodo vas a crear
#El tercer y cuarto argumento son la posición en la que los vas a dejar.
bridge = lab.create_node("bridge", "external_connector", 20, 20)
un_sw = lab.create_node("un_sw", "unmanaged_switch", 60, 20)
r1 = lab.create_node("r1", "iosv", 100, 20)
sw1 = lab.create_node("sw1", "nxosv", 100, 80)
host1 = lab.create_node("host1", "desktop", 70, 160)
host2 = lab.create_node("host2", "desktop", 130, 160)

#Con esto generamos la configuracion por default de cada nodo
lab.build_configurations()

#Con esto creamos interfaces dentro de los nodos
bridge_i1 = bridge.create_interface()
un_sw_i1 = un_sw.create_interface()
un_sw_i2 = un_sw.create_interface()
un_sw_i3 = un_sw.create_interface()
un_sw_i4 = un_sw.create_interface()
un_sw_i5 = un_sw.create_interface()
r1_i1 = r1.create_interface()
r1_i2 = r1.create_interface()
sw1_i1 = sw1.create_interface()
sw1_i2 = sw1.create_interface()
sw1_i3 = sw1.create_interface()
sw1_i4 = sw1.create_interface()
host1_i1 = host1.create_interface()
host1_i2 = host1.create_interface()
host2_i1 = host2.create_interface()
host2_i2 = host2.create_interface()

#Con esto conectamos dichas interfaces
lab.create_link(bridge_i1, un_sw_i1)
lab.create_link(un_sw_i2, r1_i1)
lab.create_link(un_sw_i3, sw1_i1)
lab.create_link(un_sw_i4, host1_i1)
lab.create_link(un_sw_i5, host2_i1)
lab.create_link(r1_i2, sw1_i2)
lab.create_link(host1_i2, sw1_i3)
lab.create_link(host2_i2, sw1_i4)



#lab.start() #Tarda unos minutos
#lab.wipe()
#lab.stop()
#lab.download()