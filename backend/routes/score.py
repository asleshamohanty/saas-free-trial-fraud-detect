from flask import Blueprint, request, jsonify

from services.feature_builder import build_features
from risk_engine.rules import calculate_risk

score_blueprint = Blueprint("score", __name__)


@score_blueprint.route("/score", methods=["POST"])
def score():
    data = request.get_json()

    features = build_features(data)

    result = calculate_risk(features)

    return jsonify(result)