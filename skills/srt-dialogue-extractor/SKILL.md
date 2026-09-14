---
name: srt-dialogue-extractor
description: >-
  Converts SRT subtitle files into clean, plain-text Markdown dialogue files (.md)
  by stripping timecodes, SDH audio descriptions, music lyrics, character tags,
  and formatting markup, while merging split sentence continuations across blocks
  and separating multi-speaker turns onto individual lines with single-line spacing.
---

# SRT Dialogue Extractor

## Overview

This skill processes SubRip Subtitle (`.srt`) files and converts them into clean, plain-text Markdown (`.md`) scripts containing **only spoken human dialogue**. It is designed for dubbing translators, voiceover adapters, script editors, and NLP workflows that require clean transcript text without subtitle timing clutter or non-speech noise captions.

---

## Capabilities & Key Rules

1. **Timecode & Subtitle Index Removal:**
   Strips subtitle entry block numbers and timing lines (`00:00:34,880 --> 00:00:39,550`).

2. **SDH & Audio Noise Filtering:**
   Filters out non-speech SDH (Subtitles for Deaf and Hard of Hearing) sound descriptions, background music lyrics, and sound effect cues:
   - ALL-CAPS audio cues (e.g., `PHONE RINGS`, `CAR RADIO PLAYS LOUDLY`, `BABY CRIES`, `SHE LAUGHS`, `KNOCK ON DOOR`, `DOG BARKS`).
   - Bracketed sound cues (e.g., `[PHONE RINGS]`, `(CHICKENS CLUCKING)`).
   - Music notes and background song lyrics blocks (containing `♪` or music note symbols).

3. **Character Tag & Formatting Removal:**
   - Strips character labels in ALL CAPS or preceding colons (e.g., `MATURE JENNY:`, `TRIXIE:`).
   - Strips bracketed character names (e.g., `[CHARACTER_NAME]`, `(CHARACTER_NAME)`).
   - Strips HTML styling tags (`<i>`, `</i>`, `<b>`, `</b>`, `<font>`, etc.).
   - Strips single quotes used as voiceover/narration markers at line boundaries (`'When a child is born...`), while preserving internal apostrophes (`don't`, `it's`, `she's`, `I'm`, `didn't`).
   - Strips all ellipses (`...`, `..`, `…`) commonly used as hesitation markers or pauses, ensuring clean, continuous sentences.

4. **Multi-Speaker Line Separation:**
   When multiple speakers talk inside a single subtitle block (indicated by leading `- ` or `~ `), each speaker's turn is separated onto its own individual line, and the leading dashes or tildes are removed.

5. **Sentence Continuation Merging:**
   Sentences broken across consecutive subtitle blocks (e.g., block N ends without sentence punctuation or with a comma/hyphen, or block N+1 starts with lowercase) are merged into complete, intact dialogue lines.

6. **Output Formatting:**
   Outputs clean dialogue lines separated by a **single newline (`\n`)** with **no blank lines between lines**.

---

## Bundled Helper Script

The skill includes an automated Python script at `scripts/clean_srt.py` that processes single `.srt` files or entire folders of `.srt` files.

### Script Location
`~/.gemini/config/skills/srt-dialogue-extractor/scripts/clean_srt.py`

### Usage Instructions

#### Single File Processing:
```bash
python3 ~/.gemini/config/skills/srt-dialogue-extractor/scripts/clean_srt.py /path/to/subtitle.srt
```
*Outputs: `/path/to/subtitle.md`*

To specify a custom output path:
```bash
python3 ~/.gemini/config/skills/srt-dialogue-extractor/scripts/clean_srt.py /path/to/subtitle.srt -o /path/to/output_script.md
```

#### Batch Directory Processing:
```bash
python3 ~/.gemini/config/skills/srt-dialogue-extractor/scripts/clean_srt.py /path/to/srt_folder/
```
*Processes all `.srt` files in the folder and generates corresponding `.md` files.*

