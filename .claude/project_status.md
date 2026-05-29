---
title: Project Status -- Playground PDCA log
type: log
status: active
version: 3.1
updated: 2026-05-29
description: Playground (claude_play) PDCA log. Session elején Claude olvassa be. NEM tantárgy-specifikus.
---

<!-- TODOs (strukturális rendrakás következő session-ben):
TODO: templates/project_status_sablon.md + templates/context_sablon.md → course_development_template.md (egyesítés)
TODO: Ez a fájl szerkezetileg szétesett -- rendbe kell tenni (gép+ember olvasható legyen)
-->

# Project Status -- Playground PDCA Log

_Frissítve: 2026-05-29 (4. update -- iteráció 2 tanulságok)_

## ⚡ AKTUÁLIS BRANCH: meta_file_updates

### Iteráció 2 eredmények (2026-05-29)

**Elvégzett (J változások):**

| J | Változás | Eredmény |
|---|---------|---------|
| J1 | Prompt B: prose + ismétlés tilalma + ## kötelező | User elvégezte NLM notebookon |
| J2 | `--max-level 2` (37→23 query) | Bullet 85%→40%, Prose 15%→59% |
| J3 | Q1 bevezető-prompt | Q1: 5269→1213 kar (-77%) |
| J4 | Rule J terminológia (11_typesetter) | 18 terminológiai javítás/futás |
| J5 | Mindmap cleanup (Aszálybetegség→Korai tűzjelzés) | Off-topic node eltávolítva |

**Megtalált bugok (javítva):**
- `05_assemble.py` L1/L2 `##` duplikáció: J1 Prompt B + assembler konfliktusnál kettős fejléc → `extract_section_title()` most L1/L2-nél is strip-el

**Nyitott (következő session):**
- Q14–Q23 NLM RESOURCE_EXHAUSTED; `--resume` futtatandó ha kvóta resetel
- Terminológia Rule J bővítendő tantárgy-specifikus párral (tantárgyanként `TERM_MAP`)
- Kvóta reset időpontja: Google-fiók szintű, kb. éjfél PT (Pacific Time)

**Utolsó commit:** `fix(pipeline): RC-1/RC-2/RC-3 — heading structure, L1 sectioning, citations`

**Nyitott P-prioritások:**
| # | Feladat | Státusz |
|---|---------|---------|
| **P0-A** | Prompt B `##` heading kötelező (RC-1) | ✅ 2026-05-29 |
| **P0-B** | Assembler L1-szekcionálás + `dfs_node_list.json` (RC-2) | ✅ 2026-05-29 |
| **P0-C** | `07_citations_renumber.py` `--week-dir` + `<sup>` konverzió (RC-3) | ✅ 2026-05-29 |
| **P1-A** | `11b_quality_reviewer` skill (RC-6) | ✅ 2026-05-29 |
| **P1-B** | NLM Qfig alapú VLM pótlás (RC-4) | 🔲 következő session |
| **P1-C** | `project_status.md` strukturális rendrakás | 🔲 következő session |
| **P1-D** | `nlm_prompts.md` felbontás `./claude/prompts/` mappába | 🔲 következő session |
| **F6** | Szószedet NLM-alapra | 🔲 |
| **F7** | Kérdésbank NLM-alapra | 🔲 |
| **F8** | PPTX architektúra döntés | 🔲 |
| Branch cleanup | main merge + régi ágak törlése | 🔲 |

## ✅ 2026-05-29 -- Mini teszt post-mortem + P0 fixek

**Mini teszt:** 2 forrás (FLIR PDF + InfraTec HTML), 37 DFS query, `mini/1_het/`

**Talált hibák és javítások:**

| RC | Tünet | Fix | Eredmény |
|----|-------|-----|----------|
| RC-1 | 0/37 query generált `##` headinget | Prompt B `## kötelező első sor` szabály | Következő futásnál érvényes |
| RC-2 | 4. fejezet: 72 alszekció | `dfs_node_list.json` + L1-szekcionálás | 72 → 4 alszekció |
| RC-3 | `07_citations_renumber.py` elavult | Teljes újraírás `--week-dir`-rel | `<sup>` citáció + forrásblokk eltávolítás |
| Bug | `05_assemble.py` hiányzó `main()` | Javítva (előző commit) | Script fut |
| Bug | `extract_section_title()` csak `##`-t fogadott | `#{2,3}` regex | `###` is elfogadott |

**Vision bypass:** Ultra Explorer törött → Claude vision → PNG-ből `nlm_mindmap_export.md` rekonstrukció (`08_mindmap_manager §8`).

**Kvalitatív review (university editor):**
- Publikálhatóság: 1/5 (P0 fixek előtt) → becsült 3/5 (P0 fixek után)
- Kritikus: 72-pontos fejezet, `[2],[2]` dupla citációk, inline forrásblokkok

**Pipeline lefutott (01–11):**
- ✅ MinerU: 11 kép, `flir_IR_thermography.md`
- ✅ Vision bypass: mindmap PNG → `nlm_mindmap_export.md`
- ✅ 37/37 DFS query
- ✅ Assembler (bug fix-szel)
- ✅ 07 citations (újraírva): 699 `<sup>`, 113 forrásblokk-sor eltávolítva
- ✅ 10 notes collector: 144 ToC bejegyzés
- ✅ 11 typesetter: Rule A 164, Rule B 202, Rule H 155
- ❌ Képek: VLM blokkolt (ANTHROPIC_API_KEY hiánya)
- ❌ 06 excerpt blocks: API kulcs hiánya

# 1. Plan (következő lépések)

_Frissítve: 2026-05-24 -- refactor/v2 branch_

| # | Feladat | Felelős | Megjegyzés |
|:--|:--------|:--------|:-----------|
| **R1** | **Termografia_teszt_v3 pipeline futtatás** -- új mappastruktúrával (1_raw_inputs/2_clean_inputs/3_raw_outputs/4_wip_outputs/5_clean_outputs) | 🤖+😎 | 🔲 következő prioritás |
| **R2** | **MinerU** -- `03_run_mineru_pipeline.py` tesztje Termografia_teszt_v3-on | 🐍 | 🔲 |
| ~~**R3**~~ | ~~**context_sablon.md** lépésszámok frissítése~~ | 🤖 | ✅ KÉSZ 2026-05-26 |
| **R4** | **nlm_integration.md notebook-lista** frissítése (Termografia v2+v3 hozzáadva) | 🤖 | 🔲 -- beolvadt 02_nlm_notebook_setup-ba |
| **R5** | **NLM Prompt B pedagógiai felülvizsgálata** | 🤖+😎 | nlm_prompts.md átírás |
| **R6** | **du_template.pptx** megszerkesztése | 😎 | hiányzik, bypass él |
| **R7** | **03_mineru_extractor**: tesztelés -- per-forrás 2_clean_inputs/<nev>/ almappa | 🐍 | 🔲 |

# 2. Do (elvégzett munkák)

## 2026-05-25 -- feature_test_step_by_step branch (Fourier_teszt)

**01. lépés -- NOTE-ok:**

