---
title: 3_PREZENTACIO.MD -- Infravörös termográfia
type: output
het: 3
updated: 2026-05-24
status: DRAFT
notebook: 2af3a356-2a36-47f1-8adc-1da4bc44de72
---

# 3. Prezentáció -- Infravörös termográfia

**Hét:** 3. hét | **Dátum:** 2026-05-24 | **Státusz:** DRAFT

## 1. dia -- Bevezetés: az IR termográfia elve

Minden $T > 0\ K$ hőmérsékletű test elektromágneses sugárzást bocsát ki.

- Érintésmentes és roncsolásmentes mérés
- Infravörös tartomány: $0{,}75$--$1000\ \mu$m
- Valós időben alkalmazható

---

## 2. dia -- Stefan-Boltzmann: sugárzási teljesítmény

$$W = \varepsilon \sigma T^4$$

| Jelölés | Jelentés | Érték |
|:--------|:---------|:------|
| $\varepsilon$ | emisszivitás | $0$--$1$ |
| $\sigma$ | Stefan-Boltzmann állandó | $5{,}67 \cdot 10^{-8}\ \text{W/m}^2\text{K}^4$ |
| $T$ | abszolút hőmérséklet | [K] |

---

## 3. dia -- Emisszivitás: anyagspecifikus korrekció

- Fekete test: $\varepsilon = 1$
- Csiszolt acél: $\varepsilon \approx 0{,}1$
- Emberi bőr: $\varepsilon \approx 0{,}98$

**Alacsony $\varepsilon$ → a visszavert környezeti sugárzás dominálja a mért értéket!**

---

## 4. dia -- Hőkamera felépítése: főegységek

- **Objektív**: germániumlencse (IR-áteresztő, látható fényre átlátszatlan)
- **Detektor**: mikrobolométer (nem hűtött) vagy hűtött rendszer
- **Jelfeldolgozó**: NUC kalibráció, hőmérsékletté alakítás

---


| | Mikrobolométer | Hűtött (InSb/MCT) |
|:--|:---------------|:------------------|
| Ár | Olcsó | Drága |
| Érzékenység | Közepes | Magas |
| Hűtés | Nincs | LN₂ / Peltier |
| Tartomány | LWIR ($8$--$14\ \mu$m) | MWIR/LWIR |

---

## 6. dia -- Atmoszférikus ablakok

A levegő csak bizonyos hullámhosszokon áteresztő:

- **$1$--$5\ \mu$m** (MWIR): magas hőmérsékletű tárgyakhoz
- **$8$--$14\ \mu$m** (LWIR): szobahőmérsékletű tárgyakhoz

Üveg $>5\ \mu$m-en átlátszatlan → speciális optika szükséges.

---

## 7. dia -- Alkalmazások: ipari termográfia

- **Villamos diagnosztika**: kontakthiba, túlterhelés-detekció
- **Épületgépészet**: hőszigetelési hiányok azonosítása

---

## 8. dia -- Összefoglalás: mérési elvek

1. Emisszivitás helyes beállítása kötelező
2. Reflexiós korrekció: $\varepsilon = 1 - \rho$ (átlátszatlan testeknél)
3. Atmoszférikus ablak: $8$--$14\ \mu$m szobahőmérsékletű tárgyakhoz


# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-05-24 | 1.1 | Újragenerálva -- ékezetek javítva (08_presentation_maker) |
