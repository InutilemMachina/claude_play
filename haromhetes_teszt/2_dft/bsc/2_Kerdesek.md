---
title: 2_KERDESEK.MD -- DFT és FFT
type: output
het: 2
updated: 2026-05-24
status: DRAFT
---

# 2. Kérdések -- DFT és FFT

**Hét:** 2. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

## 1. BSc kérdések (SZINT:2-3)

**K1** SZINT:2
Melyik állítás igaz a DFT-re?
A) Új matematikai transzformáció, amelyet az FFT helyettesített
B) Diszkrét adatokat idő- és frekvenciatartomány között képez; az FFT a hatékony számítási módszere
C) Csak valós bemeneti vektorokra alkalmazható
D) Kizárólag $N = 2^k$ hosszú bemeneten működik

**Helyes:** B

**K2** SZINT:2
Mennyivel csökkenti az FFT a DFT számítási igényét $N$ elemre?
A) $N^2$-ről $N/2$-re
B) $N^2$-ről $N \log N$-re
C) $N^3$-ről $N^2$-re
D) $N \log N$-ről $N$-re

**Helyes:** B

**K3** SZINT:3
Melyik területen alkalmazzák a DFT-t rezgésdiagnosztikában?
A) Kizárólag elektromos hálózatokban
B) Periodikus jelek frekvenciakomponenseinek szétválasztásában (pl. forgógép hibafrekvenciák azonosítása)
C) Digitális képek tömörítésében
D) Adatbázis-lekérdezések gyorsításában

**Helyes:** B

**K4** SZINT:3
Mire utal a spektrum egy adott csúcsa?
A) Az adott időpillanatban mért értékre
B) A jel egy adott frekvenciájú szinuszos komponensének amplitúdójára és fázisára
C) A jel várható értékére az adott frekvenciasávban
D) A minta hosszára

**Helyes:** B

## 2. MSc kérdések (SZINT:4-5)

**K5** SZINT:4
Hogyan csökkenti a Cooley-Tukey algoritmus az $N$ pontos DFT komplexitását?
A) Memóriacsökkentéssel és gyors IO-val
B) Az $N$-pontos DFT-t két $N/2$-pontos DFT-re bontja rekurzívan, $O(N^2)$-ről $O(N \log N)$-re csökkentve az igényt
C) Véletlen mintavételezéssel közelítő megoldást számít
D) Csak a nemnulla frekvenciakomponenseket számolja ki

**Helyes:** B

**K6** SZINT:5
Mi a konvolúciós tétel jelentősége a jelfeldolgozásban?
A) Lehetővé teszi a DFT és IDFT váltakozó alkalmazását
B) Időtartomány-konvolúció $\leftrightarrow$ frekvenciatartomány-szorzat: $O(N^2)$ szűrés $O(N \log N)$-re csökkenthető
C) Megmutatja, hogy minden szűrő frekvenciafüggetlen
D) Biztosítja, hogy az inverz DFT valós értéket ad vissza

**Helyes:** B


# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (09_question_bank_collector) |
