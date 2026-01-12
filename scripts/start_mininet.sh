#!/usr/bin/env bash
set -e

echo "[+] 🧹 Dọn dẹp Mininet cũ..."
sudo mn -c

echo "[+] 🏫 Đang khởi tạo Topology Trường học..."
# Lưu ý: --topo school phải khớp với code python
sudo mn \
  --custom topology/school_topology.py \
  --topo school \
  --controller=remote,ip=127.0.0.1,port=6653 \
  --switch ovs,protocols=OpenFlow13
