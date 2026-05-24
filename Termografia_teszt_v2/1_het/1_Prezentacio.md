---
marp: true
theme: default
paginate: true
---

# Infravörös Termográfia
### 1. hét -- Alapelvek és alkalmazások
_Termografia_teszt_v2 | 2026-05-24_

---

## Témakörök

1. Áttekintés -- mi a termográfia?
2. Sugárzásfizikai alaptörvények
3. Hőkamerák és méréstechnika
4. Gyakorlati alkalmazások

---

## 1. Áttekintés

**Infravörös termográfia:** érintésmentes hőmérési eljárás
- IR sugárzás → elektronikus jel → hőtérkép (termogram)
- Felületi hőmérséklet-különbségek detektálása

**Fizikai alap:**
- Minden test T > 0 K hőmérsékleten sugároz
- Sugárzás spektruma és intenzitása → hőmérséklet

---

## 2. Sugárzásfizikai alaptörvények

| Törvény | Képlet | Tartalom |
|:--------|:-------|:---------|
| Stefan-Boltzmann | E = εσT⁴ | Összsugárzás ~ T⁴ |
| Planck | L(λ,T) | Spektrális eloszlás |
| Wien | λ_max = b/T | Csúcshullámhossz |
| Kirchhoff | ε = α | Emisszió = abszorpció |

---

<!-- MSc -->
## [MSc] Emissziós tényező és mérési hiba

**Sugárzási egyenleg:** ε + ρ + τ = 1

- ε: emissziós tényező (anyagfüggő, 0--1)
- ρ: reflexió (fényes felületek hibaforrása!)
- τ: transzmisszió (üveg, gáz hatása)

**Hőmérsékleti hiba:** ΔT = f(ε_valós − ε_beállított)

_Forrás: flir_emissivity_guide.pdf, haraszti2013_termografia.pdf_
<!-- /MSc -->

---

## 3. Hőkamerák típusai

**Hűtött (Quantum) detektor:**
- MWIR (3--5 μm), InSb, MCT elemek
- NETD < 20 mK, nagyobb érzékenység
- Drágább, hűtési rendszer kell

**Hűtetlen (Thermal) detektor:**
- LWIR (8--14 μm), mikrobolométer
- NETD 50--80 mK, kompakt, olcsóbb
- Ipari karbantartásban preferált

---

## 4. Gyakorlati alkalmazások

```
Villamos diagnosztika  →  kötéshibák, transzformátor, napelem
Gépészeti karbantartás →  csapágyak, szivattyúk, hajtóművek
Épületdiagnosztika     →  hőhidak, nedvesedés, tetőszivárgás
Tudományos célok       →  anyagvizsgálat, K+F
```

**Kulcs:** rendellenes felmelegedés → korai beavatkozás → kár megelőzése

---

## Összefoglalás

- Termográfia: sugárzásfizikán alapuló, érintésmentes diagnosztikai eljárás
- 4 alaptörvény: Stefan-Boltzmann · Planck · Wien · Kirchhoff
- Mérési pontosság: emissziós szám helyes beállítása kritikus
- Széles alkalmazás: villamos · gépészet · épület · K+F

---

## Kérdések?

_Következő: részletes mérési protokoll és kalibrációs eljárások_

