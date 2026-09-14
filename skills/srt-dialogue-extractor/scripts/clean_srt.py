#!/usr/bin/env python3
"""
SRT Dialogue Extractor Script
Extracts clean, plain-text dialogue from SRT subtitle files.

Removes:
- Timecodes & subtitle numbers
- SDH sound descriptions (ALL-CAPS audio cues, bracketed sound effects)
- Background music lyrics (lines/blocks with ♪)
- HTML tags (<i>, <b>, etc.)
- Character tags / names ([NAME], NAME:)
- Narration single-quote formatting markers

Handles:
- Encoding detection (UTF-8-SIG, UTF-8, Latin-1 fallback)
- Multi-speaker lines within the same subtitle block or single string (splitting into separate lines)
- Inline speaker dashes (e.g. "Oh! - I did well..." -> "Oh!\nI did well...")
- Sentence continuations across consecutive blocks (merging into intact dialogue lines)
- Output in Markdown format with single-line spacing (no blank lines between dialogues)
"""

import sys
import os
import re
import argparse

def is_sdh_sound_line(line: str) -> bool:
    clean = re.sub(r'^[~–\-\s\'"♪]+|[~–\-\s\'"♪]+$', '', line).strip()
    if '♪' in line:
        return True
    letters = re.sub(r'[^a-zA-Z\s]', '', clean).strip()
    if letters and letters.isupper() and len(letters.split()) <= 5:
        if letters in ["STOP", "NO", "YES", "OH", "HELP", "WAIT", "LOOK", "WHY", "WHAT"]:
            return False
        return True
    if clean.startswith('(') and clean.endswith(')'):
        return True
    if clean.startswith('[') and clean.endswith(']'):
        return True
    return False

def is_music_block(text_lines: list) -> bool:
    return any('♪' in l for l in text_lines)

def clean_text(t: str) -> str:
    # Remove HTML tags
    t = re.sub(r'<[^>]+>', '', t)
    # Remove bracketed character names / descriptions: [NAME] or (NAME)
    t = re.sub(r'\[[^\]]+\]', '', t)
    t = re.sub(r'\([^\)]+\)', '', t)
    
    # Remove ALL CAPS character label prefix with colon: e.g. MATURE JENNY:
    t = re.sub(r'^[A-Z0-9\s]{2,}:\s*', '', t)
    
    # Remove leading tilde or dash
    t = re.sub(r'^\s*[~–\-]\s*', '', t)
    # Remove music symbols
    t = re.sub(r'[♪♯♭]', '', t)
    
    # Strip leading narration single quote if not followed by double quote
    if t.startswith("'") and not t.startswith("'\"") and not t.startswith('"\''):
        t = t[1:]
    # Strip trailing narration single quote if not preceded by double quote
    if t.endswith("'") and not t.endswith('"\'') and not t.endswith("''"):
        t = t[:-1]
    
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def split_inline_speaker_turns(text: str) -> list:
    # Split inline speaker turns separated by dashes after punctuation or between turns
    # e.g., "Oh! - I did well...", "Thank you. - Oh, dear.", "Yes, - Thanks."
    processed = re.sub(r'([\.\!\?\,]"?)\s*[\-\–]\s+([A-Z"“\'])', r'\1\n\2', text)
    processed = re.sub(r'(^|\n)\s*[\-\–]\s*', r'\1', processed)
    lines = [l.strip() for l in processed.split('\n') if l.strip()]
    return lines

def process_srt_content(raw_content: str) -> str:
    blocks = re.split(r'\n\s*\n', raw_content.strip())
    
    parsed_blocks = []
    for b in blocks:
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        if len(lines) >= 3 and lines[0].isdigit() and '-->' in lines[1]:
            parsed_blocks.append((lines[0], lines[1], lines[2:]))
            
    dialogue_items = []
    for block_id, tc, text_lines in parsed_blocks:
        if is_music_block(text_lines):
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
                curr_turn = curr_turn + " " + cleaned
                
        if curr_turn:
            block_turns.append(curr_turn)
            
        for turn in block_turns:
            sub_turns = split_inline_speaker_turns(turn)
            for st in sub_turns:
                dialogue_items.append({'block': block_id, 'text': st})
            
    merged_lines = []
    curr_text = ""
    
    for item in dialogue_items:
        txt = item['text']
        if not curr_text:
            curr_text = txt
            continue
            
        last_char = curr_text[-1]
        first_char = txt[0]
        
        ends_with_ellipsis = curr_text.endswith("...") or curr_text.endswith("..") or curr_text.endswith("…")
        starts_with_ellipsis = txt.startswith("...") or txt.startswith("..") or txt.startswith("…")
        
        is_cont = (last_char not in '.!?"”') or (last_char in ',-–:') or first_char.islower() or ends_with_ellipsis or starts_with_ellipsis
        
        if is_cont:
            if ends_with_ellipsis:
                curr_text = re.sub(r'\s*([.]{2,}|\…)$', '', curr_text)
            if starts_with_ellipsis:
                txt = re.sub(r'^([.]{2,}|\…)\s*', '', txt)
                
            if txt:
                curr_text = (curr_text + " " + txt).strip()
        else:
            merged_lines.append(curr_text)
            curr_text = txt
            
    if curr_text:
        merged_lines.append(curr_text)
        
    final_lines = []
    for l in merged_lines:
        sub_splits = split_inline_speaker_turns(l)
        for sl in sub_splits:
            sl = re.sub(r'\.{2,}|\…', ' ', sl)
            sl = re.sub(r'\s+', ' ', sl).strip()
            sl = re.sub(r'\'\s*"', '"', sl)
            sl = re.sub(r'"\s*\'', '"', sl)
            sl = re.sub(r'""+', '"', sl)
            if sl:
                final_lines.append(sl)
            
    return "\n".join(final_lines) + "\n"

