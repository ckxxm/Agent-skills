#!/usr/bin/env python3
"""
Bilibili Subtitle Extractor
Extracts subtitles from Bilibili videos.
"""

import json
import sys
import re
from typing import Optional, List, Dict


def extract_bvid(url: str) -> Optional[str]:
    """Extract BV ID from Bilibili URL."""
    # Match BV ID patterns (BVxxxxxxxxxx)
    bv_match = re.search(r'(BV[a-zA-Z0-9]{10})', url)
    if bv_match:
        return bv_match.group(1)

    # Match av ID patterns (av number or /video/av/)
    av_match = re.search(r'av(\d+)', url)
    if av_match:
        return f"av{av_match.group(1)}"

    return None


def extract_subtitle_json(text_data: str) -> Optional[Dict]:
    """
    Extract subtitle JSON from the script text.
    Bilibili embeds subtitle metadata in the page HTML.
    """
    # Look for subtitle data in the page
    pattern = r'<script>\s*window\.__INITIAL_STATE__\s*=\s*({.*?});'
    match = re.search(pattern, text_data, re.DOTALL)

    if match:
        try:
            data = json.loads(match.group(1))
            return data
        except json.JSONDecodeError:
            pass

    return None


def format_subtitle_as_text(subtitle_data: List[Dict], include_timestamps: bool = True) -> str:
    """Format subtitle data as readable text."""
    lines = []

    for item in subtitle_data:
        if 'from' in item and 'to' in item:
            start = item['from']
            end = item['to']
            content = item.get('content', '').strip()

            if include_timestamps:
                # Convert seconds to readable timestamp format
                start_time = format_timestamp(start)
                end_time = format_timestamp(end)
                lines.append(f"[{start_time} --> {end_time}] {content}")
            else:
                lines.append(content)
        else:
            # Alternative format - just content and timestamp
            content = item.get('content', '').strip()
            timestamp = item.get('timestamp', 0)
            if include_timestamps:
                lines.append(f"[{format_timestamp(timestamp)}] {content}")
            else:
                lines.append(content)

    return '\n'.join(lines)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS.mmm format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def main():
    """Main entry point for subtitle extraction."""
    import urllib.request
    import urllib.error
    import gzip

    if len(sys.argv) < 2:
        print("Usage: bilibili_subtitle.py <bilibili_url> [--plain|--timestamps] [--lang=<lang_code>]", file=sys.stderr)
        print("  --plain: Output plain text without timestamps (default: with timestamps)", file=sys.stderr)
        print("  --timestamps: Output with timestamps (default)", file=sys.stderr)
        print("  --lang=<code>: Specify subtitle language code (e.g., zh-CN, en-US)", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    include_timestamps = True
    preferred_lang = None

    # Parse arguments
    for arg in sys.argv[2:]:
        if arg == '--plain':
            include_timestamps = False
        elif arg == '--timestamps':
            include_timestamps = True
        elif arg.startswith('--lang='):
            preferred_lang = arg.split('=', 1)[1]

    # Extract video ID
    bvid = extract_bvid(url)
    if not bvid:
        print(json.dumps({"error": "Could not extract BV ID or av ID from URL", "url": url}), file=sys.stderr)
        sys.exit(1)

    # Fetch video page to get subtitle info
    video_url = f"https://www.bilibili.com/video/{bvid}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bilibili.com'
    }

    try:
        req = urllib.request.Request(video_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            raw_data = response.read()
            # Handle gzip compression
            if response.info().get('Content-Encoding') == 'gzip':
                page_content = gzip.decompress(raw_data).decode('utf-8')
            else:
                page_content = raw_data.decode('utf-8')

    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Failed to fetch video page: {e}", "url": video_url}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {e}", "url": video_url}), file=sys.stderr)
        sys.exit(1)

    # Try to extract subtitle data from __INITIAL_STATE__
    initial_data = extract_subtitle_json(page_content)

    if not initial_data:
        # Try alternative pattern
        pattern = r'<script>\s*__playinfo__\s*=\s*({.*?})\s*</script>'
        match = re.search(pattern, page_content, re.DOTALL)
        if match:
            try:
                initial_data = json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

    # Extract subtitle information
    subtitle_info = None

    if initial_data:
        # Navigate through the data structure to find subtitles
        # Bilibili's structure varies, try multiple paths
        paths = [
            initial_data.get('subtitleData', {}),
            initial_data.get('videoData', {}).get('subtitle', {}),
            initial_data.get('data', {}).get('subtitle', {}),
        ]

        for path in paths:
            if path and 'subtitles' in path:
                subtitle_info = path
                break

    # If no subtitles found in initial state, try to find subtitle list in page
    if not subtitle_info:
        # Look for subtitle JSON in a different format
        pattern = r'"subtitles":\s*\[([^\]]+)\]'
        match = re.search(pattern, page_content)
        if match:
            try:
                subtitle_json = f'[{match.group(1)}]'
                subtitles = json.loads(subtitle_json)
                subtitle_info = {'subtitles': subtitles}
            except json.JSONDecodeError:
                pass

    # Check if subtitles exist
    if not subtitle_info or not subtitle_info.get('subtitles'):
        print(json.dumps({
            "error": "No subtitles available for this video",
            "bvid": bvid,
            "url": video_url
        }), file=sys.stderr)
        sys.exit(1)

    subtitles = subtitle_info['subtitles']

    # Select subtitle based on language preference
    selected_subtitle = None
    selected_lang = None

    # Prioritize Chinese subtitles
    lang_priority = ['zh-CN', 'zh', 'zh-Hans', 'zh-Hant']

    if preferred_lang:
        lang_priority.insert(0, preferred_lang)

    for lang_code in lang_priority:
        for sub in subtitles:
            sub_lang = sub.get('lang', sub.get('lan', ''))
            if sub_lang == lang_code or sub_lang.startswith(lang_code):
                selected_subtitle = sub
                selected_lang = lang_code
                break
        if selected_subtitle:
            break

    # If no preferred language found, use first available
    if not selected_subtitle and subtitles:
        selected_subtitle = subtitles[0]
        selected_lang = selected_subtitle.get('lang', selected_subtitle.get('lan', 'unknown'))

    if not selected_subtitle:
        print(json.dumps({
            "error": "No matching subtitle found",
            "bvid": bvid,
            "available": [s.get('lang', s.get('lan', 'unknown')) for s in subtitles]
        }), file=sys.stderr)
        sys.exit(1)

    # Get subtitle URL
    subtitle_url = selected_subtitle.get('subtitle_url', '')
    if not subtitle_url:
        # Try alternative field names
        subtitle_url = selected_subtitle.get('url', '')

    if not subtitle_url:
        print(json.dumps({
            "error": "Subtitle URL not found",
            "subtitle": selected_subtitle
        }), file=sys.stderr)
        sys.exit(1)

    # Construct full URL if relative
    if subtitle_url.startswith('//'):
        subtitle_url = 'https:' + subtitle_url
    elif subtitle_url.startswith('/'):
        subtitle_url = 'https://api.bilibili.com' + subtitle_url

    # Fetch subtitle content
    try:
        req = urllib.request.Request(subtitle_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            raw_data = response.read()
            # Handle gzip compression
            if response.info().get('Content-Encoding') == 'gzip':
                subtitle_content = gzip.decompress(raw_data).decode('utf-8')
            else:
                subtitle_content = raw_data.decode('utf-8')
    except urllib.error.URLError as e:
        print(json.dumps({
            "error": f"Failed to fetch subtitle: {e}",
            "subtitle_url": subtitle_url
        }), file=sys.stderr)
        sys.exit(1)

    # Parse subtitle JSON
    try:
        subtitle_json = json.loads(subtitle_content)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": f"Failed to parse subtitle JSON: {e}",
            "content": subtitle_content[:200]
        }), file=sys.stderr)
        sys.exit(1)

    # Extract subtitle lines from different possible formats
    subtitle_lines = []

    # Format 1: { "body": [...] }
    if 'body' in subtitle_json:
        subtitle_lines = subtitle_json['body']

    # Format 2: Direct array
    elif isinstance(subtitle_json, list):
        subtitle_lines = subtitle_json

    else:
        print(json.dumps({
            "error": "Unknown subtitle format",
            "structure": list(subtitle_json.keys()) if isinstance(subtitle_json, dict) else type(subtitle_json).__name__
        }), file=sys.stderr)
        sys.exit(1)

    # Format and output
    formatted_output = format_subtitle_as_text(subtitle_lines, include_timestamps)

    # Output metadata to stderr for Claude to read
    metadata = {
        "bvid": bvid,
        "url": video_url,
        "language": selected_lang,
        "timestamp_format": "included" if include_timestamps else "excluded",
        "line_count": len(subtitle_lines)
    }
    print(json.dumps(metadata), file=sys.stderr)

    # Output the actual subtitle content
    print(formatted_output)


if __name__ == "__main__":
    main()
