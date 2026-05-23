---
title: DFT Teszt 2 -- Ábrahivatkozás és explicit forrásmegjelölés
type: teszt
notebook: DFT (c894e121-3c39-4da0-af74-b1f2c82ffa69)
query: DFT spektrális felbontás, bin-szélesség, Parseval-tétel
date: 2026-05-21
metaprompt: inline (query-ba ágyazva)
status: PASS
---

# DFT Teszt 2 -- Ábrahivatkozás és Explicit Forrásmegjelölés

**Notebook:** DFT
**Kérdés:** DFT spektrális felbontása (frekvencia-vödör, bin-szélesség) és Parseval-tétel
**Metaprompt módszer:** Inline (a `question` argumentumba ágyazva)
**Dátum:** 2026-05-21

---

## 1. Elemzés: mit sikerült elérni?

| Vizsgált képesség | Eredmény | Megjegyzés |
|---|---|---|
| Explicit forrásnév kiterjesztéssel | ✅ | `Heinzel-Spectrum and spectral density.pdf` |
| Oldalszám / szakaszszám hivatkozás | ✅ | pl. `7. oldal`, `254. szakasz`, `267. oldal` |
| Számozott ábrahivatkozás | ✅ | `1. ábra` (Heinzel, 5. oldal) |
| Táblázathivatkozás | ✅ | `Table 1` (Heinzel, 7. oldal) |
| Cím nélküli diagram jelölése | ✅ | "forrásban található cím nélküli diagram (419. szakasz után)" |
| Inline metaprompt hatékonysága | ✅ | Az instrukciókat követte |
| Configure Chat Custom Instructions | ❔ | Nem tesztelt -- webes UI-on kell beállítani |

**Összesítés: PASS** -- Az inline metaprompt elegendő az ábra- és forráshivatkozáshoz.

---

## 2. NLM válasz (nyers)

### A DFT spektrális felbontása (frekvencia-vödör és bin-szélesség)

A diszkrét Fourier-transzformáció (DFT) a folytonos jelet mintavételezett pontok sorozataként kezeli, és a frekvenciatartományban diszkrét értékekre bontja fel [Heinzel-Spectrum and spectral density.pdf, 7. oldal].

- **Frekvencia-felbontás ($f_{res}$):** Más néven **bin-szélesség**, amely azt a frekvenciaközt határozza meg, amelyen belül a DFT mintát vesz a jelből [Heinzel-Spectrum and spectral density.pdf, 10. oldal]. Értéke a mintavételi frekvencia ($f_s$) és a DFT-pontok számának ($N$) hányadosa:

$$f_{res} = \frac{f_s}{N}$$

[Heinzel-Spectrum and spectral density.pdf, 10. oldal]

- **Frekvencia-vödrök (bins):** A DFT kimenete $N/2 + 1$ számú komplex értékből áll, amelyek az $f_m = m \cdot f_{res}$ frekvenciájú vödröknek felelnek meg, ahol $m = 0 \dots N/2$ [Heinzel-Spectrum and spectral density.pdf, 10. oldal]. A "bin" kifejezés az egész számú frekvencia-indexre utal [Scaling of the DFT and Some More of Its Noteworthy Properties, 254. szakasz].

- **Fizikai értelmezés:** Minden egyes vödör egy adott frekvenciasáv energiáját gyűjti össze; a 0. index ($m=0$) a jel egyenáramú (DC) összetevőjének átlagát képviseli [Heinzel-Spectrum and spectral density.pdf, 15. oldal]. A frekvenciavödrök és a Hz-ben kifejezett frekvencia közötti kapcsolat:

$$f[k] = \frac{k}{N} f_s$$

[Scaling of the DFT and Some More of Its Noteworthy Properties, 267. oldal]

- **Vizualizáció:** A forrásban található **1. ábra** szemlélteti egy 1234 Hz-es szinuszos jel spektrumát, ahol a vízszintes tengely a frekvenciát mutatja logaritmikus skálán [Heinzel-Spectrum and spectral density.pdf, 5. oldal]. A **Table 1** összefoglalja a DFT kimenetek elnevezési konvencióit (PSD, PS, LSD, LS) és azok mértékegységeit [Heinzel-Spectrum and spectral density.pdf, 7. oldal].

### Parseval-tétel

- **Alapelv:** A jel teljes energiája megegyezik az időbeli minták négyzetösszegével, illetve a spektrális komponensek négyzetösszegével [Scaling of the DFT and Some More of Its Noteworthy Properties, 267. oldal].

- **Matematikai alak** (folytonos):

$$E_x = \int_{\mathbb{R}} |X(f)|^2 \, df$$

[Scaling of the DFT and Some More of Its Noteworthy Properties, 415. szakasz]

- **Diszkrét alkalmazás** (RMS a spektrumból):

$$x_{rms} = \sqrt{\frac{1}{n} \sum_{k=0}^{n-1} |x_k|^2}$$

[Scaling of the DFT and Some More of Its Noteworthy Properties, 268. oldal]

- **Cím nélküli diagram:** A forrásban található cím nélküli diagram (a 419. szakasz után) szemlélteti, hogy a spektrális felbontás változása hogyan befolyásolja a csúcsok magasságát a Parseval-tételnek megfelelő energiamegmaradás mellett [Scaling of the DFT and Some More of Its Noteworthy Properties, 419-420. szakasz].

---

## 3. Metaprompt audit

### 3.1. Alkalmazott inline metaprompt

```
INSTRUKCIOK: (1) Minden allitas utan jelold meg a pontos forrasfajl nevet
kiterjeszessel (pl. heinzel2003.pdf), oldalszammal ha elerheto.
(2) Ha a forrasban abra, diagram vagy tablazat talalhato, hivatkozz ra
explicit modon (pl. 'Az 1. abra mutatja...', 'Lasd: N. tablazat').
(3) Ha egy abra szamozatlan, ird: 'a forrasban talalhato cim nelkuli
diagram szerint'.
KERDES: Magyarazd el a DFT spektralis felbontasat...
```

**Megj.:** Ékezetek nélkül küldve (PowerShell kódolási probléma elkerülése).

### 3.2. Metaprompt vs. Configure Chat összehasonlítás

| Dimenzió | Inline metaprompt | Configure Chat (Prompt B) |
|---|---|---|
| Beállítás | 🤖 automatikus (Claude írja) | 👤 manuális (webes UI) |
| Hatókör | Egy lekérdezés | Minden lekérdezés a notebookban |
| Token-felhasználás | Magasabb (query-ben ismétlődik) | Alacsonyabb (rendszerszinten tárolt) |
| Fenntarthatóság | Minden hívásnál újra kell adni | Egyszeri beállítás |
| Ajánlott | Teszteléshez | Éles pipeline-hoz |

### 3.3. Következtetés

Az inline metaprompt **működik** és megbízhatóan vált ki ábra- és forráshivatkozásokat. A Prompt B beállítása a Configure Chat-ben **nem kötelező** a pipeline működéséhez, de éles használatnál ajánlott (kevesebb token, konzisztensebb viselkedés).

---

**conversation_id:** 893e9197-8651-40ea-9dbf-52e3f4120a35
