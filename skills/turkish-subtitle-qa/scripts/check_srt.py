#!/usr/bin/env python3
"""
SRT Kalite Güvencesi ve Teknik Denetim Aracı (Turkish Subtitle QA)
Teknik zaman kodu sıralaması, CPL sınırı, diyalog tireleri, noktalama ve imla kontrolleri yapar.
"""

import sys
import os
import re
import argparse
import json

def parse_time(time_str):
    """00:00:00,000 formatını milisaniyeye çevirir."""
    try:
        parts = time_str.strip().split(' --> ')
        if len(parts) != 2:
            return None, None
        
        def to_ms(t):
            h, m, s = t.split(':')
            s, ms = s.split(',')
            return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)
            
        return to_ms(parts[0]), to_ms(parts[1])
    except Exception:
        return None, None

def parse_srt(file_path):
    """SRT dosyasını bloklara ayırarak ayrıştırır."""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    raw_blocks = re.split(r'\n\s*\n+', content.strip())
    parsed_blocks = []

    for b in raw_blocks:
        lines = [l.rstrip('\r') for l in b.strip().split('\n') if l.strip() != '']
        if len(lines) < 2:
            continue
        
        try:
            idx = int(lines[0])
            timecode = lines[1]
            text_lines = lines[2:]
        except ValueError:
            # Bazı hatalı dosyalarda numara eksik olabilir
            timecode = lines[0]
            text_lines = lines[1:]
            idx = -1

        start_ms, end_ms = parse_time(timecode)
        parsed_blocks.append({
            'raw_index': idx,
            'timecode': timecode,
            'start_ms': start_ms,
            'end_ms': end_ms,
            'text_lines': text_lines,
            'full_text': ' '.join(text_lines)
        })

    return parsed_blocks

def analyze_subtitles(tr_blocks, max_cpl=42, en_blocks=None):
    issues = {
        'chronology_errors': [],
        'numbering_errors': [],
        'cpl_violations': [],
        'dialogue_dash_errors': [],
        'trailing_whitespace': [],
        'ellipsis_errors': [],
        'spelling_warnings': [],
        'stats': {
            'total_blocks': len(tr_blocks),
            'max_cpl_set': max_cpl
        }
    }

    prev_end_ms = 0

    for i, block in enumerate(tr_blocks):
        idx = block['raw_index']
        start_ms = block['start_ms']
        end_ms = block['end_ms']
        text_lines = block['text_lines']

        # 1. Numaralandırma Kontrolü
        if idx != -1 and idx != (i + 1):
            issues['numbering_errors'].append({
                'block': idx,
                'expected': i + 1,
                'message': f"Blok numarası sırası bozuk: Beklenen {i+1}, bulunan {idx}"
            })

        # 2. Kronoloji ve Zaman Kodu Kontrolü (Geriye gitme / Sıra kayması)
        if start_ms is not None:
            if start_ms < prev_end_ms:
                diff_sec = (prev_end_ms - start_ms) / 1000.0
                issues['chronology_errors'].append({
                    'block': idx,
                    'timecode': block['timecode'],
                    'message': f"Zaman kodu geriye gidiyor! Başlangıç, önceki bloğun bitişinden {diff_sec:.2f} sn önce.",
                    'text': block['full_text']
                })
            prev_end_ms = end_ms if end_ms is not None else start_ms

        # 3. Satır Uzunluğu (CPL) Kontrolü
        for line_num, line in enumerate(text_lines, 1):
            char_count = len(line)
            if char_count > max_cpl:
                issues['cpl_violations'].append({
                    'block': idx,
                    'line_num': line_num,
                    'char_count': char_count,
                    'max_allowed': max_cpl,
                    'line': line
                })

            # 4. Satır Sonu Boşluk (Trailing Space)
            if line.endswith(' ') or line.endswith('\t'):
                issues['trailing_whitespace'].append({
                    'block': idx,
                    'line_num': line_num,
                    'line': line
                })

        # 5. İkili Diyalog Tire Kontrolü (Kural: Tireden sonra boşluk olmamalı '-Söz')
        # Ve aynı kartta iki konuşmacı varsa her ikisi de '-' ile başlamalı
        has_dash = [l.startswith('-') for l in text_lines]
        if any(has_dash):
            if len(text_lines) > 1 and not all(has_dash):
                issues['dialogue_dash_errors'].append({
                    'block': idx,
                    'message': "İki satırlı kartta yalnızca tek satırda diyalog tiresi var! İki konuşmacı varsa her iki satır da tire ile başlamalıdır.",
                    'lines': text_lines
                })
            for line in text_lines:
                if line.startswith('- '):
                    issues['dialogue_dash_errors'].append({
                        'block': idx,
                        'message': "Standart kural ihlali: Tireden sonra boşluk bırakılmış ('- Söz'). Boşluksuz ('-Söz') olmalıdır.",
                        'lines': text_lines
                    })

        # 6. Üç Nokta Kontrolü (Kural: Kesinlikle tek glifli ellipsis '…' kullanılmalı, '...' yasaktır)
        for line_num, line in enumerate(text_lines, 1):
            if '...' in line:
                issues['ellipsis_errors'].append({
                    'block': idx,
                    'line_num': line_num,
                    'line': line,
                    'message': "Standart kural ihlali: Üç ayrı nokta ('...') kullanılmış. Tek glifli ellipsis ('…') kullanılmalıdır."
                })

        # 7. İmla Sezgisel Uyarıları (Örn: âşık kontrolü)
        full_text = block['full_text']
        if re.search(r'\başık\b', full_text, re.IGNORECASE):
            issues['spelling_warnings'].append({
                'block': idx,
                'word': 'aşık',
                'suggestion': 'âşık (Tutkun anlamında TDK düzeltme işareti gerektirir)',
                'text': full_text
            })

    return issues

