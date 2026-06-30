from sqlalchemy import func
from prescreener import db
from prescreener.models import Analysis, CostLog
from prescreener.config import Config


def get_summary():
    total_whisper = db.session.query(func.sum(CostLog.amount)).filter(
        CostLog.service == "whisper"
    ).scalar() or 0.0

    total_claude = db.session.query(func.sum(CostLog.amount)).filter(
        CostLog.service == "claude"
    ).scalar() or 0.0

    total_opusclip = db.session.query(func.sum(CostLog.amount)).filter(
        CostLog.service == "opusclip"
    ).scalar() or 0.0

    total_spent = total_whisper + total_claude + total_opusclip
    analyses_count = db.session.query(func.count(Analysis.id)).filter(
        Analysis.status == "complete"
    ).scalar() or 0

    return {
        "total_budget": Config.TOTAL_BUDGET,
        "total_spent": round(total_spent, 2),
        "remaining": round(Config.TOTAL_BUDGET - total_spent, 2),
        "whisper_spent": round(total_whisper, 4),
        "claude_spent": round(total_claude, 4),
        "opusclip_spent": round(total_opusclip, 2),
        "analyses_count": analyses_count,
        "avg_cost": round(total_spent / analyses_count, 4) if analyses_count else 0,
    }


def get_recent_costs(limit=20):
    logs = (
        CostLog.query
        .order_by(CostLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": l.id,
            "service": l.service,
            "amount": round(l.amount, 4),
            "details": l.details,
            "analysis_title": l.analysis.source_title if l.analysis else "Manual",
            "created_at": l.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for l in logs
    ]


def log_opusclip(credits_used, notes=""):
    cost_per_credit = 29.0 / 300  # Pro plan: $29 for 300 credits
    amount = credits_used * cost_per_credit
    log = CostLog(
        analysis_id=None,
        service="opusclip",
        amount=round(amount, 4),
        details={"credits": credits_used, "notes": notes},
    )
    db.session.add(log)
    db.session.commit()
    return round(amount, 4)
