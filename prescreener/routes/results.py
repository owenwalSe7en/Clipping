from flask import Blueprint, render_template, abort
from prescreener import db
from prescreener.models import Analysis

bp = Blueprint("results", __name__)


@bp.route("/results/<int:analysis_id>")
def show(analysis_id):
    analysis = db.session.get(Analysis, analysis_id)
    if not analysis:
        abort(404)
    return render_template("results.html", analysis=analysis)
