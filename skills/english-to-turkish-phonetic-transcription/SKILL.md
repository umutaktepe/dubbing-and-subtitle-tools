---
name: english-to-turkish-phonetic-transcription
description: >-
  Converts English names, place names, brand names, and uncommon foreign words
  into their Turkish phonetic equivalents for dubbing and voiceover scripts.
  Uses IPA-based systematic rules (General American pronunciation) so that a
  Turkish voice actor can read the script and pronounce every foreign word
  correctly without needing to know English. Supports both single-word lookup
  and batch file processing. Preserves Turkish words and character tags.
---

# English-to-Turkish Phonetic Transcription for Dubbing

## Overview

This skill provides a systematic, IPA-based methodology for converting English words (names, places, brands, technical terms) into **phonetic Turkish spelling** so that a Turkish dubbing artist can read the script and pronounce every foreign word correctly.

**Standard:** General American English (GenAm) pronunciation — the standard accent of Hollywood film and television.

**Scope of conversion:**
- Person names (first names, surnames, nicknames)
- Place names (cities, states, countries, streets)
- Brand / product names
- Agency & institution acronyms (e.g. FBI -> EfBiAy, CIA -> SiAyEy, DEA -> DiİEy)
- Uncommon foreign words that haven't been naturalised into Turkish

**What NOT to convert:**
- Words already naturalised into Turkish (ambulans, sigorta, maraton, palyaço…)
- Turkish words that coincidentally look like English words
- Character identifier tags (e.g. `[EVE]`, `GEORGIA:`)

---

## Dependencies

* **No External Agents/AIs:** Do not delegate any phonetic transcription task to another AI, API, or external tool. Apply the IPA mapping rules below using your own reasoning and linguistic knowledge.

---

## Core Rules: IPA → Turkish Letter Mapping

### Consonants

| IPA | English Sound | Turkish Letter(s) | Example (EN → TR) |
|:---:|:---|:---:|:---|
| /dʒ/ | **J**, soft **G** (judge, George) | **C** | John → **Con**, George → **Corc**, Jesse → **Cesi** |
| /tʃ/ | **CH** (church, Richard) | **Ç** | Charlie → **Çarli**, Richard → **Riçırd** |
| /ʃ/ | **SH** (ship, Washington) | **Ş** | Shawn → **Şon**, Washington → **Vaşingtın** |
| /ʒ/ | **ZH** (measure, vision) | **J** | Treasure → **Trejır** |
| /θ/ | **TH** voiceless (think, math) | **T** | Martha → **Marta**, Seth → **Set** |
| /ð/ | **TH** voiced (the, rather) | **D** | Rather → **Redır** |
| /w/ | **W** (water, Wayne) | **V** | Wayne → **Veyn**, Walter → **Voltır**, William → **Vilyım** |
| /ŋ/ | **NG** (king, walking) | **NG** | King → **King**, Long → **Long** |
| /r/ | **R** (AmE rhotic) | **R** | Robert → **Robert**, Harris → **Heris** |
| /h/ | **H** (home, Henry) | **H** | Henry → **Henri**, Howard → **Havırd** |
| /j/ | **Y** (yes, you) | **Y** | York → **York**, Yale → **Yeyl** |
| /k/ | **K**, hard **C** (cat, key) | **K** | Kevin → **Kevin**, Carl → **Karl** |
| /s/ | **S**, soft **C** (sun, city) | **S** | Steve → **Stiv**, City → **Siti** |
| /z/ | **Z**, **S** (zoo, rose) | **Z** | Rose → **Roz** |
| /p/ | **P** | **P** | Paul → **Pol**, Peter → **Pitır** |
| /b/ | **B** | **B** | Bob → **Bob**, Buck → **Bak** |
| /t/ | **T** | **T** | Tom → **Tom**, Matt → **Met** |
| /d/ | **D** | **D** | David → **Deyvid**, Duke → **Dyuk** |
| /f/ | **F** | **F** | Frank → **Frenk** |
| /v/ | **V** | **V** | Victor → **Viktır** |
| /m/ | **M** | **M** | Mike → **Mayk** |
| /n/ | **N** | **N** | Nancy → **Nensi** |
| /l/ | **L** | **L** | Larry → **Leri** |

### Vowels & Diphthongs

