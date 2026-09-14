---
name: dubbing-script-timecode-converter
description: >-
  Converts player-based video timecodes in dubbing and voiceover scripts into
  embedded (BITC / Burn-In Timecode) timecodes. Handles 23.976 fps to 24.0 fps
  drift correction, start BITC offset, dot separator formatting (HH.MM.SS / MM.SS),
  frame rounding, and ensures tab (\t) placement immediately after [CHARACTER_NAME]
  square brackets for Microsoft Word tab stop alignment.
---

# Dubbing Script Timecode Converter

## Overview

This skill converts **player-based timecodes** (starting at `00:00:00:00` or `01:59` running at `23.976 fps`) in dubbing/voiceover script files into **burned-in video timecodes (BITC)** running at `24.0 fps` starting from a user-specified embedded offset (e.g., `00:58:29:00`).

It also enforces production-standard script formatting for Microsoft Word alignment:
- Dot separator (`.`) instead of colon (`:`)
- Saniye precision (salise/frames excluded)
- Omission of `00.` hour prefix when hours == 0 (`MM.SS` vs `HH.MM.SS`)
- Exact Tab (`\t`) placement immediately after `[CHARACTER_NAME]` square brackets

---

## Inputs & Prerequisites

1. **Source Script File:** Markdown (`.md`), text (`.txt`), or script format containing timecodes.
2. **Start BITC Offset (`start_bitc`):** The embedded video timecode at player `00:00:00:00` (e.g. `00:58:29:00`).
   > ⚠️ **MANDATORY CHECK:** If the user does NOT specify the start BITC offset in their prompt, you **MUST** prompt the user to provide the start BITC before proceeding!

---

## Conversion Formula & FPS Drift Correction

### 1. Seconds Conversion
Convert player timecode `player_tc` to seconds (`s_player`):
- `MM:SS` or `MM.SS` -> `m * 60 + s`
- `HH:MM:SS` or `HH.MM.SS` -> `h * 3600 + m * 60 + s`
- `HH:MM:SS:FF` -> `h * 3600 + m * 60 + s + (f / 24.0)`

Convert `start_bitc` (e.g. `00:58:29:00`) to seconds (`s_start`):
- `s_start = (h_start * 3600) + (m_start * 60) + s_start + (f_start / 24.0)`
- For `00:58:29:00`, `s_start = 3509.0` seconds.

### 2. 23.976 FPS -> 24.0 FPS Drift Adjustment
$$\text{s\_bitc} = \text{s\_start} + \left( \frac{\text{s\_player}}{1.001} \right)$$

### 3. Time Component Breakdown & Frame Rounding
```python
import math

hours = int(s_bitc // 3600)
remainder = s_bitc % 3600
minutes = int(remainder // 60)
seconds = int(remainder % 60)

fractional = s_bitc - math.floor(s_bitc)
frames = int(round(fractional * 24.0))

# Frame rounding overflow check
if frames >= 24:
  frames = 0
  seconds += 1
  if seconds >= 60:
    seconds = 0
    minutes += 1
    if minutes >= 60:
      minutes = 0
      hours += 1
```

---

## Output Timecode Formatting Rules

1. **No Frames / Salise:** Exclude frames from output.
2. **Dot Separator:** Use dot (`.`) instead of colon (`:`).
3. **Hours Prefix Rule:**
   - **If `hours == 0` (`"00"`):** Format as `MM.SS` (e.g. `58.29`, `59.12`).
   - **If `hours > 0` (`"01"`, `"02"`, etc.):** Format as `HH.MM.SS` (e.g. `01.00.27`, `02.27.43`).

### Output Format Table

| Calculated Time | Hours | Formatted BITC Output |
|:---|:---:|:---|
| 0 hours, 58 min, 29 sec | 0 | `58.29` |
| 0 hours, 59 min, 12 sec | 0 | `59.12` |
| 1 hour, 0 min, 27 sec | 1 | `01.00.27` |
| 1 hour, 4 min, 26 sec | 1 | `01.04.26` |
| 2 hours, 27 min, 43 sec | 2 | `02.27.43` |

---

## Character Tag & Tab Alignment Rule

For Microsoft Word dubbing script alignment (cetvel düzeni):

1. **Exact Tab Placement:** Place exactly **ONE Tab (`\t`)** immediately after the square-bracketed character name `[CHARACTER_NAME]`.
2. **Modifiers Location:** Any parenthetical modifiers like `(GD)` (Görsel Dışı), `(Ü)` (Üstüste), `(FİLTRE)`, etc., belong in the dialogue column **AFTER** the tab (`\t`).