- NOTE 💬 A pipeline eleje döcögős -- 01. lépésnél Claude azonnal visszakérdezett (forrásmetaadatok hiánya), holott a user tudta, mi kell. Nem bug, hanem nyitott design-kérdés: a pipeline belépési pontja nem elég önálló; skill pontosítás vagy strukturáltabb indítási kontextus kell.
- NOTE 💬 Heti mappa alstruktúra számozva: `1_raw_inputs`, `2_clean_inputs`, `3_raw_outputs`, `4_wip_outputs`, `5_clean_outputs`. Fourier_teszt-en átvezetva; pipeline.md és CLAUDE.md frissítése szükséges.

**01. lépés -- elvégzett:**

- ✅ `test_outputs/Fourier_teszt/1_het/` mappastruktúra (számozott)
- ✅ `azad2012_webpage.html` letöltve, `1_raw_inputs/`-ba mentve
- ℹ️ Meglévő: `rockmore1999_article.pdf`, `typinski2014_slides.pdf`, `The Fast Fourier transform (FFT).pptx` (utóbbinak naming-javítás szükséges)

**02. lépés -- NOTE-ok (NLM UI visszajelzés):**

- NOTE 💬 Csak 3 forrás jelent meg -- a PPTX feltöltés NLM CLI-vel sikertelen (pitfalls.md §2.5).
- NOTE 💬 Az NLM UI-ban a forráscímeket az NLM átnevezi (a fájlnév helyett a dokumentum tartalmából generál nevet) -- ezért a source listában nem látható könnyen, melyik fájlból melyik forrás lett, és melyik feltöltése nem sikerült. A `nlm source list <NB>` parancs visszaadja az eredeti fájlnevet is -- ezt érdemes a 02. lépés végén loggolni. (pitfalls.md §2.7)
- NOTE 💬 A notebook középső ablakában automatikusan generált absztrakt szöveg jelenik meg -- felhasználható a tananyag bevezető szövegéként (pipeline integrálni kell, pl. 05_source_controller vagy 06_excerpt_block_maker inputjaként).
- NOTE 💬 Mindmap sikeresen létrejött a Studio fülön.
- NOTE 💬 Prompt B (Metaparancs) sikeresen beillesztve -- "Egyéni" mód aktív.
- ✅ Válasz hossza: `nlm chat configure $NB --response-length longer` (tesztelve 2026-05-26 -- helyes flag: `longer`, nem `long`).

**14. lépés -- eredmény:**

- ⚠️ `14_bsc_filter.py` script nem létezik -- a skill is jelzi (§2: "Script még nem létezik"). A szűrést manuálisan végzem el. *(✅ 2026-05-26: script elkészült -- `scripts/14_bsc_filter.py`)*
- ✅ `5_clean_outputs/bsc/` létrehozva, BSc-szűrt fájlok bemásolva (MSc blokkok kivágva).

**14. lépés -- NOTE-ok (pre-futás):**

- NOTE 💬 **Camera-ready scope:** Nem csak a prezentáció, hanem a Jegyzet is camera-ready formában exportálandó (`5_clean_outputs/`-ba). A 14_bsc_filter feladata nemcsak szűrés, hanem végtermék-előállítás: Jegyzet + Prezentáció + Szószedet + Mindmap + Kérdések mind kerüljenek `5_clean_outputs/bsc/`-ba.
- NOTE 💬 **Dash kiirtás (pipeline-szintű):** Minden `4_wip_outputs/` és `5_clean_outputs/` fájlból el kell távolítani a `--` dupla kötőjelet, az n-dasht (`–`) és m-dasht (`—`). Magyarban ezek ritkák, a pipeline-ban szinte mindig hibák. Megoldandó: `11_typesetter.py` Rule H-ként, vagy önálló pre-export szűrőként.
- ❌ **Kérdésbank NLM-alapú:** A 13_question_bank_collector NLM-queryt kell használjon, ne Claude-feladatot. Az NLM a forrásokból pontosabb, citált kérdéseket generál. A jelenlegi `1_Kerdesek.md` placeholder -- újragenerálandó NLM-queryvel a következő iterációban.
- ⚠️ **MSc jelölés -- emberi döntés:** Az MSc/BSc határt ember dönti el (nem pipeline). A Mindmap csomópontjainak BSc/MSc besorolása kézi review után kerül a skillbe.
- ⚠️ **NLM Mindmap export -- kritikus elem:** A Studio Gondolattérkép exportja (Ultra Explorer bővítmény, §2.2) az egész pipeline sarokköve. A mindmap-csomópontok adják a query-struktúrát (04), a BSc/MSc határt (13-14), és a pedagógiai szerkezetet (05, 06). Ha kell, külön session-t szánunk rá.

**13. lépés -- elvégzett:**

- ✅ `4_wip_outputs/1_Kerdesek.md` generálva: 6 BSc (SZINT 2-3) + 2 MSc (SZINT 4-5) kérdés, A/B/C/D formátum, helyes válaszokkal
- NOTE 💬 **Forrás:** Claude-feladatként, `1_Jegyzet.md` alapján. NLM-query alapú generálás (13_question_bank_collector §NLM) tesztelendő a következő iterációban.

**12. lépés -- NOTE-ok:**

- NOTE 💬 **Mindmap camera-ready hiányzik:** `1_Mindmap.md` DRAFT státuszban van -- a pipeline-nak `5_clean_outputs/`-ba is kell egy camera-ready verziót előállítani (pl. renderelt kép vagy exportált PDF). Megoldandó: 12. vagy 14. lépés felelőssége definiálandó.
- NOTE 💬 **Marp prezentáció hiányosságai:** (1) Nincs TOC-dia; (2) kevés szöveg -- a diákon csak bullet-ok, előadói szöveg (speaker notes) hiányzik; (3) a 06_excerpt_block_maker `💡 Lényeg` blokkjai ideálisak lennének speaker notes-ként.
- NOTE 💬 **PPTX sablon nem alkalmazódott:** A `12_pptx_gyarto.py` nem a `due_prenetation_template.pptx` layoutjait használja -- a Marp tartalom a meglévő sablon-diák után kerül beillesztésre, nem felül. A sablon XML-ben nincs kódolva (placeholder mapping hiányzik).
- NOTE 💬 **PPTX tipográfia:** Nyers Markdown szintaxis jelenik meg a diákon (pl. `**félkövér**` helyett félkövér formázás). A `12_pptx_gyarto.py` nem értelmezi a Markdown inline formázást python-pptx szinten.
- ❔ **Architektúra döntés (nyitott):** Három lehetséges irány a PPTX generáláshoz: (1) XML-alapú PowerPoint sablon (python-pptx placeholder mapping); (2) Pandoc (Marp MD → PPTX, saját sablon); (3) fejlesztett Marp + böngészős export (pl. Headless Chrome). Döntés szükséges a 12. lépés következő iterációja előtt.

**11. lépés -- NOTE-ok:**

