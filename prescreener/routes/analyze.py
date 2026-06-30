import threading
from flask import Blueprint, request, redirect, url_for, flash, current_app
from prescreener import db
from prescreener.models import Analysis
from prescreener.services.analyzer import run_analysis
from prescreener.services.downloader import save_upload

bp = Blueprint("analyze", __name__)


@bp.route("/analyze", methods=["POST"])
def start_analysis():
    source_type = request.form.get("source_type", "youtube_url")

    if source_type == "youtube_url":
        url = request.form.get("url", "").strip()
        if not url:
            flash("Please enter a YouTube URL.", "error")
            return redirect(url_for("dashboard.index"))

        analysis = Analysis(
            source_type="youtube_url",
            source_url=url,
            source_title="Loading...",
            status="pending",
        )
        db.session.add(analysis)
        db.session.commit()

    elif source_type == "file_upload":
        file = request.files.get("file")
        if not file or not file.filename:
            flash("Please select a file.", "error")
            return redirect(url_for("dashboard.index"))

        audio_path, meta = save_upload(file)
        analysis = Analysis(
            source_type="file_upload",
            source_url=audio_path,
            source_title=meta["title"],
            duration_seconds=meta["duration"],
            status="pending",
        )
        db.session.add(analysis)
        db.session.commit()

    else:
        flash("Invalid source type.", "error")
        return redirect(url_for("dashboard.index"))

    app = current_app._get_current_object()
    thread = threading.Thread(
        target=run_analysis, args=(app, analysis.id), daemon=True
    )
    thread.start()

    return redirect(url_for("results.show", analysis_id=analysis.id))
