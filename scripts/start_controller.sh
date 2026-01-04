#!/usr/bin/env bash
set -e

echo "[+] Starting Ryu Controller on port 6653"
ryu-manager controller/sdn_firewall_app.py --ofp-tcp-listen-port 6653
