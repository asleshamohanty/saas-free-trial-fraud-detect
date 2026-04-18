def calculate_risk(features):
    score = 0
    reasons = []

    # High risk signals
    if features["is_disposable_email"]:
        score += 30
        reasons.append("Disposable email")

    if features["accounts_per_device"] > 2:
        score += 40
        reasons.append("Multiple accounts from same device")

    if features["is_vpn"]:
        score += 20
        reasons.append("VPN detected")

    # Behavioral signals
    if features["time_to_submit"] < 3000:
        score += 20
        reasons.append("Form filled too fast")

    if features["mouse_distance"] == 0:
        score += 15
        reasons.append("No mouse movement")

    if features["keystrokes"] < 5:
        score += 10
        reasons.append("Very few keystrokes")

    return min(score, 100), reasons