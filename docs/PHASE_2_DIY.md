# Phase 2: Claude Code DIY Clip Generation (Weeks 5-8+, Optional)

**Trigger:** Only build this IF earning $300+/week at end of Phase 1

---

## Architecture Overview

```
Content Source (Twitch/YouTube/Podcast)
  ↓
Whisper (Transcription)
├─ Open-source, free, 98%+ accuracy
├─ Runs locally on GPU or Hugging Face API
├─ Output: Timestamped transcript
└─ Time: 1-3 minutes per 60-min video
  ↓
PySceneDetect (Scene Detection)
├─ Free, open-source
├─ Detects shot boundaries (when scene changes)
├─ 85-92% accuracy (vs OpusClip 93%)
└─ Time: 2-4 minutes per 60-min video
  ↓
Claude API (Moment Analysis)
├─ Analyzes transcript for viral moments
├─ Scores by virality potential
├─ Cost: $0.05/video (Haiku model)
├─ Output: Timestamped moments with scores
└─ Time: 2-3 minutes per video
  ↓
FFmpeg (Rendering)
├─ GPU-accelerated H.264 encoding
├─ Aspect ratio conversion (vertical/square/horizontal)
├─ Free, open-source
├─ Time: 1-3 minutes per clip (GPU-dependent)
└─ Output: Publication-ready MP4 files
  ↓
Multi-Platform Publishing
├─ Same as Phase 1 (ShortSync or Repurpose.io)
└─ Send to all 4 bounty platforms
```

---

## Implementation: Claude Code Stack

### Stage 1: Transcription (Whisper)

```python
# Claude Code: whisper_transcriber.py

from faster_whisper import WhisperModel
import json

class WhisperTranscriber:
    def __init__(self, model_size="large-v3"):
        # Options: tiny, small, medium, large-v3
        # Use "large-v3" for best accuracy (98%+)
        self.model = WhisperModel(
            model_size, 
            device="cuda",  # GPU acceleration
            compute_type="float16"
        )
    
    def transcribe(self, audio_file):
        """Transcribe audio with timestamps"""
        segments, info = self.model.transcribe(audio_file)
        
        transcript = {
            "language": info.language,
            "segments": [
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text
                }
                for segment in segments
            ]
        }
        
        return transcript
    
    def get_duration(self, audio_file):
        """Get total duration"""
        import librosa
        y, sr = librosa.load(audio_file)
        duration = librosa.get_duration(y=y, sr=sr)
        return duration

# Usage
transcriber = WhisperTranscriber()
transcript = transcriber.transcribe("podcast.mp3")

# Save for next stage
with open("transcript.json", "w") as f:
    json.dump(transcript, f)

# Estimated cost: $0 (free, runs locally)
# Processing time: 1-3 min per 60-min audio
```

### Stage 2: Scene Detection (PySceneDetect)

```python
# Claude Code: scene_detector.py

from scenedetect import detect, AdaptiveDetector
import json

class SceneDetector:
    def __init__(self):
        pass
    
    def detect_scenes(self, video_file):
        """Find scene boundaries"""
        scenes = detect(video_file, AdaptiveDetector())
        
        scene_list = []
        for i, scene in enumerate(scenes):
            scene_list.append({
                "scene_num": i,
                "timestamp": scene.get_seconds(),
                "frame": scene.get_frames()
            })
        
        return scene_list
    
    def get_video_duration(self, video_file):
        """Get total video duration"""
        import cv2
        cap = cv2.VideoCapture(video_file)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps
        cap.release()
        return duration

# Usage
detector = SceneDetector()
scenes = detector.detect_scenes("stream.mp4")

# Save for next stage
with open("scenes.json", "w") as f:
    json.dump(scenes, f)

# Estimated cost: $0 (free, open-source)
# Processing time: 2-4 min per 60-min video
```

### Stage 3: Moment Analysis (Claude API)

