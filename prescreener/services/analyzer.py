import logging
import traceback
from datetime import datetime, timezone

from flask import Flask

from prescreener import db
from prescreener.models import Analysis, Moment, CostLog
from prescreener.services import downloader, whisper_service, claude_service

log = logging.getLogger("prescreener.analyzer")


def run_analysis(app: Flask, analysis_id: int):
    with app.app_context():
        analysis = db.session.get(Analysis, analysis_id)
        if not analysis:
            log.error("Analysis %d not found in database", analysis_id)
            return

        log.info("Starting analysis %d: type=%s, source=%s",
                 analysis_id, analysis.source_type,
                 analysis.source_url[:100] if analysis.source_url else "?")

        audio_path = None
        try:
            _update(analysis, "downloading", 10, "Downloading audio...")
            log.info("[%d] Downloading audio...", analysis_id)

            if analysis.source_type == "youtube_url":
                audio_path, meta = downloader.download_audio(analysis.source_url)
            else:
                audio_path = analysis.source_url
                meta = {
                    "title": analysis.source_title,
                    "channel": "File Upload",
                    "duration": 0,
                    "thumbnail": "",
                }

            analysis.source_title = meta.get("title", analysis.source_title)
            analysis.source_channel = meta.get("channel", "")
            analysis.thumbnail_url = meta.get("thumbnail", "")
            analysis.duration_seconds = meta.get("duration", 0)
            db.session.commit()

            _update(analysis, "transcribing", 30, "Transcribing with Whisper...")
            log.info("[%d] Transcribing %ds of audio...",
                     analysis_id, int(analysis.duration_seconds))

            result = whisper_service.transcribe(audio_path)

            analysis.transcript_text = result["text"]
            analysis.transcript_json = result["segments"]
            analysis.duration_seconds = result["duration_seconds"] or analysis.duration_seconds
            analysis.whisper_cost = result["cost"]
            db.session.commit()

            _log_cost(analysis.id, "whisper", result["cost"], {
                "duration_minutes": round(result["duration_seconds"] / 60, 1),
                "rate": "0.006/min",
            })
            log.info("[%d] Transcription complete: %d segments, cost=$%.4f",
                     analysis_id, len(result["segments"]), result["cost"])

            _update(analysis, "analyzing", 60, "Finding clip-worthy moments...")
            log.info("[%d] Analyzing transcript with Claude...", analysis_id)

            claude_result = claude_service.analyze_moments(
                result["segments"], analysis.source_title
            )

            analysis.claude_cost = claude_result["cost"]
            analysis.total_cost = analysis.whisper_cost + analysis.claude_cost
            db.session.commit()

            _log_cost(analysis.id, "claude", claude_result["cost"], {
                "input_tokens": claude_result["input_tokens"],
                "output_tokens": claude_result["output_tokens"],
                "model": "claude-sonnet-4-6",
            })
            log.info("[%d] Claude found %d moments, cost=$%.4f",
                     analysis_id, len(claude_result["moments"]), claude_result["cost"])

            _update(analysis, "saving", 85, "Saving moments...")
            for m in claude_result["moments"]:
                moment = Moment(
                    analysis_id=analysis.id,
                    start_seconds=m.get("start_seconds", 0),
                    end_seconds=m.get("end_seconds", 0),
                    transcript_excerpt=m.get("transcript_excerpt", ""),
                    virality_score=m.get("virality_score", 5),
                    category=m.get("category", "quotable"),
                    reason=m.get("reason", ""),
                )
                db.session.add(moment)
            db.session.commit()

            analysis.status = "complete"
            analysis.progress_pct = 100
            analysis.current_step = "Done"
            analysis.completed_at = datetime.now(timezone.utc)
            db.session.commit()

            log.info("[%d] Analysis complete. Total cost: $%.4f, moments: %d",
                     analysis_id, analysis.total_cost, len(claude_result["moments"]))

        except Exception as e:
            tb = traceback.format_exc()
            error_msg = str(e)

            analysis.status = "failed"
            analysis.error_message = error_msg
            analysis.current_step = "Failed"
            db.session.commit()

            log.error("[%d] Analysis failed at step '%s': %s",
                      analysis_id, analysis.current_step, error_msg)
            log.debug("[%d] Full traceback:\n%s", analysis_id, tb)

        finally:
            if audio_path and analysis.source_type == "youtube_url":
                downloader.cleanup(audio_path)


def _update(analysis, status, pct, step):
    analysis.status = status
    analysis.progress_pct = pct
    analysis.current_step = step
    db.session.commit()


def _log_cost(analysis_id, service, amount, details):
    log_entry = CostLog(
        analysis_id=analysis_id,
        service=service,
        amount=amount,
        details=details,
    )
    db.session.add(log_entry)
    db.session.commit()
