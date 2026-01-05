from mininet.topo import Topo

class SchoolTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')

        # Student
        h1 = self.addHost('h1', ip='10.0.0.1/24')

        # Accounting department
        h2 = self.addHost('h2', ip='10.0.0.2/24')

        # Attacker (internal threat)
        h3 = self.addHost('h3', ip='10.0.0.100/24')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

topos = { 'school': SchoolTopo }