- NOTE 💬 **Phase 1 (bullet→próza Claude API) ejtve:** A `11_typesetter.py` Phase 1 funkcióját el kell hagyni. Indok: az NLM `--response-length longer` beállítással eleve folyó prózát ad vissza -- ha ez működik, a Claude API-s konverzió felesleges overhead. Phase 1 eltávolítandó a scriptből; a `11_typesetter.py` csak Phase 2 (linting) maradjon. A script `--lint-only` flagje ezzel válik az egyetlen futtatási móddá.

**10. lépés -- NOTE-ok:**

- NOTE 💬 **ToC hierarchikus számozás hiányzik:** A ToC linkek nem tartalmazzák a sorszámokat (pl. `1. Matematikai...` helyett `Matematikai...`), mert a `##` fejlécek sem voltak egységesen számozva a Jegyzetben. Megoldandó: `util_heading_numberer.py` futtatása a `05_assemble.py` után, mielőtt a ToC generálódik.
- NOTE 💬 **ToC leading spaces (Q1 szekció):** Az első 3 bejegyzés (`Mi a Fourier-transzformáció?` stb.) felesleges 2 szóközzel kezdődik a ToC-ban -- a `###` fejlécek `##` szülő nélkül szerepelnek. Gyökérok: Q1 kimenetben nincs `##` szintű szülő (ismert heading-hierarchia hiba, 06. lépés NOTE-jaiban rögzítve).

**09. lépés -- eredmény:**

- ⚠️ `09_figure_mapper` kihagyva: 56 entry, 0 keywords (03b_qfig_parser 0 egyezés miatt -- ismert hiba, pitfalls §3.2). Script korrekten figyelmeztet: `[Warning] No entries with vlm_done=True`. `figure_catalog.json` változatlan, `inserted_after_paragraph` mezők nem töltöttek ki. A 10_notes_collector ábrát nem illeszt be.
- ❌ **KRITIKUS:** Képek nélkül a tananyag csonka -- az ábrai tartalom a pedagógiailag egyik legfontosabb elem. A 03b_qfig_parser 0 egyezése blokkolja az összes downstream képbeillesztést (09, 10). A gyökérok (BOM + szabad NLM formátum) megoldásáig a pipeline képek nélkül fut végig -- ez a legmagasabb prioritású nyitott hiba.

**07. lépés -- NOTE-ok:**

- NOTE 💬 **Szószedet forrása:** A `1_Szozedet.md` Claude által, a `1_Jegyzet.md` szövegéből lett összeállítva -- nem NLM-alapú. Következmény: (1) nem reprodukálható (más futáson más fogalmak); (2) nem auditálható (nincs Studio-beli nyom, nem látszik melyik forrásból jött az adat); (3) token-igényes. Megoldandó: a szószedet NLM-query alapra teendő (dedikált Prompt C vagy külön `nlm query` hívás), amelynek válasza a Studio-ban is megjelenik és UUID-alapú citációkkal érkezik. Ez konzisztens lenne a pipeline többi NLM-lépésével.

**07. lépés -- elvégzett:**

- ✅ `3_raw_outputs/citations.json` generálva (3 aktív forrás; [4] PPTX kihagyva, nlm_uuid null)
- ✅ `4_wip_outputs/1_Szozedet.md` generálva (20 kulcsfogalom, 5 tematikus szekció, IEEE hivatkozásokkal)
- ⚡ `[6-8]` feloldatlan hivatkozástartomány a `1_Jegyzet.md` 17. sorában (Q1 blokk) -- a `05_assemble.py` a range-formátumú local ID-kat nem konvertálja globálisra. Pitfalls §3.3-ban rögzített ismert hiba.

**06b. lépés -- NOTE-ok (table_caption_injector):**

- NOTE 💬 **n-dash a feliratban:** A generált caption `*1. táblázat -- (automatikus felirat)*` dupla kötőjelet (`--`) tartalmaz. A kimeneti dokumentumban n-dash kerülendő -- a scriptet javítani kell: `--` helyett `:` vagy vessző.
- NOTE 💬 **Automatikus felirat placeholder:** Az `(automatikus felirat)` szöveg jelenik meg, holott kontextusbeli felirat kellene. A script jelenleg nem tudja kiolvasni a táblázat tartalmát és értelmes feliratot generálni. Megoldandó: (1) NLM-query alapú felirat generálás, vagy (2) Claude-feladatként a táblázat sorai alapján automatikus összefoglalás.

**06. lépés -- NOTE-ok (excerpt_block_maker):**

- ✅ A lépés sikeresen lefutott: 💡 Lényeg blockquote-ok minden ### szekció után, 🗺️ Fejezet összegzés minden ## szekció után; fejezet-címek pontosítva (pl. "1. Matematikai és geometriai alapok").
- NOTE 💬 Lista whitespace: generált szövegben `*   **...**` forma (több szóköz) -- legyen `* **...**`. Megoldandó: 11_typesetter lint-szabályba felvéve.
- NOTE 💬 Heading hierarchia: Q1 kimenetben `###` közvetlenül `#` alatt (nincs `##`); többi szekció Q2+ helyes `## + ###` struktúrát kap. VSCode vázlatban és ToC-ban inkonzisztens. Megoldandó: 05_assemble.py Q1-hez `## Bevezetés` szülőt generáljon, vagy Prompt B módosítás.
- NOTE 💬 Formázási alternatíva: blockquote helyett `<div>` alapú doboz (markdown_textboxes.md 3. megoldás) -- 06_excerpt_block_maker.md v2-ben implementálandó.
- NOTE 💬 Studio panel: NLM válaszokat a Studio panelbe is menteni kell (auditálhatóság) -- 02_nlm_notebook_setup.md-ben rögzítve.

**05. lépés -- NOTE-ok (Jegyzet struktúra):**

- NOTE 💬 `1_Jegyzet.md` jelenlegi struktúrája pedagógiailag nem megfelelő: (1) `# 1. Hét` cím után rögtön `### Mi a Fourier-transzformáció?` következik -- számozatlan, 3 db #, nincs absztrakt; (2) a Q1 bevezető kérdések (Mi a Fourier-transzformáció? Miért fontos? Alapfogalmak) jó kiindulás, de hallgató számára ismeretlen fogalmakat feltételez -- pedagógiai átgondolás szükséges; (3) az NLM notebook absztrakt szövege (középső panel) ideális lenne a cím után első elemként.

**03b. lépés -- eredmény:**

- ❌ 03b_qfig_parser: 0 egyezés. Okok: (1) BOM-os UTF-8 a nlm_qfig_raw.txt-ben (pitfalls §1.2); (2) az NLM szabad markdown formátumban válaszolt, nem a parser által várt strukturált FORRÁS/SZÁM/ALÁÍRÁS mezőkkel. A figure_catalog.json caption/keywords mezői üresek maradtak -- 03c és tovább ezzel fut.

**03. lépés -- NOTE-ok:**

