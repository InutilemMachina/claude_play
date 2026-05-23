# Tantárgyfejlesztési Projekt Blueprint
## 13 hetes tananyag — Cowork pipeline

---

## MAPPASTRUKTÚRA

```
tantargy_nev/                          ← ez a Cowork munkamappa gyökere
│
├── .claude/
│   ├── instructions.md                ← Cowork mappa-szintű utasítások
│   └── skills/
│       ├── minerU/
│       │   └── SKILL.md
│       ├── md_to_pptx/
│       │   └── SKILL.md
│       └── kerdesbank/
│           └── SKILL.md
│
├── _meta/                             ← projekt "idegrendszere"
│   ├── project_status.md              ← session memória (minden session elején beadod)
│   ├── tematika.md                    ← 13 hetes terv (az "igazság forrása")
│   ├── style_guide.md                 ← MD sablon + tartalmi szabványok
│   ├── decisions.md                   ← metodológiai döntések naplója
│   ├── pipeline_log.txt               ← auto-generált futásnapló
│   └── backups/                       ← retroaktív módosítás előtti mentések
│
├── _scripts/                          ← Python scriptek
│   ├── process_all.py                 ← master pipeline orchestrator
│   ├── md_audit.py                    ← style guide compliance checker
│   ├── retroactive_update.py          ← schema migration script
│   ├── pptx_generator.py              ← MD → PPTX konverter
│   └── kerdesbank_gen.py              ← kérdésbank generátor
│
├── 00_inputs/                         ← nyers inputok (érintetlen)
│   ├── w01/
│   │   ├── scan_01.pdf
│   │   └── scan_02.pdf
│   ├── w02/
│   └── ... (w03–w13)
│
├── 01_processed/                      ← MinerU kimenet
│   ├── w01/
│   │   ├── text_raw.md                ← MinerU nyers szöveg
│   │   └── figures/
│   │       ├── fig_001.png
│   │       └── fig_002.png
│   ├── w02/
│   └── ... (w03–w13)
│
├── 02_notes/                          ← NotebookLM + szerkesztett MD jegyzetek
│   ├── w01/
│   │   ├── notes.md                   ← fő tartalom (style guide szerint)
│   │   └── notebooklm_queries.md      ← milyen kérdéseket tettél fel NLM-nek
│   ├── w02/
│   └── ... (w03–w13)
│
├── 03_figures/                        ← Python-ban reprodukált ábrák
│   ├── w01/
│   │   ├── fig_01_pressure_curve.py   ← script
│   │   └── fig_01_pressure_curve.png  ← generált output
│   ├── w02/
│   └── ... (w03–w13)
│
├── 04_pptx/                           ← Generált prezentációk
│   ├── w01_slides.pptx
│   ├── w02_slides.pptx
│   └── ... (w03–w13)
│
├── 05_kerdesbank/                     ← Kérdésbank
│   ├── w01_questions.md
│   ├── w02_questions.md
│   └── master_bank.md                 ← összesített kérdésbank
│
└── 06_final/                          ← Végleges, lektorált anyagok
    ├── w01/
    └── ... (w03–w13)
```

---

## META FÁJLOK TARTALMA

### _meta/style_guide.md (sablon — EZT VÁLTOZTATOD, ha metodológia változik)

```markdown
# Style Guide — MD Jegyzetek Sablon

## Kötelező szekciók (ebben a sorrendben)

### 1. Fejléc
- Hét száma, cím, dátum
- Státusz: [DRAFT / REVIEW / FINAL]

### 2. Tanulási célok
- 3-5 mérhető cél (ige + tartalom)
- Példa: "A hallgató képes lesz megkülönböztetni X-t Y-tól"

### 3. Főszöveg
- Max. 800 szó/szekció
- Ábrákra hivatkozás: ![leírás](../../03_figures/wXX/fig_XX_nev.png)
- Fogalmak kiemelése: **félkövér**

### 4. Kulcsfogalmak
- Glosszárium formában: **Fogalom:** definíció

### 5. Összefoglaló szövegdoboz
:::info Fejezet összefoglalója
3-5 mondatban a fejezet lényege.
**Kulcsgondolat:** [egy mondat]
:::

### 6. Kérdések (önellenőrzéshez)
- 3-5 kérdés, növekvő nehézséggel

## Tipográfiai szabályok
- H2 (##) = fő szekció
- H3 (###) = alszekció
- Kódblokk csak valódi kódhoz
- Táblázat csak összehasonlításhoz
```