| IPA | English Sound | Turkish Letter(s) | Example (EN → TR) |
|:---:|:---|:---:|:---|
| /æ/ | short A (cat, pat, man) | **E** | Pat → **Pet**, Matt → **Met**, Maddy → **Medi** |
| /ɑː/ | broad A (father, car, mark) | **A** | Mark → **Mark**, Clark → **Klark** |
| /ʌ/ | short U (but, cup, luck) | **A** | Buck → **Bak**, Hutch → **Haç** |
| /ɜːr/ | ER (her, bird, Turner) | **ÖR** | Turner → **Törner**, Herbert → **Hörbırt** |
| /ər/ | unstressed schwa+R (water, Peter) | **IR / ır** | Peter → **Pitır**, Walter → **Voltır** |
| /ə/ | schwa (about, sofa) | **I / ı** (or dropped) | Madeline → **Medılin**, Jonathan → **Conatın** |
| /ɪ/ | short I (bit, sit, Kim) | **İ** | Kim → **Kim**, Bill → **Bil** |
| /iː/ | long EE (see, Eve, Lee) | **İ** | Eve → **İv**, Lee → **Li**, Steve → **Stiv** |
| /eɪ/ | AY diphthong (day, Wayne, late) | **EY** | Wayne → **Veyn**, Day → **Dey**, Kate → **Keyt** |
| /aɪ/ | long I (like, Mike, night) | **AY** | Mike → **Mayk**, Lyme → **Laym**, Wright → **Rayt** |
| /oʊ/ | long O (go, Joe, home) | **O** | Joe → **Co**, Home → **Hom**, Moore → **Mur** |
| /uː/ | long OO (food, Luke, Duke) | **U** | Duke → **Dyuk**, Luke → **Luk**, June → **Cun** |
| /ʊ/ | short OO (book, good) | **U** | Brooklyn → **Bruklin** |
| /ɔː/ | AW (law, Paul, all) | **O** | Paul → **Pol**, Wall → **Vol**, George → **Corc** |
| /ɔɪ/ | OY (boy, joy) | **OY** | Joy → **Coy**, Lloyd → **Loyd** |
| /aʊ/ | OW (how, Howard, town) | **AV** | Howard → **Havırd**, Town → **Tavn** |

### Special Combinations

| Pattern | Rule | Example |
|:---|:---|:---|
| Silent letters (k in know, b in dumb) | Drop them | Knight → **Nayt**, Dumb → **Dam** |
| -TION / -SION | **-ŞIN** | Station → **Steyşın**, Vision → **Vijın** |
| -TURE | **-ÇIR** | Culture → **Kalçır** |
| PH | **F** | Philip → **Filip**, Phone → **Fon** |
| QU | **KV** or **K** | Queen → **Kvin** |
| X (= /ks/) | **KS** | Alex → **Eleks**, Max → **Meks** |
| Double consonants | Reduce to single | Bill → **Bil**, Matt → **Met** |
| Final -LE (after consonant) | **-IL** | Apple → **Epıl** |
| Final -ER | **-IR** | Peter → **Pitır**, Barber → **Barbır** |
| Final -LY | **-Lİ** | Beverly → **Beverli** |

---

## Collision Avoidance: Protecting Turkish Words

When processing a translated Turkish script, English names may collide with existing Turkish words. This section defines how to avoid corrupting Turkish text.

### Critical Rules

1. **Use regex word boundaries** (`\b`) for replacements. Never use naive `str.replace()` for names that are substrings of Turkish words.
   - ❌ `"Eve"` inside `"Evet"` (Turkish for "yes") → would produce `"İvt"` — WRONG
   - ✅ `\bEve\b` matches only the standalone word `Eve`

2. **Case-sensitive matching.** Turkish words in mid-sentence are lowercase; English names are capitalised.
   - `eve` (lowercase) = Turkish dative of "ev" (home) → DO NOT TOUCH
   - `Eve` (capitalised) = English name → convert to `İv`

3. **Process multi-word phrases FIRST**, then single words (longest to shortest).
   - Replace `"John Wayne"` → `"Con Veyn"` before replacing `"John"` alone
   - Replace `"Evie"` → `"İvi"` before replacing `"Eve"` → `"İv"`
   - Replace `"Bucky"` → `"Baki"` before replacing `"Buck"` → `"Bak"`

4. **Preserve structural tags.** Character identifiers must never be modified:
   - `[EVE]` (square-bracket tags) → keep as-is
   - `EVE:` (colon-style at line start) → keep as-is
   - `EVE` (all-caps at line start before tab) → keep as-is
   - Only the dialogue text (after the tag delimiter) is subject to conversion.

5. **Context-aware exceptions.** Some names produce Turkish words when converted:
   - `Buck` → `Bak` (= Turkish "look") — acceptable, context disambiguates
   - `Pat` → `Pet` (= Turkish PET plastic) — acceptable, capitalised as name
   - `Eve` → `İv` — but if `Eve` means Turkish "to home" in context (e.g., answer to "Where?"), leave it

### Known Collision Pairs