```python
# Claude Code: moment_analyzer.py

from anthropic import Anthropic
import json

class MomentAnalyzer:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)
    
    def analyze_transcript(self, transcript_json):
        """Use Claude to find viral moments"""
        
        # Build prompt with transcript
        prompt = f"""
        Analyze this transcript and identify the top 15 most viral/clip-worthy moments.
        
        For each moment, provide:
        1. Start timestamp
        2. End timestamp
        3. The quoted text
        4. Why it's viral-worthy (emotional, surprising, quotable, funny?)
        5. Virality score (1-10)
        6. Recommended platforms (TikTok, YouTube, Instagram?)
        
        Return as JSON array.
        
        TRANSCRIPT:
        {json.dumps(transcript_json, indent=2)}
        """
        
        # Call Claude API (Haiku = cheapest)
        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Parse response
        moments = json.loads(response.content[0].text)
        return moments

# Usage
analyzer = MomentAnalyzer(api_key="your_key")

# Load transcript from Stage 1
with open("transcript.json") as f:
    transcript = json.load(f)

# Analyze
moments = analyzer.analyze_transcript(transcript)

# Save for next stage
with open("moments.json", "w") as f:
    json.dump(moments, f)

# Estimated cost: $0.05/video (Haiku model @ 3K input tokens)
# Processing time: 2-3 min per video
```

### Stage 4: Clip Extraction (FFmpeg)

```python
# Claude Code: clip_renderer.py

import subprocess
import json

class ClipRenderer:
    def __init__(self, use_gpu=True):
        self.use_gpu = use_gpu
        self.codec = "h264_nvenc" if use_gpu else "libx264"
        self.preset = "fast" if use_gpu else "veryfast"
    
    def render_clip(self, video_file, start_time, end_time, output_format="vertical"):
        """Extract and render clip using FFmpeg"""
        
        # Define aspect ratio filters
        filters = {
            "vertical": "scale=1080:1920,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "square": "scale=1080:1080",
            "horizontal": "scale=1920:1080"
        }
        
        output_file = f"clip_{start_time:.0f}s_{end_time:.0f}s.mp4"
        
        # Build FFmpeg command
        cmd = f"""
        ffmpeg -i {video_file} \
          -ss {start_time} -to {end_time} \
          -vf "{filters[output_format]}" \
          -c:v {self.codec} -preset {self.preset} \
          -b:v 8M \
          -c:a aac -b:a 128k \
          {output_file}
        """
        
        # Execute
        result = subprocess.run(cmd, shell=True, capture_output=True)
        
        if result.returncode == 0:
            return output_file, "success"
        else:
            return None, result.stderr.decode()
    
    def batch_render(self, video_file, moments_list):
        """Render all clips from moments"""
        clips = []
        
        for moment in moments_list:
            if moment["virality_score"] < 5:
                continue  # Skip low-scoring moments
            
            output_file, status = self.render_clip(
                video_file,
                moment["start"],
                moment["end"],
                output_format="vertical"
            )
            
            if status == "success":
                clips.append({
                    "file": output_file,
                    "moment": moment
                })
        
        return clips

# Usage
renderer = ClipRenderer(use_gpu=True)

# Load moments from Stage 3
with open("moments.json") as f:
    moments = json.load(f)

# Render all clips
clips = renderer.batch_render("stream.mp4", moments)

# Save manifest
with open("clips_manifest.json", "w") as f:
    json.dump(clips, f)

# Estimated cost: $0 (free, local GPU)
# Processing time: 1-3 min per clip (30-60 clips per source)
```

### Stage 5: Complete Orchestration

