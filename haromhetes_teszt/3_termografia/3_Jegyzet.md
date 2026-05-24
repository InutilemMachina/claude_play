---
title: 3_JEGYZET.MD -- Infravörös termográfia
type: output
het: 3
updated: 2026-05-24
status: DRAFT
notebook: 2af3a356-2a36-47f1-8adc-1da4bc44de72
---

# 3. Heti Jegyzet -- Infravörös termográfia

**Hét:** 3. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

## Tanulási célok

1. Megérteni a Stefan-Boltzmann törvény fizikai tartalmát és a képlet tagjai szerepét.
2. Megmagyarázni az emisszivitás szerepét a pontos hőmérséklet-mérésben.
3. Azonosítani a hőkamera főegységeit (detektor, objektív, jelfeldolgozó).
4. Felsorolni tipikus ipari termográfiai alkalmazásokat.
5. [MSc] Összehasonlítani a hűtött és nem hűtött detektor műszaki paramétereit.


<!-- Q:1 -->
## 2. Fizikai alapok

Az infravörös termográfia alapelve: minden $T > 0\ \text{K}$ hőmérsékletű test elektromágneses sugárzást bocsát ki. A **Stefan-Boltzmann törvény**: $W = \varepsilon \sigma T^4$. <sup>[[1]](#ref-1)</sup>

| Fogalom | Képlet | Forrás |
|:--------|:-------|:-------|
| Stefan-Boltzmann (valós test) | $W = \varepsilon \sigma T^4$ | [1] |
| Stefan-Boltzmann állandó | $\sigma = 5{,}67 \cdot 10^{-8}\ \text{W m}^{-2}\text{K}^{-4}$ | [1] |
| Wien eltolódási törvény | $\lambda_m = 2897\ \mu\text{m}\cdot\text{K} / T$ | [1] |
| Kirchhoff sugárzási törvénye | $\alpha + \rho + \tau = 1$ | [1] |

> **💡 Lényeg:** Az emisszivitás ($\varepsilon$) az anyagspecifikus korrekciós tényező -- helytelen beállítása szisztematikus mérési hibát okoz.

<!-- Q:2 -->
## 3. Emisszivitás és mérési hiba

Az **emisszivitás** a valódi test sugárzásának aránya az ideális fekete test sugárzásához képest ($\varepsilon \in [0,1]$). Felületi állapot-, szög- és hullámhossz-függése jelentős. <sup>[[1]](#ref-1)</sup>

Átlátszatlan testeknél: $\tau = 0$ → $\varepsilon = \alpha = 1 - \rho$.

> **💡 Lényeg:** Tükröző felületek (pl. csiszolt fém, $\varepsilon < 0{,}1$) esetén a visszavert környezeti sugárzás dominálhatja a mért értéket -- ez a leggyakoribb mérési hiba forrása.

> **🗺️ Fejezet összegzés -- 3. Emisszivitás**

<!-- Q:3 -->
## 4. Hőkamera felépítése

Főegységek: **IR objektív** (germániumlencse), **detektor** (mikrobolométer vagy hűtött), **jelfeldolgozó egység** (NUC, kalibrálás). <sup>[[1]](#ref-1)</sup>

> **💡 Lényeg:** A mikrobolométer nem hűtött, ezért kompakt és olcsó, de érzékenysége alacsonyabb a hűtött detektorokénál.

> **[MSc]** InSb és MCT hűtött detektorok MWIR/LWIR tartományban magasabb $D^*$ értéket érnek el; folyékony nitrogén vagy Peltier-hűtés szükséges. <sup>[[1]](#ref-1)</sup>

> **🗺️ Fejezet összegzés -- 4. Hőkamera**

<!-- Q:4 -->
## 5. Alkalmazások

**Villamos diagnosztika**: kontakthiba, túlterhelés-detekció kapcsolószekrényekben. **Épületgépészet**: hőszigetelési hiányok azonosítása. **[MSc] PM rendszer**: periodikus hőtérképes-készítés trendkövetéssel. <sup>[[1]](#ref-1)</sup>

> **💡 Lényeg:** A termográfiai vizsgálat beruhazóbarát: egyetlen menetjárat-mentes, érintésmentes felvétellel kiterjedt hibakatasztert ad.

> **🗺️ Fejezet összegzés -- 5. Alkalmazások**


---

## Tárgymutató

- [2. Fizikai alapok](#2-fizikai-alapok)
- [3. Emisszivitás és mérési hiba](#3-emisszivitas-es-meresi-hiba)
- [4. Hőkamera felépítése](#4-hokamera-felepitese)
- [5. Alkalmazások](#5-alkalmazasok)

---

## Hivatkozások

<a name="ref-1"></a>[1] Ismeretlen szerző (2021). *Műszaki Diagnosztika II -- A termográfia elméleti alapjai*. 10-Termografia-1.pdf.


# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (01-07 pipeline) |
