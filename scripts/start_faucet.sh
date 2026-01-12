#!/usr/bin/env bash
set -e

echo "[+] 🚰 Đang khởi động FAUCET Controller..."

# --- SỬA DÒNG NÀY ---
# Cũ (Sai): export FAUCET_CONFIG=/etc/faucet/faucet.yaml
# Mới (Đúng): Trỏ vào file trong thư mục hiện tại của bạn
export FAUCET_CONFIG=$(pwd)/faucet/faucet.yaml
# --------------------

export FAUCET_LOG=STDOUT

# Chạy Faucet
faucet --verbose
