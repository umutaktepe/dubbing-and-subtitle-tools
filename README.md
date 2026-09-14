# Dubbing & Subtitle Tools (Antigravity Plugin)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Antigravity](https://img.shields.io/badge/Platform-Antigravity-orange.svg)](https://github.com/google/antigravity)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](requirements.txt)

A comprehensive plugin for **Google Antigravity** designed for film and television dubbing (seslendirme), lip-sync translation, SRT subtitle processing, timecode conversion, and automated dialogue quality auditing.

---

## 🌟 Features & Included Skills

This plugin bundles **6 specialized skills** equipped with prompt methodologies and production-ready Python automation scripts:

| Skill | Description | Key Capabilities |
| :--- | :--- | :--- |
| **`dubbing-pipeline`** | End-to-end automated dubbing pipeline | 4-phase sequential workflow from ElevenLabs Scribe V2 JSON to finalized, phonetically transcribed dubbing scripts. |
| **`dubbing-translator-guide-english-to-turkish`** | English-to-Turkish lip-sync dubbing guide | Spoken syllable count matching ($\pm 10\%$), viseme/mouth shape alignment, strict anti-padding rules, automated Python audit, and comparative XLSX generator. |
| **`dubbing-translator-french-to-turkish`** | French-to-Turkish lip-sync translation | Spoken syllable timing, front/back rounded vowels (Ü, Ö, U), nasal vowels, and Turkish pro-drop optimizations. |
| **`english-to-turkish-phonetic-transcription`** | IPA-based phonetic transcription | Converts foreign names, places, and brands into Turkish phonetics (e.g. *Williams* $\rightarrow$ *Vilyıms*, *FBI* $\rightarrow$ *EfBiAy*) for dubbing artists. |
| **`srt-dialogue-extractor`** | SRT subtitle dialogue cleaner | Strips timecodes, SDH audio descriptions, background music notes (`♪`), merges broken sentence continuations, and formats single-spaced Markdown dialogue. |
| **`dubbing-script-timecode-converter`** | Video timecode converter & Word aligner | Converts player-based timecodes (`23.976 fps`) into embedded Burn-In Timecodes (BITC, `24.0 fps`), drift correction, and Microsoft Word tab stop alignment. |

---

## 📁 Repository Structure

```
dubbing-and-subtitle-tools/
├── plugin.json                                      # Antigravity plugin manifest
├── requirements.txt                                 # Python dependencies for audit scripts
├── LICENSE                                          # MIT License
├── README.md                                        # Documentation
├── .gitignore
└── skills/
    ├── dubbing-pipeline/
    │   └── SKILL.md                                 # 4-stage ElevenLabs JSON dubbing pipeline
    ├── dubbing-script-timecode-converter/
    │   └── SKILL.md                                 # 23.976 to 24fps BITC timecode converter
    ├── dubbing-translator-french-to-turkish/
    │   └── SKILL.md                                 # French -> Turkish lip-sync translation methodology
    ├── dubbing-translator-guide-english-to-turkish/
    │   ├── SKILL.md                                 # English -> Turkish syllable & lip-sync methodology
    │   └── scripts/
    │       ├── count_and_audit.py                   # Automated syllable & rule audit script
    │       └── generate_excel_audit.py              # 5-column comparative Excel audit generator
    ├── english-to-turkish-phonetic-transcription/
    │   └── SKILL.md                                 # IPA-to-Turkish phonetic conversion standard
    └── srt-dialogue-extractor/
        ├── SKILL.md                                 # SRT cleanup rules and usage
        └── scripts/
            └── clean_srt.py                         # SRT parser and text normalizer
```

---

## 🚀 Installation

### Option 1: Global Installation (All Antigravity Projects)

Clone this repository directly into your Antigravity global plugins directory:

```bash
git clone https://github.com/umutaktepe/dubbing-and-subtitle-tools.git ~/.gemini/config/plugins/dubbing-and-subtitle-tools
```

### Option 2: Project-Level Installation (Workspace Specific)

Clone into your workspace's `.agents/plugins/` directory:

```bash
git clone https://github.com/umutaktepe/dubbing-and-subtitle-tools.git .agents/plugins/dubbing-and-subtitle-tools
```

### Python Dependencies

The audit and processing scripts require Python 3.9+ and a couple of lightweight libraries:

```bash
pip install -r requirements.txt
```

*(Installs `syllables` for English syllable estimation and `openpyxl` for Excel audit sheet generation.)*

---

## 🛠️ Usage Details

### 1. Dubbing Preparation Pipeline (`dubbing-pipeline`)
- **Trigger**: Run with an ElevenLabs Scribe V2 JSON transcript.
- **Workflow**:
  1. Interactive gatekeeping (prompts for Movie Title and IMDb URL).
  2. Phase 1: Parses pauses, word boundaries, and produces initial dialogue blocks.
  3. Phase 2: Generates character list and speaker mappings.
  4. Phase 3: Researches character background and context.
  5. Phase 4: Applies full Turkish phonetic transcription to proper names and titles.

### 2. English-to-Turkish Lip-Sync Translator (`dubbing-translator-guide-english-to-turkish`)
- **Syllable Counting**: Spoken syllables matched within $\pm 10\%$.
- **Automated Verification**:
  ```bash
  python3 skills/dubbing-translator-guide-english-to-turkish/scripts/count_and_audit.py source_en.md dubbing_tr.md
  ```
- **Excel Report**:
  ```bash
  python3 skills/dubbing-translator-guide-english-to-turkish/scripts/generate_excel_audit.py source_en.md dubbing_tr.md audit_report.xlsx
  ```

### 3. SRT Dialogue Extractor (`srt-dialogue-extractor`)
- Strips SDH cues, sound effects, music brackets, and fixes multi-speaker dashes:
  ```bash
  python3 skills/srt-dialogue-extractor/scripts/clean_srt.py input.srt -o dialogue_clean.md
  ```

### 4. Timecode Converter (`dubbing-script-timecode-converter`)
- Converts `23.976 fps` player timecodes to `24.0 fps` burned-in timecodes (BITC):
  - $\text{s\_bitc} = \text{s\_start} + \left( \frac{\text{s\_player}}{1.001} \right)$
  - Formats output with dot separators (`MM.SS` / `HH.MM.SS`) and tabs (`\t`) after character tags for seamless Microsoft Word pasting.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 👤 Author

**Umut Aktepe**
- GitHub: [@umutaktepe](https://github.com/umutaktepe)
