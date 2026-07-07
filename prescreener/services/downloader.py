import json
import logging
import shutil
import subprocess
import sys
from pathlib import Path

from flask import current_app

log = logging.getLogger("prescreener.downloader")

NODE_PATH = "/home/agent99/.local/share/mise/installs/node/25.1.0/bin/node"

def _find_yt_dlp():
    venv_bin = Path(sys.executable).parent / "yt-dlp"
    if venv_bin.exists():
        return str(venv_bin)
    found = shutil.which("yt-dlp")
    if found:
        return found
    raise FileNotFoundError(
        "yt-dlp not found. Install it with: pip install yt-dlp"
    )

YT_DLP_PATH = _find_yt_dlp()
YT_DLP_BASE = [YT_DLP_PATH, "--no-playlist"]


def _yt_dlp_flags():
    flags = list(YT_DLP_BASE)
    if Path(NODE_PATH).exists():
        flags += ["--js-runtimes", "node"]
    return flags


def _run_yt_dlp(args, label="yt-dlp"):
    cmd = _yt_dlp_flags() + args
    log.debug("Running: %s", " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stderr:
        for line in result.stderr.strip().splitlines():
            if "WARNING" in line:
                log.warning("[%s] %s", label, line.strip())
            elif result.returncode != 0:
                log.error("[%s] %s", label, line.strip())

    if result.returncode != 0:
        stderr_msg = result.stderr.strip() if result.stderr else "No error output"
        raise RuntimeError(
            f"yt-dlp failed (exit {result.returncode}): {_extract_error(stderr_msg)}"
        )

    return result


def _extract_error(stderr):
    for line in reversed(stderr.splitlines()):
        line = line.strip()
        if line.startswith("ERROR:"):
            return line[6:].strip()
    last_lines = stderr.strip().splitlines()[-3:]
    return "\n".join(last_lines) if last_lines else "Unknown error"


def download_audio(url):
    log.info("Starting download: %s", url)
    tmp = Path(current_app.config["TEMP_FOLDER"])
    tmp.mkdir(parents=True, exist_ok=True)
    out_template = str(tmp / "%(id)s.%(ext)s")

    info = _get_info(url)
    duration = info.get("duration", 0) or 0
    title = info.get("title", "Untitled")
    log.info("Video info: title=%r, duration=%ds, channel=%s",
             title, duration, info.get("channel", "?"))

    max_dur = current_app.config["MAX_VIDEO_DURATION"]
    if duration > max_dur:
        cost_est = (duration / 60) * current_app.config["WHISPER_RATE_PER_MIN"]
        raise ValueError(
            f"Video is {duration // 3600}h {(duration % 3600) // 60}m — "
            f"exceeds {max_dur // 3600}h limit. Estimated Whisper cost: ${cost_est:.2f}"
        )

    _run_yt_dlp(
        ["-x", "--audio-format", "mp3", "--audio-quality", "5",
         "-o", out_template, url],
        label="download",
    )

    vid_id = info.get("id", "audio")
    audio_path = tmp / f"{vid_id}.mp3"
    if not audio_path.exists():
        for f in tmp.iterdir():
            if f.suffix == ".mp3" and vid_id in f.name:
                audio_path = f
                break

    if not audio_path.exists():
        raise FileNotFoundError(f"yt-dlp did not produce audio file for {url}")

    log.info("Audio saved: %s (%.1f MB)", audio_path.name,
             audio_path.stat().st_size / 1024 / 1024)

    metadata = {
        "title": title,
        "channel": info.get("channel", info.get("uploader", "")),
        "duration": duration,
        "thumbnail": info.get("thumbnail", ""),
        "url": url,
    }
    return str(audio_path), metadata


def save_upload(file_storage):
    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = file_storage.filename or "upload"
    safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in filename)
    dest = upload_dir / safe_name
    file_storage.save(str(dest))
    log.info("Upload saved: %s (%.1f MB)", safe_name,
             dest.stat().st_size / 1024 / 1024)

    audio_path = str(dest)
    if dest.suffix.lower() in (".mp4", ".webm", ".mkv", ".mov", ".avi"):
        mp3_path = dest.with_suffix(".mp3")
        log.info("Converting %s to mp3 with ffmpeg", dest.suffix)
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", str(dest), "-vn", "-q:a", "5", str(mp3_path)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            log.error("ffmpeg conversion failed: %s", result.stderr[-500:] if result.stderr else "no output")
            raise RuntimeError(f"Failed to convert {dest.suffix} to mp3: {result.stderr[-200:] if result.stderr else 'unknown error'}")
        audio_path = str(mp3_path)
        dest.unlink(missing_ok=True)

    duration = _probe_duration(audio_path)

    metadata = {
        "title": Path(filename).stem,
        "channel": "File Upload",
        "duration": duration,
        "thumbnail": "",
        "url": "",
    }
    return audio_path, metadata


def cleanup(audio_path):
    try:
        p = Path(audio_path)
        if p.exists():
            p.unlink()
            log.debug("Cleaned up: %s", p.name)
    except Exception as e:
        log.warning("Cleanup failed for %s: %s", audio_path, e)


def _get_info(url):
    log.debug("Fetching metadata for: %s", url)
    result = _run_yt_dlp(["--dump-json", url], label="metadata")
    return json.loads(result.stdout)


def _probe_duration(path):
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-show_entries",
            "format=duration", "-of", "json", path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except Exception as e:
        log.warning("ffprobe duration failed for %s: %s", path, e)
        return 0
