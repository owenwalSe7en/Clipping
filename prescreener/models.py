from datetime import datetime, timezone
from prescreener import db


class Analysis(db.Model):
    __tablename__ = "analyses"

    id = db.Column(db.Integer, primary_key=True)
    source_type = db.Column(db.String(20))  # youtube_url | file_upload
    source_url = db.Column(db.String(500))
    source_title = db.Column(db.String(255), default="Untitled")
    source_channel = db.Column(db.String(255), default="")
    thumbnail_url = db.Column(db.String(500), default="")
    duration_seconds = db.Column(db.Float, default=0)
    transcript_text = db.Column(db.Text, default="")
    transcript_json = db.Column(db.JSON, default=list)
    status = db.Column(db.String(50), default="pending")
    progress_pct = db.Column(db.Integer, default=0)
    current_step = db.Column(db.String(100), default="")
    error_message = db.Column(db.Text, nullable=True)
    whisper_cost = db.Column(db.Float, default=0.0)
    claude_cost = db.Column(db.Float, default=0.0)
    total_cost = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

    moments = db.relationship("Moment", back_populates="analysis", cascade="all, delete-orphan")
    cost_logs = db.relationship("CostLog", back_populates="analysis", cascade="all, delete-orphan")


class Moment(db.Model):
    __tablename__ = "moments"

    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey("analyses.id"), nullable=False)
    start_seconds = db.Column(db.Float)
    end_seconds = db.Column(db.Float)
    transcript_excerpt = db.Column(db.Text, default="")
    virality_score = db.Column(db.Integer, default=5)
    category = db.Column(db.String(50), default="quotable")
    reason = db.Column(db.Text, default="")
    approved = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)

    analysis = db.relationship("Analysis", back_populates="moments")

    @property
    def duration(self):
        return (self.end_seconds or 0) - (self.start_seconds or 0)

    @property
    def start_display(self):
        return _fmt(self.start_seconds)

    @property
    def end_display(self):
        return _fmt(self.end_seconds)

    @property
    def color(self):
        if self.virality_score >= 9:
            return "red"
        if self.virality_score >= 7:
            return "orange"
        if self.virality_score >= 5:
            return "yellow"
        return "gray"


class CostLog(db.Model):
    __tablename__ = "cost_logs"

    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey("analyses.id"), nullable=True)
    service = db.Column(db.String(50))  # whisper | claude | opusclip
    amount = db.Column(db.Float, default=0.0)
    details = db.Column(db.JSON, default=dict)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    analysis = db.relationship("Analysis", back_populates="cost_logs")


def _fmt(seconds):
    if seconds is None:
        return "00:00"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"
