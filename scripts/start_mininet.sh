#!/usr/bin/env bash
set -e
echo "[+] Starting Mininet topology"
cd controller/topology
sudo python3 school_topology.py
#!/bin/bash
sudo mn -c
sudo mn --custom controller/topology/school_topology.py \
        --topo school \
        --controller=remote,ip=127.0.0.1,port=6633 \
        --switch ovs,protocols=OpenFlow13
