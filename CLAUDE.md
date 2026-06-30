# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**Clipping Venture:** Build themed social media channels (mindset/self-improvement for young men 18-30) that combine **curated content for audience building** with **paid campaign clips for monetization**—a flywheel where followers boost campaign performance.

**Core Strategy (Hybrid Model):**
- **Curated Content** (50-60% of volume): Free clips from creators, audience-building focused
- **Campaign Content** (40-50% of volume): Paid bounty platform clips, monetization-focused
- **Payoff:** Engaged followers from curated content → higher view counts on campaign clips → better bounty earnings → reinvest in more content

**Phase 1 (Weeks 1-4):** OpusClip-based validation with manual publishing + theme channel setup ($29/month OpusClip subscription)

**Phase 2 (Weeks 5-8+, optional):** DIY Claude Code-based clip generation system (if Phase 1 earnings exceed $300+/week)

**Target Markets:** Themed YouTube/TikTok/Instagram channels (audience-first) + bounty platforms (Content Rewards, Whop, Vyro, Clipify) paying $2-10 per 1K views on campaign content

**Sub-Niches:** Entrepreneurship, fitness/discipline, podcast wisdom, gaming competition, finance mindset, confidence/social skills

---

## Documentation

All docs live in `docs/`. No subfolders, no indexes — just the docs themselves.

```
docs/
├─ STRATEGY.md              # Master plan — start here
├─ IMPLEMENTATION.md         # Week-by-week execution roadmap
├─ PHASE_1_AUTOMATION.md     # OpusClip automation scripts (Python)
├─ PHASE_2_DIY.md            # Optional DIY system (Whisper + Claude + FFmpeg)
├─ BOT_AVOIDANCE.md          # Platform rate limits & ban prevention
├─ ACCOUNT_SETUP.md          # Google Workspace & multi-account structure
├─ BOUNTY_PLATFORMS.md       # Content Rewards, Whop, Vyro, Clipify guide
├─ CREATORS.md               # Vetted campaign creators (BOGGLES, HIVISE, etc.)
├─ CURATED_SOURCES.md        # Channels to monitor for curated content
├─ SOCIAL_MEDIA.md           # Handles, bios, visual identity, content pillars
└─ MONITORING.md             # Content monitoring automation (Hermes, Claude Code /schedule)
```

---

## How Claude Code Fits In

Claude Code is used for **automation scripting and orchestration** during both phases:

### Phase 1: OpusClip + Hybrid Content Strategy
The `PHASE_1_AUTOMATION_BLUEPRINT.md` includes 5 production-ready Python scripts (copy-paste ready):

1. **Content Curator** - Select and organize curated clips from multiple creators (audience-building content)
2. **OpusClip Orchestrator** - Download VODs, submit to OpusClip, retrieve generated campaign clips
3. **Hybrid Publisher** - Publish curated and campaign clips to themed channels (YouTube/TikTok/Instagram) + bounty platforms
4. **Earnings Aggregator** - Track views and earnings across platforms; separate curated (audience metric) from campaign (revenue metric)
5. **Bot Avoidance Safety Gates** - Enforce posting limits and humanized delays per platform, account for higher volume (curated + campaign)

**Claude Code's Role:** Write these orchestration scripts, manage theme-based curation logic, adapt per niche, monitor execution and audience growth

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

### Phase 1: OpusClip + Hybrid Content (Weeks 1-4)
- **Cost:** $29/month OpusClip + $15-35/month distribution tools
- **Time:** 2-3 hours/day for 4 weeks
- **Target Volume:** 100-140 clips published (50-70 curated + 50-70 campaign)
- **Target Revenue:** $200-1,000 (bounty payouts from campaign content only)
- **Target Audience:** 500-2,000 followers on themed channel (from curated content)
- **Success Metrics:** 
  - $150+/week earnings from campaign bounties by Week 4
  - 1,000+ followers on channel by Week 4
  - Campaign clips averaging 30-50% better views than Week 1 (audience flywheel effect)

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

