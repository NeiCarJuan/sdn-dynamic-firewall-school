#!/usr/bin/env bash
set -e

echo "[+] Updating system"
sudo apt update

echo "[+] Installing base packages"
sudo apt install -y git python3-pip openvswitch-switch mininet

echo "[+] Installing Python libs"
pip3 install ryu numpy flask requests

echo "[+] Done bootstrap"
