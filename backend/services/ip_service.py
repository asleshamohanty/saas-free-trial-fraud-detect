import requests
from functools import lru_cache

@lru_cache(maxsize=500)
def get_ip_intelligence(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=proxy,hosting,country,isp,org"
        response = requests.get(url, timeout=3)
        data = response.json()

        return {
            "is_suspicious_ip": data.get("proxy", False) or data.get("hosting", False),
            "country": data.get("country", ""),
            "isp": data.get("isp", ""),
            "org": data.get("org", "")
        }

    except Exception:
        return {
            "is_suspicious_ip": False,
            "country": "",
            "isp": "",
            "org": ""
        }