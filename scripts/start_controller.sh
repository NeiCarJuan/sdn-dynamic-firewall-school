#!/usr/bin/env bash
set -e

echo "[+] Starting Ryu Controller..."
ryu-manager controller/sdn_firewall_app.py
