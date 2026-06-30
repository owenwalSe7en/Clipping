import csv
import io
from flask import Blueprint, jsonify, request, Response
from prescreener import db
from prescreener.models import Analysis, Moment

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/status/<int:analysis_id>")
def status(analysis_id):
    a = db.session.get(Analysis, analysis_id)
    if not a:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "status": a.status,
        "progress_pct": a.progress_pct,
        "current_step": a.current_step,
        "error": a.error_message,
        "title": a.source_title,
        "duration": a.duration_seconds,
        "whisper_cost": a.whisper_cost,
        "claude_cost": a.claude_cost,
        "total_cost": a.total_cost,
    })


@bp.route("/timeline/<int:analysis_id>")
def timeline(analysis_id):
    a = db.session.get(Analysis, analysis_id)
    if not a:
        return jsonify({"error": "Not found"}), 404

    moments = sorted(a.moments, key=lambda m: m.start_seconds or 0)
    return jsonify({
        "title": a.source_title,
        "duration_seconds": a.duration_seconds,
        "moments": [
            {
                "id": m.id,
                "start": m.start_seconds,
                "end": m.end_seconds,
                "duration": m.duration,
                "virality_score": m.virality_score,
                "category": m.category,
                "reason": m.reason,
                "excerpt_preview": (m.transcript_excerpt or "")[:120],
                "color": m.color,
                "approved": m.approved,
                "start_display": m.start_display,
                "end_display": m.end_display,
            }
            for m in moments
        ],
    })


@bp.route("/moments/<int:moment_id>/approve", methods=["POST"])
def approve_moment(moment_id):
    m = db.session.get(Moment, moment_id)
    if not m:
        return jsonify({"error": "Not found"}), 404
    m.approved = not m.approved
    db.session.commit()
    return jsonify({"approved": m.approved})


@bp.route("/moments/<int:moment_id>/notes", methods=["POST"])
def save_notes(moment_id):
    m = db.session.get(Moment, moment_id)
    if not m:
        return jsonify({"error": "Not found"}), 404
    m.notes = request.json.get("notes", "")
    db.session.commit()
    return jsonify({"ok": True})


@bp.route("/export/<int:analysis_id>")
def export_csv(analysis_id):
    a = db.session.get(Analysis, analysis_id)
    if not a:
        return jsonify({"error": "Not found"}), 404

    approved = [m for m in a.moments if m.approved]
    approved.sort(key=lambda m: m.virality_score or 0, reverse=True)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Start Time", "End Time", "Duration (s)", "Score",
        "Category", "Reason", "Excerpt", "Source URL",
    ])
    for m in approved:
        writer.writerow([
            m.start_display, m.end_display, round(m.duration, 1),
            m.virality_score, m.category, m.reason,
            (m.transcript_excerpt or "")[:200], a.source_url or "",
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=clips_{analysis_id}.csv"},
    )
