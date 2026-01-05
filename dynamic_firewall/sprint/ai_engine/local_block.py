blocked_hosts = set()

def local_block(ip):
    blocked_hosts.add(ip)
    print(f"[AI] Temporarily blocking host {ip}")

def is_blocked(ip):
    return ip in blocked_hosts
