# Current Progress

This document summarizes the evolution of the system across versions (v0.1 → v0.4), what has been built, and how to test each stage.

---

# v0.1 — MVP (Rule-Based Fraud Detection)

## What Was Built

* Flask API (`/score`)
* Rule-based risk scoring engine
* Basic feature extraction
* Decision logic (allow / captcha / block)

---

## Key Files

```text
backend/
├── app.py
├── routes/score.py
├── services/feature_builder.py
├── risk_engine/rules.py
```

---

## How It Works

1. User sends request to `/score`
2. Features are extracted from input
3. Rules engine assigns risk score
4. Action is returned

---

## How to Test (v0.1)

```json
{
  "email": "test@tempmail.com",
  "ip": "1.2.3.4",
  "device_id": "device123",
  "time_to_submit": 1000,
  "keystrokes": 2,
  "mouse_distance": 0
}
```

Expected:

* High risk score
* Action: block

---

## Limitations

* No memory of past users
* Each request treated independently

---

# v0.2 — Multi-Signal Detection (In-Memory)

## What Was Added

* Email intelligence
* Device tracking (in-memory)
* Behavioral signals:

  * time to submit
  * keystrokes
  * mouse movement

---

## Key Update

`feature_builder.py` tracked:

```python
accounts_per_device
accounts_per_ip
```

(using Python dictionaries / memory)

---

## How to Test

Send same request multiple times.

Expected:

```text
1st request → low risk
2nd request → higher risk
3rd request → even higher risk
```

---

## Limitations

* Data resets when server restarts
* Not scalable
* No persistence

---

# v0.3 — Database Integration (Supabase)

## What Was Added

* PostgreSQL (Supabase)
* SQLAlchemy ORM
* Persistent event storage
* Historical fraud detection
* Real identity linking

---

## Database Tables

* `users` → email identity
* `fingerprints` → device identity
* `signup_events` → signup history

---

## Key Files

```text
backend/
├── db/
│   ├── db.py
│   ├── models.py
│   ├── init_db.py
│   ├── optimize.sql
│   ├── run_sql.py
```

---

## What Changed

Before:

```python
DEVICE_COUNT = {}
```

After:

```python
db.query(SignupEvent).filter_by(...).count()
```

Now counts persist permanently.

---

## Optimizations Applied

* Index on `signup_events.ip_address`
* Index on `signup_events.fingerprint_id`
* Index on `signup_events.user_id`
* Unique fingerprint hash
* Index on `users.email`

---

## How to Test

Send same payload repeatedly.

Expected:

| Request | accounts_per_device |
| ------- | ------------------- |
| 1st     | 1                   |
| 2nd     | 2                   |
| 3rd     | 3                   |

Risk score rises.

---

## What This Enabled

* Persistent fraud memory
* Cross-session detection
* Device reuse detection
* Real-world backend architecture

---

# v0.4 — Intelligence Layer

## What Was Added

* Email normalization
* Disposable email detection
* Browser/device fingerprint hashing
* IP intelligence
* Suspicious IP infrastructure detection
* Cloud-hosted IP detection
* Calibrated weighted scoring
* Better allow / captcha / block logic

---

## Email Intelligence

Detects alias abuse like:

```text
trial@gmail.com
trial+1@gmail.com
t.r.i.a.l@gmail.com
```

Normalized into one identity signal.

---

## Fingerprinting Upgrade

Instead of trusting manual `device_id`, system now hashes:

* user_agent
* screen_resolution
* timezone
* language

This creates a more stable device identity.

---

## IP Intelligence

Uses external IP metadata to detect:

* proxy / VPN style traffic
* hosting / datacenter traffic
* suspicious providers

Signals stored as:

```python
is_suspicious_ip
country
isp
org
```

---

## Risk Engine Upgrade

Now scores from multiple categories:

* Email risk
* Device reuse
* IP reuse
* Suspicious infrastructure
* Behavioral bot signals

---

## Key Files

```text
backend/
├── services/
│   ├── email_service.py
│   ├── ip_service.py
│   ├── feature_builder.py
│
├── risk_engine/
│   └── rules.py
```

---

## How to Test (v0.4)

## Test 1 — Clean User

```json
{
  "email": "fresh@gmail.com",
  "ip": "normal_ip",
  "user_agent": "Chrome",
  "screen_resolution": "1440x900",
  "timezone": "Asia/Kolkata",
  "language": "en-US",
  "time_to_submit": 4000,
  "keystrokes": 15,
  "mouse_distance": 350
}
```

Expected:

```text
allow
```

---

## Test 2 — Alias Abuse

```json
{
  "email": "trial+1@gmail.com"
}
```

Then:

```json
{
  "email": "t.r.i.a.l@gmail.com"
}
```

Expected:

```text
captcha / rising risk
```

---

## Test 3 — Reused Device

Same browser fingerprint + many emails.

Expected:

```text
captcha → block later
```

---

## Test 4 — Suspicious IP + Fast Signup

Expected:

```text
block
```

---

## What This Enabled

* Detect disguised repeat users
* Detect hosted/VPN infrastructure
* Stronger confidence scoring
* Reduced false positives via weighted signals

---

# Summary

| Version | Capability                                 |
| ------- | ------------------------------------------ |
| v0.1    | Basic rule-based detection                 |
| v0.2    | Multi-signal detection (memory only)       |
| v0.3    | Persistent database-backed fraud detection |
| v0.4    | Intelligence-driven multi-signal detection |

---

# Current Status

Backend System: Production-style intelligent fraud detection engine
Version: v0.4
Next Milestone: v0.5 — Machine Learning Risk Scoring
