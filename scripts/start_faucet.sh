#!/usr/bin/env bash
set -e

echo "[+] 🚰 Đang khởi động FAUCET Controller..."
# Đảm bảo file cấu hình tồn tại
if [ ! -f /etc/faucet/faucet.yaml ]; then
    echo "ERROR: Không tìm thấy /etc/faucet/faucet.yaml"
    exit 1
fi

# Chạy Faucet và hiển thị log ra màn hình
faucet --verbose --config /etc/faucet/faucet.yaml
