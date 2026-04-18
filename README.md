This project is being built incrementally, following a versioned development roadmap.
![Version](https://img.shields.io/badge/version-v0.3-blue)
![Status](https://img.shields.io/badge/status-active%20development-yellow)

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
Unlike traditional systems that rely on a single signal (IP or email), this system builds a probabilistic identity using multiple weak signals combined into a unified risk score.

User → Fingerprint + Behavior + IP → Risk Score → Action

---

## Current Implementation Scope

The current version includes a fully functional rule-based fraud detection system with real-time scoring via a REST API.

Machine learning, advanced IP intelligence, and dashboarding are planned in upcoming versions.

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

Flask, PostgreSQL (Supabase), SQLAlchemy, Python

---

## Development Roadmap

The project is built in incremental versions, starting from a simple rule-based system and evolving into a scalable, production-ready SaaS fraud detection platform.

| Version | Focus        | Key Additions                                    | Outcome                                  |
| ------- | ------------ | ------------------------------------------------ | ---------------------------------------- |
| v0.1    | MVP          | Flask API, rule-based scoring                    | Basic working fraud detection API        |
| v0.2    | Signals      | Email checks, device tracking, basic behavior    | Multi-signal detection working           |
| v0.3    | Database     | PostgreSQL (Supabase), event storage             | Persistent history-based detection       |
| v0.4    | Intelligence | IP analysis, VPN detection, feature improvements | Stronger fraud detection accuracy        |
| v0.5    | ML           | Train model, combine with rules                  | Adaptive fraud detection system          |
| v0.6    | Dashboard    | React dashboard, risk visualization              | System observability and demo capability |
| v0.7    | Actions      | CAPTCHA, OTP, blocking logic                     | Full fraud response system               |
| v0.8    | Hardening    | Anti-evasion, subnet/ASN tracking                | Handles advanced attackers               |
| v1.0    | Production   | Multi-tenant, API keys, monitoring               | Scalable SaaS-ready platform             |

---

### Progression Strategy

The system evolves in three major phases:

* **Foundation (v0.1 – v0.3)**
  Build core fraud detection logic and introduce persistent storage for tracking user behavior over time.

* **Intelligence (v0.4 – v0.5)**
  Improve detection accuracy using richer signals and machine learning.

* **Productization (v0.6 – v1.0)**
  Add dashboards, enforcement mechanisms, and scalability features to transform the system into a production-ready SaaS platform.

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

## Project Status

- Current Version: v0.1 (MVP Complete)
- Next Milestone: v0.3 — Database Integration (PostgreSQL / Supabase)

### Completed
- Flask API with `/score` endpoint
- Rule-based fraud detection engine
- Multi-signal feature extraction (email, device, behavior)
- Risk scoring + decision system (allow / captcha / block)

### In Progress
- Persistent storage (Supabase PostgreSQL)
- Replacing in-memory tracking with database queries
