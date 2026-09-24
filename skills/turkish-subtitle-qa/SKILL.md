---
name: turkish-subtitle-qa
description: Use when reviewing, proofreading, or quality-checking Turkish subtitles (.srt), fixing translation awkwardness, verifying CPL line lengths, dialogue dashes, cross-card quotes, or auditing subtitle synchronization and Turkish grammar.
---

# Turkish Subtitle QA & Proofreader (Türkçe Alt Yazı Kalite Güvencesi)

## Overview
Türkçe alt yazı (`.srt`) dosyalarını; teknik zaman kodu sıralaması, satır uzunluğu (CPL), diyalog ve tırnak kuralları, TDK imla standartları, anlatım bozuklukları ve kaynak metin bağlamı açısından denetleyen ve iki aşamalı (Denetim Raporu -> Onaylı Düzeltme) iş akışıyla düzelten profesyonel kalite güvencesi kılavuzudur.

---

## Zorunlu Ön Sorular (IRON RULES - Atlanamaz Adımlar)

Herhangi bir alt yazı analizi veya düzeltme işlemine başlamadan önce kullanıcıya **`ask_question`** aracı ile sırayla şu 2 soru **MUTLAKA** sorulmalıdır:

1. **CPL Sınırı Belirleme:**
   > *"Bu proje için hedef maksimum satır uzunluğu (CPL) nedir?"*
   > - `42 CPL (Standart VOD / Dijital Platformlar - Netflix)`
   > - `36 CPL (Genişletilmiş / Dar Ekran Standardı)`

2. **Kaynak / Orijinal Dosya Varlığı:**
   > *"Çeviri ve bağlam doğruluğunu çapraz kontrol etmek için orijinal/kaynak (İngilizce vb.) bir dosya var mı?"*
   > - `Evet, kaynak dosya var (Lütfen dosya yolunu belirtin).`
   > - `Hayır, kaynak dosya yok (Yalnızca Türkçe metin ve teknik akış üzerinden ilerle).`

*Not: Kullanıcı kaynak dosya olmadığını belirtirse, denetim yalnızca Türkçe dosyanın iç mantığı, akıcılığı ve teknik kuralları üzerinden sürdürülür.*

---

## Alt Yazı Standartları ve Tipografik Kurallar

### 1. Satır Başı ve Diyalog Tiresi
- **Boşluksuz Tire Standardı:** İkili diyaloglarda tireden sonra **kesinlikle boşluk bırakılmaz**:
  - ✅ `-Tamam, geliyorum.`
  - ❌ `- Tamam, geliyorum.`
- **İki Konuşmacı Kuralı:** Aynı alt yazı kartında iki farklı konuşmacı varsa, **her iki satırın başında da** tire yer almalıdır:
  ```srt
  -Nereye gidiyorsun?
  -Eve dönüyorum.
  ```
  *(Tek satırda tire olup diğerinde olmaması standart hatasıdır).*

### 2. Kartlar Arası Tırnak İşareti ve Alıntı Kuralları
Bir doğrudan alıntı birden fazla alt yazı kartına bölünüyorsa:
1. Tırnak işareti **yalnızca ilk kartta** alıntının başladığı yerde açılır: `"Pokpak, sonsuza kadar…`
2. Alıntı henüz bitmediği için ara kartlarda **tırnak kapatılmaz**: `…böyle arkada mı kalacaksın?` (ve kart başında tekrar tırnak açılmaz).
3. Alıntının tamamen bittiği son kartta soru/ünlem/nokta konur, **tırnak burada kapatılır** ve ana cümlenin aktarım/yüklem fiili tırnağın dışına yazılır: `Önde olmak istemiyor musun?" dediği andı.`
4. TDK Kuralı gereği tırnaktan sonra küçük harfle devam edilir: `..." dediği andı.`

### 3. TDK İmla ve Düzeltme İşareti (Şapka)
- **Düzeltme İşareti:** Tutkun/sevdalı anlamındaki sözcük mutlaka **"âşık"** olarak yazılır (*"aşık"* kemik adıdır).
- **Bağlaç Olan de/da ve ki:** Her zaman ayrı yazılır (*"Lisa da ben de"*, *"Bence de"*, *"öyle ki"*).
- **Ek Olan -de/-da ve -ki:** Bitişik yazılır (*"stüdyoda"*, *"içindeki"*).
- **Kesme İşaretleri:** Özel adlara ve kısaltmalara gelen çekim ekleri kesmeyle ayrılır (*"Lisa'nın"*, *"YG'ye"*, *"Spotify'da"*, *"LA'e"*).

