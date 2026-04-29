import hashlib

from db.db import SessionLocal
from db.models import User, Fingerprint, SignupEvent

from services.email_service import normalize_email, is_disposable_email
from services.ip_service import get_ip_intelligence


def generate_fingerprint(data):
    raw = (
        str(data.get("user_agent", "")) +
        str(data.get("screen_resolution", "")) +
        str(data.get("timezone", "")) +
        str(data.get("language", ""))
    )

    return hashlib.sha256(raw.encode()).hexdigest()


def get_or_create_user(db, email):
    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


def get_or_create_fingerprint(db, device_id):
    fp = db.query(Fingerprint).filter_by(hash=device_id).first()

    if not fp:
        fp = Fingerprint(hash=device_id)
        db.add(fp)
        db.commit()
        db.refresh(fp)

    return fp


def build_features(data):
    db = SessionLocal()

    raw_email = data.get("email", "")
    email = normalize_email(raw_email)

    ip = data.get("ip", "")

    device_id = generate_fingerprint(data)

    ip_info = get_ip_intelligence(ip)

    user = get_or_create_user(db, email)
    fingerprint = get_or_create_fingerprint(db, device_id)

    # store signup event
    event = SignupEvent(
        user_id=user.id,
        fingerprint_id=fingerprint.id,
        ip_address=ip
    )

    db.add(event)
    db.commit()

    # counts
    accounts_per_device = db.query(SignupEvent)\
        .filter_by(fingerprint_id=fingerprint.id)\
        .count()

    accounts_per_ip = db.query(SignupEvent)\
        .filter_by(ip_address=ip)\
        .count()

    accounts_per_user = db.query(SignupEvent)\
        .filter_by(user_id=user.id)\
        .count()

    features = {
        "accounts_per_device": accounts_per_device,
        "accounts_per_ip": accounts_per_ip,
        "accounts_per_user": accounts_per_user,

        "time_to_submit": data.get("time_to_submit", 0),
        "keystrokes": data.get("keystrokes", 0),
        "mouse_distance": data.get("mouse_distance", 0),

        "is_disposable_email": int(is_disposable_email(raw_email)),
        "normalized_email": email,

        "fingerprint_hash": device_id,

        "is_suspicious_ip": int(ip_info["is_suspicious_ip"]),
        "country": ip_info["country"],
        "isp": ip_info["isp"],
        "org": ip_info["org"]
    }

    db.close()

    return features