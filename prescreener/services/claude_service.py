import json
import logging

import anthropic
from flask import current_app

log = logging.getLogger("prescreener.claude")

SYSTEM_PROMPT = """You are an expert at identifying viral, clip-worthy moments in long-form \
content for a mindset/self-improvement audience (young men 18-30).

You analyze transcripts and find the moments that would make excellent 15-90 second clips \
for TikTok, Instagram Reels, and YouTube Shorts. You focus on:
- Emotional peaks (vulnerability, anger, excitement, confrontation)
- Quotable wisdom (one-liners, mental models, life advice)
- Controversial takes (opinions that spark debate)
- Story arcs (narrative turning points, breakthroughs, realizations)
- Wisdom bombs (actionable frameworks, counterintuitive advice)
- Wealth and money talk (making money, millions/billions, getting rich, financial wins, \
buying expensive things, wealth flexes, money mindset shifts)

You return ONLY valid JSON — no markdown fencing, no explanation."""

USER_PROMPT_TEMPLATE = """Analyze this transcript and identify the top {max_moments} \
clip-worthy moments for a mindset/self-improvement short-form video page.

VIDEO TITLE: {title}

TRANSCRIPT (with timestamps in seconds):
{transcript}

For each moment return a JSON object with these exact keys:
- "start_seconds" (number): exact start timestamp from the transcript
- "end_seconds" (number): end timestamp (clip should be 30-90 seconds)
- "transcript_excerpt" (string): the exact quoted text from that segment
- "virality_score" (integer 1-10):
    9-10 = must-clip (emotional peak, shocking, major revelation)
    7-8 = strong (quotable wisdom, surprising take, raw vulnerability)
    5-6 = decent (interesting point, good story beat)
    1-4 = skip
- "category" (string): one of "emotional_peak", "quotable", "controversial", "story_arc", "wisdom_bomb", "wealth_money"
- "reason" (string, max 80 chars): why this moment is clip-worthy

RULES:
- Only return moments with virality_score >= 5
- Timestamps MUST match actual transcript segments — do not invent timestamps
- Each clip should be 30-90 seconds (end_seconds - start_seconds)
- Rank by virality_score descending
- Be realistic with scores — most moments are 5-7, very few are 9-10
- Prioritize emotional/vulnerable moments over purely informational ones
- Any mention of specific dollar amounts (millions, billions), making money, getting rich, \
or wealth flexes should score at least 7 — these consistently perform well with the target audience

Return a JSON array of objects. Nothing else."""


def analyze_moments(transcript_segments, video_title=""):
    client = anthropic.Anthropic(api_key=current_app.config["ANTHROPIC_API_KEY"])

    transcript_text = "\n".join(
        f"[{s['start']:.1f}s - {s['end']:.1f}s] {s['text'].strip()}"
        for s in transcript_segments
    )

    max_moments = current_app.config["MAX_MOMENTS"]

    response = client.messages.create(
        model=current_app.config["CLAUDE_MODEL"],
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(
                    max_moments=max_moments,
                    title=video_title,
                    transcript=transcript_text,
                ),
            }
        ],
    )

    raw = response.content[0].text
    log.debug("Claude raw response length: %d chars", len(raw))

    moments = _parse_moments(raw)

    input_cost = response.usage.input_tokens * current_app.config["CLAUDE_INPUT_RATE"]
    output_cost = response.usage.output_tokens * current_app.config["CLAUDE_OUTPUT_RATE"]

    log.info("Claude analysis: %d moments found, %d input tokens, %d output tokens",
             len(moments), response.usage.input_tokens, response.usage.output_tokens)

    return {
        "moments": moments,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cost": round(input_cost + output_cost, 4),
    }


def _parse_moments(raw_text):
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    start = text.find("[")
    end = text.rfind("]") + 1
    if start == -1 or end == 0:
        log.warning("Could not find JSON array in Claude response: %s...", text[:200])
        return []

    try:
        return json.loads(text[start:end])
    except json.JSONDecodeError as e:
        log.error("Failed to parse Claude JSON response: %s", e)
        log.debug("Raw response was: %s", text[:1000])
        raise ValueError(f"Claude returned invalid JSON: {e}") from e
