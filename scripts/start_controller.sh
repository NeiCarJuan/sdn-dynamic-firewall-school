#!/usr/bin/env bash

# Tạo thư mục logs nếu chưa có
mkdir -p logs

echo "[+] 🧠 Đang khởi động Firewall API (Brain)..."
python3 firewall_api/api.py > logs/api.log 2>&1 &
PID_API=$!
echo "   -> API chạy với PID: $PID_API"

echo "[+] 🌐 Đang khởi động Captive Portal..."
python3 portal/app.py > logs/portal.log 2>&1 &
PID_PORTAL=$!
echo "   -> Portal chạy với PID: $PID_PORTAL"

echo "[+] ✅ SERVICES STARTED (API + PORTAL)"
echo "   (Dùng tên start_controller.sh nhưng chạy Services nhé)"

# Giữ script không bị tắt
wait
