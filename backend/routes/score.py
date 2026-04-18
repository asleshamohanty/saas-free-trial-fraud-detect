from flask import Blueprint, request, jsonify
from services.feature_builder import build_features
from risk_engine.rules import calculate_risk

score_blueprint = Blueprint("score", __name__)

@score_blueprint.route("/score", methods=["POST"])
def score():
    data = request.json

    # 1. Build features
    features = build_features(data)

    # 2. Calculate risk
    risk_score, reasons = calculate_risk(features)

    # 3. Decide action
    if risk_score < 30:
        action = "allow"
    elif risk_score < 60:
        action = "captcha"
    else:
        action = "block"

    return jsonify({
        "risk_score": risk_score,
        "action": action,
        "reasons": reasons
    })