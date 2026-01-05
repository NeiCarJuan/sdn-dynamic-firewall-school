import httpx

RYU_API = "http://10.0.0.1:8080/firewall/block"

def send_block_ip(ip: str):
    payload = {"ip": ip}
    response = httpx.post(RYU_API, json=payload, timeout=3)

    return {
        "ryu_status": response.status_code,
        "ryu_response": response.json()
    }
