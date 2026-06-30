from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from prescreener.services.costs import get_summary, get_recent_costs, log_opusclip

bp = Blueprint("costs", __name__)


@bp.route("/costs")
def show():
    summary = get_summary()
    recent = get_recent_costs()
    return render_template("costs.html", summary=summary, recent=recent)


@bp.route("/api/costs/summary")
def api_summary():
    return jsonify(get_summary())


@bp.route("/api/costs/opusclip", methods=["POST"])
def api_opusclip():
    data = request.json or {}
    credits = data.get("credits", 0)
    notes = data.get("notes", "")
    if credits <= 0:
        return jsonify({"error": "Credits must be positive"}), 400
    amount = log_opusclip(credits, notes)
    return jsonify({"logged": True, "amount": amount})
