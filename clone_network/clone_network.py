import sys
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.node import RemoteController
from mininet.topo import Topo

import random
import string

from floodlight import FloodlightController

devices, switches, links = [], [], []

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
           self.addSwitch(switch["label"], dpid=str(switch["mac"]))

        # clone devices
        for device in devices:
            print(device["label"])
            self.addHost(device["label"])

        #clone links
        for link in links:
            self.addLink(link["src_label"], link["dst_label"], link["src_port"], link["dst_port"])



def print_usage():
    print(
        'sudo -E python clone_network.py <prod_controller_ip> <prod_rest_port> <clone_controller_ip> <clone_openflow_port>'
    )


def randdpid():
    return ''.join(random.choice(string.digits) for _ in range(16))


# return true if successfully deleted a node, false if not
def delete_node(node_label):
    global devices
    global switches

    devs = [d for d in devices if d["label"] == node_label]
    if len(devs) > 0:
        return delete_device(devs[0])

    sws = [s for s in switches if s["label"] == node_label]
    if len(sws) > 0:
        return delete_switch(sws[0])

    return "Failed to delete node. It is not a switch or a host"


def delete_device(device):
    global devices
    global links
    devices = [d for d in devices if d["label"] != device["label"]]

    # Remove all links associated with that device.
    links_to_remove = []
    for link in links:
        if link["src_label"] == device["label"]:
            links_to_remove.append(link)
        elif link["dst_label"] == device["label"]:
            links_to_remove.append(link)
    links = [l for l in links if l not in links_to_remove]
    return ""


def delete_switch(switch):
    global switches
    global links
    switches = [s for s in switches if s["label"] != switch["label"]]

    # Remove all links associated with that switch.
    links_to_remove = []
    for link in links:
        if link["src_label"] == switch["label"]:
            links_to_remove.append(link)
        elif link["dst_label"] == switch["label"]:
            links_to_remove.append(link)
    links = [l for l in links if l not in links_to_remove]
    return ""


def delete_link(node1, node2):
    global links
    for link in links:
        if (link["src_label"] == node1 and link["dst_label"] == node2) \
                or (link["src_label"] == node2 and link["dst_label"] == node1):
            links.remove(link)
            return "Failed to remove link from links list."
    return ""


def add_device(label, mac):
    global devices, switches
    if label in [device["label"] for device in devices] or label in [switch["label"] for switch in switches]:
        return "Failed to add host. Host already exists"
    devices.append({"label": label, "mac": mac})
    return ""


def add_switch(label, mac):
    global switches, devices
    if label in [device["label"] for device in devices] or label in [switch["label"] for switch in switches]:
        return "Failed to add switch. Switch already exists"
    switches.append({"label": label, "mac": mac})
    return ""


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
    source_nodes = [n for n in nodes if n["label"] == src_label]
    destination_nodes = [n for n in nodes if n["label"] == dst_label]
    if not source_nodes or not destination_nodes:
        return "Failed to add link. Either source or destination does not exist."
    links.append({
        "src_label": src_label,
        "src_port": None,
        "dst_label": dst_label,
        "dst_port": None
    })
    return ""


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
            elif len(line) > 3:
                err = delete_link(line[2], line[3])
                if err:
                    print err
                continue
            else:
                err = delete_node(line[1])
                if err:
                    print err
                continue
        elif line[0] == "add":
            if line[1] == "host":
                if (len(line) != 3):
                    print "usage: add host NAME"
                    continue
                else:
                    err = add_device(line[2], randdpid())
                    if err:
                        print err
            elif line[1] == "switch":
                if (len(line) != 3):
                    print "usage: add switch NAME"
                    continue
                else:
                    if line[2] in topo.nodes():
                        print "node already in topology"
                    else:
                        err = add_switch(line[2], randdpid())
                        if err:
                            print err
            elif line[1] == "link":
                if (len(line) != 4):
                    print "usage: add link NODE NODE"
                    continue
                else:
                    err = add_link(line[2], line[3])
                    if err:
                        print err
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

