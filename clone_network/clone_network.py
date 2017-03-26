import sys
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.node import RemoteController
from mininet.topo import Topo

from requests import get

import random
import string



devices, switches, links = [], [], []

class FloodlightController:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._switches = None
        self._devices = None
        self._switch_links = None

    @property
    def switches(self):
        if not self._switches:
            self._switches = self._floodlight_request('/wm/core/controller/switches/json').json()

        return self._switches

    @property
    def devices(self):
        if not self._devices:

            self._devices = self._floodlight_request('/wm/device/').json().get('devices')

        return self._devices

    @property
    def switch_links(self):

        if not self._switch_links:
            self._switch_links = self._floodlight_request('/wm/topology/links/json').json()

        return self._switch_links

    def _floodlight_request(self, endpoint):

        full_url = 'http://{controller_ip}:{controller_port}{endpoint}'.format(
            controller_ip=self.ip,
            controller_port=self.port,
            endpoint=endpoint
        )

        response = get(full_url)

        response.raise_for_status()

        return response
"""
Prerequisites:
    - Must be run in an environment with mininet installed and in the $PATH
    - Python environment requires the mininet package.

Instructions to run the topo:
    1. Go to directory where this file is.
    2. run: sudo -E python clone_network.py <prod_controller_ip> <prod_rest_port> <clone_controller_ip> <clone_openflow_port>
"""

class ClonedFloodlightTopology(Topo):
    """Cloned network topology which is based upon the provided floodlight controller."""

    def __init__(self, floodlight_controller, devices=[], switches=[], links=[], **opts):
        """Create custom topo."""

        # Initialize topology
        # It uses the constructor for the Topo cloass
        super(ClonedFloodlightTopology, self).__init__(**opts)
        # Clone Switches
        for switch in switches:
           self.addSwitch(switch["label"], dpid=str(switch["max"]))

        # clone devices
        for device in devices:
            self.addHost(device["label"])

        #clone links
        for link in links:
            self.addLink(link["src_mac"], link["src_port"], link["dst_mac"], link["dst_port"])



def print_usage():
    print(
        'sudo -E python clone_network.py <prod_controller_ip> <prod_rest_port> <clone_controller_ip> <clone_openflow_port>'
    )


def randdpid():
    return ''.join(random.choice(string.digits) for _ in range(16))


# return true if successfully deleted a node, false if not
def delete_node(node_label):
    device = next([d for d in devices if d["label"] == node_label], None)
    if device:
        return delete_device(device)
    switch = next([s for s in switches if s["label"] == node_label], None)
    if switch:
        return delete_switch(switch)
    return False


def delete_device(device):
    global devices
    global links
    try:
        devices.remove(device)
    except ValueError:
        return False

    # Remove all links associated with that device.
    links_to_remove = []
    for link in links:
        if link["src_mac"] == device["mac"]:
            links_to_remove.append(link)
        elif link["dst_mac"] == device["mac"]:
            links_to_remove.append(link)
    links = [l for l in links if l not in links_to_remove]
    return True


def delete_switch(switch):
    global switches
    global links
    try:
        switches.remove(switch)
    except ValueError:
        return False

    # Remove all links associated with that switch.
    links_to_remove = []
    for link in links:
        if link["src_mac"] == switch["mac"]:
            links_to_remove.append(link)
        elif link["dst_mac"] == switch["mac"]:
            links_to_remove.append(link)
    links = [l for l in links if l not in links_to_remove]
    return True


def delete_link(node1, node2):
    global links
    for link in links:
        if (link["src_label"] == node1 and link["dst_label"] == node2) \
                or (link["src_label"] == node2 and link["dst_label"] == node1):
            links.remove(link)
            return True
    return False


def add_device(label, mac):
    global devices, switches
    if label in [device["label"] for device in devices] or label in [switch["label"] for switch in switches]:
        return False
    devices.append({"label": label, "mac": mac})
    return True


def add_switch(label, mac):
    global switches, devices
    if label in [device["label"] for device in devices] or label in [switch["label"] for switch in switches]:
        return False
    switches.append({"label": label, "mac": mac})
    return True


# Return true if the link could be added, false if it couldn't.
def add_link(src_label, dst_label):
    """
    :return: True if the link could be added, false if not. It may fail to add due to a device/switch with the given
            macs not existing.
    """
    global devices, switches, links
    # don't allow circular links
    macs = [device["mac"] for device in devices] + [switch["mac"] for switch in switches]

    nodes = [n1 for n1 in devices] + [n2 for n2 in switches]
    source_nodes = [n for n in nodes if n["src_label"] == src_label]
    destination_nodes = [n for n in nodes if n["dst_label"] == dst_label]
    if not source_nodes or not destination_nodes:
        return False
    source_node = source_nodes[0]
    destination_node = destination_nodes[0]
    links.append({"src_mac": source_node["mac"], "src_port": None, "dst_mac": destination_node["mac"], "dst_port": None})
    return True


def run():
    if len(sys.argv) != 5:
        print_usage()
        return 1

    global devices, switches, links
    prod_controller_ip = sys.argv[1]
    prod_rest_port = sys.argv[2]
    clone_controller_ip = sys.argv[3]
    clone_openflow_port = int(sys.argv[4])

    simulation_controller = RemoteController('c', clone_controller_ip, clone_openflow_port)
    production_controller = FloodlightController(prod_controller_ip, prod_rest_port)

    devices, switches, links = production_controller.devices, production_controller.switches, production_controller.links
    topo = ClonedFloodlightTopology(production_controller, devices=devices, switches=switches, links=links)

    cloned_network = Mininet(
        topo=topo,
        host=CPULimitedHost,
        controller=None
    )

    cloned_network.addController(simulation_controller)
    cloned_network.start()

    while True:
        line = sys.stdin.readline().strip(" \t\n").lower().split()

        #line = input("Enter a command: ").strip(" \t\n").lower()
        if line[0] == "mn":
            CLI(cloned_network)
        elif line[0] == "commit":
            cloned_network.stop()
            # do network modifications
            topo = ClonedFloodlightTopology(production_controller, devices=devices, switches=switches, links=links)
            cloned_network = Mininet(
                topo=topo,
                host=CPULimitedHost,
                controller=simulation_controller
            )
            cloned_network.start()
        elif line[0] == "del":
            if len(line) < 2:
                print "Error: Must give the name of the node to delete"
                continue
            if delete_node(line[1]):
                continue
            elif len(line) > 3 and delete_link(line[2], line[3]):
                continue
            print "Failed to delete Node."

        elif line[0] == "add":
            if line[1] == "host":
                if (len(line) != 3):
                    print "usage: add host NAME"
                    continue
                else:
                    if not add_device(line[2], randdpid()):
                        print "ERROR: FAILED TO ADD HOST"
            elif line[1] == "switch":
                if (len(line) != 3):
                    print "usage: add switch NAME"
                    continue
                else:
                    if line[2] in topo.nodes():
                        print "node already in topology"
                    else:
                        if not add_switch(line[2], randdpid()):
                            print "ERROR: FAILED TO ADD SWITCH"
            elif line[1] == "link":
                if (len(line) != 4):
                    print "usage: add link NODE NODE"
                    continue
                else:
                    if not add_link(line[2], line[3]):
                        print "ERROR: FAILED TO ADD LINK"
            else:
                print "add a what?"
        elif line == "quit":
            print "Exiting\n"
            break
        else:
            print "Nah. Can't let you do that.\n"

    cloned_network.stop()

# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
    run()


