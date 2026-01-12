#!/usr/bin/env bash

echo "[+] 🛑 Đang dừng toàn bộ hệ thống..."

# 1. Tắt các tiến trình Python (API, Portal, IDS)
pkill -f "python3 firewall_api/api.py" || true
pkill -f "python3 portal/app.py" || true
pkill -f "python3 ids_watcher.py" || true

# 2. Tắt Faucet
pkill -f faucet || true

# 3. Dọn dẹp Mininet
echo "[+] 🧹 Dọn dẹp Mininet..."
sudo mn -c

echo "[+] ✅ Đã tắt xong!"
