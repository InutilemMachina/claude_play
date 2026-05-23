---
title: 1_KERDESEK.MD -- Matrix Profile: Alapok es Alkalmazasok
type: output
het: 1
updated: 2026-05-22
status: DRAFT
---

# 1. Kerdesek -- Matrix Profile: Alapok es Alkalmazasok

**Het:** 1. het | **Datum:** 2026-05-22 | **Statusz:** DRAFT

## 1. BSc kerdések (SZINT:2-3)

**K1** SZINT:2
Mit ábrázol a Matrix Profile $P$ vektor?
A) Az idősor minden elemének abszolút értékét
B) Minden részsorozat legközelebbi nem-triviális szomszédjának z-normalizált Euklideszi távolságát
C) Az idősor mozgó átlagát
D) Az összes részsorozat átlagos távolságát egymástól

**Helyes:** B

**K2** SZINT:2
Mi a kizárási zóna (exclusion zone) szerepe a Matrix Profile számításban?
A) Csökkenti a számítási igényt a távolságprofil vágásával
B) Megakadályozza, hogy egy részsorozat önmagát találja meg legközelebbi szomszédjaként
C) Kizárja a negatív értékű idősor-szakaszokat
D) Normalizálja a távolságértékeket 0 és 1 közé

**Helyes:** B

**K3** SZINT:3
Melyik állítás igaz a STAMP és a STOMP algoritmusok összehasonlításában?
A) STOMP $O(n^2 \log n)$, STAMP $O(n^2)$ komplexitású
B) STAMP véletlenszerű, anytime jellege van; STOMP rendezett, $O(n^2)$ komplexitású
C) Mindkettő ugyanolyan komplexitású, csak a GPU-implementáció különbözik
D) STAMP csak diszkord keresésre, STOMP csak motívum keresésre alkalmas

**Helyes:** B

**K4** SZINT:3
Egy EKG-idősorban kóros szívveréseket kell automatikusan azonosítani. Melyik Matrix Profile tulajdonságot kell ehhez elsődlegesen vizsgálni?
A) A $P$ vektor globális minimumait (motívumok)
B) A $P$ vektor globális maximumait (diszkordok)
C) Az $I$ vektor értékeit (szomszéd-indexek)
D) A távolságprofil átlagértékét

**Helyes:** B

<!-- MSc -->
## 2. MSc kerdések (SZINT:4-5)

**K5** SZINT:4
A SCRIMP++ algoritmus Pre-SCRIMP fázisa milyen stratégiával gyorsítja a motívumkeresést?
A) GPU-párhuzamosítással dolgozza fel a teljes távolságmátrixot
B) Ritka mintavételezéssel gyorsan azonosítja a potenciális motívumokat, amelyeket a második fázis finomít
C) FFT-alapú konvolúcióval számítja az összes dot-product-ot egyszerre
D) Csak a z-normalizált távolságok felső kvartilisét vizsgálja

**Helyes:** B

**K6** SZINT:5
A FLUSS szemantikai szegmentációs algoritmus az MP Index ($I$) ívein alapul. Milyen matematikai mennyiség minimuma jelzi a rezsimváltás helyét, és miért?
A) Az ívek hosszának átlaga -- mert a hosszabb ívek átlépik a határt
B) Az adott ponton áthaladó ívek száma (arc count) -- mert rezsimváltásnál kevesebb ív lép át a határon, mint a stacionárius szakaszon belül
C) A $P$ vektor lokális szórása -- mert a határon az MP értékei megugranak
D) Az $I$ vektor gradiense -- mert az index ugrásszerűen változik a rezsimhatáron

**Helyes:** B
<!-- /MSc -->

## Valtozasnaplo

- 2026-05-22 -- Letrehozva (09_question_bank_collector, 4 BSc + 2 MSc kerdes)