- NOTE 💬 A mindmap már a 02. lépés végén kimenthető lenne (a 03. MinerU előtt), de az NLM műveletek legyenek csoportosítva -- a mindmap export is maradjon a 02-es NLM-blokkban (ne kerüljön a 03. elé).
- NOTE 💬 NOTE (csak tervezés, nem implementálandó most): a heti mappa alstruktúrát logikai sorrendbe kell számozni: `1_raw_inputs → 1_raw_inputs`, `2_clean_inputs → 2_clean_inputs`, `3_raw_outputs → 3_raw_outputs`, `4_wip_outputs → 4_wip_outputs`, `5_clean_outputs → 5_clean_outputs`. Ez a változtatás az összes érintett scriptet (03, 05, 06b, 09, 10, 11, 12, 14...) egyszerre kell érintse -- ne félúton vezessük be. A Fourier_teszt mappáit visszanevezzük az eredeti nevekre (MinerU lefutása után), és a `03_run_mineru_pipeline.py`-ban elvégzett csere is visszaállítandó.
- ⚠️ Általánosabb tanulság: mappastruktúra-konvenció változtatása pipeline KÖZBEN nem ajánlott -- minden scriptet egyszerre kell frissíteni.
- NOTE 💬 MinerU futása során nem jelenik meg automatikusan egy terminal, ahol a user is nyomon követhetné az állapotot -- ez UX probléma, különösen hosszú fájloknál (1-5 perc/PDF). Start-Process indításkor felugrik egy cmd ablak, de üres -- a rich progress output nem jelenik meg benne. Megoldandó: vagy `-WindowStyle Hidden` (ha nincs szükség a kimenetre), vagy a stdout/stderr egy log fájlba irányítandó, amit a user megnyithat.
- NOTE 💬 MinerU MCP-n át nem futtatható: az MCP tool-nak ~30 másodperces hard timeout-ja van, MinerU ennél sokkal tovább fut. Háttérfolyamat (Start-Process + polling) alternatíva token-pazarló. A MinerU futtatása 😎 manuális lépésként kezelendő, vagy külön terminálból indítandó -- a pipeline-ban ez egy természetes szünet.
- NOTE 💬 MinerU részleges lefutás: `typinski2014_slides.pdf` feldolgozása lezárult; `rockmore1999_article.pdf` mappája létrejött (`2_clean_inputs/rockmore1999_article`), de a feldolgozás nem fejeződött be (vagy még fut). Az `azad2012_webpage.html` és a PPTX MinerU által nem feldolgozható -- ezek várhatóan kimaradnak. Gyökérok ismeretlen (méret? timeout? crash?). ❔ Nyitott: a részleges kimenettel továbblépünk-e, vagy rockmore újrafuttatás szükséges?

**02. lépés -- saját munkafolyamat megfigyelések:**

- NOTE 💬 HTML forrás letöltése helyi fájlba (`azad2012_webpage.html`) felesleges volt -- az NLM CLI csak URL-t fogad el webes tartalomnál, a helyi HTML fájlt visszautasítja. Token-pazarlás volt a helyi mentés. Ezentúl: weblap → URL direkten az NLM-be.
- NOTE 💬 `citations_seed.json` a 01. lépés outputja, de az ebben a futásban skip-elődött (user hozta a forrásokat) -- a seed nélkül a 02. lépés nem indítható el. A két lépés szorosan függ egymástól.

## 2026-05-26 -- Technical debt sprint (meta_file_updates branch)

**Elvégzett:**

- ✅ **B1 fix** `scripts/03-1_qfig_parser.py` v2: FIELD_RE Markdown-bold formátum (`*   **Forrás:**`) kezelése + FELIRAT/ÁBRA SZÁMA aliasok + `_keywords_from_text()` fallback (ha TÉMAKÖR hiányzik). Teszt: 15 entry parsed, 9 matched (Fourier_teszt).
- ✅ **S1** `scripts/generate_index.py`: ToC generálás (GFM anchor, accent-aware exclude) + figure insertion figure_catalog.json alapján.
- ✅ **S2** `scripts/14_bsc_filter.py`: `<!-- MSc -->` blokk, Mermaid `[MSc]` node és `SZINT:4-5` kérdés eltávolítás; `5_clean_outputs/` kiírás `_bsc` suffixszel.
- ✅ **A1 confirm**: `05_assemble.py` line 182 -- `## 0. Bevezetés` wrapper már megvan.
- ✅ **A2 confirm**: `04_nlm_dfs_queries.py` teljes DFS traversal már megvan (--resume, --sleep, RESOURCE_EXHAUSTED detekció).
- ✅ **A3** `nlm_prompts.md §4` Prompt D: NLM CLI szószedet ASCII query.
- ✅ **A4** `nlm_prompts.md §5` Prompt E: NLM CLI kérdésbank ASCII query.
- ✅ **M1** `templates/context_sablon.md`: 01-14 lépéscsoportok (01-02 / 03-04 / 05-07 / 08-10 / 11-12 / 13-14).
- ✅ **Q7 confirm**: `rule_b_bullet_whitespace()` v3.1 már kezeli a `*   **...` → `* **...` esetet.
- ✅ `pitfalls.md §3.4`: B1 fix dokumentálva.

**Nyitott:**
- 🔲 B2: NLM RESOURCE_EXHAUSTED --resume teszt (Termografia_teszt_v3)
- 🔲 R1, R2, R7: Termografia_teszt_v3 end-to-end futtatás (MinerU + NLM)
- 🔲 D1-D5: Architektúrális döntések (😎 jóváhagyás szükséges)

## 2026-05-25 -- Content quality session (feature/content-quality)

- ✅ `scripts/03b_qfig_parser.py` -- Qfig NLM output → figure_catalog caption+keywords *(átnevezve: `03-1_qfig_parser.py`; BOM+Markdown-bold fix 2026-05-26)*
- ✅ `scripts/03c_dedup_figures.py` -- hash-alapú figura deduplication (duplicate flag) *(átnevezve: `03-2_dedup_figures.py`)*
- ✅ `scripts/05_assemble.py` -- Q1-Q4 összefűzés, CLI-alapú, portábilis (hardcoded _assemble.py felváltja)
- ✅ `scripts/06b_table_caption_injector.py` -- GFM táblázat captionök FELÜLRE injektálása
- ✅ `scripts/09_figure_mapper.py` -- keyword × paragraph matching (dict-formátum javítva)
- ✅ `scripts/10_notes_collector.py` -- ToC generálás + figura beillesztés paragraph-koordináta alapján
- ✅ `scripts/11_typesetter.py` -- két fázis: bullet→próza (Claude API) + linting (Phase 1 megtartva)
- ✅ `scripts/12_pptx_gyarto.py` -- szegmens-alapú body: add_picture + add_table + text
- ✅ `scripts/util_heading_numberer.py` -- Roman-numeral double-prefix bug javítva
- ✅ `.claude/skills/04_nlm_query_runner.md` -- Qfig §4 hozzáadva, szekcióátszámozás, YAML name javítva
- ✅ `.claude/pipeline.md` -- v5.0: 03b/03c/05/06b lépések beillesztve, ⚠️ megjegyzés feloldva
- ✅ Git commit: `feature/content-quality` branch

## 2026-05-24 -- P1 pipeline output újragenerálás