### _meta/tematika.md (13 hetes terv)

```markdown
# Tematika — [Tantárgy neve]

| Hét | Téma | Kulcsfogalmak | Előfeltétel | Státusz |
|-----|------|---------------|-------------|---------|
| 01  | Bevezetés | ... | — | DRAFT |
| 02  | ... | ... | w01 | TODO |
| ... | | | | |
| 13  | Összefoglalás | — | w01–w12 | TODO |

## Pipeline státusz összesítő
| Hét | Input | Processed | Notes | Figures | PPTX | Kérdések | Final |
|-----|-------|-----------|-------|---------|------|----------|-------|
| 01  | ✅ | ✅ | 🔄 | ❌ | ❌ | ❌ | ❌ |
| 02  | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
```

---

## SCRIPTEK

### _scripts/process_all.py — Master Pipeline Orchestrator

```python
#!/usr/bin/env python3
"""
Master pipeline script — tantárgyfejlesztés
Futtatás: python _scripts/process_all.py --week 01 --stage all
          python _scripts/process_all.py --week all --stage audit --dry-run
"""

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime

STAGES = ["mineru", "audit", "figures", "pptx", "kerdesbank"]

STAGE_SCRIPTS = {
    "mineru":     "python _scripts/mineru_batch.py",
    "audit":      "python _scripts/md_audit.py",
    "figures":    "python _scripts/figure_runner.py",
    "pptx":       "python _scripts/pptx_generator.py",
    "kerdesbank": "python _scripts/kerdesbank_gen.py",
}

def run_stage(stage: str, week: str, dry_run: bool = False) -> bool:
    cmd = f"{STAGE_SCRIPTS[stage]} --week {week}"
    print(f"\n{'='*50}")
    print(f"  STAGE: {stage.upper()} | HÉT: w{week}")
    print(f"{'='*50}")

    if dry_run:
        print(f"  [DRY RUN] Futtatná: {cmd}")
        return True

    result = subprocess.run(cmd, shell=True)
    success = result.returncode == 0
    print(f"  → {'✓ OK' if success else '✗ HIBA'}")
    return success

def update_tematika_status(week: str, stage: str, ok: bool):
    """Frissíti a tematika.md pipeline státusz táblázatát."""
    # Egyszerűsített verzió — Cowork ezt részletesebben kezeli
    log_path = Path("_meta/pipeline_log.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        status = "OK" if ok else "FAIL"
        f.write(f"{datetime.now().isoformat()} | w{week} | {stage} | {status}\n")

def main():
    parser = argparse.ArgumentParser(description="Tantárgyfejlesztés pipeline")
    parser.add_argument("--week", required=True,
                        help="Hét száma (pl: 01, 02) vagy 'all'")
    parser.add_argument("--stage", default="all",
                        choices=STAGES + ["all"],
                        help="Melyik stage fusson")
    parser.add_argument("--dry-run", action="store_true",
                        help="Csak mutatja, mit futtatna")
    parser.add_argument("--from-stage", default=None,
                        help="Ettől a stage-től kezdje (korábbiak skip)")
    args = parser.parse_args()

    # Hetek listája
    weeks = (
        [f"{i:02d}" for i in range(1, 14)]
        if args.week == "all"
        else [args.week.zfill(2)]
    )

    # Stage-ek listája
    if args.stage == "all":
        stages = STAGES
        if args.from_stage and args.from_stage in STAGES:
            start = STAGES.index(args.from_stage)
            stages = STAGES[start:]
    else:
        stages = [args.stage]

    print(f"\nPIPELINE INDÍTÁS")
    print(f"  Hetek: {weeks}")
    print(f"  Stage-ek: {stages}")
    print(f"  Dry run: {args.dry_run}")

    failed = []
    for week in weeks:
        for stage in stages:
            ok = run_stage(stage, week, args.dry_run)
            update_tematika_status(week, stage, ok)
            if not ok:
                failed.append(f"w{week}/{stage}")
                print(f"\n[!] Hiba — leállás ennél: w{week} / {stage}")
                print(f"    Javítás után futtasd: --week {week} --from-stage {stage}")
                sys.exit(1)

    print(f"\n{'='*50}")
    print(f"✓ Pipeline kész. Log: _meta/pipeline_log.txt")

if __name__ == "__main__":
    main()
```