| English Name | Turkish Phonetic | Turkish Word Collision | Resolution |
|:---|:---|:---|:---|
| Eve | İv | `eve` (to home), `Evet` (yes) | Use `\bEve\b` regex; never match inside `Evet` |
| Buck | Bak | `bak` (look) | Acceptable — capitalised as name in context |
| Pat | Pet | `pet` (PET plastic) | Acceptable — capitalised as name |
| Joe | Co | — | No collision |
| Lou | Lu | — | No collision |

---

## Workflow

### Mode A: Single Word / Name Transcription

When the user provides a single English name or word:

1. **Identify the IPA pronunciation** using General American phonetics.
2. **Apply the IPA → Turkish mapping table** phoneme by phoneme.
3. **Handle stress and syllable structure:**
   - Stressed syllables retain full vowels.
   - Unstressed syllables use schwa → `ı` or vowel is dropped if natural.
4. **Return the phonetic Turkish spelling** with a brief IPA breakdown.

**Example:**

```
Input:  "Elizabeth"
IPA:    /ɪˈlɪzəbəθ/
Step 1: /ɪ/ → İ, /l/ → L, /ɪ/ → İ, /z/ → Z, /ə/ → ı, /b/ → B, /ə/ → ı, /θ/ → T
Step 2: İ-Lİ-Zı-BıT → İlizıbıt
Output: İlizıbıt
```

### Mode B: Batch File Transcription

When the user provides a full dialogue/script file:

1. **Load the source file** (MD, TXT, XLSX).
2. **Detect the format:**
   - Tab-separated: `[CHARACTER]\t{dialogue}`
   - Colon-separated: `CHARACTER: {dialogue}`
   - All-caps at line start: `CHARACTER {dialogue}`
3. **Split each line** into tag (preserved) and dialogue (to be processed).
4. **Scan the dialogue text** for foreign names/words.
5. **Build a replacement dictionary:**
   - Multi-word phrases first (longest first)
   - Then single words (longest first)
   - Apply IPA → Turkish mapping for each entry
6. **Apply replacements** using regex word boundaries (`\b`).
7. **Manually review known collision cases** (Eve/Evet, etc.).
8. **Write the output** to a new file (e.g., `{filename}_phonetic.md`).

**Important:** Always keep the original file intact. Write output to a NEW file.

---

## Reference Table: Common English Names

### Male First Names

| English | IPA (GenAm) | Turkish Phonetic |
|:---|:---|:---|
| John | /dʒɑːn/ | **Con** |
| James | /dʒeɪmz/ | **Ceymz** |
| George | /dʒɔːrdʒ/ | **Corc** |
| William | /ˈwɪljəm/ | **Vilyım** |
| Michael | /ˈmaɪkəl/ | **Maykıl** |
| David | /ˈdeɪvɪd/ | **Deyvid** |
| Robert | /ˈrɑːbərt/ | **Robırt** |
| Richard | /ˈrɪtʃərd/ | **Riçırd** |
| Charles | /tʃɑːrlz/ | **Çarlz** |
| Thomas | /ˈtɑːməs/ | **Tamıs** |
| Joseph | /ˈdʒoʊzəf/ | **Cozıf** |
| Henry | /ˈhɛnri/ | **Henri** |
| Edward | /ˈɛdwərd/ | **Edvırd** |
| Jack | /dʒæk/ | **Cek** |
| Steve | /stiːv/ | **Stiv** |
| Kevin | /ˈkɛvɪn/ | **Kevin** |
| Patrick | /ˈpætrɪk/ | **Petrik** |
| Frank | /fræŋk/ | **Frenk** |
| Jesse | /ˈdʒɛsi/ | **Cesi** |
| Duke | /djuːk/ | **Dyuk** |

### Female First Names

| English | IPA (GenAm) | Turkish Phonetic |
|:---|:---|:---|
| Eve | /iːv/ | **İv** |
| Georgia | /ˈdʒɔːrdʒə/ | **Corciya** |
| Elizabeth | /ɪˈlɪzəbəθ/ | **İlizıbıt** |
| Jessica | /ˈdʒɛsɪkə/ | **Cesika** |
| Catherine | /ˈkæθrɪn/ | **Ketrin** |
| Dorothy | /ˈdɔːrəθi/ | **Dorıti** |
| Margaret | /ˈmɑːrɡrɪt/ | **Margrit** |
| Virginia | /vərˈdʒɪniə/ | **Vırciniya** |
| Patricia | /pəˈtrɪʃə/ | **Pıtrişa** |
| Nancy | /ˈnænsi/ | **Nensi** |
| Audrey | /ˈɔːdri/ | **Odri** |
| Madeline | /ˈmædəlɪn/ | **Medılin** |
| Juliana | /ˌdʒuːliˈɑːnə/ | **Culiyana** |
| Donna | /ˈdɑːnə/ | **Dona** |
| Olivia | /oʊˈlɪviə/ | **Olivya** |