def main():
    parser = argparse.ArgumentParser(description="SRT Turkish QA Checker")
    parser.add_argument("srt_file", help="Denetlenecek Türkçe .srt dosyası")
    parser.add_argument("--cpl", type=int, choices=[36, 42], default=42, help="Maksimum CPL (36 veya 42)")
    parser.add_argument("--en-srt", help="Kaynak İngilizce .srt dosyası (çapraz kontrol için)", default=None)
    parser.add_argument("--json", action="store_true", help="JSON formatında çıktı ver")

    args = parser.parse_args()

    if not os.path.exists(args.srt_file):
        print(f"Hata: Dosya bulunamadı: {args.srt_file}", file=sys.stderr)
        sys.exit(1)

    tr_blocks = parse_srt(args.srt_file)
    en_blocks = parse_srt(args.en_srt) if args.en_srt and os.path.exists(args.en_srt) else None

    issues = analyze_subtitles(tr_blocks, max_cpl=args.cpl, en_blocks=en_blocks)

    if args.json:
        print(json.dumps(issues, ensure_ascii=False, indent=2))
        return

    print("=" * 60)
    print(f"SRT DENETİM RAPORU: {os.path.basename(args.srt_file)}")
    print(f"Toplam Blok: {issues['stats']['total_blocks']} | Hedef Max CPL: {issues['stats']['max_cpl_set']}")
    print("=" * 60)

    # 1. Kronoloji Hataları
    if issues['chronology_errors']:
        print(f"\n🚨 [KRİTİK] Zaman Kodu ve Sıralama Hataları ({len(issues['chronology_errors'])} adet):")
        for err in issues['chronology_errors']:
            print(f"  - Blok #{err['block']} [{err['timecode']}]: {err['message']}")
            print(f"    Metin: {err['text']}")
    else:
        print("\n✅ Zaman kodu kronolojisi ve akışı düzgün.")

    # 2. CPL Hataları
    if issues['cpl_violations']:
        print(f"\n⚠️  [CPL AŞIMI] Maksimum {args.cpl} Karakter Aşımı ({len(issues['cpl_violations'])} satır):")
        for v in issues['cpl_violations']:
            print(f"  - Blok #{v['block']}, Satır {v['line_num']} ({v['char_count']} karakter): \"{v['line']}\"")
    else:
        print(f"\n✅ Tüm satırlar {args.cpl} CPL sınırına uygun.")

    # 3. Diyalog Tire Hataları
    if issues['dialogue_dash_errors']:
        print(f"\n⚠️  [DİYALOG TİRESİ] Standart Dışı Tire Kullanımı ({len(issues['dialogue_dash_errors'])} adet):")
        for d in issues['dialogue_dash_errors']:
            print(f"  - Blok #{d['block']}: {d['message']}")
    else:
        print("\n✅ Diyalog tireleri standartlara uygun ('-Söz').")

    # 4. Satır Sonu Boşlukları
    if issues['trailing_whitespace']:
        print(f"\n⚠️  [BOŞLUK] Satır Sonu Gereksiz Boşluklar ({len(issues['trailing_whitespace'])} adet):")
        for w in issues['trailing_whitespace']:
            print(f"  - Blok #{w['block']}, Satır {w['line_num']}: \"{w['line']}\"")

    # 5. Üç Nokta / Ellipsis Hataları
    if issues['ellipsis_errors']:
        print(f"\n⚠️  [ELLIPSIS STANDART İHLALİ] Üç Ayrı Nokta ('...') Kullanımı ({len(issues['ellipsis_errors'])} adet):")
        for e in issues['ellipsis_errors']:
            print(f"  - Blok #{e['block']}, Satır {e['line_num']}: \"{e['line']}\"")
            print(f"    Öneri: '...' yerine tek glifli ellipsis '…' kullanılmalıdır.")
    else:
        print("\n✅ Üç nokta standartlara uygun (Yalnızca tek glifli '…' kullanılmış).")

    # 6. İmla Uyarıları
    if issues['spelling_warnings']:
        print("\n📝 [İMLA UYARISI] TDK Uyum Önerileri:")
        for s in issues['spelling_warnings']:
            print(f"  - Blok #{s['block']}: '{s['word']}' -> Öneri: {s['suggestion']}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
