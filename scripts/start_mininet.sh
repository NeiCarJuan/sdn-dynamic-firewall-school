#!/usr/bin/env bash
set -e
echo "[+] Starting Mininet topology"
cd controller/topology
sudo python3 school_topology.py
