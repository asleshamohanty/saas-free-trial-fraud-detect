def is_vpn_ip(ip):
    # dummy logic for now
    if ip.startswith("10.") or ip.startswith("192.168"):
        return False
    return False  # later replace with real API