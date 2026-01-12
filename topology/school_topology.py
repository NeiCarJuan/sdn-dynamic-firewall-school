from mininet.topo import Topo

class SchoolTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')

        # --------------------------------------------------
        # Host 1: Student (Alice)
        # IP: 10.0.0.1, MAC: 00:00:00:00:00:01
        # --------------------------------------------------
        h1 = self.addHost('h1', 
                          ip='10.0.0.1/24', 
                          mac='00:00:00:00:00:01',
                          defaultRoute='via 10.0.0.254')

        # --------------------------------------------------
        # Host 2: Admin/Accounting Staff (Bob)
        # IP: 10.0.0.2, MAC: 00:00:00:00:00:02
        # --------------------------------------------------
        h2 = self.addHost('h2', 
                          ip='10.0.0.2/24', 
                          mac='00:00:00:00:00:02',
                          defaultRoute='via 10.0.0.254')

        # --------------------------------------------------
        # Host 3: Server Kế Toán (Mục tiêu bảo vệ)
        # IP: 10.0.0.3, MAC: 00:00:00:00:00:03
        # --------------------------------------------------
        h3 = self.addHost('h3', 
                          ip='10.0.0.3/24', 
                          mac='00:00:00:00:00:03',
                          defaultRoute='via 10.0.0.254')

        # Kết nối vào Switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

topos = { 'school': SchoolTopo }
