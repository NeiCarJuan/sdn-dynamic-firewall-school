#!/usr/bin/env bash
set -e
echo "[+] Stopping Mininet & Ryu"
sudo mn -c || true
pkill -f ryu-manager || true
echo "[+] Done"
