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

### 5. Sayıların Yazımı (Yazıyla mı Rakamla mı? - Netflix & TDK Standardı)
- **0 ile 9 Arası Sayılar (Harfle / Yazıyla):** Yer veya zaman kısıtlaması (CPL/CPS taşması) bulunmadıkça 0'dan 9'a kadar olan sayılar yazıyla yazılır:
  - ✅ `"üç gün sonra"`, `"beş kişi"`, `"dokuz ay"`
  - ❌ `"3 gün sonra"`, `"5 kişi"`, `"9 ay"`
- **10 ve Üzeri Sayılar (Rakamla):** 10 dahil ve 10'dan büyük tüm sayılar rakamla yazılır:
  - ✅ `"10 yıldır"`, `"14 yaşında"`, `"25 kişi"`, `"150 metre"`
  - ❌ `"on yıldır"`, `"on dört yaşında"`, `"yirmi beş kişi"`
- **Ölçü, Ağırlık ve Para Birimleri:** Sayı değerine bakılmaksızın rakamla yazılır:
  - ✅ `"4 kilo"`, `"5 metre"`, `"10 dolar"`, `"%50"`
- **Deyimler ve Kalıplaşmış İfadeler (İstisna):** Sayı değeri ne olursa olsun her zaman yazıyla yazılır:
  - ✅ `"kırk kere söyledim"`, `"bin dereden su getirmek"`, `"on parmağında on marifet"`
  - ❌ `"40 kere söyledim"`, `"1000 dereden su getirmek"`
- **Geri Sayımlar ve Seri Sayımlar:** Seri halinde sayımlarda tutarlılık için yazıyla yazılır:
  - ✅ `"Üç, iki, bir, kayıt!"`
- **Binlik ve Ondalık Sayı Biçimi (TDK Standardı):**
  - **Binlik Ayırıcı:** Türkçede binlik basamaklar **nokta (.)** ile ayrılır (İngilizce virgül kullanılmaz): `4.000`, `10.500` (❌ `4,000`).
  - **Ondalık Ayırıcı:** Ondalık kısımlar **virgül (,)** ile ayrılır: `3,5 milyon`, `12,75` (❌ `3.5 milyon`).
  - **Büyük Sayılar:** Milyon, milyar gibi büyük sayılarda basamak yığılmasını önlemek için rakam + kelime kullanılır: `15 milyon`, `4 milyar`.

### 6. Alt Yazı Blok Süreleri (Minimum ve Maksimum Sınır)
- **Minimum Süre:** Bir alt yazı kartının ekranda kalma süresi **0.833 saniyeden (833 milisaniye / 20 kare)** kısa olamaz.
- **Maksimum Süre:** Bir alt yazı kartının ekranda kalma süresi **7.0 saniyeden (7000 milisaniye)** uzun olamaz.

### 7. ⚠️ SÜREYE MÜDAHALE YASAĞI (IRON RULE - DÜZELTME ASLA YAPILAMAZ)
- **KESİN KURAL:** Alt yazı süreleri (başlangıç ve bitiş zaman kodları) doğrudan video kurgusuna, konuşmacının dudak hareketlerine ve sahne kesimlerine bağlıdır.
- **YAPAY ZEKA ASLA SÜRE DÜZELTMESİ YAPMAZ:**
  - Kullanıcı **özellikle ve açıkça talep etse dahi**, süre uzatma, süre kısaltma, kartları ileri/geri kaydırma veya zaman kodlarını değiştirme işlemi **KESİNLİKLE YAPILAMAZ**.
  - Ajan/Skill, süre limit aşımı (< 0.833 sn veya > 7.0 sn) durumunda **YALNIZCA DENETİM RAPORU SUNAR**.
  - Süre düzeltmesi ve zamanlama (re-timing) tamamen kullanıcının kendi inisiyatifindedir ve kullanıcı tarafından yapılmalıdır.
  - Aşama 2'de düzeltilmiş SRT dosyası üretilirken blokların başlangıç ve bitiş zaman kodları (`00:00:00,000 --> 00:00:00,000`) **birebir korunur**.

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
2. **Blok Süresi Limit Aşımı:** 0.833 saniyeden kısa veya 7.0 saniyeden uzun süren kartlar (süreleri ve metinleriyle listelenir).
3. **CPL Sınırı Aşımı:** Kullanıcının seçtiği CPL sınırını (36 veya 42) aşan satır numaraları ve karakter sayıları.
4. **Anlatım Bozuklukları ve Eksiklik/Fazlalıklar:** Yüklem-özne uyumsuzlukları, tamlama yanlışları, pleonazmlar (*"ilk öncü"* vb.), motamot deyim kopyalamaları (*"şans vermek"* vb.), anglisizmler (*"özgür hissettiriyor"* vb.).
5. **Bağlam ve Çeviri Hataları:** Kaynak metin varsa orijinal konuşmayla uyuşmayan, anlamı tersine çeviren veya özneyi muğlaklaştıran yerler.
6. **Noktalama, Diyalog Tiresi ve İmla:** Tırnak içi nokta eksikleri, tek kalan diyalog tireleri, satır sonu boşlukları.
7. **Sayıların Yazımı Uyarıları:** 0-9 arası sayıların gereksiz rakamla yazılması, 10 ve üzeri sayıların harfle yazılması, binlik ve ondalık ayırıcı biçimlendirme hataları (`4,000` yerine `4.000`, `2.5` yerine `2,5`).

### Aşama 2: Temiz SRT Dosyası Üretme
Kullanıcı rapordaki düzeltmeleri onayladığında:
- Hatalar düzeltilir (metin, diyalog tireleri, tırnaklar, imla).
- Blok numaraları `1`den başlayarak sıralı hale getirilir.
- **Zaman Kodları Kesinlikle Korunur:** Blokların başlangıç ve bitiş zaman kodlarına (`00:00:00,000 --> 00:00:00,000`) kesinlikle dokunulmaz. Kullanıcı talep etse dahi otomatik süre uzatma veya kısaltma **yapılmaz**.
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
| `3 gün sonra` | 0-9 arası sayılar yer kısıtı yoksa yazıyla yazılır | `üç gün sonra` |
| `yirmi beş yaşında` | 10 ve üzeri sayılar (deyimler hariç) rakamla yazılır | `25 yaşında` |
| `4,000 kişi` | Türkçede binlik basamak ayırıcı noktadır (virgül değil) | `4.000 kişi` |
| `2.5 milyon` | Türkçede ondalık basamak ayırıcı virgüldür (nokta değil) | `2,5 milyon` |
| `40 kere söyledim` | Deyimler ve kalıplaşmış sözler yazıyla yazılır | `kırk kere söyledim` |
| Kart süresi < 0.833 sn | Minimum süre ihlali (yalnızca raporlanır, süreye müdahale edilmez) | Kullanıcı tarafından re-timing yapılmalı |
| Kart süresi > 7.0 sn | Maksimum süre ihlali (yalnızca raporlanır, süreye müdahale edilmez) | Kullanıcı tarafından bölünmeli |