**BOGGLES** (from `docs/CREATORS.md`)
- Platform: Twitch
- Followers: 44,961
- Growth: 45% month-over-month (fastest growing)
- Content: Elden Ring challenge runs (highly emotional, naturally viral)
- Clipper Competition: **ZERO** (whitespace opportunity)
- Expected First Week Performance: 5K-15K views per clip, $30-50/day earnings

**Backup:** HIVISE (180K followers, 42% growth, 60h/week content, same content type)

---

## Week 1 Execution Checklist

Reference `docs/PHASE_1_AUTOMATION.md` for full details. Claude Code involvement:

- [ ] Day 1-2: Infrastructure setup (manual—OpusClip, bounty platforms, ShortSync/Repurpose.io, theme channel creation)
- [ ] Day 2-3: Curate 10-15 free clips from creators matching mindset/self-improvement theme
- [ ] Day 3-4: Download VODs with `yt-dlp`, submit to OpusClip (manual for now)
- [ ] Day 5-7: Publish 20-30 clips total (10-15 curated + 10-15 campaign) to themed channel + bounty platforms
- **Claude Code Tasks:**
  - Write `vod_downloader.py` (yt-dlp wrapper)
  - Write `content_curator.py` (identify and organize theme-relevant clips from multiple sources)
  - Write `hybrid_publisher.py` (route curated vs campaign clips to appropriate platforms)
  - Write `engagement_tracker.py` (track followers, views by content type, earnings by content type)
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

## File Organization

- **`prescreener/`** — Self-contained Flask app (Whisper + Claude moment analysis). Run with `python -m prescreener` from project root. Has its own `requirements.txt`, `.env`, and `__main__.py`. Nothing leaks into the project root.
- **All strategy/planning lives in `docs/`.** Don't duplicate — reference existing files.
- **`Content/`** holds actual clip files organized by creator.
- **Future automation scripts** go in their own directories, not the project root.

---

## Decision Points & Next Steps

### Week 4 (Phase 1 Checkpoint)
If earnings < $150/week: Reconsider creator choice or content source  
If earnings $150-$300/week: Continue Phase 1, optionally start Phase 2  
If earnings $300+/week: Strongly consider Phase 2 DIY development

### Phase 2 Go/No-Go (Week 5)
Only proceed if Phase 1 is earning $300+/week. See `docs/PHASE_2_DIY.md` for full DIY stack.

---

## Key References

- **Strategy:** `docs/STRATEGY.md`
- **Phase 1:** `docs/PHASE_1_AUTOMATION.md` (includes Python code templates)
- **Phase 2:** `docs/PHASE_2_DIY.md` (if needed)
- **Safety:** `docs/BOT_AVOIDANCE.md` (platform limits & posting patterns)
- **Campaign Creators:** `docs/CREATORS.md` (BOGGLES/HIVISE first)
- **Curated Sources:** `docs/CURATED_SOURCES.md` (Jocko, Huberman, Lex, GaryVee, etc.)
- **Branding:** `docs/SOCIAL_MEDIA.md` (handles, bios, visual identity)
- **Monitoring:** `docs/MONITORING.md` (Hermes agent, Claude Code /schedule)

---

## Account Infrastructure

- **Google Workspace** on custom domain for email accounts (replaces multi-Gmail approach)
- **YouTube Shorts deferred to Month 2** — Workspace trial accounts can't access YouTube until $30+ payment processed or 30 days elapsed. Not worth the extra cost in Month 1; focus distribution on TikTok, Instagram, and bounty platforms instead.

---

## Current Status

- [x] Phase 1 strategy finalized (OpusClip + manual publishing)
- [x] Phase 2 DIY architecture blueprinted (Whisper → Claude → FFmpeg)
- [x] Creator analysis complete (BOGGLES/HIVISE recommended)
- [x] Bot avoidance playbook documented
- [x] Google Workspace account created for multi-account email management
- [x] **Hybrid content strategy pivoted** (curated + campaign flywheel model)
- [x] Theme identified: Mindset/self-improvement for young men (18-30)
- [ ] Week 1 execution begins (choose creator, curate initial content, subscribe OpusClip)
- [ ] Automation code written as Phase 1 progresses
