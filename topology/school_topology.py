from mininet.topo import Topo

class SchoolTopo(Topo):
    def build(self):
        # Tạo Switch trung tâm
        s1 = self.addSwitch('s1')

        # --------------------------------------------------
        # Host 1: Student (Alice) - KẺ TẤN CÔNG
        # Vai trò: Thực hiện DDoS Flood làm giảm Entropy
        # --------------------------------------------------
        h1 = self.addHost('h1',
                          ip='10.0.0.1/24',
                          mac='00:00:00:00:00:01')

        # --------------------------------------------------
        # Host 2: Web Server/Target - NẠN NHÂN
        # Vai trò: Bị tấn công (Trong demo đã chặn RST tại đây)
        # --------------------------------------------------
        h2 = self.addHost('h2',
                          ip='10.0.0.2/24',
                          mac='00:00:00:00:00:02')

        # --------------------------------------------------
        # Host 3: Admin/Normal User (Bob) - NGƯỜI VÔ TỘI
        # Vai trò: Dùng để kiểm chứng mạng vẫn thông (Entropy cao)
        # --------------------------------------------------
        h3 = self.addHost('h3',
                          ip='10.0.0.3/24',
                          mac='00:00:00:00:00:03')

        # Kết nối vào Switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

topos = { 'school': SchoolTopo }
