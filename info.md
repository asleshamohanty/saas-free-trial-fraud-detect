# Current Progress

This document summarizes what has been built so far, how the system works, and how to test it.

---

## What We Have Built

We now have a **working backend fraud detection system** with:

* Flask API (`/score`)
* Feature extraction pipeline
* Rule-based risk scoring engine
* Decision logic (allow / captcha / block)
* Basic in-memory tracking (device/IP counts)

This is the **core engine** of the project.

---

## Folder Structure (Current Scope)

```
backend/
│
├── app.py
├── routes/
│   └── score.py
│
├── services/
│   ├── feature_builder.py
│   ├── email_service.py
│   ├── ip_service.py
│
├── risk_engine/
│   └── rules.py
```

---

## File-by-File Explanation

### `app.py`

* Entry point of the Flask app
* Registers routes
* Starts the server

---

### `routes/score.py`

* Defines `/score` endpoint
* Handles incoming request
* Calls feature builder
* Calls risk engine
* Returns final response

---

### `services/feature_builder.py`

* Converts raw input → structured features
* Tracks:

  * accounts per device
  * accounts per IP
* Combines all signals into a single feature dictionary

---

### `services/email_service.py`

* Detects disposable email domains
* Simple rule-based check

---

### `services/ip_service.py`

* Placeholder logic for VPN detection
* Will be replaced with real IP intelligence later

---

### `risk_engine/rules.py`

* Core fraud detection logic
* Assigns risk score based on:

  * email type
  * device reuse
  * behavior
* Returns:

  * score (0–100)
  * reasons list

---

## Data Flow

1. User sends request to `/score`
2. Backend receives JSON input
3. Feature builder processes raw data
4. Features passed to rules engine
5. Risk score calculated
6. Decision logic applied
7. Response returned

Flow:

User → API (/score) → Feature Builder → Rules Engine → Decision → Response

---

## Sample Postman Request

### Endpoint

```
POST http://127.0.0.1:5000/score
```

### Headers

```
Content-Type: application/json
```

### Body

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

---

## Sample Response

```json
{
  "risk_score": 95,
  "action": "block",
  "reasons": [
    "Disposable email",
    "Form filled too fast",
    "No mouse movement",
    "Very few keystrokes"
  ]
}
```

---

## What This System Currently Does

* Detects obvious fraud patterns
* Flags:

  * disposable emails
  * repeated device usage
  * bot-like behavior
* Assigns a risk score
* Suggests an action

---

## Current Limitations

* No database (yet)
* Uses in-memory counters (resets on restart)
* No real IP intelligence
* No ML model

---

## What Comes Next

Next upgrade will include:

1. Supabase (PostgreSQL) integration
2. Persistent storage:

   * users
   * fingerprints
   * events
3. Real history-based fraud detection
4. Replace in-memory tracking with DB queries

---

## Key Concept

This system answers:

> “Is this signup likely coming from a real new user or the same user abusing free trials?”

---

## Status

Backend MVP: Complete
Ready for: Database integration
