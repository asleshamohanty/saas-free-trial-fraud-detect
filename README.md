This project is being built incrementally, following a versioned development roadmap.

![Version](https://img.shields.io/badge/version-v0.4-blue)
![Status](https://img.shields.io/badge/status-active%20development-yellow)

# saas free-trial fraud detection system

while using claude i kept running out of limits and all i did was log in from multiple emails, but that got me thinking — if i had a SaaS platform, i would not want users abusing trials this way. after some research, i realized this is a real problem called free-trial fraud, where a single user masks themselves as multiple users (guilty as charged — someone gift me claude pro).

---

## Problem

SaaS platforms commonly face free-trial abuse where users:

* create multiple accounts using different email addresses
* use VPNs or proxies to mask IP identity
* use incognito mode or fresh browsers
* automate account creation using bots

This leads to revenue loss, infrastructure abuse, and misleading product metrics.

---

## Solution

i'm building a composite identity for each user using multiple signals and assigning a risk score to every signup attempt.

Unlike traditional systems that rely on one signal (IP or email), this system builds a probabilistic identity using multiple weak signals combined into one unified fraud score.

```text id="e0ek0u"
User → Fingerprint + Behavior + IP + Email → Risk Score → Action
```

---

## Current Implementation Scope

The current version includes a working backend fraud detection engine with:

* REST API scoring endpoint
* persistent PostgreSQL storage
* historical identity tracking
* email intelligence
* browser fingerprinting
* IP intelligence
* calibrated allow / captcha / block actions

Machine learning, dashboards, and advanced anti-evasion systems are planned in upcoming versions.

---

## Features

### Device Fingerprinting

* user agent
* screen resolution
* timezone
* language
* hashed pseudonymous device identity

### Network Intelligence

* IP reuse analysis
* suspicious proxy / hosting detection
* cloud provider detection
* provider metadata (ISP / org / country)

### Email Intelligence

* disposable email detection
* gmail alias normalization
* canonical identity mapping

### Behavioral Analysis

* time taken to complete signup
* keystroke count
* mouse movement distance

### Risk Scoring Engine

* weighted rule-based scoring
* multi-signal fraud confidence model
* optional ML layer planned in v0.5

### Decision Engine

* allow low-risk users
* trigger CAPTCHA for medium risk
* block high-risk signups

---

## Tech Stack

Flask, PostgreSQL (Supabase), SQLAlchemy, Python

---

## Development Roadmap

The project is built in incremental versions, starting from a simple rule-based system and evolving into a scalable fraud prevention platform.

| Version | Focus        | Key Additions                                    | Outcome                            |
| ------- | ------------ | ------------------------------------------------ | ---------------------------------- |
| v0.1    | MVP          | Flask API, rule-based scoring                    | Basic working fraud detection API  |
| v0.2    | Signals      | Email checks, device tracking, behavior signals  | Multi-signal detection             |
| v0.3    | Database     | PostgreSQL (Supabase), event storage             | Persistent history-based detection |
| v0.4    | Intelligence | IP analysis, fingerprinting, email normalization | Stronger fraud detection accuracy  |
| v0.5    | ML           | Train model, combine with rules                  | Adaptive fraud detection           |
| v0.6    | Dashboard    | React dashboard, risk visualization              | System observability               |
| v0.7    | Actions      | CAPTCHA, OTP, blocking logic                     | Full fraud response system         |
| v0.8    | Hardening    | Anti-evasion, subnet / ASN tracking              | Handles advanced attackers         |
| v1.0    | Production   | Multi-tenant, API keys, monitoring               | SaaS-ready platform                |

---

## Progression Strategy

The system evolves in three major phases:

### Foundation (v0.1 – v0.3)

Build core fraud detection logic and persistent storage for user history.

### Intelligence (v0.4 – v0.5)

Improve detection accuracy using richer signals and machine learning.

### Productization (v0.6 – v1.0)

Add dashboards, enforcement mechanisms, and scalability features.

---

## How It Works

1. user visits signup page
2. frontend collects device, network, and behavioral data
3. data is sent to backend scoring API
4. features are computed
5. risk score is generated
6. decision engine determines action
7. outcome is logged for future learning

---

## Demo Scenario

* user signs up with multiple email variations
* system detects same fingerprint
* IP history is reused
* risk score increases
* CAPTCHA or blocking is triggered

---

## Future Improvements

* machine learning fraud scoring
* graph-based fraud rings detection
* streaming real-time detection
* explainability dashboard
* multi-tenant SaaS deployment

---

## Project Status

* Current Version: v0.4 (Intelligence Layer Complete)
* Next Milestone: v0.5 — Machine Learning Risk Scoring

### Completed

* Flask API with `/score`
* rule-based fraud engine
* PostgreSQL persistent storage
* historical IP / device tracking
* browser fingerprinting
* email normalization
* disposable email checks
* suspicious IP intelligence
* calibrated fraud actions

### In Progress

* dataset generation for ML
* feature logging for training
* fraud probability model (v0.5)
