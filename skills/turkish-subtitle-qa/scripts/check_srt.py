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
        'duration_warnings': [],
        'numbering_errors': [],
        'cpl_violations': [],
        'dialogue_dash_errors': [],
        'trailing_whitespace': [],
        'ellipsis_errors': [],
        'spelling_warnings': [],
        'number_warnings': [],
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

        # 3. Blok Süresi Kontrolü (Minimum 0.833 sn / 833 ms, Maksimum 7.0 sn)
        if start_ms is not None and end_ms is not None:
            dur_sec = (end_ms - start_ms) / 1000.0
            if dur_sec < 0.833:
                issues['duration_warnings'].append({
                    'block': idx,
                    'type': 'too_short',
                    'duration_sec': dur_sec,
                    'timecode': block['timecode'],
                    'message': f"Süre çok kısa ({dur_sec:.3f} sn)! Standart kural: Alt yazı kartı 0.833 saniyeden (833 ms) kısa olamaz.",
                    'text': block['full_text']
                })
            elif dur_sec > 7.0:
                issues['duration_warnings'].append({
                    'block': idx,
                    'type': 'too_long',
                    'duration_sec': dur_sec,
                    'timecode': block['timecode'],
                    'message': f"Süre çok uzun ({dur_sec:.3f} sn)! Standart kural: Alt yazı kartı 7.0 saniyeden uzun olamaz.",
                    'text': block['full_text']
                })

        # 4. Satır Uzunluğu (CPL) Kontrolü
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

        # 8. Sayıların Yazımı Kontrolü (Netflix & TDK Kuralı: 0-9 yazıyla, 10+ rakamla, binlik/ondalık biçimi)
        # 8.1. Binlik basamaklarda İngilizce virgül kullanımı (Örn: 4,000 yerine 4.000 olmalı)
        comma_thousands = re.findall(r'\b\d{1,3},\d{3}\b', full_text)
        if comma_thousands:
            for ct in comma_thousands:
                issues['number_warnings'].append({
                    'block': idx,
                    'type': 'binlik_virgul_hatasi',
                    'found': ct,
                    'suggestion': ct.replace(',', '.'),
                    'message': f"Türkçe standart ihlali: Binlik basamak ayırıcı virgül (,) değil nokta (.) olmalıdır ('{ct}' yerine '{ct.replace(',', '.')}')."
                })

        # 8.2. Ondalık sayılarda İngilizce nokta kullanımı (Örn: 2.5 milyon yerine 2,5 milyon olmalı)
        dot_decimals = re.findall(r'\b(\d+\.\d+)\s*(milyon|milyar|trilyon|kat|oranında|derece|litre|metre|kg|kilo)\b', full_text, re.IGNORECASE)
        if dot_decimals:
            for dd, unit in dot_decimals:
                issues['number_warnings'].append({
                    'block': idx,
                    'type': 'ondalik_nokta_hatasi',
                    'found': f"{dd} {unit}",
                    'suggestion': f"{dd.replace('.', ',')} {unit}",
                    'message': f"Türkçe standart ihlali: Ondalık ayırıcı nokta (.) değil virgül (,) olmalıdır ('{dd}' yerine '{dd.replace('.', ',')}')."
                })

        # 8.3. 0-9 arası sayıların tek başına rakamla yazılması (Ölçü birimi yoksa yazıyla yazılmalıdır)
        units_pattern = r'(?:kg|kilo|kiloyum|km|m|cm|mm|gb|mb|tb|dolar|euro|tl|lira|kuruş|mil|kat|inç|adet|tane|%|:|\.|\/)'
        standalone_digits = re.findall(r'(?<![0-9,\.:\/-])\b([0-9])\b(?![0-9,\.:\/-])', full_text)
        DIGIT_WORDS = {'0': 'sıfır', '1': 'bir', '2': 'iki', '3': 'üç', '4': 'dört', '5': 'beş', '6': 'altı', '7': 'yedi', '8': 'sekiz', '9': 'dokuz'}
        for digit in standalone_digits:
            is_unit = re.search(r'\b' + digit + r'\s*' + units_pattern, full_text, re.IGNORECASE)
            if not is_unit and not re.search(r'\b(bölüm|sezon|sayfa|no|madde)\s*' + digit, full_text, re.IGNORECASE):
                word_rep = DIGIT_WORDS.get(digit, digit)
                issues['number_warnings'].append({
                    'block': idx,
                    'type': 'kucuk_sayi_rakamla',
                    'found': digit,
                    'suggestion': word_rep,
                    'message': f"Sayı standardı: 0-9 arası sayılar yer kısıtı yoksa kural gereği yazıyla yazılmalıdır ('{digit}' yerine '{word_rep}')."
                })

        # 8.4. 10 ve üzeri sayıların harfle yazılması (Deyimler ve ikilemeler hariç rakamla yazılmalıdır)
        idiom_pattern = r'\b(kırk\s+kere|bin\s+bir|bin\s+dereden|on\s+parmağında|dört\s+başı|yüz\s+akı|yüz\s+yüze|bir\s+iki|üç\s+beş|üç\s+dört)\b'
        num_words_pattern = r'\b(on\s+(?:bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz)|yirmi|otuz|kırk|elli|altmış|yetmiş|seksen|doksan)\b'
        if not re.search(idiom_pattern, full_text, re.IGNORECASE):
            w_matches = re.findall(num_words_pattern, full_text, re.IGNORECASE)
            if w_matches:
                for wm in w_matches:
                    issues['number_warnings'].append({
                        'block': idx,
                        'type': 'buyuk_sayi_harfle',
                        'found': wm,
                        'suggestion': 'Rakamla yazım',
                        'message': f"Sayı standardı: 10 ve üzeri sayılar (deyimler hariç) alt yazılarda rakamla yazılmalıdır ('{wm}')."
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

    # 2. Blok Süresi Limit Aşımı (< 0.833 sn veya > 7.0 sn)
    if issues['duration_warnings']:
        print(f"\n⏱️  [SÜRE STANDART UYARILARI] Kart Süresi Limit Aşımı ({len(issues['duration_warnings'])} adet):")
        for dur in issues['duration_warnings']:
            print(f"  - Blok #{dur['block']} [{dur['timecode']}] ({dur['duration_sec']:.3f} sn): {dur['message']}")
            print(f"    Metin: \"{dur['text']}\"")
        print("  ⚠️  DİKKAT: Süre düzeltmesi ses/video kurgusu ve senkron gerektirdiğinden düzeltilmiş SRT oluşturulurken süreye kesinlikle müdahale edilmez.")
    else:
        print("\n✅ Tüm alt yazı kart süreleri standartlara uygun (0.833 sn - 7.0 sn aralığında).")

    # 3. CPL Hataları
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

    # 7. Sayıların Yazımı Uyarıları
    if issues['number_warnings']:
        print(f"\n🔢 [SAYI STANDART UYARILARI] Sayı/Rakam Format Hataları ({len(issues['number_warnings'])} adet):")
        for num_err in issues['number_warnings']:
            print(f"  - Blok #{num_err['block']}: {num_err['message']}")
    else:
        print("\n✅ Sayıların yazımı standartlara uygun (0-9 yazıyla, 10+ rakamla, binlik/ondalık doğru).")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