### 4. Noktalama ve Boşluk Temizliği
- **Satır Sonu Boşlukları (Trailing Whitespace):** Satır sonlarında görünmez boşluk karakteri kalmamalıdır.
- **Üç Nokta / Ellipsis Standardı:** Üç ayrı nokta (`...`) **kesinlikle kullanılmaz**. Bunun yerine her zaman tek bir karakter olan Unicode yatay üç nokta / ellipsis (`…` / U+2026) kullanılmalıdır. Metinde geçen tüm `...` kullanımları tek glifli `…` ile değiştirilmelidir.

---

## İki Aşamalı İş Akışı

```
[Kullanıcı İstemi]
       │
       ▼
[Zorunlu Sorular: CPL (36/42) & Kaynak Dosya?]
       │
       ▼
[Aşama 1: check_srt.py Betiğini Çalıştır + Dilbilgisel/Bağlamsal Analiz]
       │
       ▼
[Detaylı Denetim Raporu Sunumu]
       │
       ▼
[Kullanıcı Onayı Alınır]
       │
       ▼
[Aşama 2: Düzeltilmiş _duzeltilmis.srt Dosyasını Üret]
```

### Aşama 1: Detaylı Denetim Raporu Sunma
Dosyayı doğrudan değiştirmeden önce kullanıcıya şu başlıklar altında kategorize edilmiş bir rapor sunulur:
1. **Zaman Kodu ve Blok Sıralaması (Kronoloji Hataları):** Zaman kodları geriye giden, sıralaması karışmış veya başka kartın arasına kaçmış bloklar (Örn: blok 60 senkron hatası).
2. **CPL Sınırı Aşımı:** Kullanıcının seçtiği CPL sınırını (36 veya 42) aşan satır numaraları ve karakter sayıları.
3. **Anlatım Bozuklukları ve Eksiklik/Fazlalıklar:** Yüklem-özne uyumsuzlukları, tamlama yanlışları, pleonazmlar (*"ilk öncü"* vb.), motamot deyim kopyalamaları (*"şans vermek"* vb.), anglisizmler (*"özgür hissettiriyor"* vb.).
4. **Bağlam ve Çeviri Hataları:** Kaynak metin varsa orijinal konuşmayla uyuşmayan, anlamı tersine çeviren veya özneyi muğlaklaştıran yerler.
5. **Noktalama, Diyalog Tiresi ve İmla:** Tırnak içi nokta eksikleri, tek kalan diyalog tireleri, satır sonu boşlukları.

### Aşama 2: Temiz SRT Dosyası Üretme
Kullanıcı rapordaki düzeltmeleri onayladığında:
- Hatalar düzeltilir.
- Blok numaraları `1`den başlayarak sıralı hale getirilir.
- Orijinal dosya korunur, çıktı `[DosyaAdi]_duzeltilmis.srt` olarak kaydedilir veya kullanıcının açık talebi varsa üzerine yazılır.

---

## Yardımcı Betik Kullanımı (`check_srt.py`)

Teknik hataları deterministik ve hızlı taramak için skill içinde yer alan Python aracı çalıştırılır:

```bash
python3 /home/umutaktepe/.gemini/config/plugins/dubbing-and-subtitle-tools/skills/turkish-subtitle-qa/scripts/check_srt.py <dosya_yolu.srt> --cpl <36|42> [--en-srt <kaynak_yolu.srt>]
```

**JSON çıktısı almak için:**
```bash
python3 /home/umutaktepe/.gemini/config/plugins/dubbing-and-subtitle-tools/skills/turkish-subtitle-qa/scripts/check_srt.py <dosya_yolu.srt> --cpl 42 --json
```

---

## Yaygın Hatalar Tablosu (Quick Reference)

| Hatalı Kullanım | Neden Yanlış? | Düzeltilmiş Hali |
| :--- | :--- | :--- |
| `- Söz` | Standart kural: Tireden sonra boşluk olmaz | `-Söz` |
| 1. satırda tire yok, 2. satırda `-Söz` var | Aynı kartta 2 konuşmacı varsa ikisinde de tire olmalıdır | `-1. konuşmacı`<br>`-2. konuşmacı` |
| `ilk öncülerden biriydi` | "Öncü" zaten ilk olandır; pleonazm / gereksiz sözcük | `öncülerden biriydi` |
| `Her şey çok özgür hissettiriyor` | Durumlar özgür hissetmez; anglisizm | `İnsan kendini çok özgür hissediyor` |
| `"Alıntı" dedi.` | TDK: Tırnak içi cümlenin noktası tırnak içinde kalır | `"Alıntı." dedi.` |
| `aşık olmak` | TDK: Sevdalı anlamındaki sözcük düzeltme işareti alır | `âşık olmak` |
| `istediğim bir şeyleri` | Belirsiz "bir" ile belirtili "-leri" çelişkisi | `istediğim şeyleri` |
| `...` (üç ayrı nokta) | Standart ihlali: Üç ayrı nokta kullanılmaz; tek glifli ellipsis zorunludur | `…` (tek karakter ellipsis) |