def read_file_with_fallback(path: str) -> str:
    with open(path, "rb") as f:
        raw_bytes = f.read()

    # 1. Try UTF-8 encodings
    for enc in ["utf-8-sig", "utf-8"]:
        try:
            text = raw_bytes.decode(enc)
            # Check for misdecoded Turkish characters from Latin-1
            tr_fix = {'Ý': 'İ', 'ý': 'ı', 'Þ': 'Ş', 'þ': 'ş', 'Ð': 'Ğ', 'ð': 'ğ'}
            for k, v in tr_fix.items():
                text = text.replace(k, v)
            return text
        except UnicodeDecodeError:
            pass

    # 2. Try charset_normalizer if available
    try:
        import charset_normalizer
        result = charset_normalizer.from_bytes(raw_bytes).best()
        if result and result.encoding:
            text = str(result)
            tr_fix = {'Ý': 'İ', 'ý': 'ı', 'Þ': 'Ş', 'þ': 'ş', 'Ð': 'Ğ', 'ð': 'ğ'}
            for k, v in tr_fix.items():
                text = text.replace(k, v)
            return text
    except Exception:
        pass

    # 3. Try single-byte encodings (iso-8859-9 and cp1254 before cp1252/latin-1)
    for enc in ["iso-8859-9", "cp1254", "cp1252", "latin-1"]:
        try:
            text = raw_bytes.decode(enc)
            tr_fix = {'Ý': 'İ', 'ý': 'ı', 'Þ': 'Ş', 'þ': 'ş', 'Ð': 'Ğ', 'ð': 'ğ'}
            for k, v in tr_fix.items():
                text = text.replace(k, v)
            return text
        except UnicodeDecodeError:
            continue

    text = raw_bytes.decode("utf-8", errors="replace")
    tr_fix = {'Ý': 'İ', 'ý': 'ı', 'Þ': 'Ş', 'þ': 'ş', 'Ð': 'Ğ', 'ð': 'ğ'}
    for k, v in tr_fix.items():
        text = text.replace(k, v)
    return text

def process_file(input_path: str, output_path: str = None):
    if not output_path:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".md"
        
    raw = read_file_with_fallback(input_path)
    clean_md = process_srt_content(raw)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(clean_md)
        
    print(f"Processed: {input_path} -> {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert SRT subtitles into clean plain-text Markdown dialogue files.")
    parser.add_argument("input", help="Path to input .srt file or directory containing .srt files.")
    parser.add_argument("-o", "--output", help="Optional output .md path (for single file) or output directory (for folder).")
    
    args = parser.parse_args()
    
    input_path = os.path.abspath(args.input)
    
    if os.path.isfile(input_path):
        if not input_path.lower().endswith(".srt"):
            print("Error: Input file must be an .srt file.")
            sys.exit(1)
        process_file(input_path, args.output)
    elif os.path.isdir(input_path):
        out_dir = args.output if args.output else input_path
        os.makedirs(out_dir, exist_ok=True)
        
        srt_files = [f for f in sorted(os.listdir(input_path)) if f.lower().endswith(".srt")]
        if not srt_files:
            print(f"No .srt files found in {input_path}")
            sys.exit(0)
            
        print(f"Found {len(srt_files)} .srt files in {input_path}")
        for sfile in srt_files:
            in_file = os.path.join(input_path, sfile)
            base_name, _ = os.path.splitext(sfile)
            out_file = os.path.join(out_dir, base_name + ".md")
            process_file(in_file, out_file)
    else:
        print(f"Error: Path {input_path} does not exist.")
        sys.exit(1)

if __name__ == "__main__":
    main()
