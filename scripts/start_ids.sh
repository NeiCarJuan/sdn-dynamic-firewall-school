#!/usr/bin/env bash
set -e

echo "[+] 👁️ Đang khởi động IDS Watcher trên Switch s1..."
# Yêu cầu quyền sudo để chạy ovs-ofctl
sudo python3 ids_watcher.py
