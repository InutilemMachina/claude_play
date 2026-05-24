"""
Fix 1_Jegyzet.md structure:
1. Cim a TOC ele (nem ala)
2. Targymutato -> Tartalomjegyzek
3. ### -> ## szint, #### -> ### szint, helyes szamozas
4. Hivatkozasjelzek a vegere
5. TOC ujrageneralas helyes anchorokkal
"""

import re
import os

FILEPATH = r"C:\Users\lasz\claude_play\Termografia_teszt_v2\1_het\1_Jegyzet.md"
FILEPATH_POSIX = "/sessions/gifted-epic-edison/mnt/claude_play/Termografia_teszt_v2/1_het/1_Jegyzet.md"

with open(FILEPATH_POSIX, 'r', encoding='utf-8') as f:
    content = f.read()

# --- 1. YAML frontmatter kiemelese ---
fm_match = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
frontmatter = fm_match.group(1) if fm_match else ""
rest = content[len(frontmatter):]

# --- 2. Cim es alcim kiemelese ---
title_match = re.search(r'^(# 1_Jegyzet[^\n]+)', rest, re.MULTILINE)
title_line = title_match.group(1) if title_match else "# 1_Jegyzet -- Infravörös Termográfia"

subtitle_match = re.search(r'^(_Forrás:[^\n]+_)', rest, re.MULTILINE)
subtitle_line = subtitle_match.group(1) if subtitle_match else ""

# --- 3. Body kiemelese (az elso szamozott fejezettol) ---
body_match = re.search(r'^# \d+\.', rest, re.MULTILINE)
body = rest[body_match.start():] if body_match else rest

# --- 4. Fejlec szintek javitasa (exact match soronkent) ---
heading_map = {
    # 1. fejezet
    "### Alkalmazási területek":                              "## 1.1. Alkalmazási területek",
    "### Fizikai alapelvek":                                  "## 1.2. Fizikai alapelvek",
    "### Leglényegesebb jellemzők és paraméterek":            "## 1.3. Leglényegesebb jellemzők és paraméterek",
    # 2. fejezet
    "### 1. Stefan–Boltzmann-törvény":                   "## 2.1. Stefan–Boltzmann-törvény",
    "### 2. Planck-féle sugárzási törvény":                   "## 2.2. Planck-féle sugárzási törvény",
    "### 3. Wien-féle eltolódási törvény":                    "## 2.3. Wien-féle eltolódási törvény",
    "### 4. Kirchhoff-féle sugárzási törvény":                "## 2.4. Kirchhoff-féle sugárzási törvény",
    "### Összefoglaló táblázat":                              "## 2.5. Összefoglaló táblázat",
    # 3. fejezet
    "### Hőkamerás mérőeszközök típusai":                     "## 3.1. Hőkamerás mérőeszközök típusai",
    "#### 1. Hűtött (Quantum) vs. Hűtetlen (Thermal) detektorok": "### 3.1.1. Hűtött (Quantum) vs. Hűtetlen (Thermal) detektorok",
    "#### 2. Spektrális tartományok":                         "### 3.1.2. Spektrális tartományok",
    "### A mérési pontosságot befolyásoló tényezők":          "## 3.2. A mérési pontosságot befolyásoló tényezők",
    "#### 1. Emissziófüggőség":                               "### 3.2.1. Emissziófüggőség",
    "#### 2. Reflexió (Visszaverődés)":                       "### 3.2.2. Reflexió (Visszaverődés)",
    "#### 3. Kalibráció és szoftveres korrekció":             "### 3.2.3. Kalibráció és szoftveres korrekció",
    "### Összefoglaló a mérést befolyásoló adatokról":        "## 3.3. Összefoglaló a mérést befolyásoló adatokról",
    # 4. fejezet
    "### 1. Általános karbantartás és állapotfüggő diagnosztika": "## 4.1. Általános karbantartás és állapotfüggő diagnosztika",
    "### 2. Villamosipari alkalmazások":                      "## 4.2. Villamosipari alkalmazások",
    "### 3. Gépészeti diagnosztika":                          "## 4.3. Gépészeti diagnosztika",
    "### 4. Épületdiagnosztika és építészet":                 "## 4.4. Épületdiagnosztika és építészet",
    "### Összefoglaló táblázat a diagnosztikai példákról":    "## 4.5. Összefoglaló táblázat a diagnosztikai példákról",
}

matched = 0
for old, new in heading_map.items():
    new_body, n = re.subn(r'^' + re.escape(old) + r'$', new, body, flags=re.MULTILINE)
    if n > 0:
        matched += n
        body = new_body

print(f"  Fejlec szintek javitva: {matched}/{len(heading_map)}")

# --- 5. TOC ujrageneralas ---
def make_anchor(text):
    """GFM-stilus anchor: kisbetu, pontok es spec. karakterek torlesevel."""
    t = text.lower()
    t = t.replace('.', '')         # 1.1. → 11
    t = re.sub(r'\s+', '-', t)    # szokozok → -
    t = re.sub(r'[^\w\-]', '', t, flags=re.UNICODE)  # spec. karakterek
    t = re.sub(r'-+', '-', t).strip('-')
    return '#' + t

toc_lines = []
for line in body.split('\n'):
    m = re.match(r'^(#{1,3}) (.+)$', line)
    if m:
        hashes = m.group(1)
        heading_text = m.group(2)
        level = len(hashes)
        anchor = make_anchor(heading_text)
        indent = '  ' * (level - 1)
        toc_lines.append(f"{indent}- [{heading_text}]({anchor})")

print(f"  TOC bejegyzesek: {len(toc_lines)}")

# --- 6. Hivatkozasjegyzek ---
hivatkozas = """\n# Hivatkozásjegyzék

[1] D1 Lecture Notes -- Termografia. Előadásjegyzet, kézirat.

[2] FLIR Systems, *IR Thermography: How It Works*, FLIR Systems Inc., 2024.

[3] FLIR Systems, *Infrared Energy, Emissivity, Reflection & Transmission Guide*, FLIR Systems Inc.

[4] Gy. Haraszti, *Termografiai vizsgalatok*, 2013.

[5] M. Reszler, "Hőtérkép-készítés a karbantartó szemszögéből," 2010.

[6] Wikipedia, "Emissivity," *Wikipedia, The Free Encyclopedia*, 2026. [Online]. Elérhető: https://en.wikipedia.org/wiki/Emissivity

[7] Thermo Delta Kft., "Mikrobolométer technológia," 2026. [Online]. Elérhető: https://thermodelta.hu

[8] IRExpert, "Hőkamerák villamos szakembereknek," 2026. [Online]. Elérhető: https://irexpert.hu
"""

# --- 7. Vegso dokumentum osszerakasa ---
new_toc_block = "# Tartalomjegyzék\n\n" + '\n'.join(toc_lines) + "\n\n---\n"

output = (
    frontmatter
    + "\n"
    + title_line + "\n\n"
    + subtitle_line + "\n\n"
    + new_toc_block + "\n"
    + body.lstrip('\n')
    + hivatkozas
)

with open(FILEPATH_POSIX, 'w', encoding='utf-8') as f:
    f.write(output)

print("✅ Kész -- 1_Jegyzet.md felulirva")