---

### _scripts/md_audit.py — Style Guide Compliance Checker

```python
#!/usr/bin/env python3
"""
MD Audit — ellenőrzi, hogy a notes.md fájlok megfelelnek-e a style guide-nak.

Futtatás:
  python _scripts/md_audit.py --week 01          # egy hét ellenőrzése
  python _scripts/md_audit.py --week all          # minden hét
  python _scripts/md_audit.py --week all --fix    # hiányzó szekciók hozzáadása

Ez az a script, amit akkor futtatsz, ha megváltozik a style_guide.md —
megtalálja az összes fájlt, amiben hiányoznak az új szekciók.
"""

import argparse
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List
from datetime import datetime

# ── Style guide szabályok ─────────────────────────────────────────────────────
# Ha megváltozik a style_guide.md, ITT kell frissíteni ezt a listát,
# majd --fix kapcsolóval futtatni → automatikusan hozzáadja a placeholdereket.

REQUIRED_SECTIONS = [
    "## Tanulási célok",
    "## Kulcsfogalmak",
    "## Összefoglaló szövegdoboz",   # ← ha ezt adod hozzá utólag, az audit megtalálja
    "## Kérdések",
]

REQUIRED_HEADER_FIELDS = ["Hét:", "Státusz:"]
MAX_WORDS_PER_SECTION = 800

PLACEHOLDER_TEMPLATES = {
    "## Tanulási célok": """## Tanulási célok

> [TODO] 3-5 mérhető cél:
- A hallgató képes lesz ...
- A hallgató meg tudja különböztetni ...
""",
    "## Kulcsfogalmak": """## Kulcsfogalmak

> [TODO] Glosszárium:
- **Fogalom:** definíció
""",
    "## Összefoglaló szövegdoboz": """## Összefoglaló szövegdoboz

:::info Fejezet összefoglalója
> [TODO] 3-5 mondatban a fejezet lényege.

**Kulcsgondolat:** [ide kerül]
:::
""",
    "## Kérdések": """## Kérdések

> [TODO] 3-5 önellenőrző kérdés:
1. Mi a különbség ...?
2. Hogyan hat ...?
3. Milyen esetben ...?
""",
}
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class AuditResult:
    file: Path
    missing_sections: List[str] = field(default_factory=list)
    missing_header_fields: List[str] = field(default_factory=list)
    long_sections: List[str] = field(default_factory=list)
    ok: bool = True

    def has_issues(self) -> bool:
        return bool(self.missing_sections or self.missing_header_fields)


def audit_file(md_path: Path) -> AuditResult:
    result = AuditResult(file=md_path)
    content = md_path.read_text(encoding="utf-8")
    lower = content.lower()

    # Kötelező szekciók
    for section in REQUIRED_SECTIONS:
        if section.lower() not in lower:
            result.missing_sections.append(section)
            result.ok = False

    # Fejléc mezők
    for field_name in REQUIRED_HEADER_FIELDS:
        if field_name.lower() not in lower:
            result.missing_header_fields.append(field_name)
            result.ok = False

    # Szóhossz ellenőrzés szekciónként
    parts = re.split(r'\n## ', content)
    for part in parts[1:]:  # első elem a fejléc, azt skip
        words = len(part.split())
        if words > MAX_WORDS_PER_SECTION:
            title = part.split('\n')[0].strip()
            result.long_sections.append(f"{title} ({words} szó)")

    return result


def fix_file(md_path: Path, missing: List[str]) -> None:
    """Hozzáadja a hiányzó szekciókat a fájl végéhez placeholder-rel."""
    additions = f"\n\n---\n<!-- AUTO-ADDED by md_audit.py @ {datetime.now().date()} -->\n"
    for section in missing:
        template = PLACEHOLDER_TEMPLATES.get(section, f"\n{section}\n\n> [TODO]\n")
        additions += template

    with open(md_path, "a", encoding="utf-8") as f:
        f.write(additions)


def main():
    parser = argparse.ArgumentParser(description="MD Style Guide Audit")
    parser.add_argument("--week", default="all",
                        help="Hét száma (pl: 01) vagy 'all'")
    parser.add_argument("--fix", action="store_true",
                        help="Hiányzó szekciókat hozzáadja TODO placeholder-rel")
    args = parser.parse_args()

    base = Path("02_notes")
    if args.week == "all":
        md_files = sorted(base.rglob("notes.md"))
    else:
        md_files = sorted((base / f"w{args.week.zfill(2)}").rglob("notes.md"))

    if not md_files:
        print(f"[!] Nem találtam notes.md fájlokat a keresett helyen.")
        return

    print(f"\nMD AUDIT — {len(md_files)} fájl vizsgálata")
    print(f"Style guide: {len(REQUIRED_SECTIONS)} kötelező szekció\n")

    issues = []
    for md in md_files:
        result = audit_file(md)
        rel = md.relative_to(Path("."))

        if result.has_issues():
            issues.append(result)
            print(f"❌ {rel}")
            for s in result.missing_sections:
                print(f"   Hiányzó szekció: {s}")
            for f in result.missing_header_fields:
                print(f"   Hiányzó fejléc:  {f}")
            if args.fix:
                fix_file(md, result.missing_sections)
                print(f"   → Hozzáadva placeholder-rel")
        else:
            print(f"✅ {rel}", end="")

        for warn in result.long_sections:
            print(f"\n   ⚠ Túl hosszú: {warn}", end="")
        print()

    print(f"\n{'─'*50}")
    print(f"Összesítő: {len(issues)}/{len(md_files)} fájlban van probléma")
    if issues and not args.fix:
        print("→ Futtasd --fix kapcsolóval az automatikus javításhoz")
    elif issues and args.fix:
        print("→ Placeholder-ek hozzáadva. Kézi kitöltés szükséges!")


if __name__ == "__main__":
    main()
```

