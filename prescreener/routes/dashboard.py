from flask import Blueprint, render_template
from prescreener.models import Analysis

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    recent = (
        Analysis.query
        .order_by(Analysis.created_at.desc())
        .limit(20)
        .all()
    )
    return render_template("dashboard.html", analyses=recent)
