# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**Clipping Venture:** A two-phase automated system for generating and monetizing short-form video clips from long-form content (Twitch streams, podcasts, YouTube).

**Phase 1 (Weeks 1-4):** OpusClip-based validation with manual publishing ($29/month OpusClip subscription)

**Phase 2 (Weeks 5-8+, optional):** DIY Claude Code-based clip generation system (if Phase 1 earnings exceed $300+/week)

**Target Markets:** Video bounty platforms (Content Rewards, Whop, Vyro, Clipify) paying $2-10 per 1K views

---

## Documentation Architecture

All strategy and execution documentation lives in `MGMT_docs/`. These are **not code files**—they are specification documents for the venture itself.

```
MGMT_docs/
├─ YOUR_STRATEGY.md                    # Your exact implementation path (start here)
├─ PHASE_1_AUTOMATION_BLUEPRINT.md     # Complete Phase 1 setup & Python automation code
├─ PHASE_2_OPUSCLIP_REPLACEMENT.md     # Optional DIY replacement (Whisper + Claude API + FFmpeg)
├─ CREATOR_ANALYSIS_REPORT.md          # Top 10+ vetted creators to clip from (BOGGLES, HIVISE recommended)
├─ 01_IMPLEMENTATION_STEPS.md          # Week-by-week detailed roadmap
├─ 02_BOT_AVOIDANCE_PLAYBOOK.md        # Platform rate limits, posting patterns, ban prevention
├─ CRITICAL_UPDATE_OPUSCLIP_PRICING.md # Pricing analysis ($0.10/clip at 300 clips/month)
├─ INDEX.md                            # Full navigation map
└─ _ARCHIVE/                           # Legacy documents (reference only)
```

---

## How Claude Code Fits In

Claude Code is used for **automation scripting and orchestration** during both phases:

### Phase 1: OpusClip Integration Scripts
The `PHASE_1_AUTOMATION_BLUEPRINT.md` includes 4 production-ready Python scripts (copy-paste ready):

1. **OpusClip Orchestrator** - Download VODs, submit to OpusClip, retrieve generated clips
2. **Multi-Platform Publisher** - Publish clips to ShortSync, Rumble, and bounty platforms
3. **Earnings Aggregator** - Track views and earnings across platforms in real-time
4. **Bot Avoidance Safety Gates** - Enforce posting limits and humanized delays per platform

**Claude Code's Role:** Write these orchestration scripts, adapt them per creator, monitor execution

### Phase 2: DIY Clip Generation (Optional)
If Phase 1 succeeds, `PHASE_2_OPUSCLIP_REPLACEMENT.md` provides complete DIY architecture:

1. **Whisper (Transcription)** - Python script for audio→text
2. **PySceneDetect (Scene Detection)** - Scene boundary detection
3. **Claude API (Moment Analysis)** - Transcript analysis for viral moments
4. **FFmpeg (Rendering)** - GPU-accelerated clip extraction
5. **Orchestrator** - Full pipeline coordination

**Claude Code's Role:** Build, test, and optimize the entire pipeline

---

## Critical Numbers & Economics

### Phase 1: OpusClip (Weeks 1-4)
- **Cost:** $29/month OpusClip + $15-35/month distribution tools
- **Time:** 2-3 hours/day for 4 weeks
- **Target Volume:** 50-70 clips published
- **Target Revenue:** $200-1,000 (bounty payouts)
- **Success Metric:** $150+/week earnings by Week 4

### Phase 2: DIY (Optional, Weeks 5-8+)
- **Cost:** $60-170/month (infrastructure + Claude API)
- **Development Time:** 40-60 hours (spread over 4 weeks, parallel to Phase 1)
- **Payback Period:** 3-4 months (only if Phase 1 succeeds)
- **Scaling Capacity:** 600+ clips/month (vs 300 max with OpusClip tiers)

---

## Key Platform Constraints (Bot Avoidance)

These constraints **must** be enforced in automation code:

```
TikTok:     Max 3-5 posts/week per account (older); 10+ = instant ban
YouTube:    10,000 units/day (roughly 6 Shorts/day per account)
Instagram:  50 API posts/24hr limit
Rumble:     No rate limits documented, but manual upload (no official API)
```

