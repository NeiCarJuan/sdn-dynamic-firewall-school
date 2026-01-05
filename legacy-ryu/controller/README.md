# SDN Controller & Dynamic Firewall (Ryu)

## Vai trò
Thư mục `controller/` chứa phần **SDN-based Dynamic Firewall**:
- Ryu Controller (OpenFlow)
- Thu thập thống kê traffic
- Phát hiện bất thường bằng z-score
- Cơ chế học thích nghi (auto-learn)
- REST API cho Captive Portal / Dashboard

## Công nghệ
- Python 3
- Ryu Controller
- OpenFlow
- Mininet + Open vSwitch
- NumPy

## Cấu trúc chính
controller/
- sdn_firewall_app.py # Ryu app chính
- rest_api.py # REST API
- topology/ # Mininet topology
- modules/ # AI, rule engine, collector
- data/ # learned signatures, rules
- tests/ # traffic / attack scripts

