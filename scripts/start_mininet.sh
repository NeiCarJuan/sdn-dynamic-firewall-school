#!/usr/bin/env bash
set -e

echo "[+] Cleaning old Mininet state..."
sudo mn -c

echo "[+] Starting Mininet topology (port=6653)..."
sudo mn --custom controller/topology/school_topology.py \
        --topo school \
        --controller=remote,ip=127.0.0.1,port=6653 \
        --switch ovs,protocols=OpenFlow13
