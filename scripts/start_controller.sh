#!/usr/bin/env bash
set -e

echo "[+] Activating Ryu virtualenv"
source ~/ryu-env/bin/activate

echo "[+] Starting Ryu Controller on port 6653"
cd controller
ryu-manager sdn_firewall_app.py --ofp-tcp-listen-port 6653