### Surnames

| English | IPA (GenAm) | Turkish Phonetic |
|:---|:---|:---|
| Smith | /smɪθ/ | **Smit** |
| Johnson | /ˈdʒɑːnsən/ | **Consın** |
| Washington | /ˈwɑːʃɪŋtən/ | **Vaşingtın** |
| Kennedy | /ˈkɛnədi/ | **Kenedi** |
| Mitchell | /ˈmɪtʃəl/ | **Miçıl** |
| Turner | /ˈtɜːrnər/ | **Törner** |
| Wright | /raɪt/ | **Rayt** |
| Moore | /mʊr/ | **Mur** |
| Campbell | /ˈkæmbəl/ | **Kembıl** |
| McDonald | /məkˈdɑːnəld/ | **MıkDonıld** |

### Place Names

| English | IPA (GenAm) | Turkish Phonetic |
|:---|:---|:---|
| New York | /njuː jɔːrk/ | **Nyu York** |
| Los Angeles | /lɒs ˈændʒəliːz/ | **Los Ancelıs** |
| Hollywood | /ˈhɑːliwʊd/ | **Halivud** |
| Washington | /ˈwɑːʃɪŋtən/ | **Vaşingtın** |
| San Francisco | /sæn frənˈsɪskoʊ/ | **Sen Frensisko** |
| Chicago | /ʃɪˈkɑːɡoʊ/ | **Şikago** |
| Manhattan | /mænˈhætn/ | **Menhetn** |
| Broadway | /ˈbrɔːdweɪ/ | **Brodvey** |
| Harvard | /ˈhɑːrvərd/ | **Harvırd** |
| Bronx | /brɑːŋks/ | **Bronks** |

### Brands & Products

| English | Turkish Phonetic |
|:---|:---|
| Barney's | **Barni's** |
| Mercedes | **Mersedes** |
| Lamborghini | **Lamborgini** |
| Vogue | **Vog** |

### Acronyms & Agencies

| English | Spoken As | Turkish Phonetic |
|:---|:---|:---|
| FBI | /ˌɛf.biːˈaɪ/ | **EfBiAy** |
| CIA | /ˌsiː.aɪˈeɪ/ | **SiAyEy** |
| DEA | /ˌdiː.iːˈeɪ/ | **DiİEy** |
| NSA | /ˌɛn.ɛsˈeɪ/ | **EnEsEy** |
| NYPD | /ˌɛn.waɪ.piːˈdiː/ | **EnVayPiDi** |
| LAPD | /ˌɛl.eɪ.piːˈdiː/ | **ElEyPiDi** |
| SWAT | /swɑːt/ | **Svat** |
| CEO | /ˌsiː.iːˈoʊ/ | **SiİO** |
| VIP | /ˌviː.aɪˈpiː/ | **ViAyPi** |

---

## Common Mistakes

1. **Translating from written English, not spoken English.** English spelling is notoriously irregular. Always derive the Turkish phonetic from the *spoken pronunciation* (IPA), not the written letters.
   - ❌ `Knight` → "Knayıt" (reading the K)
   - ✅ `Knight` /naɪt/ → **Nayt**

2. **Corrupting Turkish words.** Naively replacing `"Eve"` inside `"Evet"` yields `"İvt"`. Always use word-boundary-aware matching.
   - ❌ `str.replace("Eve", "İv")` → turns "Evet" into "İvt"
   - ✅ `re.sub(r"\bEve\b", "İv", text)` → "Evet" stays intact

3. **Using a single Turkish letter for schwa (/ə/) everywhere.** The schwa maps to different Turkish vowels depending on consonant environment:
   - After back consonants: use **ı** (Madeline → Med**ı**lin)
   - After front consonants: use **i** or **e** may also work
   - Sometimes dropped entirely for naturalness

4. **Breaking multi-word names.** Process compound names as a unit before processing individual words.
   - ❌ Replace "John" → "Con" and "Wayne" → "Veyn" separately (might miss "John Wayne" as compound)
   - ✅ Replace "John Wayne" → "Con Veyn" first, then handle remaining "John" or "Wayne" individually

5. **Modifying character tags.** Never change text inside structural markers like `[EVE]`, `GEORGIA:`, or all-caps line-start identifiers. Only process the dialogue portion.

6. **Ignoring stress patterns.** English stress determines which vowels are full vs. reduced (schwa). Stressed syllables get clear Turkish vowels; unstressed syllables get **ı/i** or the vowel is dropped.
   - `Elizabeth` /ɪˈLɪZ.ə.bəθ/ — stress on 2nd syllable → İl**i**zıbıt (not İlizabet)