---

### _scripts/retroactive_update.py — Schema Migration Script

```python
#!/usr/bin/env python3
"""
Retroaktív frissítés — ha megváltozik a style guide (pl. új szekciót vezetsz be),
ezt futtatva az összes korábbi fájl megkapja az új szekciót placeholder-rel.

Futtatás:
  python _scripts/retroactive_update.py --change summary_box --dry-run
  python _scripts/retroactive_update.py --change summary_box

Minden futtatás AUTOMATIKUSAN:
  1. Lementi a régi fájlokat _meta/backups/ mappába
  2. Módosítja a fájlokat
  3. Naplózza a döntést _meta/decisions.md-be
"""

import argparse
import shutil
from pathlib import Path
from datetime import datetime

# ── Elérhető változtatások ────────────────────────────────────────────────────
# Új metodológiai döntésnél: add hozzá ide, majd futtasd a scriptet.

CHANGES = {
    "summary_box": {
        "description": "Összefoglaló szövegdoboz hozzáadása minden fejezet végéhez",
        "applies_to":  "02_notes/**/notes.md",
        "check_marker": ":::info Fejezet összefoglalója",
        "content_to_append": """

## Összefoglaló szövegdoboz

:::info Fejezet összefoglalója
> [TODO] 3-5 mondatban a fejezet lényege.

**Kulcsgondolat:** [ide kerül]
:::
""",
    },

    "learning_objectives": {
        "description": "Tanulási célok szekció hozzáadása a fejléc után",
        "applies_to":  "02_notes/**/notes.md",
        "check_marker": "## Tanulási célok",
        "content_to_append": """

## Tanulási célok

> [TODO] 3-5 mérhető cél:
- A hallgató képes lesz ...
""",
    },

    "add_status_field": {
        "description": "Státusz mező hozzáadása a fejléchez",
        "applies_to":  "02_notes/**/notes.md",
        "check_marker": "Státusz:",
        "content_to_prepend": "Státusz: DRAFT\n",  # fejlécbe szúrja
    },
}
# ─────────────────────────────────────────────────────────────────────────────


def make_backup(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("_meta") / "backups" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    dest = backup_dir / path.name
    shutil.copy2(path, dest)
    return dest


def apply_change(md_path: Path, change: dict, dry_run: bool) -> bool:
    content = md_path.read_text(encoding="utf-8")

    # Ha már tartalmazza → skip
    if change["check_marker"] in content:
        if not dry_run:
            print(f"  → Már tartalmazza — skip: {md_path.name}")
        return False

    if dry_run:
        print(f"  [DRY RUN] Módosítaná: {md_path}")
        return True

    # Backup
    backup_path = make_backup(md_path)

    # Módosítás
    if "content_to_append" in change:
        new_content = content + change["content_to_append"]
    elif "content_to_prepend" in change:
        # A fejléc utáni első sor elé szúrja
        lines = content.split("\n")
        insert_at = next(
            (i for i, line in enumerate(lines) if line.startswith("# ")),
            0
        ) + 1
        lines.insert(insert_at, change["content_to_prepend"])
        new_content = "\n".join(lines)
    else:
        print(f"  [!] Ismeretlen művelet: {change}")
        return False

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  ✓ Frissítve: {md_path} (backup: {backup_path.name})")
    return True


def log_decision(change_name: str, change: dict, affected_count: int) -> None:
    log_path = Path("_meta") / "decisions.md"
    log_path.parent.mkdir(exist_ok=True)

    entry = f"""
## {datetime.now().strftime('%Y-%m-%d')} — `{change_name}`

**Változtatás:** {change['description']}
**Érintett fájlok:** {affected_count} db
**Backup helye:** `_meta/backups/{datetime.now().strftime('%Y%m%d_%H%M%S')}/`

---
"""
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="Retroaktív schema migration")
    parser.add_argument("--change", required=True,
                        choices=list(CHANGES.keys()),
                        help="Melyik változtatást alkalmazza")
    parser.add_argument("--dry-run", action="store_true",
                        help="Csak mutatja, mit változtatna")
    args = parser.parse_args()

    change = CHANGES[args.change]
    files = sorted(Path(".").glob(change["applies_to"]))

    print(f"\nRETROAKTÍV FRISSÍTÉS: {args.change}")
    print(f"Leírás: {change['description']}")
    print(f"Érintett fájlok: {len(files)} db")
    print(f"Dry run: {args.dry_run}\n")

    modified = 0
    for md in files:
        if apply_change(md, change, args.dry_run):
            modified += 1

    print(f"\n{'─'*50}")
    print(f"Módosítva: {modified}/{len(files)} fájl")

    if not args.dry_run and modified > 0:
        log_decision(args.change, change, modified)
        print(f"✓ Döntés naplózva: _meta/decisions.md")
        print(f"✓ Backup: _meta/backups/")


if __name__ == "__main__":
    main()
```

