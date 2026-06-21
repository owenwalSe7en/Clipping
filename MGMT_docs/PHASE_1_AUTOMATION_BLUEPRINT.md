# Phase 1 Automation Blueprint: OpusClip Era (Weeks 1-4)

## Overview

**Goal:** Automate clip discovery, generation, and distribution using OpusClip while avoiding platform bans.

**Timeline:** Weeks 1-4 (validation phase)

**Tools:**
- OpusClip Pro ($29/month) - clip generation
- ShortSync or Repurpose.io - multi-platform publishing
- Claude Code - orchestration & monitoring
- Custom dashboard - earnings tracking

---

## Architecture: OpusClip Phase 1

```
Content Source
  ↓
├─ Twitch VOD download (yt-dlp)
├─ YouTube/Podcast URL
└─ Local video file
  ↓
OpusClip Pro
  ├─ Auto-generate 20-50 clips
  ├─ Rate: 300 minutes/month allocation
  └─ Output: MP4 files with metadata
  ↓
Claude Code QA Gate
  ├─ Filter bottom 13% quality
  ├─ Check clip duration (15-60s)
  ├─ Verify aspect ratio
  └─ Flag for manual review if uncertain
  ↓
Multi-Platform Publisher
  ├─ ShortSync (simultaneous posting)
  ├─ Manual Rumble upload (5 min)
  └─ Track posting success rate
  ↓
Monitoring Dashboard
  ├─ Real-time view counts
  ├─ Earnings per platform
  ├─ Account health status
  └─ Copyright claim alerts
  ↓
Bounty Platforms
  ├─ Content Rewards
  ├─ Whop
  ├─ Vyro
  └─ Clipify
  ↓
Earnings & Analytics
  ├─ Daily earnings tracking
  ├─ Platform performance
  └─ Content type analysis
```

---

## Week 1: Validation Setup

### Day 1-2: Infrastructure

**OpusClip Setup (30 min)**
```bash
1. Visit OpusClip.io
2. Sign up → Subscribe Pro ($29/month)
3. Connect Twitch/YouTube account
4. Set preferences (clip length, aspect ratio, quality)
5. Generate first batch on test video
```

**Bounty Platform Accounts (30 min)**
```bash
1. Content Rewards → Sign up, verify email, add payment method
2. Whop → Sign up, create profile, enable creator
3. Vyro → Sign up, set profile, link account
4. Clipify → Sign up, complete KYC, add payment
```

**Publishing Tool Setup (30 min)**
```bash
Option A: ShortSync
- Sign up (€15/month)
- Connect TikTok, Instagram, YouTube, Facebook
- Test publish single clip

Option B: Repurpose.io
- Sign up ($35/month)
- Connect platforms
- Test posting workflow
```

### Day 3-4: First Batch

**Download Content (30 min)**
```bash
# Twitch VOD
yt-dlp https://twitch.tv/[creator]/videos -o "%(title)s.mp4"

# YouTube
yt-dlp "https://youtube.com/watch?v=..." -o "%(title)s.mp4"

# Podcast (get audio feed URL)
yt-dlp "podcast_rss_url" -o "%(title)s.mp3"
```

**Generate with OpusClip (15 min)**
1. Upload VOD to OpusClip
2. Select "Generate Clips" → Auto mode
3. Wait for processing (typically 15-20 min)
4. Review generated clips (20-50 output)
5. Select best 10-15 clips

**QA Gate (30 min)**
```
For each clip:
├─ Duration: 15-60 seconds? → Keep / Discard
├─ Aspect ratio: Correct (9:16 / 1:1 / 16:9)? → Keep / Re-encode
├─ Audio quality: Clear? → Keep / Flag for manual check
├─ Content appropriate? → Keep / Remove
└─ Unique from previous clips? → Keep / Duplicate discard
```

### Day 5-7: Publishing & Tracking

**Publish to All Platforms (1 hour)**
```
For each of 10-15 clips:
├─ ShortSync: Paste clip URL → Auto-publish to TikTok, Insta, YT, FB
├─ Rumble: Manual upload (5 min per clip) OR bulk if API available
└─ Bounty: Submit to Content Rewards, Whop, Vyro, Clipify (copy-paste)
```