### Examples (Before vs After)

| Original Line | Corrected Output Line |
|:---|:---|
| `01.59` | `01.00.27` |
| `[EVE](GD) Alo?` | `[EVE]\t(GD) Alo?` |
| `[LOU](GD) (FİLTRE) Neredesin?` | `[LOU]\t(GD) (FİLTRE) Neredesin?` |
| `[EVE]Merhaba.` | `[EVE]\tMerhaba.` |
| `/// (05.58) Geçelim mi?` | `/// (01.04.26) Geçelim mi?` |

---

## Python Execution Reference

When executing script conversions on a file, use the following logic pattern:

```python
import math
import re


def player_to_bitc_formatted(
    tc_str: str, start_bitc: str, fps: float = 24.0
) -> str:
  parts = [float(p) for p in re.split(r'[\.\:]', tc_str.strip())]
  if len(parts) == 2:
    h, m, s, f = 0.0, parts[0], parts[1], 0.0
  elif len(parts) == 3:
    h, m, s, f = parts[0], parts[1], parts[2], 0.0
  elif len(parts) == 4:
    h, m, s, f = parts[0], parts[1], parts[2], parts[3]
  else:
    return tc_str

  s_player = (h * 3600.0) + (m * 60.0) + s + (f / fps)

  start_parts = [float(p) for p in start_bitc.split(':')]
  s_start = (
      (start_parts[0] * 3600.0)
      + (start_parts[1] * 60.0)
      + start_parts[2]
      + (start_parts[3] / fps)
  )

  s_bitc = s_start + (s_player / 1.001)

  hours = int(s_bitc // 3600)
  remainder = s_bitc % 3600
  minutes = int(remainder // 60)
  seconds = int(remainder % 60)

  fractional = s_bitc - math.floor(s_bitc)
  frames = int(round(fractional * fps))

  if frames >= int(fps):
    frames = 0
    seconds += 1
    if seconds >= 60:
      seconds = 0
      minutes += 1
      if minutes >= 60:
        minutes = 0
        hours += 1

  if hours == 0:
    return f'{minutes:02d}.{seconds:02d}'
  else:
    return f'{hours:02d}.{minutes:02d}.{seconds:02d}'


def format_script_line(line: str, start_bitc: str) -> str:
  stripped = line.strip()

  # 1. Standalone timecode line (e.g., 01.59, 01.08.51)
  if re.match(
      r'^\s*(\d{1,2}[\.\:]\d{2}(?:[\.\:]\d{2})?(?:[\.\:]\d{2})?)\s*$', stripped
  ):
    tc_val = re.match(
        r'^\s*(\d{1,2}[\.\:]\d{2}(?:[\.\:]\d{2})?(?:[\.\:]\d{2})?)\s*$', stripped
    ).group(1)
    new_tc = player_to_bitc_formatted(tc_val, start_bitc)
    newline = '\n' if not line.endswith('  \n') else '  \n'
    return f'{new_tc}{newline}'

  # 2. Inline timecodes in parentheses (e.g. (05.58))
  def replace_inline(m):
    return f'({player_to_bitc_formatted(m.group(1), start_bitc)})'

  line_tc_replaced = re.sub(
      r'\((\d{1,2}[\.\:]\d{2}(?:[\.\:]\d{2})?(?:[\.\:]\d{2})?)\)',
      replace_inline,
      line,
  )

  # 3. Format character tag lines: [NAME] \t rest
  stripped_tc = line_tc_replaced.strip()
  m_char = re.match(r'^(\[[^\]]+\])(.*)$', stripped_tc)
  if m_char:
    bracket = m_char.group(1).strip()  # e.g., [EVE]
    rest = m_char.group(2).replace('\t', ' ').strip()  # e.g., (GD) Alo?

    newline = '\n' if not line.endswith('  \n') else '  \n'
    return f'{bracket}\t{rest}{newline}'

  return line_tc_replaced
```

---

## Workflow Steps

1. **Check for `start_bitc`:** If not provided in the user prompt, ask the user for it immediately.
2. **Read the source script file.**
3. **Run the timecode conversion & character tab formatting script.**
4. **Save output to a new file** (e.g. `{filename}_timecode_edited.md`).
5. **Verify output:** Confirm all timecodes are formatted with dots, frame rounding is correct, and tabs (`\t`) are placed immediately after `[CHARACTER_NAME]`.