- ✅ `scripts/regen_outputs.py` futtatva: 15+15 fájl újragenerálva ékezetes magyarral
- ✅ Ékezetsűrűség: 5-13% minden pipeline outputban (✓ küszöb: >1.5%)
- ✅ 0% maradék: `stumpy2024_webpage.md`, `rockmore1999_article.md` -- MinerU angol forrásanyag (helyes)

## 2026-05-24 -- Diagnosztika + kódolásjavítás

- ✅ pipeline.md: 55 mojibake csere (emoji + →); C1-control fallback logika
- ✅ pitfalls.md: 13 csere (§, →, á, é, Á, 🗺, 💡)
- ✅ 00c_mineru_extractor.md: 14 csere (§, →, Á, 🐍, 🔌)
- ✅ nlm_prompts.md: cím "es" → "és" (2x)
- ✅ .gitignore: `.raw_sources/` → `**/raw_sources/`, `.clean_sources/` → `**/clean_sources/`
- ✅ project_status.md: §Check + §Plan frissítve (diagnosztika eredményei)
- ❌ LELET: 15 pipeline output fájl 0% ékezetsűrűség -- újrafuttatás szükséges

## 2026-05-23 -- Meta-fájlok konszolidáció (2. kör)

- ✅ .claude/CLAUDE.md törölve -- tartalom root CLAUDE.md v3.0-ban
- ✅ pipeline.md: §6 Heti outputok törölve (duplikátum); NLM granularitás note + Nyitott kérdések szekció hozzáadva
- ✅ project_status.md: §4 Act + §5 Arch törölve (git history + CLAUDE.md lefedi)
- ✅ nlm_integration.md v2.1: YAML fix, --- elválasztók eltávolítva, Változásjegyzék táblává
- ✅ Nyitott kérdések elosztva: 06_notes_collector, 10_bsc_filter, 00b_nlm_notebook_setup, pipeline.md
- ✅ context_sablon.md: C00-C08 oszlopok → 00b/01/02/03-05/06-07/08/09/10
- ✅ git commit: 2 commit, összesen 329 sor törlés + 150 hozzáadás

## 2026-05-23 -- Workspace rendrakás

