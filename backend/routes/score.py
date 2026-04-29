from flask import Blueprint, request, jsonify

from services.feature_builder import build_features
from risk_engine.rules import calculate_risk
from ml.inference import predict_fraud_probability

score_blueprint = Blueprint("score", __name__)


@score_blueprint.route("/score", methods=["POST"])
def score():
    data = request.get_json()

    # Build features
    features = build_features(data)

    # Rules score
    rules_result = calculate_risk(features)
    rules_score = rules_result["risk_score"]

    # ML probability
    ml_prob = predict_fraud_probability(features)
    ml_score = ml_prob * 100

    # Hybrid score
    final_score = int((0.6 * rules_score) + (0.4 * ml_score))

    # Final action
    if final_score >= 60:
        action = "block"
    elif final_score >= 30:
        action = "captcha"
    else:
        action = "allow"

    return jsonify({
        "rules_score": rules_score,
        "ml_probability": round(ml_prob, 4),
        "final_score": final_score,
        "action": action,
        "reasons": rules_result["reasons"]
    })