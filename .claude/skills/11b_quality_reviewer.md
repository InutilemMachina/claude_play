---
name: 11b_quality_reviewer
title: 11B_QUALITY_REVIEWER -- Kvalitatív minőségellenőrzés
type: skill
tags: [meta, skill, review]
status: active
version: 1.0
updated: 2026-05-29
description: Pedagógiai és szerkesztői minőségellenőrzés a kész Jegyzeten. Explore agent alapú -- nem igényel Claude API-t. Pipeline 11b. lépése (11_typesetter UTÁN, 12_presentation_maker ELŐTT).
---

# 11B_QUALITY_REVIEWER

## 1. Cél

A `4_wip_outputs/N_Jegyzet.md` pedagógiai, szerkesztői és publikációs minőségének ellenőrzése **mielőtt** a prezentáció és kérdésbank generálódik. Célja, hogy a 72-pontos fejezet típusú strukturális hibák ne maradjanak észrevétlenül.

## 2. Bemenetek

- `4_wip_outputs/N_Jegyzet.md` -- 11_typesetter kimenet

## 3. Eljárás

### 3.1. Automatikus metrikák (Python)

```powershell
python -c "
import pathlib, re
text = pathlib.Path('test_outputs/<Tantargy>/N_het/4_wip_outputs/N_Jegyzet.md').read_text(encoding='utf-8')
lines = text.splitlines()
h2 = [l for l in lines if l.startswith('## ') and not l.startswith('### ')]
h3 = [l for l in lines if l.startswith('### ')]
sups = text.count('<sup>')
inline_src = len([l for l in lines if re.match(r'Felhaszn', l, re.IGNORECASE)])
dup = len(re.findall(r'<sup>\[(\d+)\]</sup>,\s*<sup>\[\1\]</sup>', text))
# Chapter balance check
ch_sizes = {}
cur = None
for l in lines:
    if l.startswith('## ') and not l.startswith('### '): cur = l
    elif l.startswith('### ') and cur: ch_sizes[cur] = ch_sizes.get(cur, 0) + 1
print(f'## szekciók: {len(h2)} | ### alszekciók: {len(h3)}')
print(f'<sup> citációk: {sups} | Inline forrásblokk: {inline_src} | Dupla citáció: {dup}')
print('Fejezet-egyensúly:')
for k, v in sorted(ch_sizes.items(), key=lambda x: -x[1])[:5]:
    flag = ' ⚠️ TÚLTERHELT' if v > 15 else ''
    print(f'  {k}: {v} alszekció{flag}')
"
```

**Elfogadható értékek:**
| Metrika | OK | Figyelmeztetés | Kritikus |
|:--------|:---|:---------------|:---------|
| `##` szekciók száma | 5–12 | 3–4 vagy 13–15 | <3 vagy >15 |
| Egy fejezet max. alszekciói | ≤15 | 16–25 | >25 |
| Inline forrásblokk | 0 | -- | >0 |
| Dupla `<sup>[N]</sup>` | 0 | -- | >0 |
| `<sup>` citáció | >100 | 10–100 | <10 |

### 3.2. Kvalitatív ellenőrzés (Explore agent)

Az Explore agent az alábbi szempontok szerint értékeli a dokumentumot:

**Szerepkör prompt:**
```
Te egy magyar egyetemi tananyagszerkesztő vagy. Olvasd el a Jegyzetet és értékeld:
1. Pedagógiai struktúra (fejezet-logika, ismétlések, haladás)
2. Fejezet-arány (van-e >15 alszekciójú fejezet?)
3. Citáció (vannak-e dupla [N],[N] sorozatok? Inline forrásblokkok?)
4. Publikálhatóság: 1-5 skálán (1=nem publikálható, 5=ready)
5. Top 3 kritikus probléma + top 3 javítás
```

### 3.3. 😎 Döntési pont

| Értékelés | Következő lépés |
|:----------|:----------------|
| Publikálhatóság ≥ 3/5, nincs kritikus hiba | ✅ Folytatás (12_presentation_maker) |
| Publikálhatóság 2/5, javítható strukturális hiba | ⚠️ Assembler újrafuttatás Prompt B frissítés után |
| Publikálhatóság 1/5, fundamentális probléma | ❌ DFS query újrafuttatás szükséges |

## 4. Kimenetek

- `4_wip_outputs/N_Review.md` -- szerkesztői jelentés + a **tartalmi/minőségi visszajelzés kanonikus helye** (Instructions §11.1, kétcsatornás modell).

### 4.1. Visszajelzés-csatornák (Instructions §11.1)

A wip/clean outputról szóló visszajelzés a **természete** szerint kerül a helyére:

| Visszajelzés típusa | Hely | Élettartam |
|---|---|---|
| **Tartalmi/minőségi** -- a konkrét tananyagról (pl. „a 4. fejezet redundáns") | `N_Review.md` (e skill kimenete, a kimenet mellett) | eldobható a teszttel |
| **Pipeline-tanulság** -- a kimenet pipeline-hibát tár fel (pl. „a Rule H tönkreteszi a kommenteket") | a megfelelő skill `§8` | tartós |

Ha egy tartalmi észrevétel tartós pipeline-tanulsággá érik, **átemelendő** a `N_Review.md`-ből a megfelelő skill `§8`-ba.

## 5. Ellenőrzési lista

- [ ] `##` szekciók száma 5–12 között
- [ ] Egy fejezetnek sincs >15 alszekciója
- [ ] Inline forrásblokk: 0
- [ ] Dupla citáció: 0
- [ ] `<sup>` tagek jelen vannak (07_citations_renumber lefutott)
- [ ] Publikálhatóság ≥ 3/5 (agent értékelés)

## 6. Hibakezelés

| Tünet | Gyökérok | Megoldás |
|:------|:---------|:---------|
| Egy fejezet >25 alszekciója | RC-1: Prompt B nem írja elő `##`-t | Prompt B frissítése + DFS újrafuttatás |
| Minden szekció egy fejezetbe esik | RC-2: `dfs_node_list.json` hiányzik | `04_nlm_dfs_queries.py` újrafuttatás (generálja) |
| Inline forrásblokkok maradtak | 07_citations_renumber nem futott | `python scripts/07_citations_renumber.py --week-dir ...` |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [11_typesetter.md](11_typesetter.md) -- előfeltétel
- [12_presentation_maker.md](12_presentation_maker.md) -- következő lépés

## 8. Visszajelzések

- 💬 NOTE: Az Explore agent nem igényel külön ANTHROPIC_API_KEY-t -- a FleetView harness kezeli. API-kulcs nélkül is futtatható.

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-30 | 1.1 | K0 cleanup: 2 ✅ → §9 (script elkészült, skill létrehozva) |
| 2026-05-29 | 1.0 | Létrehozva: RC-6 fix; automatikus metrikák + Explore agent workflow |