```python
# Claude Code: clip_pipeline_orchestrator.py

import json
import time
from whisper_transcriber import WhisperTranscriber
from scene_detector import SceneDetector
from moment_analyzer import MomentAnalyzer
from clip_renderer import ClipRenderer
from multi_platform_publisher import MultiPlatformPublisher

class ClipPipelineOrchestrator:
    def __init__(self, api_key):
        self.transcriber = WhisperTranscriber()
        self.detector = SceneDetector()
        self.analyzer = MomentAnalyzer(api_key)
        self.renderer = ClipRenderer(use_gpu=True)
        self.publisher = MultiPlatformPublisher()
    
    def process_vod(self, video_file, creator_name="Unknown"):
        """End-to-end: VOD → Clips → Published"""
        
        print(f"[1/5] Transcribing {video_file}...")
        start_time = time.time()
        transcript = self.transcriber.transcribe(video_file)
        print(f"  ✓ Transcription complete ({time.time() - start_time:.1f}s)")
        
        print(f"[2/5] Detecting scenes...")
        start_time = time.time()
        scenes = self.detector.detect_scenes(video_file)
        print(f"  ✓ Scene detection complete ({time.time() - start_time:.1f}s)")
        
        print(f"[3/5] Analyzing moments...")
        start_time = time.time()
        moments = self.analyzer.analyze_transcript(transcript)
        print(f"  ✓ Moment analysis complete ({time.time() - start_time:.1f}s)")
        
        print(f"[4/5] Rendering clips ({len(moments)} candidates)...")
        start_time = time.time()
        clips = self.renderer.batch_render(video_file, moments)
        print(f"  ✓ Rendered {len(clips)} clips ({time.time() - start_time:.1f}s)")
        
        print(f"[5/5] Publishing to platforms...")
        start_time = time.time()
        results = self.publisher.publish_batch(clips)
        print(f"  ✓ Published to all platforms ({time.time() - start_time:.1f}s)")
        
        return {
            "video": video_file,
            "clips_generated": len(clips),
            "clips_published": sum(1 for r in results if r.get("status") == "success"),
            "moments": moments,
            "results": results
        }

# Daily execution
orchestrator = ClipPipelineOrchestrator(api_key="your_key")

# Monitor Twitch for new VODs
vods = get_recent_vods(creator_name="your_creator")

for vod in vods:
    result = orchestrator.process_vod(vod["url"], creator_name=vod["creator"])
    
    # Log results
    with open(f"run_{int(time.time())}.json", "w") as f:
        json.dump(result, f)
    
    print(f"✓ Completed: {result['clips_published']} clips published")
```

---

## Phase 1 → Phase 2 Transition

### Parallel Operation (Weeks 5-8)

**What's happening:**
- OpusClip continues running Phase 1 (300 clips/month target)
- Claude DIY builds alongside
- Both systems running in parallel
- Quality comparison

```
Timeline:
Week 5:
├─ OpusClip: Publish 50-75 clips (normal operation)
├─ DIY: Build infrastructure (50+ hours)
└─ Status: DIY still in development

Week 6:
├─ OpusClip: Publish 50-75 clips (normal operation)
├─ DIY: Testing on 2-3 VODs
└─ Status: Comparing output quality

Week 7:
├─ OpusClip: Publish 50-75 clips (normal operation)
├─ DIY: Processing 10-15 VODs
└─ Status: Accuracy metrics collected

Week 8:
├─ OpusClip: Publish 50-75 clips (normal operation)
├─ DIY: Full testing complete
└─ Status: Decision on replacement/hybrid
```

### Week 8 Decision

**Evaluate DIY Performance:**

```
Compare:
├─ Accuracy: DIY vs. OpusClip (same VOD)
├─ Speed: DIY vs. OpusClip (processing time)
├─ Cost: DIY ($120/mo) vs. OpusClip ($29 at 300/mo)
├─ Quality: User satisfaction with DIY clips
└─ Scaling: Can DIY handle 600+ clips/month?

Decision Matrix:

If DIY ≥ OpusClip accuracy + cost < OpusClip:
└─ → REPLACE OpusClip, use pure DIY

If DIY accuracy slightly < OpusClip OR high uncertainty:
└─ → HYBRID: OpusClip 300 clips + DIY overflow

If DIY problematic (high failure rate):
└─ → CANCEL DIY, stick OpusClip ($29/month indefinitely)
```

---

## Migration Path: OpusClip → DIY

### Option 1: Cold Switch (Risky)
```
Week 8 Friday: Cancel OpusClip subscription
Week 9 Monday: Start publishing DIY clips only
Risk: If DIY breaks, revenue stops
NOT RECOMMENDED
```

