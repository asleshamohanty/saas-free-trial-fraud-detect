import pandas as pd
from db.db import SessionLocal
from db.models import SignupEvent

db = SessionLocal()

rows = db.query(SignupEvent).all()

data = []

for row in rows:
    data.append({
        "user_id": row.user_id,
        "fingerprint_id": row.fingerprint_id,
        "ip_address": row.ip_address
    })

df = pd.DataFrame(data)

df.to_csv("ml/data/dataset.csv", index=False)

print("dataset exported")

db.close()