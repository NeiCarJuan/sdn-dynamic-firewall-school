"""
Ninh: Mininet topology for school network
"""
# TODO: implement Mininet topology
from mininet.topo import Topo

class SchoolTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')

        h_student = self.addHost('h1', ip='10.0.0.1/24')
        h_teacher = self.addHost('h2', ip='10.0.0.2/24')
        h_server  = self.addHost('h3', ip='10.0.0.100/24')

        self.addLink(h_student, s1)
        self.addLink(h_teacher, s1)
        self.addLink(h_server,  s1)

topos = {
    'school': (lambda: SchoolTopo())
}
