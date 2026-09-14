---
name: dubbing-translator-french-to-turkish
description: >-
  Provides a structured methodology for translating film scripts/dialogues
  from French to Turkish for dubbing (lip-sync). Focuses on spoken syllable counts,
  front/back rounded and nasal vowels, and natural spoken Turkish flow.
---

# French-to-Turkish Dubbing & Lip-Sync Translation Guide

## Overview
This skill defines the engineering methodology and workflow for translating film scripts and dialogues from French to Turkish for dubbing (lip-sync) purposes. French and Turkish are both syllable-timed languages, but differences in agglutination, pronoun dropping, silent spelling, and nasal vowels present unique synchronization challenges. This guide ensures that translations match speaking duration (spoken syllable counts) and mouth shapes/visemes without sacrificing natural spoken flow.

## Dependencies
* **No External Agents/AIs:** **CRITICAL:** Do not use, invoke, or delegate any task to another AI, LLM API, or external autonomous agent running on the user's computer. Perform all translations, syllable evaluations, and lip-sync validations using only your own intelligence, reasoning, and context.

## Quick Start
To translate a dialogue line:
1. Calculate the spoken (phonetic) French syllable count (ignoring silent letters and accounting for elisions/liaisons).
2. Note onset and offset mouth shapes, paying special attention to rounded vowels (Ü, Ö, U) and open nasals.
3. Draft a natural Turkish translation matching the spoken syllable count ($N_{TR} = N_{FR} \pm 1$).
4. Maximize Turkish pronoun dropping (pro-drop) and short suffixes to maintain the target length.
5. Remove robotic filler words.

## Workflow

### 1. Phonetic Parsing & Segmenting
* Read the French script. Remove parenthetical scene directions (e.g., `(en riant)`, `(à part)`).
* Segment the dialogue by sentence boundaries.
* Compute the **spoken syllable count** by ignoring silent letters and accounting for liaison/elision.

### 2. Viseme Extraction
Detect critical visual markers:
* **Onset:** Check if the French sentence begins with a rounded vowel (/u/, /y/, /ø/, /œ/) or a bilabial/labiodental consonant (P, B, M, F, V).
* **Offset:** Detect whether the mouth closes (bilabial) or remains open (nasal, open vowel) at the end of the sentence.

### 3. Pro-Drop and Agglutination Optimization
Generate Turkish translation candidates:
* Drop subject pronouns (*ben, sen, o...*) unless emphasis is strictly required.
* Choose shorter verb suffixes (e.g., Aorist *-r* or Present Continuous *-yor* vs. past/future forms) to match short French syllables.
* Use synonyms to adjust syllable count (e.g., *“oui”* -> *“evet”* [2] or *“hıhı”* [2] or *“ya”* [1]).

### 4. Iterative Validation & Refinement
Verify the translation candidate against:
* **Syllable count match:** Turkish syllable count must be within $\pm 1$ of the spoken French syllable count.
* **Viseme alignment:** Onset and offset lip shapes must match:
  * **Front Rounded Vowels:** Align French /y/, /ø/, and /œ/ to Turkish **Ü** and **Ö** to preserve puckered lip shapes.
  * **Back Rounded Vowels:** Align French /u/ directly to Turkish **U**.
  * **Nasal Vowels:** For French open/nasal endings (/ɑ̃/, /ɛ̃/, /ɔ̃/, /œ̃/), end the Turkish sentence with an open vowel (A, E, O) or soft nasal (N), avoiding hard bilabial closures (M, P, B).
  * **Bilabials:** Match French P, B, M with Turkish P, B, M.
* **Robotic Filter:** Ensure no awkward syntax or artificial Turkish words are added to match the pacing.

---

## 5. Prompt Template for the French-to-Turkish Translation Agent

```markdown
You are a professional film dubbing and lip-sync specialist translating from French to Turkish.

Source French Text: {french_sentence}
Target Sync Metadata:
- Spoken French Syllables: {spoken_syllables} (Counted phonetically, ignoring silent letters)
- Onset Viseme: {onset_viseme} (e.g., Bilabial [P/B/M], Rounded Vowel [U/Ü/Ö], Open [A/E])
- Offset Viseme: {offset_viseme}

Instructions:
1. Translate to 100% natural, colloquial Turkish suitable for the film's genre and era.
2. Prioritize spoken syllable count and duration. The Turkish translation MUST have exactly {spoken_syllables} (tolerated: +/- 1) spoken syllables.
3. Match the visual lip movements:
   - If Onset is 'Bilabial' or 'Rounded Vowel', begin the Turkish sentence with a matching lip shape (B, P, M, U, Ü, Ö).
   - If Offset is 'Open' or 'Nasal', do not end the Turkish sentence with a closed-lip consonant (M, P, B).
4. Utilize Turkish pro-drop rules (drop pronouns) and agglutinative suffixes to condense the text naturally. Avoid filler words.

Return your response in the following JSON format:
{
  "french": "{french_sentence}",
  "turkish": "your_translation_here"
}
```

---

## 6. Case Studies: French vs. Turkish Dubbing Sync

| French Sentence | Spoken Syllables | Incorrect (Literal / Too Long) | Correct (Duration & Lip-Sync Match) | Rationale |
| :--- | :---: | :--- | :--- | :--- |
| **“Tu as vu ?”** (spoken: /ty.a.vy/) | 3 | *“Sen gördün mü ?”* (4 syllables) | *“Gördün mü ?”* (3 syllables) | Dropping the subject pronoun *“Sen”* perfectly matches the 3-syllable count. The onset starts with a dental/rounded shape. |
| **“Je ne sais pas.”** (casual: /ʃe.pa/) | 2 | *“Ben bunu bilmiyorum.”* (7 syllables) | *“Bilmem.”* (2 syllables) | In casual French speech, *“Je ne sais pas”* is contracted to 2 syllables. *“Bilmem”* matches the 2-syllable rhythm and starts with a bilabial (/b/), aligning with the visual closure of /ʃ/. |
| **“Pourquoi tu mens ?”** (spoken: /puʁ.kwa.ty.mɑ̃/) | 4 | *“Neden bana yalan söylüyorsun ?”* (10 syllables) | *“Niye yalan ?”* (4 syllables) | The literal version is far too long. *“Niye yalan ?”* matches the 4 spoken syllables and ends with /n/ which keeps the mouth open, matching the French nasal /ɑ̃/ in *“mens”*. |
| **“C'est impossible !”** (spoken: /sɛ.tɛ̃.po.sibl/) | 4 | *“Bu kesinlikle imkansız bir durum !”* (11 syllables) | *“İmkansız bu !”* (4 syllables) | Condenses the phrase to match the 4 spoken syllables. Starts with /i/ (spread lips) and ends with /u/ (rounded), matching the visual profile of the French source. |
| **“Mais oui !”** (spoken: /mɛ.wi/) | 2 | *“Evet ama öyle !”* (6 syllables) | *“Tabii !”* or *“Aynen !”* (2 syllables) | Matches the 2-syllable length and starts with a bilabial/dental onset, fitting the mouth shape of /m/ in *“Mais”*. |

## Common Mistakes
* **Counting Written Syllables:** Attempting to count French syllables based on written text rather than spoken phonetics (e.g. counting silent letters/e's).
* **Adding Pronouns:** Retaining Turkish pronouns (*ben, sen, o...*), which inflates the syllable count unnecessarily.
* **Mismatched Nasal Vowel Offsets:** Ending with a closed bilabial (like *“bulamam”*) when the French speaker's mouth remains wide open on a nasal vowel ending.