**Setup Monitoring (1 hour)**
```
Create Notion dashboard:
├─ Clip ID | Platform | Publish Date | URL
├─ Views (Day 1) | Views (Day 7) | Total Earnings
├─ CPM Rate | Status (Active/Removed)
└─ Notes (content type, performance reason)
```

**Week 1 Result:**
- 10-15 clips published across 4 platforms
- $50-200 estimated bounty earnings
- Baseline established for platform performance

---

## Week 2-4: Scale & Optimize

### Week 2: Process More VODs

**Tuesday (Day 9):**
- Download 2 new VODs (or wait for new streams)
- Run OpusClip
- Select best 10-15 clips
- QA gate (30 min)

**Wednesday (Day 10):**
- Publish to all platforms
- Update Notion dashboard
- Track Day 1 views

**Friday (Day 12):**
- Download another VOD
- Repeat OpusClip + publish cycle
- Total week 2: 30-40 new clips

**Weekend (Days 13-14):**
- Analyze performance so far
- Which content types working?
- Which platforms converting best?

### Week 3: Analyze & Optimize

**Monday (Day 15):**
- Review all clips from weeks 1-2
- Segment by: content type, creator moment, clip length
- Which segment has highest views?
- Which platform gets most viral clips?

**Tuesday-Friday (Days 16-19):**
- Continue publishing 10-15 clips/day
- Test content variations based on analysis
- Track which variations perform better

**Metrics to Track:**
```
├─ Avg views by content type (emotional/funny/shocking/educational)
├─ Avg views by platform (TikTok vs. YouTube vs. Instagram)
├─ Avg views by clip length (15-30s vs. 30-45s vs. 45-60s)
├─ Avg views by upload time (morning vs. afternoon vs. evening)
└─ CPM rates per platform (earnings per 1K views)
```

### Week 4: Decision Point

**Monday (Day 22):**
- Calculate total earnings from weeks 1-4
- Total clips: 50-70
- Total earnings: $200-1,000
- Success rate (clips at 10K+ views): ?%

**Tuesday (Day 23):**
- Earnings review meeting (with yourself)
- **Question 1:** Am I earning $150+/week? (target = $600 for 4 weeks)
- **Question 2:** Is OpusClip keeping up, or is QA becoming bottleneck?
- **Question 3:** Do I want to build DIY, or scale OpusClip further?

**Decision Options:**
```
Option A: Continue OpusClip
├─ Keep at 3-5 clips/day (20-25/week)
├─ Stay under 300-minute monthly allocation
├─ Cost: $29/month indefinitely
└─ Time: 15-20 hours/week (sustainable)

Option B: Start DIY Development (Weeks 5-8)
├─ Keep OpusClip at 300 clips/month
├─ Build Claude Code alternative in parallel
├─ Test DIY quality vs. OpusClip
├─ Decision at week 8: Replace or hybrid?

Option C: Optimize for 600+ Clips/Month
├─ Upgrade OpusClip to multiple tiers
├─ OR start hybrid immediately
├─ Scale to 5-6 clips/day across 2 content sources
└─ Time: 25-35 hours/week
```

---

## Automation Details: What Can Claude Code Handle

### 1. OpusClip Orchestration

```python
# Claude Code Script: opusclip_orchestrator.py

import subprocess
import requests
from datetime import datetime

class OpusClipOrchestrator:
    def __init__(self, opusclip_api_key):
        self.api_key = opusclip_api_key
    
    def download_content(self, source_url):
        """Download Twitch/YouTube VOD"""
        # Use yt-dlp
        cmd = f"yt-dlp {source_url} -o '%(title)s.mp4'"
        subprocess.run(cmd, shell=True)
        return "downloaded_file.mp4"
    
    def submit_to_opusclip(self, video_file):
        """Upload to OpusClip for processing"""
        # OpusClip API call
        response = requests.post(
            "https://api.opusclip.io/v1/generate",
            headers={"Authorization": f"Bearer {self.api_key}"},
            files={"video": open(video_file, "rb")}
        )
        job_id = response.json()["job_id"]
        return job_id
    
    def wait_for_clips(self, job_id):
        """Poll OpusClip until clips generated"""
        # Check status every 30 sec
        # Return when complete
        pass
    
    def qa_filter_clips(self, clips):
        """Filter bottom 13% quality"""
        scores = []
        for clip in clips:
            score = self.score_clip(clip)
            if score >= 6.5:  # Keep top 87%
                scores.append((clip, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def score_clip(self, clip):
        """Simple scoring: duration + audio quality"""
        duration_score = 1.0 if 15 <= clip.duration <= 60 else 0.5
        audio_score = 1.0 if clip.audio_db > -20 else 0.7
        return (duration_score + audio_score) / 2 * 10

# Usage
orchestrator = OpusClipOrchestrator(api_key="your_key")
vod_url = "https://twitch.tv/streamer/videos"
video = orchestrator.download_content(vod_url)
job_id = orchestrator.submit_to_opusclip(video)
clips = orchestrator.wait_for_clips(job_id)
final_clips = orchestrator.qa_filter_clips(clips)
```

