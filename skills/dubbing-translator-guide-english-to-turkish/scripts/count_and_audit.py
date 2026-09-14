#!/usr/bin/env python3
"""
Dubbing Syllable Counter & Comprehensive Audit Script
Used by dubbing-translator-guide-english-to-turkish skill.

Calculates English phoneme syllables and Turkish vowel syllables.
Scans for:
1. Out-of-bounds syllable counts (|N_tr - N_en| > tolerance)
2. Incomplete / truncated sentences & suspicious trailing words
3. Artificial repetitive filler tags and prohibited padding phrases
4. Untranslated professional title transliterations (e.g. Nörs, Sıstır)
5. Dynamic Repetitive Ending Word Heuristic (detects unlisted repeated tail words across batch)
"""

import sys
import os
from collections import Counter
import syllables

def count_syllables_en(text: str) -> int:
    """Calculates English spoken syllable count using CMUDict/syllables library."""
    words = text.split()
    return sum(syllables.estimate(w) for w in words)

def count_syllables_tr(text: str) -> int:
    """Calculates Turkish spoken syllable count by counting vowels in phonetic text."""
    vowels = "aeıioöuüAEIİOÖUÜ"
    return sum(1 for char in text if char in vowels)

def audit_dubbing_files(en_file_path: str, tr_file_path: str):
    if not os.path.exists(en_file_path):
        print(f"Error: English source file not found at '{en_file_path}'")
        sys.exit(1)
    if not os.path.exists(tr_file_path):
        print(f"Error: Turkish dubbing file not found at '{tr_file_path}'")
        sys.exit(1)

    with open(en_file_path, "r", encoding="utf-8") as f:
        en_lines = [l.strip() for l in f if l.strip()]

    with open(tr_file_path, "r", encoding="utf-8") as f:
        tr_lines = [l.strip() for l in f if l.strip()]

    print(f"=== DUBBING SYLLABLE & COMPREHENSIVE AUDIT ===")
    print(f"English Source Lines : {len(en_lines)}")
    print(f"Turkish Dubbing Lines: {len(tr_lines)}")

    if len(en_lines) != len(tr_lines):
        print(f"[CRITICAL ERROR] Line count mismatch! EN={len(en_lines)} vs TR={len(tr_lines)}")
    
    # Suspicious words that should not end a complete sentence
    suspicious_endings = {
        "bana", "söküp", "mi", "mı", "mu", "mü", "ile", "için", "veya", "gibi", "kadar",
        "daha", "çok", "bir", "ve", "de", "da", "bu", "şu", "o", "ama", "fakat", "ancak",
        "ise", "ki", "diye", "olarak", "üzere", "sonra", "önce", "tarafından", "hakkında",
        "göre", "karşı", "rağmen", "çünkü", "hem", "ne"
    }

    # Prohibited filler tags and repetitive mechanical padding phrases
    forbidden_fillers = [
        "polisler", "yani", "anladın mı", "adamım", "gerçeği söylemek gerekirse",
        "kesinlikle aslında", "bence sanırım", "aslında bakarsan", "şöyle ki"
    ]

    # Prohibited transliterations of professional titles (should be translated)
    title_transliterations = [
        "Nörs", "Sıstır", "Doktır", "Serfınt", "Ofısır", "Löftenan", "Mecır", "Kılonıl", "Paster", "Revırınd"
    ]

    out_of_bounds = []
    incomplete_sentences = []
    filler_violations = []
    untranslated_titles = []
    ending_words = []

    for idx, (en, tr) in enumerate(zip(en_lines, tr_lines), 1):
        n_en = count_syllables_en(en)
        n_tr = count_syllables_tr(tr)
        tol = max(1, round(0.10 * n_en))
        diff = abs(n_tr - n_en)

        # 1. Syllable bounds check
        if diff > tol:
            out_of_bounds.append((idx, en, n_en, tr, n_tr, diff, tol))

        # 2. Check incomplete sentence conditions
        en_complete = en.endswith(".") or en.endswith("!") or en.endswith("?")
        tr_has_punct = tr.endswith(".") or tr.endswith("!") or tr.endswith("?")
        last_word = tr.strip().rstrip(".!?,\"").split()[-1].lower() if tr.strip().rstrip(".!?,\"").split() else ""

        if last_word:
            ending_words.append((idx, last_word))

        if (en_complete and not tr_has_punct) or (en_complete and last_word in suspicious_endings and not tr.endswith("?")):
            incomplete_sentences.append((idx, en, tr, last_word))

        # 3. Check for forbidden filler tags / phrases
        tr_lower = tr.lower()
        for filler in forbidden_fillers:
            if filler in tr_lower:
                filler_violations.append((idx, tr, filler))
                break

        # 4. Check for untranslated title transliterations
        for title in title_transliterations:
            if title in tr:
                untranslated_titles.append((idx, tr, title))
                break

    # Dynamic Heuristic: Detect abnormally repeated sentence ending words across the batch
    # Ignore common legitimate verbs like "olur", "yaptı", "geldi" unless frequency is unnaturally high
    tail_counts = Counter([w for _, w in ending_words if len(w) > 2])
    suspicious_repeated_tails = []
    for word, count in tail_counts.items():
        if count >= 3 and word not in {"değil", "oldu", "yaptı", "geldi", "gitti", "dedi", "olur", "yok", "var"}:
            affected_rows = [i for i, w in ending_words if w == word]
            suspicious_repeated_tails.append((word, count, affected_rows))

    print("\n--- AUDIT SUMMARY ---")
    print(f"Syllable Out-of-Bounds Lines (|N_tr - N_en| > tol) : {len(out_of_bounds)}")
    print(f"Incomplete / Truncated Sentence Candidates        : {len(incomplete_sentences)}")
    print(f"Forbidden Filler / Tag Violations                 : {len(filler_violations)}")
    print(f"Untranslated Title Transliterations               : {len(untranslated_titles)}")
    print(f"Suspicious Repetitive Ending Word Patterns        : {len(suspicious_repeated_tails)}")

    if out_of_bounds:
        print("\n[ATTENTION] Syllable Out-of-Bounds Lines:")
        for idx, en, n_en, tr, n_tr, diff, tol in out_of_bounds:
            print(f"  Row {idx:3d} | EN={n_en} vs TR={n_tr} | Diff={diff} (Max Tol={tol})")
            print(f"    EN: {en}")
            print(f"    TR: {tr}")

    if incomplete_sentences:
        print("\n[ATTENTION] Incomplete / Truncated Sentence Candidates:")
        for idx, en, tr, last in incomplete_sentences:
            print(f"  Row {idx:3d} (Ends suspiciously with '{last}')")
            print(f"    EN: {en}")
            print(f"    TR: {tr}")

    if filler_violations:
        print("\n[ATTENTION] Forbidden Filler / Tag Violations:")
        for idx, tr, filler in filler_violations[:10]:
            print(f"  Row {idx:3d} (Contains forbidden phrase '{filler}')")
            print(f"    TR: {tr}")

    if suspicious_repeated_tails:
        print("\n[ATTENTION] Suspicious Repetitive Ending Words (Possible unlisted filler tag):")
        for word, count, rows in suspicious_repeated_tails:
            print(f"  Word '{word}' repeated as sentence ending {count} times in rows: {rows}")

    if untranslated_titles:
        print("\n[ATTENTION] Untranslated Titles Found:")
        for idx, tr, title in untranslated_titles[:10]:
            print(f"  Row {idx:3d} (Contains untranslated title '{title}')")
            print(f"    TR: {tr}")

    has_errors = bool(out_of_bounds or incomplete_sentences or filler_violations or untranslated_titles or suspicious_repeated_tails or len(en_lines) != len(tr_lines))

    if not has_errors:
        print("\n[SUCCESS] Script integrity verified! Zero errors, zero truncated sentences, and clean lip-sync stats.")
    else:
        print("\n[WARNING] Audit found issues that must be fixed in Stage 3 or Stage 4 before finalizing.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 count_and_audit.py <english_source.md> <turkish_dubbing.md>")
        sys.exit(1)
    audit_dubbing_files(sys.argv[1], sys.argv[2])
