---
name: bilibili-subtitle
description: Extract subtitle content from Bilibili videos. Use when Claude needs to retrieve subtitles for Bilibili URLs. Handles videos with or without subtitles, supports multiple output formats (plain text or with timestamps), and prioritizes Chinese subtitles by default. Triggers on requests like "get subtitle from this bilibili video", "extract subtitles from bilibili", "download bilibili CC", or any Bilibili video URL with subtitle requests.
---

# Bilibili Subtitle

## Overview

This skill extracts subtitle content from Bilibili videos. It handles the complete workflow of fetching video metadata, locating available subtitles, and returning formatted subtitle text.

**Important**: Not all Bilibili videos have subtitles. This skill gracefully handles cases where subtitles are unavailable.

## Quick Start

### Basic Usage (With Timestamps)

```bash
python3 scripts/bilibili_subtitle.py "https://www.bilibili.com/video/BV1xx411c7mD/"
```

### Plain Text Output (No Timestamps)

```bash
python3 scripts/bilibili_subtitle.py "https://www.bilibili.com/video/BV1xx411c7mD/" --plain
```

### Specify Language

```bash
python3 scripts/bilibili_subtitle.py "https://www.bilibili.com/video/BV1xx411c7mD/" --lang=en-US
```

## Workflow

### Step 1: Extract Video ID

Parse the Bilibili URL to extract the BV ID or av ID.

**Supported URL formats:**
- `https://www.bilibili.com/video/BV{xxxxxxxxxx}/`
- `https://www.bilibili.com/video/av{number}/`
- `b23.tv/shortlinks` (after redirect)

### Step 2: Fetch Video Page

Request the video page to extract subtitle metadata. The script:
- Uses proper User-Agent headers
- Parses `__INITIAL_STATE__` embedded JSON data
- Extracts subtitle list and metadata

### Step 3: Select Subtitle Language

The script prioritizes languages in this order:

1. User-specified language (via `--lang` flag)
2. Chinese variants (`zh-CN`, `zh`, `zh-Hans`, `zh-Hant`)
3. First available subtitle (fallback)

### Step 4: Fetch and Parse Subtitle Content

Download the subtitle JSON file and format it according to user preferences.

**Timestamp format:** `[HH:MM:SS.mmm --> HH:MM:SS.mmm] Content`

**Plain text format:** `Content` (one line per subtitle)

## Output Format

### Standard Output

The actual subtitle content is written to stdout.

### Metadata (stderr)

Script metadata is written to stderr as JSON for Claude to parse:

```json
{
  "bvid": "BV1xx411c7mD",
  "url": "https://www.bilibili.com/video/BV1xx411c7mD/",
  "language": "zh-CN",
  "timestamp_format": "included",
  "line_count": 123
}
```

## Error Handling

The script handles various error cases:

| Error | stderr Output | Exit Code |
|-------|---------------|-----------|
| Invalid URL | `{"error": "Could not extract BV ID...", "url": "..."}` | 1 |
| Network error | `{"error": "Failed to fetch video page: ...", "url": "..."}` | 1 |
| No subtitles | `{"error": "No subtitles available for this video", "bvid": "...", "url": "..."}` | 1 |
| Parse error | `{"error": "Failed to parse subtitle JSON: ...", "content": "..."}` | 1 |

## Usage Guidelines

### When to Use This Skill

Use the bilibili-subtitle skill when:
- User provides a Bilibili video URL and mentions subtitles, CC, or caption extraction
- User asks to "get the transcript" or "download subtitles" from a Bilibili video
- User wants to translate or summarize a Bilibili video's spoken content
- Any request involving Bilibili video subtitle content

### Language Handling

**Default behavior:** Prioritize Chinese subtitles (`zh-CN`, `zh`, `zh-Hans`, `zh-Hant`), fallback to any available subtitle.

**Override:** Use `--lang=<code>` to specify a different language (e.g., `en-US`, `ja-JP`).

### Output Format Selection

- **Default:** Include timestamps - provides context for when each line was spoken
- **`--plain`:** Plain text only - better for reading, summarization, or translation

## Resources

### scripts/bilibili_subtitle.py

The main subtitle extraction script. Handles:
- URL parsing (BV ID, av ID extraction)
- HTML scraping and JSON extraction
- Subtitle downloading and parsing
- Multiple output formatting options

**Key dependencies:** Standard library only (`json`, `re`, `urllib`)

**Usage pattern:** Execute via Bash tool, capture stdout for subtitle content, parse stderr for metadata.