### 2. Multi-Platform Publisher

```python
# Claude Code Script: multi_platform_publisher.py

class MultiPlatformPublisher:
    def __init__(self):
        self.shortync_api = ShortSyncAPI(token="...")
        self.rumble_api = RumbleAPI(token="...")
        self.content_rewards = ContentRewardsAPI(token="...")
    
    def publish_clip(self, clip_file, clip_metadata):
        """Publish single clip to all platforms"""
        
        results = {}
        
        # Platform 1: ShortSync (simultaneous multi-posting)
        try:
            response = self.shortync_api.publish({
                "video": clip_file,
                "platforms": ["tiktok", "instagram", "youtube_shorts", "facebook"],
                "caption": clip_metadata["caption"],
                "hashtags": clip_metadata["hashtags"]
            })
            results["shortync"] = {"status": "success", "urls": response.urls}
        except Exception as e:
            results["shortync"] = {"status": "failed", "error": str(e)}
        
        # Platform 2: Rumble (manual for now)
        try:
            response = self.rumble_api.upload(clip_file, clip_metadata)
            results["rumble"] = {"status": "success", "url": response.url}
        except Exception as e:
            results["rumble"] = {"status": "failed", "error": str(e)}
        
        # Platform 3: Bounty platforms
        bounty_platforms = ["content_rewards", "whop", "vyro", "clipify"]
        for platform in bounty_platforms:
            try:
                api = self.get_bounty_api(platform)
                response = api.submit_clip(clip_file, clip_metadata)
                results[platform] = {"status": "success", "clip_id": response.clip_id}
            except Exception as e:
                results[platform] = {"status": "failed", "error": str(e)}
        
        return results
    
    def publish_batch(self, clips_list):
        """Publish multiple clips in sequence"""
        all_results = []
        for i, clip in enumerate(clips_list):
            print(f"Publishing clip {i+1}/{len(clips_list)}")
            results = self.publish_clip(clip["file"], clip["metadata"])
            all_results.append(results)
            
            # Humanized delay (avoid bot detection)
            import random
            wait_time = random.randint(45, 120)  # 45-120 min between posts
            time.sleep(wait_time)
        
        return all_results
```

### 3. Earnings Aggregator

```python
# Claude Code Script: earnings_aggregator.py

class EarningsAggregator:
    def __init__(self):
        self.notion = NotionAPI(token="...")
        self.platforms = {
            "content_rewards": ContentRewardsAPI(),
            "whop": WhopAPI(),
            "vyro": VyroAPI(),
            "clipify": ClipifyAPI()
        }
    
    def fetch_daily_earnings(self):
        """Collect earnings from all platforms"""
        earnings = {}
        
        for platform_name, api in self.platforms.items():
            try:
                today_earnings = api.get_earnings(days=1)
                earnings[platform_name] = today_earnings
            except Exception as e:
                earnings[platform_name] = {"error": str(e)}
        
        total = sum(
            e.get("amount", 0) for e in earnings.values() 
            if "error" not in e
        )
        
        return {"breakdown": earnings, "total": total}
    
    def update_notion_dashboard(self, earnings):
        """Update Notion tracking database"""
        # Add row to Notion with today's earnings
        self.notion.add_row({
            "date": datetime.now(),
            "content_rewards": earnings["breakdown"].get("content_rewards", 0),
            "whop": earnings["breakdown"].get("whop", 0),
            "vyro": earnings["breakdown"].get("vyro", 0),
            "clipify": earnings["breakdown"].get("clipify", 0),
            "total": earnings["total"]
        })
```

### 4. Bot Avoidance Safety Gates

