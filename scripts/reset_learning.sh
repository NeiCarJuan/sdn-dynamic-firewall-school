#!/usr/bin/env bash
set -e
echo "[+] 🧹 Resetting AI Memory..."

# Reset file trạng thái của model trong thư mục firewall_api
echo '{
  "threshold": 5.0,
  "history": []
}' > firewall_api/model_state.json

echo "[+] Đã xóa lịch sử học của AI về mặc định."