- ✅ Mappastruktúra refaktor: tests/, templates/, .claude/ konszolidáció
- ✅ test_sources_* → tests/*/forrasok/ (matrixprofil, dft, termografia, surge_stall_choke)
- ✅ matrixprofil_teszt_2 (kanonikus) → tests/matrixprofil/1_het/
- ✅ 1_Prezentacio.md + .pptx (teszt_1-ből) → tests/matrixprofil/1_het/
- ✅ templates/ létrehozva: du_template.pptx, context_sablon.md, project_status_sablon.md, assets/
- ✅ kepek_workflow.md v2.0: figure_pipeline_design.md + mineru_kepek_nevezektan.md beolvasztva
- ✅ pipeline.md v2.0: 01_nlm_query_runner, 00c, 05b beillesztve; IO táblázat hozzáadva
- ✅ CLAUDE.md újraírva master indexként (v2.0)
- ✅ git init + .gitignore
- ✅ Archivált: nlm-claude_integration_research.md, pipeline_next_steps.md, DFT_teszt*.md, _claude/, sablonok

## 2026-05-22 -- Teljes end-to-end pipeline-teszt (MP 1. hét)

- ✅ Mappastruktúra: matrixprofil_teszt/1_het/forrasok/ + Studio outputok
- ✅ 05_mindmap_manager: Export-Tool MD → Mermaid flowchart LR
- ✅ NLM lekérdezések (4 db, level-2): Áttekintés, Alapfogalmak, Algoritmusok, Alkalmazások
- ✅ 1_Jegyzet.md összeállítva (329 sor) + citations.json (6 forrás, UUID-ek)
- ✅ 06_notes_collector: Tárgymutató (22 anchor-link)
- ✅ 03_excerpt_block_maker: 13 💡 + 4 🗺️ blokk
- ✅ 07_typesetter: A=1, D=21 javítás
- ✅ 08_presentation_maker: 1_Prezentacio.md (14 dia) + 1_Prezentacio.pptx
- ✅ scripts/pptx_gyarto.py megírva (Marp MD → PPTX)
- ✅ 09_question_bank_collector: 1_Kerdesek.md (4 BSc + 2 MSc kérdés)
- ✅ 10_bsc_filter: bsc_export.py megírva + bsc/ feltöltve (4 fájl)

## 2026-05-21 -- NLM CLI integráció + DFT teszt

- ✅ NLM CLI integráció tesztelve (notebooklm-mcp-cli, Windows-MCP PowerShell hídon)
- ✅ DFT teszt 1 és 2: PASS
- ✅ **Kritikus lelet:** Prompt B (Configure Chat) hat a CLI-re
- ✅ nlm_prompts.md (rev2), nlm_integration.md (rev2), CLAUDE.md inkonzisztenciák javítva

## 2026-05-20 -- .claude/ megtisztítás

- ✅ NLM-only pipeline; nevezéktan és pipeline.md egységesítve

# 3. Check (tanulságok az utolsó futásból)

## 2026-05-25 -- feature_test_step_by_step: Fourier_teszt teljes pipeline futás (01-14)

| Komponens | Eredmény | Tanulság |
|:----------|:---------|:---------|
| 01-05 forrás + NLM + MinerU | ✅ | 3 forrás aktív (PPTX NLM-ből kizárva, null UUID) |
| 06 excerpt_block_maker | ✅ | Legpedagógiailag értékesebb lépés; Q1-hez `##` szülő hiánya miatt `🗺️` nem generálódott |
| 06b table_caption_injector | ✅ | `--` a caption-ban és `(automatikus felirat)` placeholder -- mindkettő javítandó |
| 07 citations_maker (szószedet) | ⚠️ | Claude-alapú, nem NLM-alapú -- nem auditálható, nem reprodukálható |
| 08 mindmap_manager | ✅ | Fourier_teszt: Studio export kész, `, N gyermek` suffix tisztítva, `4_wip_outputs/1_Mindmap.md` létezik |
| 09 figure_mapper | ❌→✅ | 0 kép Fourier_teszt-en (03-1_qfig_parser BOM+Markdown-bold hiba) -- javítva 2026-05-26 (B1 fix); Termografia_teszt_v3-on verifikálandó |
| 10 notes_collector (ToC) | ⚠️ | ToC hierarchikus számozás hiányzik; leading spaces Q1-nél (heading hierarchia bug) |
| 11 typesetter (lint-only) | ✅ | v3.0: Phase 1 kódból eltávolítva; Rule H (dash cleanup) implementálva; 305→186 sor |
| 12 presentation_maker (PPTX) | ⚠️ | Sablon nem alkalmazódott; raw Markdown szintaxis látható; TOC-dia hiányzik |
| 13 question_bank_collector | ⚠️ | Claude-alapú, nem NLM-query -- placeholder, újragenerálandó |
| 14 bsc_filter | ✅ | `scripts/14_bsc_filter.py` kész 2026-05-26; `_bsc` suffix konvenció rögzítve |
| ~~**Kritikus:** 03-1_qfig_parser~~ | ✅ | BOM + Markdown-bold fix 2026-05-26 (B1); Termografia_teszt_v3 verifikálandó |

## 2026-05-25 -- feature/content-quality: architektúrai döntések

### P4/P6 revízió: NLM ingyenes alternatíva a Claude Vision API helyett

**Probléma:** Az előző session P4/P6 tervei Claude Vision API hívásokat alkalmaznak (claude-sonnet-4-6) képenként → fizetős, lassú (131 kép × API hívás).

**Döntés:** Az NLM ingyenes és már látja a PDF forrásokat (szöveges és vizuális tartalmat egyaránt). Egy dedikált NLM figura-query (Qfig) kérhető a notebooktól:

```
"Sorold fel az összes ábrát, diagramot és táblázatot a forrásokban! Minden elemhez add meg:
a forrás nevét, az ábra számát (ha van), a captionját (ha van), és 1-2 mondatos leírását."
```

Ez a kimenet:
- Feldolgozható regex-szel → `keywords` + `caption` mezők a `figure_catalog.json`-ban
- Ingyenes (NLM kvóta terhére)
- Kontextuálisan gazdagabb (NLM ismeri az ábra körüli szöveget is)

**Következmény:**
- `scripts/03_build_figure_catalog.py --vlm` (Claude Vision API): elhalasztva / opcionális fallback
- `scripts/09_figure_mapper.py` algoritmusa változatlan marad (keywords × paragraph matching)
- Új lépés: **Qfig** query a `04_nlm_query_runner`-ben (Q1-Q4 mellett)
- P4/P6 státusza: script kész, de éles futtatás Qfig-alapú megközelítéssel tesztelendő

| | Vision API (régi terv) | NLM Qfig (új terv) |
|:--|:--|:--|
| Költség | Fizetős | Ingyenes |
| Sebesség | Lassú (131 hívás) | Egy query |
| Kontextus | Kép pixelei | Kép + körülötte lévő szöveg |
| Megbízhatóság | Magas (direkt látás) | Közepes (NLM értelmezi) |
| Implementáció | `--vlm` flag, kész | Qfig query + parser, TODO |

### _assemble.py: rossz helyen van, hiányzik a pipeline-ból

**Tünet:** `test_outputs/Termografia_teszt_v3/_assemble.py` létezik; a `scripts/` mappában nincs assembler; a pipeline 04→06 között nincs dokumentált lépés, pedig `N_Jegyzet.md` draft-ot valahogy létre kell hozni.

**Gyökérok:** Az assembler ad-hoc, tesztelés közben íródott, sosem lett formalizálva.

**Megoldás:**
- `_assemble.py` → `scripts/05_assemble.py` (átnevezés + CLI argumentumok, abs. path eltávolítás)
- Pipeline-ba beillesztés: `04_nlm_query_runner` → **05_assemble** → `05_source_controller` → `06_excerpt_block_maker`
- Skill fájl: `.claude/skills/05_assemble.md` (TODO)
- `_assemble.py` eredeti helye (`test_outputs/`) gitignore-d -- sosem volt a repóban

**Dokumentálva:** pipeline.md v4.0 -- ⚠️ jelöléssel a hiányzó lépésnél.

## 2026-05-22 -- MP 1. hét end-to-end teszt

| Komponens | Eredmény | Tanulság |
|:----------|:---------|:---------|
| NLM CLI + Prompt B | ✅ PASS | Strukturált citáció, LaTeX képletek, táblázatok jól működnek |
| 05_mindmap_manager | ✅ PASS | Export-Tool MD → Mermaid konverzió megbízható |
| 06_notes_collector | ✅ PASS | Anchor-link ékezetes magyar szövegre is helyes |
| 03_excerpt_block_maker | ✅ PASS | whitespace szabály (\n\n>) beépítve |
| 07_typesetter Rule D | ⚠️ 21 javítás | 03 whitespace fix után várhatóan csökken |
| 09_question_bank_collector | ✅ PASS | NLM BSc/MSc differenciált kérdések |
| 10_bsc_filter | ✅ PASS | Hármas szűrés (MSc blokk + Mermaid node + SZINT) rögtön jól működött |
| Citation globális sorszámozás | ❌ | NLM query-nként [1]-től számoz → UUID-dedup szükséges (04 skillben) |
| pptx_gyarto.py LaTeX | ❌ | python-pptx nem tud LaTeX-et -- elfogadott korlát |
| Képek | ❌ | PDF-ek hiányoztak → placeholder rendszer (kepek_workflow.md) |

## 2026-05-24 -- 3 hetes teszt diagnosztika (teljes scan)

| Komponens | Eredmény | Tanulság |
|:----------|:---------|:---------|
| pipeline.md emoji mojibake | ✅ JAVÍTVA | 55 csere (🚀👤🤖🐍🔌🛑💡✅⚠️→); C1-control fallback szükséges a 🐍-hez |
| pitfalls.md mojibake | ✅ JAVÍTVA | 13 csere; §6.1 példa-stringek részben javultak (mellékhatás) |
| 00c_mineru_extractor.md | ✅ JAVÍTVA | 14 csere |
| Összes skill fájl (15 db) | ✅ TISZTA | Nincs mojibake |
| NLM outputok (clean_sources) | ✅ OK | Helyes magyar ékezetekkel, táblázat + LaTeX + citáció ✓ |
| nlm_prompts.md Prompt B | ✅ SZÁNDÉKOS | ASCII ékezetnélküliség dokumentált (PowerShell compat.) |
| nlm_prompts.md cím | ✅ JAVÍTVA | "es" → "és" (2 helyen) |
| .gitignore raw/clean_sources | ✅ JAVÍTVA | `.raw_sources/` → `**/raw_sources/` (pont hiba) |
| **Pipeline outputok (15 fájl)** | ❌ **KRITIKUS** | **0% ékezetsűrűség** -- minden heti output ékezet nélküli magyar. Gyökérok: a pipeline-futás idején a skill fájlok mojibake-ben voltak → Claude ékezetnélkülien generált. Újrafuttatás szükséges. |
| matrixprofil Q4 | ⚠️ SZIMULÁLT | [SIM] flag -- valós NLM query nem futott le |
| citations.json | ⚠️ HIÁNYOS | `file` mező üres, `title` = 'source_1' generikus |

# Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-26 | 2.6 | Do §4: DFT DFS session + RESOURCE_EXHAUSTED; §5 Branch cleanup terv; P-elvek áthozva |
| 2026-05-25 | 2.5 | Check: Fourier_teszt 01-14 step-by-step tanulságok; Plan F1-F10 prioritások |
| 2026-05-25 | 2.3 | Check: NLM vs Vision API döntés + _assemble.py probléma dokumentálva |
| 2026-05-25 | 2.2 | feature/content-quality Do szekció; Plan P-státuszok frissítve |
| 2026-05-22 | 1.0 | Létrehozva: Do szekciók, következő lépések |
| 2026-05-23 | 2.0 | PDCA struktúra: Plan/Do/Check/Act; tanulságok táblázatba rendezve; pipeline_next_steps.md beolvasztva |
| 2026-05-23 | 2.1 | §4 Act + §5 Arch törölve (git history + CLAUDE.md/pipeline.md lefedi) |

## 2026-05-24 -- refactor/v2: teljes pipeline és meta-mappa refaktorálás

- ✅ Git branch: `refactor/v2` létrehozva
- ✅ Skill fájlok átnevezve: 00/00b/00c/01..10 → 01-14 prefixek
- ✅ Script fájlok átnevezve: `NN_script.py` konvenció
- ✅ `01_html_to_md.md` archivált (elavult skill)
- ✅ `kepek_workflow.md` → `03_mineru_extractor.md`-be beolvasztva, archivált
- ✅ `nlm_integration.md` → `02_nlm_notebook_setup.md`-be beolvasztva, archivált
- ✅ `03_run_mineru_pipeline.py`: `magic-pdf` → `mineru`, `1_raw_inputs/`, `2_clean_inputs/<forrás>/`
- ✅ `pipeline.md` v3.0: TODO-k eltávolítva, 01-14 lépések, IO táblázat aktív linkekkel
- ✅ `CLAUDE.md` v4.0: §0 Session indítás szekció, új mappastruktúra, 01-14 katalógus
- ✅ Mappastruktúra: `1_raw_inputs/` + `2_clean_inputs/` + `3_raw_outputs/` + `4_wip_outputs/` + `5_clean_outputs/`
- ✅ `test_outputs/` mint kimeneti gyökér mappa
- ⚠️ MinerU teszt (Termografia_teszt_v2): process futott, de 0 fájl keletkezett -- R2 tesztelés szükséges

## 2026-05-24 -- Termografia_teszt_v2 teljes pipeline futtatás

- ✅ Mappastruktúra: Termografia_teszt_v2/1_het/ + raw_sources/ + clean_sources/ + bsc/
- ✅ HTML forrás: Emissivity - Wikipedia, web_fetch-el mentve (képek nélkül -- SingleFile CLI teszt köv.)
- ✅ Fájlválogatás: 4 PDF + 3 URL (html) + 1 DOCX = 8 forrás (raw_sources-ban)
- ✅ 00b: NLM notebook létrehozva (ID: 21c5da9f), 9 forrás feltöltve (1 duplikátum), Prompt B aktív
- ✅ 01: Q1-Q4 NLM lekérdezések, 7.7-8.8% ékezetűség; Q2 numbered cit., Q1/3/4 inline cit.
- ✅ 02-07: Jegyzet (21590 char), Szószedet (15 fogalom), Mindmap (Mermaid, 6 node), Citations.json
- ✅ 08: Prezentáció (9 dia Marp MD + 105KB PPTX)
- ✅ 09: Kérdések (4 BSc + 2 MSc, LaTeX képletekkel)
- ✅ 10: BSc filter (Prezentáció -15 sor, Kérdések -17 sor)
- ✅ self_attention_log.md: 17 bejegyzés, 3 pitfall dokumentálva
- ⚠️ NYITOTT: SingleFile CLI teszt -- képeket tartalmazó HTML (user kérés)

## Do -- 2026-05-25 (feature/content-quality: minőségi réteg)

| # | Feladat | Eredmény |
|:--|:--------|:---------|
| P2 | JAMP forrás eltávolítása NLM notebookból (`nlm source delete`) + citations_seed.json | ✅ 3 forrás maradt; `nlm source list` ellenőrizve |
| P3 | Q1 query redesign: `04_nlm_query_runner.md` v1.2 -- bevezető/összefoglaló szerepkör; redundancia-szabály; §5.2 citations fallback frissítve; Q4 minta hozzáadva | ✅ |
| P1 | `11_typesetter.md` v2.0 -- kétfázisú működés (prose + linting) dokumentálva; `scripts/11_typesetter.py` megírva | ✅ |
| P4 | `scripts/03_build_figure_catalog.py` -- VLM bővítés: `--vlm` flag, `run_vlm_on_catalog()`, `vlm_done` + `inserted_after_paragraph` mezők | ✅ szintaxis OK |
| P6 | `09_figure_mapper.md` v2.0 teljes újraírás (VLM keywords × bekezdés matching); `scripts/09_figure_mapper.py` megírva | ✅ szintaxis OK |

Nem elvégzett (következő session):
- [ ] P5: HTML források NLM-be URL-ként (`nlm source add --url`)
- [ ] Q1-Q4 újrafuttatás a megtisztított (JAMP nélküli) notebookban
- [ ] `11_typesetter.py` éles futtatása a meglévő `4_wip_outputs/1_Jegyzet.md`-n
- [ ] `03_build_figure_catalog.py --vlm` futtatás (131 kép)
- [ ] `09_figure_mapper.py` futtatás a VLM catalog után

## Do -- 2026-05-25 (Termografia_teszt_v3 pipeline futás)

- [x] 1_raw_inputs -> 1_raw_inputs átnevezés (v3 mappa)
- [x] 03 MinerU: 4 PDF feldolgozva -> 2_clean_inputs/<stem>/auto/ (kettős nesting bug javítva)
- [x] 02 NLM notebook "Termografia_teszt_v3" létrehozva (ID: 15b84ae7...)
- [x] 02 Prompt B konfigurálva (Python subprocess)
- [x] 04 Q1-Q4 NLM lekérdezések -> 3_raw_outputs/ (Q1:5.6KB, Q2:3.4KB, Q3:3.9KB, Q4:3.6KB)
- [x] 05 citations_seed.json létrehozva (4 forrás + notebook meta)
- [x] 10 1_Jegyzet.md assembly -> 4_wip_outputs/ (18.5 KB)
- [x] 06 1_Szozedet.md -> 4_wip_outputs/ (4 KB)
- [x] 08 1_Mindmap.md -> 4_wip_outputs/ (3.1 KB)
- [x] 13 1_Kerdesek.md -> 4_wip_outputs/ (4 KB)
- [x] pitfalls.md §4.3 hozzáadva (MinerU kettős nesting)
- [x] scripts/03_run_mineru_pipeline.py javítva (clean_dir / pdf.stem -> clean_dir)

Nyitott:
- [ ] 1_Prezentacio.md + .pptx (12_pptx_gyarto.py)
- [ ] 14 BSc filter futtatása
- [ ] context.md v3 frissítése (notebook ID, státuszok)
- [ ] util_heading_numberer.py: dupla prefix bug (### I. -> ### 1.1. I.)
# 3. Plan -- következő session prioritások

_Frissítve: 2026-05-25 (feature_test_step_by_step session után)_

## Prioritások (Fourier_teszt tanulságai alapján)

| # | Feladat | Megjegyzés | Státusz |
|:--|:--------|:-----------|:--------|
| **F1** | **03-1_qfig_parser javítás** -- BOM + Markdown-bold formátum kezelése | KRITIKUS: képek nélkül a pipeline csonka | ✅ 2026-05-26 |
| **F2** | **NLM Studio Mindmap export** -- Ultra Explorer automatizálás (Claude in Chrome MCP?) | Architektúrai sarokkő | ✅ 2026-05-26 (manuális; `, N gyermek` cleanup dokumentálva) |
| **F3** | **Heading hierarchia fix** -- `05_assemble.py` Q1-hez `## Bevezetés` szülő VAGY Prompt B módosítás | ToC + excerpt_block_maker Q1 | ✅ 2026-05-26 |
| **F4** | **Dash cleanup Rule H** -- `11_typesetter.py` Rule H: `--` / `–` / `—` eltávolítás | Pipeline-széles probléma | ✅ 2026-05-25 |
| **F5** | **Phase 1 eltávolítás** -- `11_typesetter.py` Phase 1 (bullet→próza) kódból kivágni | User döntés: NLM long response elég | ✅ 2026-05-25 |
| **F6** | **Szószedet NLM-alapra** -- `07_citations_maker` → NLM Prompt C query + Studio panel mentés | Auditálhatóság, reprodukálhatóság | ⚙️ terv rögzítve (`07_citations_maker.md` NOTE) |
| **F7** | **Kérdésbank NLM-alapra** -- `13_question_bank_collector` NLM-query verzió | Jelenlegi placeholder | ⚙️ következő iteráció |
| **F8** | **PPTX architektúra döntés** -- XML placeholder mapping vs Pandoc vs Marp+Headless Chrome | `12_pptx_gyarto.py` jelenleg nem használja a sablont | ⚙️ következő iteráció |
| **F9** | **Camera-ready scope** -- minden végtermék `5_clean_outputs/` alá `_bsc` suffixszel | `14_bsc_filter.md`-ban rögzítve | ✅ 2026-05-26 (döntés dokumentálva) |
| **F10** | **`14_bsc_filter.py` script megírása** -- `_bsc` suffix konvencióval | Jelenleg manuális | ✅ 2026-05-26 |
| **F11** | **MinerU UX log** -- `mineru_run.log` automatikus írása | Start-Process empty CMD fix | ✅ 2026-05-26 |
| **F12** | **01-02 seed függőség** -- seed skip workaround dokumentálva | `01_references_collector.md` NOTE | ✅ 2026-05-26 |
| **F13** | **Studio audit trail** -- `04_nlm_query_runner.md` NOTE; válasz hossza config | dokumentáció | ✅ 2026-05-26 |
| **F14** | **Bullet whitespace Rule B** -- `11_typesetter.py` `*   **` → `* **` | lint rule | ✅ 2026-05-26 |
| **F15** | **Table caption n-dash** -- `06b_table_caption_injector.py` `--` → `:` | lint rule | ⚙️ következő iteráció |
| **F16** | **DFS NLM query resume** -- `--resume --sleep 5` flag a kvóta-limit miatt | pitfalls §2.8 | 🔲 holnap futtatandó |
| **F17** | **Git branch cleanup** -- main-re squash + régi ágak törlése | lásd §4 Branch-állapot | 🔲 |
| **F18** | **Automata elvárás dokumentálása** -- heurisztikák TILOSAK, minden lépés automatizálható kell legyen | feature/content-quality-ból áthozva | 🔲 pipeline.md-be |

