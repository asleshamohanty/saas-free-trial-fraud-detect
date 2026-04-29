def calculate_risk(features):
    score = 0
    reasons = []

    # -----------------------------------------
    # Email Signals
    # -----------------------------------------
    if features.get("is_disposable_email"):
        score += 20
        reasons.append("Disposable email")

    # -----------------------------------------
    # IP / Network Signals
    # -----------------------------------------
    if features.get("is_suspicious_ip"):
        score += 15
        reasons.append("Suspicious IP infrastructure")

    accounts_per_ip = features.get("accounts_per_ip", 0)

    if 5 <= accounts_per_ip < 10:
        score += 15
        reasons.append("Moderate IP reuse")

    elif accounts_per_ip >= 10:
        score += 25
        reasons.append("High IP reuse")

    # Cloud provider check
    cloud_words = ["amazon", "google", "digitalocean", "ovh", "hetzner"]

    isp = features.get("isp", "").lower()

    if any(word in isp for word in cloud_words):
        score += 10
        reasons.append("Cloud-hosted IP")

    # -----------------------------------------
    # Device Signals
    # -----------------------------------------
    accounts_per_device = features.get("accounts_per_device", 0)

    if accounts_per_device == 2:
        score += 10
        reasons.append("Repeated device usage")

    elif 3 <= accounts_per_device < 5:
        score += 20
        reasons.append("Heavy device reuse")

    elif accounts_per_device >= 5:
        score += 30
        reasons.append("Extreme device reuse")

    # -----------------------------------------
    # Behavioral Signals
    # -----------------------------------------
    time_to_submit = features.get("time_to_submit", 99999)
    keystrokes = features.get("keystrokes", 0)
    mouse_distance = features.get("mouse_distance", 0)

    if time_to_submit < 800:
        score += 10
        reasons.append("Signup completed too fast")

    if keystrokes <= 2:
        score += 10
        reasons.append("Very low typing activity")

    if mouse_distance == 0:
        score += 10
        reasons.append("No mouse movement")

    # -----------------------------------------
    # Cap Score
    # -----------------------------------------
    if score > 100:
        score = 100

    # -----------------------------------------
    # Decision Engine
    # -----------------------------------------
    if score >= 60:
        action = "block"
    elif score >= 30:
        action = "captcha"
    else:
        action = "allow"

    return {
        "risk_score": score,
        "action": action,
        "reasons": reasons
    }