**Multi-Account Strategy:** 5 accounts × 20 clips/month = 100 clips safely
- Space posts 45-120 min apart
- Vary posting times ±30-60 min daily
- Never same time twice in 7 days
- Use residential proxies ($50-200/month for safety)

---

## Recommended Starting Creator

**BOGGLES** (from CREATOR_ANALYSIS_REPORT.md)
- Platform: Twitch
- Followers: 44,961
- Growth: 45% month-over-month (fastest growing)
- Content: Elden Ring challenge runs (highly emotional, naturally viral)
- Clipper Competition: **ZERO** (whitespace opportunity)
- Expected First Week Performance: 5K-15K views per clip, $30-50/day earnings

**Backup:** HIVISE (180K followers, 42% growth, 60h/week content, same content type)

---

## Week 1 Execution Checklist

Reference `PHASE_1_AUTOMATION_BLUEPRINT.md` for full details. Claude Code involvement:

- [ ] Day 1-2: Infrastructure setup (manual—OpusClip, bounty platforms, ShortSync/Repurpose.io)
- [ ] Day 3-4: Download VODs with `yt-dlp`, submit to OpusClip (manual for now)
- [ ] Day 5-7: Publish 10-15 clips to all platforms; establish monitoring dashboard
- **Claude Code Tasks:**
  - Write `vod_downloader.py` (yt-dlp wrapper)
  - Write `earnings_tracker.py` (Notion API or spreadsheet automation)
  - Create bot safety gate checks in publishing script

---

## Tools & Services (Non-Code)

These are external services, **not managed by Claude Code:**

| Service | Cost | Role |
|---------|------|------|
| OpusClip Pro | $29/month | Clip generation (Phase 1) |
| ShortSync or Repurpose.io | €15-$35/month | Multi-platform publishing |
| Residential Proxies | $50-200/month | Bot detection avoidance |
| Notion/Airtable | Free-$10/month | Earnings tracking dashboard |
| Claude API | $0.05/video | Moment analysis (Phase 2 only) |
| Whisper/PySceneDetect | Free | Transcription & scene detection (Phase 2 only) |

---

## File Organization Notes

- **No source code in this project yet.** Everything is documentation-driven strategy.
- **Automation code is examples within docs.** When you write automation, it will be new Python files (e.g., `orchestrator.py`, `publisher.py`, `monitor.py`).
- **All economics/strategy is in MGMT_docs/.** Don't duplicate or re-document—reference existing files.
- **_ARCHIVE folder:** Legacy docs kept for reference; not active execution.

---

## Decision Points & Next Steps

### Week 4 (Phase 1 Checkpoint)
If earnings < $150/week: Reconsider creator choice or content source  
If earnings $150-$300/week: Continue Phase 1, optionally start Phase 2  
If earnings $300+/week: Strongly consider Phase 2 DIY development

### Phase 2 Go/No-Go (Week 5)
Only proceed if Phase 1 is earning $300+/week. See `PHASE_2_OPUSCLIP_REPLACEMENT.md` for full DIY stack.

---

## Key References

- **Strategy:** `MGMT_docs/YOUR_STRATEGY.md`
- **Phase 1 Details:** `MGMT_docs/PHASE_1_AUTOMATION_BLUEPRINT.md` (includes Python code templates)
- **Phase 2 Details:** `MGMT_docs/PHASE_2_OPUSCLIP_REPLACEMENT.md` (if needed)
- **Safety:** `MGMT_docs/02_BOT_AVOIDANCE_PLAYBOOK.md` (platform limits & posting patterns)
- **Creators:** `MGMT_docs/CREATOR_ANALYSIS_REPORT.md` (vetted list; BOGGLES/HIVISE first)
- **Navigation:** `MGMT_docs/INDEX.md`

---

## Current Status

- [x] Phase 1 strategy finalized (OpusClip + manual publishing)
- [x] Phase 2 DIY architecture blueprinted (Whisper → Claude → FFmpeg)
- [x] Creator analysis complete (BOGGLES/HIVISE recommended)
- [x] Bot avoidance playbook documented
- [ ] Week 1 execution begins (choose creator, subscribe OpusClip)
- [ ] Automation code written as Phase 1 progresses