---

### _scripts/figure_runner.py — Python Ábrareprodukció (egy hét)

```python
#!/usr/bin/env python3
"""
Ábra runner — futtatja az adott hét összes fig_*.py scriptjét
és ellenőrzi, hogy megszültek-e a PNG kimenetek.

Futtatás: python _scripts/figure_runner.py --week 01
"""

import argparse
import subprocess
from pathlib import Path

def run_figure_script(py_path: Path) -> bool:
    print(f"  Futtatás: {py_path.name} ... ", end="", flush=True)
    result = subprocess.run(
        ["python", str(py_path)],
        capture_output=True, text=True,
        cwd=py_path.parent
    )
    if result.returncode == 0:
        print("✓")
        return True
    else:
        print("✗ HIBA")
        print(f"  stderr: {result.stderr[:200]}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True)
    args = parser.parse_args()

    week_dir = Path("03_figures") / f"w{args.week.zfill(2)}"
    if not week_dir.exists():
        print(f"[!] Nem létezik: {week_dir}")
        return

    scripts = sorted(week_dir.glob("fig_*.py"))
    print(f"\nÁBRA RUNNER — {len(scripts)} script, {week_dir}")

    failed = []
    for script in scripts:
        ok = run_figure_script(script)
        if not ok:
            failed.append(script.name)

        # Ellenőrzés: megvan-e a PNG?
        expected_png = script.with_suffix(".png")
        if not expected_png.exists():
            print(f"  ⚠ PNG nem jött létre: {expected_png.name}")

    print(f"\nEredmény: {len(scripts)-len(failed)}/{len(scripts)} sikeres")
    if failed:
        print(f"Sikertelen: {', '.join(failed)}")

if __name__ == "__main__":
    main()
```

---

### Példa ábra script: 03_figures/w01/fig_01_pressure_curve.py

