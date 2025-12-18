#!/usr/bin/env bash
set -e
echo "[+] Starting Ryu Controller"
cd controller
ryu-manager sdn_firewall_app.py