### Option 2: Gradual Replacement (Safe)
```
Week 8:
├─ OpusClip: 300 clips/month (full)
├─ DIY: 100 clips/month (test production)
└─ Total: 400 clips/month

Week 9-10:
├─ OpusClip: 200 clips/month (scale down)
├─ DIY: 200 clips/month (scale up)
└─ Total: 400 clips/month

Week 11-12:
├─ OpusClip: 100 clips/month (safety buffer only)
├─ DIY: 300+ clips/month (primary)
└─ Total: 400+ clips/month

Week 13:
├─ OpusClip: Cancel subscription (no longer needed)
├─ DIY: Full 600+ clips/month operation
└─ Total: 600+ clips/month
```

### Option 3: Permanent Hybrid (Flexible)
```
Forever:
├─ OpusClip: 300 clips/month (reliable, proven)
├─ DIY: 300+ clips/month (experimental)
└─ Total: 600+ clips/month
└─ Cost: $29 + $120 = $149/month

Advantage: Redundancy + unlimited scaling
Disadvantage: Always paying both
```

---

## Costs & Payback

### Development Cost

| Item | Hours | Cost |
|------|-------|------|
| Whisper integration | 4-6 | $0 (free tool) |
| PySceneDetect integration | 2-4 | $0 (free tool) |
| Claude API integration | 8-12 | ~$5-15 (API testing) |
| FFmpeg integration | 6-10 | $0 (free tool) |
| Orchestration + testing | 10-15 | $20-50 (API calls) |
| Multi-platform publishing | 5-10 | $0 (reuse Phase 1) |
| **Total** | **40-60 hours** | **~$25-65** |

### Monthly Operating Cost

| Item | Cost |
|------|------|
| Whisper (GPU) | $0-50 (depends on compute) |
| Claude API | $10-20/month (at 300-600 clips) |
| Infrastructure | $50-100/month |
| **Total** | **$60-170/month** |

### Payback Analysis

```
OpusClip at 600+ clips/month:
├─ Cost: $100-150/month (multiple tiers)
├─ Per-clip: $0.17-0.25

DIY at 600+ clips/month:
├─ Cost: $60-170/month (depends on GPU)
├─ Per-clip: $0.10-0.28
├─ One-time: $5K-6K development labor (if hiring)
├─ If you build it: $0 development (your time)

Payback Period (if earning well):
├─ If OpusClip cost > DIY cost: Payback = immediate
├─ Infrastructure cost payoff: 3-4 months
└─ Development labor payoff: 6-12 months (your time value)

Long-term benefit:
├─ Year 1: Breakeven or slight savings
├─ Year 2+: $500-1,200/year savings vs. OpusClip tiers
└─ Scaling: DIY unlimited; OpusClip tier-limited
```

---

## Success Metrics (Phase 2)

**Week 8 Evaluation:**
- ✅ DIY processes 10+ VODs without critical errors
- ✅ DIY accuracy ≥ 85% (compared to OpusClip)
- ✅ DIY speed ≥ OpusClip (10-13 min vs. 15-20 min per source)
- ✅ Cost per clip ≤ $0.30 (after volume optimization)

**Week 12 (If Proceeding):**
- ✅ 300+ clips generated monthly via DIY
- ✅ Earnings maintained or improved vs. OpusClip
- ✅ System reliability >95% (no crashes/major errors)
- ✅ Scaling tested (can handle 600+ clips/month)

---

## When NOT to Build Phase 2

- ❌ Earning < $200/week (not profitable enough)
- ❌ OpusClip working perfectly (no reason to switch)
- ❌ Can't commit 40-60 hours development
- ❌ Unwilling to maintain infrastructure
- ❌ Prefer simplicity over control

**In these cases:** Stay with OpusClip permanently ($29/month for 300 clips/month)

---

## See Also

- `PHASE_1_AUTOMATION_BLUEPRINT.md` - OpusClip phase details
- `02_CLAUDE_AUTOMATION_CAPABILITIES.md` - What Claude can do natively
- `04_OPUSCLIP_REBUILD_STRATEGY.md` - Original DIY analysis (now superseded)

