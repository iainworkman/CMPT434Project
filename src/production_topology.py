from argparse import ArgumentParser

from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI

"""
Prerequisites:
    - Must be run in an environment with mininet installed and in the $PATH
    - Python environment requires the mininet package.

Instructions to run the topo:
    1. Go to directory where this file is.
    2. run: sudo -E python production_network.py
"""

class DemoTopology(Topo):
    def addSwitch(self, i):
        name = "s" + str(i)
        dpid = str(i).zfill(16)
        return Topo.addSwitch(self, name, dpid=dpid)

    def build(self,count=5):
        hs = [ self.addHost('h%d' % (i+1) ) for i in range(count) ]
        ss = [ self.addSwitch(i+1)          for i in range(count) ]

        for i in range(count):
            self.addLink(hs[i], ss[i])

        for i in range(count-1):
            self.addLink(ss[i], ss[(i+1) % count])


class ProductionNetworkTopology(Topo):
    """The production network topology which will be cloned by the Topo cloner."""

    def build(self):
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        h9 = self.addHost('h9')
        h10 = self.addHost('h10')
        h11 = self.addHost('h11')
        h12 = self.addHost('h12')
        h13 = self.addHost('h13')
        h14 = self.addHost('h14')
        h15 = self.addHost('h15')
        h16 = self.addHost('h16')
        h17 = self.addHost('h17')
        h18 = self.addHost('h18')

        # Adding switches
        s1 = self.addSwitch('s1', dpid="0000000000000001")
        s2 = self.addSwitch('s2', dpid="0000000000000002")
        s3 = self.addSwitch('s3', dpid="0000000000000003")
        s4 = self.addSwitch('s4', dpid="0000000000000004")
        s5 = self.addSwitch('s5', dpid="0000000000000005")
        s6 = self.addSwitch('s6', dpid="0000000000000006")
        s7 = self.addSwitch('s7', dpid="0000000000000007")

        # Add links
        self.addLink(h1, s2)
        self.addLink(h2, s2)
        self.addLink(h3, s2)

        self.addLink(h4, s3)
        self.addLink(h5, s3)
        self.addLink(h6, s3)

        self.addLink(h7, s4)
        self.addLink(h8, s4)
        self.addLink(h9, s4)

        self.addLink(h10, s5)
        self.addLink(h11, s5)
        self.addLink(h12, s5)

        self.addLink(h13, s6)
        self.addLink(h14, s6)
        self.addLink(h15, s6)

        self.addLink(h16, s7)
        self.addLink(h17, s7)
        self.addLink(h18, s7)

        self.addLink(s1, s2)
        self.addLink(s1, s5)

        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s4, s7)

        self.addLink(s5, s6)
        self.addLink(s6, s7)


def getargs():
    parser = ArgumentParser(
        description="FILL ME IN" # TODO
    )

    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("-p", "--port", type=int, default=6653)

    return parser.parse_args()

def run():
    args = getargs()

    production_controller = RemoteController('c', args.host, args.port)
    production_network = Mininet(topo=ProductionNetworkTopology(), host=CPULimitedHost, controller=production_controller)
    production_network.start()

    CLI(production_network)

    production_network.stop()

# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
    run()

topos = {
    'production': ProductionNetworkTopology,
    'demo': DemoTopology
}

