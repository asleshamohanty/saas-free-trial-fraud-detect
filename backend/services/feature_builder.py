from services.email_service import is_disposable_email
from services.ip_service import is_vpn_ip

# temporary in-memory store (we'll replace with DB later)
DEVICE_COUNT = {}
IP_COUNT = {}

def build_features(data):
    email = data.get("email")
    ip = data.get("ip")
    device_id = data.get("device_id")
    time_to_submit = data.get("time_to_submit", 0)
    keystrokes = data.get("keystrokes", 0)
    mouse_distance = data.get("mouse_distance", 0)

    # update counts
    DEVICE_COUNT[device_id] = DEVICE_COUNT.get(device_id, 0) + 1
    IP_COUNT[ip] = IP_COUNT.get(ip, 0) + 1

    features = {
        "is_disposable_email": is_disposable_email(email),
        "is_vpn": is_vpn_ip(ip),
        "accounts_per_device": DEVICE_COUNT[device_id],
        "accounts_per_ip": IP_COUNT[ip],
        "time_to_submit": time_to_submit,
        "keystrokes": keystrokes,
        "mouse_distance": mouse_distance
    }

    return features