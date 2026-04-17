# saas free-trial fraud detection system

while using claude i kept running out of limits and all i did was log in from multiple emails, but that got me thinking — if I had a SaaS platform, i really would not someone doing this. after some research, i realized this is a real problem called free-trial fraud, where a single user masks themselves as multiple users (guilty as charged — someone gift me claude pro)

---

## Problem

SaaS platforms commonly face free-trial abuse where users:

* Create multiple accounts using different email addresses
* Use VPNs or proxies to mask IP identity
* Use incognito mode to bypass tracking
* Automate account creation using bots

This leads to revenue loss and misleading product metrics.

---

## Solution

I'm building a composite identity for each user using multiple signals and assigns a risk score to every signup attempt.

User → Fingerprint + Behavior + IP → Risk Score → Action

---

## Features

### Device Fingerprinting

* User agent, OS, screen resolution, timezone
* Optional canvas and WebGL hashing
* Stable pseudonymous device identification

### Network Intelligence

* IP tracking and subnet analysis
* VPN/proxy detection
* ASN classification (residential vs datacenter)

### Email Intelligence

* Disposable email detection
* Email similarity detection
* Domain validation and normalization

### Behavioral Analysis

* Time taken to complete signup
* Keystroke count
* Mouse movement tracking
* Paste event detection

### Risk Scoring Engine

* Rule-based scoring system
* Optional ML model (XGBoost / Logistic Regression)
* Combined final risk score (0–100)

### Decision Engine

* Allow low-risk users
* Trigger CAPTCHA for medium risk
* Require verification (OTP) for high risk
* Block or flag critical cases

---

## Tech Stack

Flask, PostgreSQL, Redis, React, scikit-learn/XGBoost, Docker

---

## Development Roadmap

| Version | Focus      | Key Additions                                                     | Outcome                      |
| ------- | ---------- | ----------------------------------------------------------------- | ---------------------------- |
| v0.1    | MVP        | Basic APIs, PostgreSQL, simple fingerprinting, rule-based scoring | End-to-end working pipeline  |
| v0.2    | Signals    | IP tracking, VPN detection, email intelligence                    | Improved detection accuracy  |
| v0.3    | Behavior   | Keystrokes, mouse movement, timing signals                        | Bot and automation detection |
| v0.4    | Dashboard  | React dashboard, risk visualization, logs                         | System observability         |
| v0.5    | ML         | Train model, combine with rules                                   | Adaptive fraud detection     |
| v0.6    | Actions    | CAPTCHA, OTP, blocking logic                                      | Full response system         |
| v0.7    | Hardening  | Anti-evasion, subnet/ASN tracking                                 | Handles advanced attackers   |
| v0.8    | Feedback   | Labeling, retraining, drift detection                             | Self-improving system        |
| v1.0    | Production | Multi-tenant, API keys, monitoring                                | Scalable SaaS-ready product  |

---

## How It Works

1. User visits signup page
2. Frontend collects device, network, and behavioral data
3. Data is sent to backend ingestion API
4. Features are computed
5. Risk score is generated
6. Decision engine determines action
7. Outcome is logged for future learning

---

## Demo Scenario

* User signs up with multiple email variations
* System detects same device fingerprint
* Email similarity is identified
* Risk score increases
* CAPTCHA or blocking is triggered

---

## Future Improvements

* Advanced fingerprinting techniques
* Graph-based fraud detection
* Real-time streaming pipeline
* Explainability dashboards
* Multi-tenant SaaS expansion

---