To specify an output directory for batch processing:
```bash
python3 ~/.gemini/config/skills/srt-dialogue-extractor/scripts/clean_srt.py /path/to/srt_folder/ -o /path/to/output_md_folder/
```

---

## Python Parsing Logic Reference

When implementing custom parsing or executing scripts in environment, follow this core logic:

```python
import re

def is_sdh_sound_line(line: str) -> bool:
    clean = re.sub(r'^[~–\-\s\'"♪]+|[~–\-\s\'"♪]+$', '', line).strip()
    if '♪' in line:
        return True
    letters = re.sub(r'[^a-zA-Z\s]', '', clean).strip()
    if letters and letters.isupper() and len(letters.split()) <= 5:
        if letters in ["STOP", "NO", "YES", "OH", "HELP", "WAIT", "LOOK", "WHY", "WHAT"]:
            return False
        return True
    if (clean.startswith('(') and clean.endswith(')')) or (clean.startswith('[') and clean.endswith(']')):
        return True
    return False

def clean_text(t: str) -> str:
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'\[[^\]]+\]', '', t)
    t = re.sub(r'\([^\)]+\)', '', t)
    t = re.sub(r'^[A-Z0-9\s]{2,}:\s*', '', t)
    t = re.sub(r'^\s*[~–\-]\s*', '', t)
    t = re.sub(r'[♪♯♭]', '', t)
    
    if t.startswith("'") and not t.startswith("'\"") and not t.startswith('"\''):
        t = t[1:]
    if t.endswith("'") and not t.endswith('"\'') and not t.endswith("''"):
        t = t[:-1]
    return re.sub(r'\s+', ' ', t).strip()

def process_srt_content(raw_content: str) -> str:
    blocks = re.split(r'\n\s*\n', raw_content.strip())
    parsed_blocks = []
    for b in blocks:
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        if len(lines) >= 3 and lines[0].isdigit() and '-->' in lines[1]:
            parsed_blocks.append((lines[0], lines[1], lines[2:]))
            
    dialogue_items = []
    for block_id, tc, text_lines in parsed_blocks:
        if any('♪' in l for l in text_lines):
            continue
        valid_lines = [l for l in text_lines if not is_sdh_sound_line(l)]
        if not valid_lines:
            continue
            
        block_turns = []
        curr_turn = ""
        for line in valid_lines:
            has_speaker_symbol = line.startswith('~') or line.startswith('- ') or line.startswith('– ')
            cleaned = clean_text(line)
            if not cleaned:
                continue
            if has_speaker_symbol and curr_turn:
                block_turns.append(curr_turn)
                curr_turn = cleaned
            elif not curr_turn:
                curr_turn = cleaned
            else:
                curr_turn += " " + cleaned
        if curr_turn:
            block_turns.append(curr_turn)
            
        for turn in block_turns:
            dialogue_items.append(turn)
            
    merged_lines = []
    curr_text = ""
    for txt in dialogue_items:
        if not curr_text:
            curr_text = txt
            continue
        last_char = curr_text[-1]
        first_char = txt[0]
        is_cont = (last_char not in '.!?"”') or (last_char in ',-–:') or first_char.islower()
        if is_cont:
            curr_text += " " + txt
        else:
            merged_lines.append(curr_text)
            curr_text = txt
    if curr_text:
        merged_lines.append(curr_text)
        
    final_lines = []
    for l in merged_lines:
        if l.strip():
            sl = re.sub(r'\.{2,}|\…', ' ', l)
            final_lines.append(re.sub(r'\s+', ' ', sl).strip())
            
    return "\n".join(final_lines) + "\n"
```

---

## Workflow Checklist

1. Locate input `.srt` file(s).
2. Execute `scripts/clean_srt.py` on the target `.srt` file or directory.
3. Verify output `.md` file(s):
   - Timecodes and numbers removed.
   - SDH sound effects, background music, and character tags removed.
   - Multi-speaker lines separated onto individual lines without dashes.
   - Broken sentences merged properly across subtitle frames.
   - Dialogue lines formatted with single-line breaks (`\n`).
