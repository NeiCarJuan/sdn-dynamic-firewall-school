from fastapi import APIRouter

router = APIRouter()

@router.post("/block")
def block_ip(ip: str):
    return {
        "action": "block",
        "ip": ip,
        "result": "stub (no ryu yet)"
    }
