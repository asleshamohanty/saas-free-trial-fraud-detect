from services.email_service import is_disposable_email
from services.ip_service import is_vpn_ip
from db.db import SessionLocal
from db.models import User, Fingerprint, SignupEvent


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

    email = data.get("email")
    ip = data.get("ip")
    device_id = data.get("device_id")

    user = get_or_create_user(db, email)
    fingerprint = get_or_create_fingerprint(db, device_id)

    # store event
    event = SignupEvent(
        user_id=user.id,
        fingerprint_id=fingerprint.id,
        ip_address=ip
    )
    db.add(event)
    db.commit()

    # query counts
    accounts_per_device = db.query(SignupEvent)\
        .filter_by(fingerprint_id=fingerprint.id)\
        .count()

    accounts_per_ip = db.query(SignupEvent)\
        .filter_by(ip_address=ip)\
        .count()

    features = {
        "accounts_per_device": accounts_per_device,
        "accounts_per_ip": accounts_per_ip,
        "time_to_submit": data.get("time_to_submit", 0),
        "keystrokes": data.get("keystrokes", 0),
        "mouse_distance": data.get("mouse_distance", 0),
        "is_disposable_email": False,  # keep your existing logic
        "is_vpn": False
    }

    db.close()
    print("DEBUG:",
      "device_count=", accounts_per_device,
      "ip_count=", accounts_per_ip)
    return features