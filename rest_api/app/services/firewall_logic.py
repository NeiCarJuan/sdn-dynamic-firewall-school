from app.services.ryu_client import send_block_ip
from app.core.logger import logger

known_attacks = set()

def analyze_attack(data):
    src_ip = data.get("src_ip")
    attack_type = data.get("type")

    signature = f"{src_ip}:{attack_type}"

    if signature in known_attacks:
        logger.info("Known attack → auto block")
        return block_ip(src_ip)

    # attack mới → học
    known_attacks.add(signature)
    logger.info("New attack learned")
    return {
        "status": "learned",
        "message": "New attack pattern recorded"
    }

def block_ip(ip):
    logger.info(f"Blocking IP {ip}")
    return send_block_ip(ip)
