# Current Progress

This document summarizes the evolution of the system across versions (v0.1 → v0.3), what has been built, and how to test each stage.

---

# v0.1 — MVP (Rule-Based Fraud Detection)

## What Was Built

* Flask API (`/score`)
* Rule-based risk scoring engine
* Basic feature extraction
* Decision logic (allow / captcha / block)

---

## Key Files

```
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

### Request

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

### Expected

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

`feature_builder.py` now tracks:

```python
accounts_per_device
accounts_per_ip
```

(using in-memory dictionaries)

---

## How It Works

* System combines:

  * email + device + behavior
* Risk increases if same device is reused

---

## How to Test (v0.2)

Send same request multiple times:

### Expected

```
1st request → low risk
2nd request → higher risk
3rd request → even higher risk
```

---

## Limitations

* Data resets when server restarts
* Not scalable
* No real persistence

---

# v0.3 — Database Integration (Supabase)

## What Was Added

* PostgreSQL (Supabase)
* Persistent event storage
* Real identity tracking
* Query-based fraud detection

---

## Database Design

### Tables

* `users` → email identity
* `fingerprints` → device identity
* `signup_events` → behavioral history

---

## Key Files

```
backend/
├── db/
│   ├── db.py              # DB connection
│   ├── models.py          # table definitions
│   ├── optimize.sql       # indexes + constraints
│   ├── init_db.py         # create tables
│   ├── run_sql.py         # apply optimizations
```

---

## What Changed in Logic

### Before (v0.2)

```python
DEVICE_COUNT = {}
```

### After (v0.3)

```python
db.query(SignupEvent).filter_by(...).count()
```

Counts now come from database (persistent)

---

## Optimizations Applied

To ensure performance at scale:

* Index on `signup_events.ip_address`
* Index on `signup_events.fingerprint_id`
* Index on `signup_events.user_id`
* Unique constraint on `fingerprints.hash`
* Index on `users.email`

This avoids full table scans and enables fast fraud queries

---

## How It Works

1. User sends request
2. System:

   * gets/creates user
   * gets/creates fingerprint
   * stores signup event
3. Queries DB:

   * accounts per device
   * accounts per IP
4. Risk engine evaluates
5. Action returned

---

## How to Test (v0.3)

### Step 1 — Send same request multiple times

```json
{
  "email": "test@gmail.com",
  "ip": "1.2.3.4",
  "device_id": "device123",
  "time_to_submit": 1000,
  "keystrokes": 2,
  "mouse_distance": 0
}
```

---

### Step 2 — Observe behavior

| Request | accounts_per_device |
| ------- | ------------------- |
| 1st     | 1                   |
| 2nd     | 2                   |
| 3rd     | 3                   |

Risk score should increase accordingly

---

### Step 3 — Verify in database

Check `signup_events` table:

* Multiple rows added
* Same `fingerprint_id`
* Same `ip_address`

---

### Step 4 — Cross-email test (important)

Change only email:

```json
{
  "email": "test2@gmail.com",
  "ip": "1.2.3.4",
  "device_id": "device123"
}
```

Expected:

* Device reuse still detected
* Fraud still flagged

---

## What This Enables

* Persistent fraud detection
* Cross-session tracking
* Device-level identity linking
* Real-world applicability

---

## Limitations (Current)

* No real VPN detection
* Simple fingerprinting
* No email similarity detection
* No ML model

---

# Summary

| Version | Capability                                  |
| ------- | ------------------------------------------- |
| v0.1    | Basic rule-based detection                  |
| v0.2    | Multi-signal detection (in-memory)          |
| v0.3    | Persistent, database-backed fraud detection |

---

## Current Status

Backend System: Production-style MVP
Version: v0.3
Ready for: Intelligence Layer (v0.4)