# 4. Do -- 2026-05-26 (DFT_teszt DFS NLM session)

## DFT_teszt 04. lépés -- DFS query futás

- ✅ `04_nlm_dfs_queries.py` megírva: mindmap DFS parser + query builder + NLM caller
- ✅ Dry-run: 29 csomópont, helyes query szövegek (L0-L4 szintek)
- ✅ `Start-Process` blokkoló hiba feloldva: `-RedirectStandardOutput` nélkül fut (script saját logot ír)
- ✅ Q01-Q06 sikeresen lefutott (5-7 KB/query, összesen 6 DFS eredmény)
- ❌ Q07-Q29 RESOURCE_EXHAUSTED: Google NLM napi kvóta kimerült 6 query után
- ✅ 23 hibás (330 B) fájl törölve a `3_raw_outputs/`-ból
- ✅ `04_nlm_dfs_queries.py` v1.1: `--resume`, `--sleep`, RESOURCE_EXHAUSTED detektálás
- ✅ pitfalls.md §2.8 hozzáadva (RESOURCE_EXHAUSTED recovery folyamat)
- ✅ self-attention.log bejegyzések 15-16

## Git állapot -- 2026-05-26

| Branch | Állapot | Tartalom |
|:-------|:--------|:---------|
| `main` | base | A squash merge előtti állapot + squash commit (`5e622bb`) |
| `feature_test_step_by_step` | AKTUÁLIS (uncommitted: 52 M) | Fourier_teszt teljes session + DFS script |
| `feature/content-quality` | elavult, NEM mergelt main-re | 5 commit, P1-P6 prioritások -- értékes tartalom áthozva |
| `refactor/v2` | elavult, NEM mergelt main-re | 4 commit, régi mappakonvenció (raw_inputs vs 1_raw_inputs) -- már felülírt |

