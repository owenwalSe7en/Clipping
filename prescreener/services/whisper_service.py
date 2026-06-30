import logging
import math
import subprocess
import json
from pathlib import Path
from openai import OpenAI
from flask import current_app

log = logging.getLogger("prescreener.whisper")

MAX_CHUNK_SIZE_MB = 24
MAX_CHUNK_BYTES = MAX_CHUNK_SIZE_MB * 1024 * 1024


def transcribe(audio_path):
    client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
    path = Path(audio_path)
    file_size = path.stat().st_size

    if file_size <= MAX_CHUNK_BYTES:
        log.info("Transcribing single file (%.1f MB)", file_size / 1024 / 1024)
        segments = _transcribe_file(client, audio_path)
    else:
        log.info("File too large (%.1f MB), chunking for transcription",
                 file_size / 1024 / 1024)
        segments = _transcribe_chunked(client, audio_path)

    full_text = " ".join(s["text"].strip() for s in segments)
    duration_seconds = segments[-1]["end"] if segments else 0
    duration_min = duration_seconds / 60
    cost = duration_min * current_app.config["WHISPER_RATE_PER_MIN"]

    return {
        "text": full_text,
        "segments": segments,
        "duration_seconds": duration_seconds,
        "cost": round(cost, 4),
    }


def _transcribe_file(client, audio_path):
    with open(audio_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )
    return [
        {"start": s.start, "end": s.end, "text": s.text}
        for s in (response.segments or [])
    ]


def _transcribe_chunked(client, audio_path):
    duration = _get_duration(audio_path)
    chunk_secs = 600  # 10-minute chunks
    num_chunks = math.ceil(duration / chunk_secs)

    all_segments = []
    tmp_dir = Path(current_app.config["TEMP_FOLDER"])

    for i in range(num_chunks):
        start = i * chunk_secs
        chunk_path = tmp_dir / f"chunk_{i}.mp3"
        log.debug("Chunking segment %d/%d (start=%ds)", i + 1, num_chunks, start)

        result = subprocess.run(
            [
                "ffmpeg", "-y", "-i", audio_path,
                "-ss", str(start), "-t", str(chunk_secs),
                "-vn", "-q:a", "5", str(chunk_path),
            ],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            log.error("ffmpeg chunk %d failed: %s", i, result.stderr[-300:] if result.stderr else "no output")
            raise RuntimeError(f"ffmpeg failed to create chunk {i}: {result.stderr[-200:] if result.stderr else 'unknown'}")

        try:
            segments = _transcribe_file(client, str(chunk_path))
            for seg in segments:
                seg["start"] += start
                seg["end"] += start
            all_segments.extend(segments)
            log.debug("Chunk %d/%d: %d segments transcribed", i + 1, num_chunks, len(segments))
        finally:
            chunk_path.unlink(missing_ok=True)

    return all_segments


def _get_duration(path):
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-show_entries",
            "format=duration", "-of", "json", path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except Exception:
        return 3600
