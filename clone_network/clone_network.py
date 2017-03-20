import sys

from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI

from floodlight.floodlight import FloodlightController
"""
Prerequisites:
    - Must be run in an environment with mininet installed and in the $PATH
    - Python environment requires the mininet package.

Instructions to run the topo:
    1. Go to directory where this file is.
    2. run: sudo -E python clone_network.py <prod_controller_ip> <prod_rest_port> <clone_controller_ip> <clone_openflow_port>
"""

class ClonedFloodlightTopology(Topo):
    """The production network topology which will be cloned by the Topo cloner."""

    def __init__(self, floodlight_controller, **opts):
        """Create custom topo."""

        # Initialize topology
        # It uses the constructor for the Topo cloass
        super(ClonedFloodlightTopology, self).__init__(**opts)

        floodlight_switches = floodlight_controller.switches()

        # Includes switches too, need to check if has ipv4 or ipv6 address: If it does it's a host
        floodlight_devices = floodlight_controller.devices()
        floodlight_switch_links = floodlight_controller.switch_links()

        cloned_switches = []

        # Clone Switches
        label_id = 1
        for raw_switch in floodlight_switches:
            dpid = raw_switch.get('switchDPID').replace(':', '')
            cloned_switches.append(
                self.addSwitch('s{}'.format(label_id), dpid=dpid)
            )
            label_id += 1

        # Link Switches together
        for raw_switch_link in floodlight_switch_links:
            source_dpid = raw_switch_link.get('src-switch').replace(':', '')
            source_port = raw_switch_link.get('src-port')

            destination_dpid = raw_switch_link.get('dst-switch').replace(':', '')
            destination_port = raw_switch_link.get('dst-port')

            source_switch = None
            destination_switch = None

            for switch in cloned_switches:
                if switch.dpid == source_dpid:
                    source_switch = switch

                if switch.dpid == destination_dpid:
                    destination_switch = switch

            if source_switch and destination_switch:
                self.addLink(source_switch, destination_switch, source_port, destination_port)

        # Clone Hosts
        label_id = 1
        for raw_device in floodlight_devices:
            # If device has a ipv4 or 6 address it is a host
            if raw_device.get('ipv4') or raw_device.get('ipv6'):
                host = self.addHost('h{}'.format(label_id))

                # Link host to all attachment points
                attachment_points = raw_device.get('attachmentPoint')
                for attachment_point in attachment_points:
                    switch_dpid = attachment_point.get('switch').replace(':', '')
                    switch_port = int(attachment_point.get('port'))

                    for switch in cloned_switches:
                        if switch.dpid == switch_dpid:
                            self.addLink(host, switch, port2=switch_port)
                label_id += 1


def print_usage():
    print(
        'sudo -E python clone_network.py <prod_controller_ip> <prod_rest_port> <clone_controller_ip> <clone_openflow_port>'
    )


def run():

    if len(sys.argv != 5):
        print_usage()
        return 1

    prod_controller_ip = sys.argv[1]
    prod_rest_port = sys.argv[2]
    clone_controller_ip = sys.argv[3]
    clone_openflow_port = int(sys.argv[4])

    simulation_controller = RemoteController('c', clone_controller_ip, clone_openflow_port)
    production_controller = FloodlightController(prod_controller_ip, prod_rest_port)

    cloned_network = Mininet(
        topo=ClonedFloodlightTopology(production_controller),
        host=CPULimitedHost,
        controller=None
    )

    cloned_network.addController(simulation_controller)
    cloned_network.start()

    CLI(cloned_network)
    cloned_network.stop()

# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
    run()


