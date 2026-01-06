import requests

# Đây KHÔNG PHẢI controller
# Đây là Firewall Module (phần của Ninh)
FIREWALL_API_URL = "http://127.0.0.1:9000/firewall/context"

def send_user_context(user, role, ip):
    payload = {
        "user": user,
        "role": role,
        "ip": ip
    }

    try:
        response = requests.post(FIREWALL_API_URL, json=payload, timeout=3)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

