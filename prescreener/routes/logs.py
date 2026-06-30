from collections import deque
from pathlib import Path

from flask import Blueprint, render_template, jsonify, request

bp = Blueprint("logs", __name__)

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


def _tail(filepath, n=200):
    if not filepath.exists():
        return []
    with open(filepath) as f:
        return list(deque(f, maxlen=n))


@bp.route("/logs")
def show():
    return render_template("logs.html")


@bp.route("/api/logs")
def get_logs():
    log_type = request.args.get("type", "all")
    lines = int(request.args.get("lines", 100))
    lines = min(lines, 500)

    if log_type == "errors":
        raw = _tail(LOG_DIR / "errors.log", lines)
    else:
        raw = _tail(LOG_DIR / "prescreener.log", lines)

    entries = []
    for line in raw:
        line = line.rstrip()
        if not line:
            continue
        level = "INFO"
        for lvl in ("ERROR", "WARNING", "DEBUG", "INFO"):
            if f" {lvl}" in line[:35]:
                level = lvl
                break
        entries.append({"text": line, "level": level})

    return jsonify({"entries": entries, "total": len(entries)})