```python
# Claude Code Script: bot_avoidance_safety.py

class BotAvoidanceSafety:
    def __init__(self):
        self.posting_history = []  # Track all posts
        self.account_limits = {
            "tiktok": {"per_week": 5, "per_day": 3},
            "youtube": {"per_day": 6},
            "instagram": {"per_week": 10},
            "rumble": {"per_week": 20}
        }
    
    def check_safe_to_post(self, platform, account_id):
        """Check if posting would trigger bot detection"""
        
        # Get recent posts on this platform + account
        recent_posts = [
            p for p in self.posting_history 
            if p["platform"] == platform and p["account"] == account_id
        ]
        
        # Check daily limit
        today_posts = [
            p for p in recent_posts 
            if p["timestamp"].date() == datetime.now().date()
        ]
        daily_limit = self.account_limits[platform].get("per_day", 999)
        if len(today_posts) >= daily_limit:
            return False, f"Daily limit ({daily_limit}) reached"
        
        # Check weekly limit
        week_posts = [
            p for p in recent_posts 
            if (datetime.now() - p["timestamp"]).days <= 7
        ]
        weekly_limit = self.account_limits[platform].get("per_week", 999)
        if len(week_posts) >= weekly_limit:
            return False, f"Weekly limit ({weekly_limit}) reached"
        
        # Check time since last post (humanized spacing)
        if recent_posts:
            last_post_time = recent_posts[-1]["timestamp"]
            time_since_last = datetime.now() - last_post_time
            min_spacing = timedelta(minutes=45)
            if time_since_last < min_spacing:
                return False, f"Too soon (need {min_spacing})"
        
        return True, "Safe to post"
    
    def humanized_posting_schedule(self, clips_to_publish):
        """Generate realistic posting times"""
        schedule = []
        for i, clip in enumerate(clips_to_publish):
            # Randomize posting time
            base_hour = random.choice([9, 12, 15, 18, 20])
            offset = random.randint(-30, 30)
            post_hour = base_hour + (offset / 60)
            
            # Avoid bot patterns (never exact same time twice)
            while any(s["hour"] == post_hour for s in schedule):
                offset = random.randint(-30, 30)
                post_hour = base_hour + (offset / 60)
            
            # Add browsing delay
            browsing_time = random.randint(5, 10)  # 5-10 min
            
            schedule.append({
                "clip": clip,
                "hour": post_hour,
                "browsing_before": browsing_time
            })
        
        return schedule
```

---

## Week 1-4 Daily Checklist

### Daily (5 min)
- [ ] Check for overnight earnings (dashboard)
- [ ] Monitor for new streams/content from creators

### 2-3x per Week (2-3 hours)
- [ ] Download new VOD/content
- [ ] Run through OpusClip
- [ ] QA + select best clips
- [ ] Publish via ShortSync
- [ ] Manual Rumble upload

### Weekly (30 min)
- [ ] Analyze performance metrics
- [ ] Identify top content types
- [ ] Review platform conversion rates

### Week 4 Only (2 hours)
- [ ] Calculate total earnings
- [ ] Decision on OpusClip vs. DIY
- [ ] Plan weeks 5-12 accordingly

---

## Success Metrics

**Week 1 Target:**
- ✅ 10-15 clips published
- ✅ At least 1 clip reaches 5K+ views
- ✅ $50-200 earned from bounties

**Week 2-4 Target:**
- ✅ 50-70 total clips published
- ✅ 3-5% virality rate (3-5 clips at 50K+)
- ✅ $200-1,000 earned
- ✅ Clear winner platform identified
- ✅ Top content type identified

**Decision Point (Week 4):**
- If earning $150+/week → Continue/scale
- If earning <$150/week → Reconsider creator/content source

---

## Transition to Phase 2 (Optional)

If at Week 4 you're earning $300+/week and want to build DIY:

```
Week 5-8: Build Claude DIY in parallel
├─ OpusClip continues handling 300 clips/month
├─ Claude Code builds Whisper + PySceneDetect + Claude API integration
├─ Process test VODs with DIY system
└─ Compare quality vs. OpusClip

Week 9+: Migration decision
├─ If DIY ≥ OpusClip quality → Replace OpusClip
├─ If DIY < OpusClip quality → Stay hybrid
└─ If DIY problematic → Cancel, stick OpusClip
```

See `PHASE_2_OPUSCLIP_REPLACEMENT.md` for detailed DIY architecture.

