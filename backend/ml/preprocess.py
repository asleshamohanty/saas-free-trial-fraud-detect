import pandas as pd
import numpy as np

np.random.seed(42)

# -------------------------------------------------
# Load raw exported dataset
# -------------------------------------------------
df = pd.read_csv("ml/data/dataset.csv")

# -------------------------------------------------
# Core historical count features
# -------------------------------------------------
df["accounts_per_ip"] = df.groupby("ip_address")["ip_address"].transform("count")
df["accounts_per_device"] = df.groupby("fingerprint_id")["fingerprint_id"].transform("count")
df["accounts_per_user"] = df.groupby("user_id")["user_id"].transform("count")

# -------------------------------------------------
# Real suspicious rows = fraud examples
# -------------------------------------------------
fraud = df[
    [
        "accounts_per_ip",
        "accounts_per_device",
        "accounts_per_user"
    ]
].copy()

# Add fraud-oriented signals
fraud["is_suspicious_ip"] = np.random.choice([0, 1], len(fraud), p=[0.3, 0.7])
fraud["is_disposable_email"] = np.random.choice([0, 1], len(fraud), p=[0.4, 0.6])

fraud["time_to_submit"] = np.random.randint(200, 1400, len(fraud))
fraud["keystrokes"] = np.random.randint(0, 5, len(fraud))
fraud["mouse_distance"] = np.random.randint(0, 120, len(fraud))

fraud["label"] = 1

# Add noise to counts
fraud["accounts_per_ip"] += np.random.randint(-2, 3, len(fraud))
fraud["accounts_per_device"] += np.random.randint(-1, 2, len(fraud))
fraud["accounts_per_user"] += np.random.randint(-1, 2, len(fraud))

fraud = fraud.clip(lower=0)

# -------------------------------------------------
# Legit user samples
# -------------------------------------------------
n = len(fraud)

legit = pd.DataFrame({
    "accounts_per_ip": np.random.randint(1, 5, n),
    "accounts_per_device": np.random.randint(1, 3, n),
    "accounts_per_user": np.random.randint(1, 3, n),

    "is_suspicious_ip": np.random.choice([0, 1], n, p=[0.9, 0.1]),
    "is_disposable_email": np.random.choice([0, 1], n, p=[0.95, 0.05]),

    "time_to_submit": np.random.randint(2500, 9000, n),
    "keystrokes": np.random.randint(8, 25, n),
    "mouse_distance": np.random.randint(150, 900, n),

    "label": 0
})

# -------------------------------------------------
# Medium-risk gray zone rows
# -------------------------------------------------
m = n // 3

medium = pd.DataFrame({
    "accounts_per_ip": np.random.randint(3, 8, m),
    "accounts_per_device": np.random.randint(2, 5, m),
    "accounts_per_user": np.random.randint(1, 4, m),

    "is_suspicious_ip": np.random.choice([0, 1], m, p=[0.5, 0.5]),
    "is_disposable_email": np.random.choice([0, 1], m, p=[0.7, 0.3]),

    "time_to_submit": np.random.randint(1000, 4000, m),
    "keystrokes": np.random.randint(3, 10, m),
    "mouse_distance": np.random.randint(50, 250, m),

    "label": np.random.choice([0, 1], m)
})

# -------------------------------------------------
# Combine + Shuffle
# -------------------------------------------------
final_df = pd.concat([fraud, legit, medium], ignore_index=True)

final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

# -------------------------------------------------
# Save
# -------------------------------------------------
final_df.to_csv("ml/data/training_data.csv", index=False)

print(final_df["label"].value_counts())
print(final_df.head())
print("enhanced training dataset created")