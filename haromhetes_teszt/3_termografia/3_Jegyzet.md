---
title: 3_JEGYZET.MD -- Termografia
type: output
het: 3
updated: 2026-05-23
status: DRAFT
notebook: 21de071f-0bf0-4c31-b4c2-e24f9d6d542a
---

# 3. Heti Jegyzet -- Termografia

**Het:** 3. het | **Datum:** 2026-05-23 | **Statusz:** DRAFT

## Tanulasi celok

1. Megerteni a Stefan-Boltzmann torveny fizikai tartalmat.
2. Magyarazni az emisszivitas szerepet a pontatos homersekletsmeresen.
3. Azonositani a hokamera fo epitoelemet (detektor, objektiv, jelfeldolgozo).
4. Felsorolni tipikus ipari termografiai alkalmazasokat.
5. [MSc] Osszehasonlitani a hutott es nem hutott detektor muuszaki parameterieit.


<!-- Q:1 -->
## 2. Fizikai alapok

Az infravoros (IR) termografia az anyagok homersukletsugaraztasi teljesitmenyenek meresere epul. A **Stefan-Boltzmann torveny** szerint $W = \varepsilon \sigma T^4$. <sup>[[1]](#ref-1)</sup>

> **💡 Lenyeg:** Az emisszivitas ($\varepsilon$) az anyagspecifikus korrrekcios tenyezo -- helytelen beallitasa szisztematikus mersikust okoz.

<!-- Q:2 -->
## 3. Emisszivitas es meresihiba

Az **emisszivitas** az anyag valodi sugarzasanak aranya a feketetest-sugarzashoz kepest. Feluleti allapot, szog es hullhamhossz-fueggese jelentos. <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>

> **💡 Lenyeg:** Tukrozo feluletek (pl. csiszolt fem) alacssony emisszivitasuak ($\varepsilon < 0.1$), igy a kornyezet visszaverodeese dominalja a mert erteket.

> **🗺️ Fejezet osszegzes -- 3. Emisszivitas**

<!-- Q:3 -->
## 4. Hokamera felepitese

Fo egysegek: **IR objektiv** (germanium), **detektor** (mikrobolometer vagy hutott), **jelfeldolgozo egyseg**. <sup>[[1]](#ref-1)</sup> <sup>[[4]](#ref-4)</sup>

> **💡 Lenyeg:** A mikrobolometer nem hutott, ezert kompakt es olcso, de erzekenyseege alacsonyabb a hutott detektorcoknal.

> **[MSc]** InSb es MCT hutott detektorok MWIR/LWIR tartomanyban magasabb D* erteket ernek el. <sup>[[5]](#ref-5)</sup>

> **🗺️ Fejezet osszegzes -- 4. Hokamera**

<!-- Q:4 -->
## 5. Alkalmazasok

**Villamos diagnosztika**: kontakthiba, tulterhelesdetekciio kapcsoloszekrenyekben. **Epuletdiagnosztika**: hoszigetelesi hianyk azonositasa. **[MSc] PM rendszer**: periodikus hoterkepes-keszites trendkovetessel. <sup>[[2]](#ref-2)</sup>

> **💡 Lenyeg:** A termografiai vizsgalat beruhazo-baratsagos: egyetlen menetjarat-mentes, kontaktus nelkuli felveteelekkel kiterjedt hibakatasztert ad.

> **🗺️ Fejezet osszegzes -- 5. Alkalmazasok**


---

## Targymutatoo

- [3. Heti Jegyzet -- Termografia](#3-heti-jegyzet----termografia)
  - [2. Fizikai alapok](#2-fizikai-alapok)
  - [3. Emisszivitas es meresihiba](#3-emisszivitas-es-meresihiba)
  - [4. Hokamera felepitese](#4-hokamera-felepitese)
  - [5. Alkalmazasok](#5-alkalmazasok)

---

## Hivatkozasok

<a name="ref-1"></a>[1] FLIR (2020). *FLIR-IR-Thermography_How-It-Works.pdf*.
<a name="ref-2"></a>[2] Ismeretlen (2022). *HOKAMERA_ALAPOK_es_GYAKORLATI_ALKALMAZASOK_4.pdf*.
<a name="ref-3"></a>[3] Ismeretlen (2021). *Infrared Energy, Emissivity, Reflection & Transmission.pdf*.
<a name="ref-4"></a>[4] JAMP (2023). *JAMP-11-230.pdf*.
<a name="ref-5"></a>[5] Rogalski (2014). *sensors-14-12305.pdf*.

# Valtozasnaplo

| Datum | Verzio | Leiras |
|-------|--------|--------|
| 2026-05-23 | 1.0 | [SIM] Letrehozva (01-07 pipeline szimulacio) |
