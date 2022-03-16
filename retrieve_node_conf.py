from virl2_client import ClientLibrary
import genie

client = ClientLibrary(url="10.10.20.161", username="developer", password="C1sco12345", ssl_verify=False)
client.is_system_ready(wait=True)
#Con esto podemos crear un lab con el nombre que queramos.
#Si nos queremos unir a un lab ya creado usaríamos: client.join_existing_lab(labId)
lab = client.find_labs_by_title("Small NXOS/IOSXE Network")[0]

pyats_testbeb = lab.get_pyats_testbed()

with open("testbed.yaml", "w") as f:
    f.write(pyats_testbeb)