```python
#!/usr/bin/env python3
"""
1. hét, 1. ábra — nyomásgörbe
Ez a fájl: 03_figures/w01/fig_01_pressure_curve.py
Output:    03_figures/w01/fig_01_pressure_curve.png

FONTOS: a script a saját mappájából fut (figure_runner.py cwd=py_path.parent),
        ezért a kimeneti path relatív a 03_figures/w01/-hoz.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Adatok ────────────────────────────────────────────────────────────────────
x = np.linspace(0, 10, 100)
y_ideal   = 2.0 * np.exp(-0.1 * x) + 0.5
y_real    = y_ideal * (1 - 0.05 * np.random.randn(100))  # zajjal

# ── Stílus ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":   "sans-serif",
    "font.size":     11,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(7, 4))

ax.plot(x, y_ideal, label="Ideális", color="#1f77b4", linewidth=2)
ax.plot(x, y_real,  label="Valós",   color="#ff7f0e", linewidth=1.5,
        linestyle="--", alpha=0.8)

ax.set_xlabel("Áramlási sebesség [m/s]")
ax.set_ylabel("Nyomásviszony [-]")
ax.set_title("Nyomásgörbe — 1. hét")
ax.legend()
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))

plt.tight_layout()
plt.savefig("fig_01_pressure_curve.png", dpi=150, bbox_inches="tight")
plt.close()
print("Mentve: fig_01_pressure_curve.png")
```

---

## HUMAN-IN-THE-LOOP CHECKPOINT TÁBLÁZAT

| Gate | Mi történik előtte (auto) | Mit ellenőrzöl te | Döntés |
|------|--------------------------|-------------------|--------|
| **Gate 1** | MinerU lefutott | Jól ismerte fel a szöveget? Ábrák rendben? | ✅ folytatás / 🔄 újrafuttatás |
| **Gate 2** | Szöveg struktúrálva | MD struktúra logikus? Fejezetek rendben? | ✅ / 🔄 átstrukturálás |
| **Gate 3** | NotebookLM feltöltve | NLM kérdések relevánsak? | ✅ / 🔄 új kérdések |
| **Gate 4** | MD notes draft kész | Tartalom szakmailag helyes? | ✅ / 🔄 javítás |
| **Gate 5** | Ábrák regenerálva | Ábrák vizuálisan jók? Skála ok? | ✅ / 🔄 script módosítás |
| **Gate 6** | PPTX + kérdésbank kész | Végleges review | ✅ → 06_final/ |

---

## COWORK INSTRUCTIONS.MD MINTA

Ezt tedd: `.claude/instructions.md` — ez minden Cowork session elején betöltődik.

```markdown
# Tantárgyfejlesztési Projekt — Cowork Utasítások

## A projekt
13 hetes tantárgyanyag fejlesztése pipeline-alapon.
A projekt gyökere ez a mappa.

## Mindig olvasd el először
- `_meta/project_status.md` — aktuális állapot
- `_meta/tematika.md` — a 13 hetes terv
- `_meta/style_guide.md` — MD fájlok kötelező formátuma

## Alapszabályok
1. Soha ne írj felül fájlt backup nélkül (→ `_meta/backups/`)
2. Minden futtatás után frissítsd `_meta/pipeline_log.txt`
3. Ha módszertani döntést hozol, naplózd `_meta/decisions.md`-be
4. A `00_inputs/` mappa CSAK OLVASHATÓ — soha ne módosítsd
5. Ha elakadsz, írj egy [BLOKKOLT] bejegyzést a project_status.md-be

## Pipeline futtatás
python _scripts/process_all.py --week 01 --stage all

## Retroaktív módosítás esetén
python _scripts/retroactive_update.py --change [change_name] --dry-run
# majd ha OK:
python _scripts/retroactive_update.py --change [change_name]
```

---

## ITERÁCIÓS RITMUS JAVASLAT

```
HETI CIKLUS (egy hétnyi anyagra):

H1 — Cowork task: MinerU futtatás + Gate 1 review (te)
H2 — Cowork task: NotebookLM lekérdezések + MD draft
H3 — Chat (itt velem): tartalmi finomítás, bekezdések javítása
H4 — Cowork task: Python ábrák + PPTX generálás
H5 — Te: Gate 6 review, 06_final/-ba másolás

METODOLÓGIA-VÁLTOZÁS ESETÉN:
1. Frissítsd _meta/style_guide.md
2. Frissítsd md_audit.py REQUIRED_SECTIONS listáját
3. Add hozzá az új entry-t retroactive_update.py CHANGES dict-be
4. Futtatás: python _scripts/retroactive_update.py --change [uj_valtozas]
5. python _scripts/md_audit.py --week all → ellenőrzés
```