**Implicit feltételezés:** `feature/content-quality` tartalmát a `feature_test_step_by_step` már befogadta squash merge-ként (`5e622bb`); az ág maga felesleges, de a benne lévő P-elvek dokumentálva lent.

## Áthozott elvek -- feature/content-quality branch (nem volt main-en)

**Automata elvárás (branch célkitűzése):**
Branch célja: élethű `wip_outputs` -- utána pipeline teljes automatizálása.
**Heurisztikák TILOSAK** (pl. page_idx közelítés) -- minden lépés automatizálható kell legyen.

| # | Feladat | Automatizálható? | Státusz |
|:--|:--------|:----------------|:--------|
| P1 | 11_typesetter: WIP md -> olvasható próza (Claude API) | igen (API) | ✅ script + skill kész |
| P2 | JAMP forrás eltávolítás NLM notebookból + citations_seed-ből | igen (nlm CLI) | ✅ KÉSZ |
| P3 | Q1 query redesign: bevezető/összefoglaló csak | igen | ✅ KÉSZ |
| P4 | VLM captioning: képenként Claude vision -> caption | igen (API, lassú) | ✅ script kész; `--vlm` futtatás szükséges |
| P5 | HTML források NLM-be URL-ként | igen (nlm CLI) | 🔲 következő session |
| P6 | 09_figure_mapper: VLM keywords x NLM szöveg -> beillesztési pont | igen | ✅ script kész; P4 után futtatható |

# 5. Branch cleanup terv (következő session)

**Cél:** Egyetlen tiszta `main` ág; régi ágak törlése.

```
Lépés 1: git checkout feature_test_step_by_step
Lépés 2: git add -A && git commit -m "docs: 2026-05-26 DFT DFS session + branch cleanup terv"
Lépés 3: git checkout main
Lépés 4: git merge --squash feature_test_step_by_step
Lépés 5: git commit -m "feat: squash merge feature_test_step_by_step (DFT teszt + DFS + refactor)"
Lépés 6: git branch -d feature_test_step_by_step feature/content-quality refactor/v2
Lépés 7: git push origin main --force-with-lease (ha remote is frissítendő)
```

**Mikor:** Következő session elején, mielőtt bármi más work indul.
