"""
regen_outputs.py -- Regenerálja az összes heti pipeline output fájlt
                    helyes magyar ékezetekkel, az NLM query outputok alapján.
2026-05-24
"""
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
WEEKS = {
    "1_matrixprofil": {
        "n": 1, "tema": "Matrix Profile",
        "ref1": '[1] STUMPY Documentation (2024). *STUMPY Basics Tutorial*. stumpy2024_webpage.',
        "uuid": "013ea69e-ee02-4a13-9389-7f46d7fb37ae",
    },
    "2_dft": {
        "n": 2, "tema": "DFT és FFT",
        "ref1": '[1] Rockmore, D. N. (1999). "The FFT -- An Algorithm the Whole Family Can Use." '
                '*Computing in Science & Engineering*, 1(1), 24--30. rockmore1999_article.pdf.',
        "uuid": "9447f8a8-d261-4522-8cc6-862befe1aabe",
    },
    "3_termografia": {
        "n": 3, "tema": "Infravörös termográfia",
        "ref1": '[1] Ismeretlen szerző (2021). *Műszaki Diagnosztika II -- '
                'A termográfia elméleti alapjai*. 10-Termografia-1.pdf.',
        "uuid": "2af3a356-2a36-47f1-8adc-1da4bc44de72",
    },
}

DATE = "2026-05-24"

# ─── CONTENT DEFINITIONS ──────────────────────────────────────────────────────

SZOZEDET = {
    "1_matrixprofil": """\
| Magyar terminus | Angol terminus | Definíció | Szint |
|:----------------|:---------------|:----------|:------|
| *Matrix Profile* | *Matrix Profile* | Vektor, amely minden részsorozat és legközelebbi szomszédja közötti z-normalizált euklideszi távolságot tárolja; $O(n)$ térkomplexitás. | BSc |
| *részsorozat* | *subsequence* | Az idősor $m$ hosszúságú ablakkal kivágott szegmense: $T[i:i+m]$. | BSc |
| *motívum* | *motif* | Visszatérő minta: a Matrix Profile globális minimumát adó részsorozat-pár. | BSc |
| *anomália* | *anomaly / discord* | Ritka, szokatlan részsorozat: a Matrix Profile globális maximumát adó elem. | BSc |
| *euklideszi távolság* | *Euclidean distance* | $D_{i,j} = \\sqrt{\\sum_{k=0}^{m-1}(T_{i+k}-T_{j+k})^2}$; a részsorozatok hasonlóságának alapmértéke. | BSc |
| *z-normalizálás* | *z-normalization* | Középre igazítás és egységnyi szórásra skálázás; amplitúdófüggetlen összehasonlítást tesz lehetővé. | BSc |
| *STOMP* | *STOMP (Scalable Time series Ordered Matrix Profile)* | 2016-os egzakt algoritmus; $O(n^2)$ idő, $O(n)$ memória; STUMPY magja. | MSc |
| *SCRUMP* | *SCRUMP* | Közelítő, gyors Matrix Profile számítás; sebesség-kritikus esetekre. | MSc |
| *Profile Index* | *Profile Index* | A Matrix Profile kísérőtömbje: minden elemhez tárolja a legközelebbi szomszéd indeksét. | MSc |
""",
    "2_dft": """\
| Magyar terminus | Angol terminus | Definíció | Szint |
|:----------------|:---------------|:----------|:------|
| *Diszkrét Fourier-transzformáció* | *Discrete Fourier Transform (DFT)* | $N$ hosszú komplex vektort frekvenciatartományba képez: $\\hat{X}(k)=\\sum_{j=0}^{N-1}X(j)W_N^{jk}$. | BSc |
| *Gyors Fourier-transzformáció* | *Fast Fourier Transform (FFT)* | A DFT hatékony számítási algoritmusa; $O(N^2)$ helyett $O(N \\log N)$ művelet. | BSc |
| *Fourier-mátrix* | *Fourier matrix* | $W_N = \\exp(2\\pi i/N)$ gyök egységei által alkotott unitér mátrix; DFT = $W_N \\cdot X$. | BSc |
| *inverz DFT* | *IDFT* | $X(j) = \\frac{1}{N}\\sum_{k=0}^{N-1}\\hat{X}(k)W_N^{-jk}$; frekvencia→idő visszatranszformálás. | BSc |
| *Cooley-Tukey algoritmus* | *Cooley-Tukey algorithm* | Az FFT legismertebb változata; $N = N_1 N_2$ felbontással rekurzív 2D DFT-vé alakítja az 1D DFT-t. | MSc |
| *butterfly-diagram* | *butterfly diagram* | Az FFT adatfolyam-grafikonja; jelzi, hogy mely elemeket kell összevonni az egyes lépésekben. | MSc |
| *spektrális szivárgás* | *spectral leakage* | Nem egész frekvenciánál megjelenő energiaszóródás; ablakfüggvényekkel csökkenthető. | MSc |
| *konvolúciós tétel* | *convolution theorem* | Időtartomány konvolúciója $\\leftrightarrow$ frekvenciatartomány szorzat; $O(N^2)$ → $O(N \\log N)$. | MSc |
""",
    "3_termografia": """\
| Magyar terminus | Angol terminus | Definíció | Szint |
|:----------------|:---------------|:----------|:------|
| *emisszivitás* | *emissivity* | Anyagspecifikus szám ($\\varepsilon \\in [0,1]$): a valódi test és a fekete test sugárzásának aránya. | BSc |
| *Stefan-Boltzmann törvény* | *Stefan-Boltzmann law* | $W = \\varepsilon \\sigma T^4$; a kisugárzott teljesítmény az abszolút hőmérséklet negyedik hatványával arányos. | BSc |
| *infravörös sugárzás* | *infrared radiation* | Elektromágneses sugárzás $0{,}75$--$1000\\ \\mu$m tartományban; hőkamerák érzékelési alapja. | BSc |
| *mikrobolométer* | *microbolometer* | Nem hűtött ellenállás-alapú IR detektor; kompakt és olcsó, de alacsonyabb érzékenységű. | BSc |
| *germániumlencse* | *germanium lens* | IR-áteresztő ($8$--$14\\ \\mu$m), látható fényre átlátszatlan optikai elem; hőkamerák objektívje. | BSc |
| *Planck-féle sugárzási törvény* | *Planck radiation law* | $I(\\nu,T)=\\frac{2h\\nu^3}{c^2}\\frac{1}{e^{h\\nu/kT}-1}$; a feketetest spektrális emisszióját írja le. | MSc |
| *Wien-féle eltolódási törvény* | *Wien displacement law* | $\\lambda_m = b/T$, ahol $b = 2897\\ \\mu\\text{m}\\cdot\\text{K}$; a sugárzási csúcs hullámhosszát adja meg. | MSc |
| *NUC korrekció* | *Non-Uniformity Correction* | Detektor-pixel egyenetlenségek kalibrációs eljárása; éles, pontos hőkép előfeltétele. | MSc |
| *Kirchhoff sugárzási törvénye* | *Kirchhoff's radiation law* | $\\alpha + \\rho + \\tau = 1$; az elnyelt, visszavert és áteresztett sugárzás összege egységnyi. | MSc |
""",
}

MINDMAP = {
    "1_matrixprofil": """\
```mermaid
flowchart LR
  MP["Matrix Profile"]
  MP --> DEF["Definíció"]
  DEF --> VECT["Távolságvektor O(n)"]
  DEF --> IDX["Profile Index"]
  DEF --> ZNORM["z-normalizált euklideszi távolság"]
  MP --> ALGO["Algoritmusok"]
  ALGO --> STOMP["STOMP -- egzakt O(n²)"]
  ALGO --> SCRUMP["SCRUMP -- közelítő"]
  ALGO --> BF["[MSc] Brute Force O(n²m)"]
  MP --> MUVELET["Műveletek"]
  MUVELET --> MOTIV["Motívumkeresés (min)"]
  MUVELET --> ANOM["Anomáliadetektálás (max)"]
  MUVELET --> SZEGM["[MSc] Szemantikus szegmentáció"]
  MP --> IMPL["Implementáció"]
  IMPL --> STUMPY["STUMPY (Python)"]
  IMPL --> GPU["[MSc] GPU/Dask párhuzamosítás"]
```
""",
    "2_dft": """\
```mermaid
flowchart LR
  DFT["DFT és FFT"]
  DFT --> DEFINICIO["Definíció"]
  DEFINICIO --> KEPLET["X̂(k) = Σ X(j)W_N^jk"]
  DEFINICIO --> MATRIX["Fourier-mátrix W_N"]
  DEFINICIO --> IDFT["Inverz DFT"]
  DFT --> FFT["FFT algoritmusok"]
  FFT --> CT["Cooley-Tukey (1965)"]
  FFT --> KOMPLEX["O(N²) → O(N log N)"]
  FFT --> BUTTERFLY["[MSc] Butterfly-diagram"]
  DFT --> ALKAL["Alkalmazások"]
  ALKAL --> JELFELDOLG["Jelfeldolgozás (MP3, modem)"]
  ALKAL --> KEPFELDOLG["Képfeldolgozás (MRI)"]
  ALKAL --> GEOFIZ["[MSc] Geofizika, csillagászat"]
  DFT --> TULAJD["Tulajdonságok"]
  TULAJD --> KONV["[MSc] Konvolúciós tétel"]
  TULAJD --> SZIVARGAS["[MSc] Spektrális szivárgás"]
```
""",
    "3_termografia": """\
```mermaid
flowchart LR
  TERMO["Infravörös termográfia"]
  TERMO --> FIZIKA["Fizikai alapok"]
  FIZIKA --> STEFAN["Stefan-Boltzmann: W=εσT⁴"]
  FIZIKA --> EMISSZ["Emisszivitás ε ∈ [0,1]"]
  FIZIKA --> KIRCHH["[MSc] Kirchhoff: α+ρ+τ=1"]
  FIZIKA --> PLANCK["[MSc] Planck-görbe"]
  FIZIKA --> WIEN["[MSc] Wien: λ_m=b/T"]
  TERMO --> KAMERA["Hőkamera felépítése"]
  KAMERA --> OBJEKT["IR objektív (germánium)"]
  KAMERA --> BOLOM["Mikrobolométer (nem hűtött)"]
  KAMERA --> HUTOTT["[MSc] Hűtött detektor (InSb, MCT)"]
  KAMERA --> NUC["[MSc] NUC korrekció"]
  TERMO --> MERESHIBAK["Mérési korlátok"]
  MERESHIBAK --> REFLEXIO["Reflexió (alacsony ε)"]
  MERESHIBAK --> ATMO["Atmoszférikus ablakok"]
  MERESHIBAK --> UVEG["Üveg: átlátszatlan >5 μm"]
  TERMO --> APP["Alkalmazások"]
  APP --> VILLAMOS["Villamos diagnosztika"]
  APP --> EPULET["Épületgépészet"]
  APP --> GEPESZET["Gépészeti PM"]
```
""",
}

KERDESEK = {
    "1_matrixprofil": """\
## 1. BSc kérdések (SZINT:2-3)

**K1** SZINT:2
Mit tárol a Matrix Profile minden eleme?
A) Az idősor adott pontjának értékét
B) A részsorozat és legközelebbi szomszédja közötti z-normalizált euklideszi távolságot
C) A részsorozat átlagát és szórását
D) Az idősor globális minimumát

**Helyes:** B

**K2** SZINT:2
Mire utal a Matrix Profile globális minimuma?
A) A leghosszabb monoton szakaszra
B) A legismétlődőbb mintapárra (motívumra)
C) A legzajosabb adatpontra
D) Az idősor trendjére

**Helyes:** B

**K3** SZINT:3
Miért előnyös a z-normalizált euklideszi távolság a nyers euklideszi távolsággal szemben?
A) Gyorsabb számítani
B) Amplitúdófüggetlen: azonos formájú, de különböző skálájú részsorozatok is hasonlónak minősülnek
C) Kevesebb memóriát igényel
D) Pontosabb anomáliadetektáláshoz vezet

**Helyes:** B

**K4** SZINT:3
Mi a különbség a STOMP és a Brute Force algoritmus komplexitása között?
A) Mindkettő $O(n^2)$, de különböző konstanssal
B) STOMP $O(n^2)$, Brute Force $O(n^2 m)$ -- STOMP a belső hurkot vektorizálással kerüli el
C) STOMP $O(n \\log n)$, Brute Force $O(n^2)$
D) STOMP párhuzamos, Brute Force szekvenciális -- egyébként azonos

**Helyes:** B

## 2. MSc kérdések (SZINT:4-5)

**K5** SZINT:4
Miben tér el a SCRUMP a STOMP-tól?
A) SCRUMP egzakt, STOMP közelítő
B) SCRUMP közelítő (approximate) és gyorsabb; STOMP egzakt, de lassabb
C) SCRUMP csak GPU-n fut; STOMP CPU-n is
D) SCRUMP csak anomáliadetektálásra, STOMP csak motívumkeresésre alkalmas

**Helyes:** B

**K6** SZINT:5
Mit tárol a Profile Index, és mire használható?
A) A részsorozatok amplitúdóját; normalizáláshoz
B) Minden elemhez a legközelebbi szomszéd indeksét; visszakeresésre és vizualizációhoz
C) Az egyes elemek kiszámítási sorrendjét; párhuzamosításhoz
D) A távolságmátrix sávszélességét; memóriaoptimalizáláshoz

**Helyes:** B
""",
    "2_dft": """\
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
B) $N^2$-ről $N \\log N$-re
C) $N^3$-ről $N^2$-re
D) $N \\log N$-ről $N$-re

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
B) Az $N$-pontos DFT-t két $N/2$-pontos DFT-re bontja rekurzívan, $O(N^2)$-ről $O(N \\log N)$-re csökkentve az igényt
C) Véletlen mintavételezéssel közelítő megoldást számít
D) Csak a nemnulla frekvenciakomponenseket számolja ki

**Helyes:** B

**K6** SZINT:5
Mi a konvolúciós tétel jelentősége a jelfeldolgozásban?
A) Lehetővé teszi a DFT és IDFT váltakozó alkalmazását
B) Időtartomány-konvolúció $\\leftrightarrow$ frekvenciatartomány-szorzat: $O(N^2)$ szűrés $O(N \\log N)$-re csökkenthető
C) Megmutatja, hogy minden szűrő frekvenciafüggetlen
D) Biztosítja, hogy az inverz DFT valós értéket ad vissza

**Helyes:** B
""",
    "3_termografia": """\
## 1. BSc kérdések (SZINT:2-3)

**K1** SZINT:2
Mit fejez ki az emisszivitás ($\\varepsilon$)?
A) A hőkamera mérési pontosságát
B) A valódi test sugárzásának arányát az ideális fekete test sugárzásához képest ($\\varepsilon \\in [0,1]$)
C) Az infravörös sugárzás frekvenciáját
D) A Stefan-Boltzmann állandó értékét

**Helyes:** B

**K2** SZINT:2
Miért használnak germániumlencsét hőkamerákban?
A) A germánium olcsó és könnyen megmunkálható
B) A germánium IR-tartományban ($8$--$14\\ \\mu$m) áteresztő, látható fényre átlátszatlan
C) A germánium UV-tartományban is áteresztő
D) A germánium nagy emisszivitású

**Helyes:** B

**K3** SZINT:3
Mire kell odafigyelni csiszolt fémfelületek termográfiai mérésekor?
A) Az emisszivitás 1-re állítására
B) A reflexió miatt kis emisszivitású felületeknél a visszavert környezeti sugárzás dominálja a mért értéket -- pontatlán emisszivitás-beállítás szisztematikus hibát okoz
C) Az érzékenység növelésére
D) A Planck-görbe eltolódására

**Helyes:** B

**K4** SZINT:3
Miért nem lehet hőkamerával üvegen "átlátni"?
A) Az üveg elnyeli az infravörös sugárzást a látható tartományban
B) Az üveg $5\\ \\mu$m felett (különösen $10\\ \\mu$m környékén) gyakorlatilag átlátszatlan az IR sugárzásra
C) Az üveg visszaveri a hősugárzást
D) Az üveg emisszivitása nulla

**Helyes:** B

## 2. MSc kérdések (SZINT:4-5)

**K5** SZINT:4
Hogyan működik a mikrobolométer?
A) Fotoelektromos hatással elektronokat állít elő
B) Az IR sugárzás felmelegíti az érzékelőelemet; az ellenállás-változásból számítják a hőmérsékletet
C) Kristályrács-rezgéssel méri a hőmérsékletet
D) Kettős rétegű piezo-effektussal detektál

**Helyes:** B

**K6** SZINT:4
Mit ír le a Kirchhoff-féle sugárzási törvény ($\\alpha + \\rho + \\tau = 1$), és mi következik belőle átlátszatlan testekre?
A) A hőmérséklet és emisszivitás kapcsolatát; átlátszatlan testekre $\\varepsilon = \\alpha$
B) A beérkező sugárzás sorsát (elnyelés + visszaverés + áteresztés = 1); átlátszatlan testekre ($\\tau=0$): $\\varepsilon = \\alpha = 1 - \\rho$ -- a nagy reflexió csökkenti a tényleges emisszivitást
C) A sugárzási teljesítmény és hőmérséklet összefüggését
D) Az optikai anyagok sávszélességét

**Helyes:** B
""",
}

PREZENTACIO = {
    "1_matrixprofil": """\
## 1. dia -- Mi a Matrix Profile?

Minden részsorozat-pár legjobb szomszédjának távolsága -- egyetlen vektorban.

- Távolságvektor: $O(n)$ méret
- z-normalizált euklideszi távolság
- Kísérő Profile Index: szomszéd indeksei

---

## 2. dia -- Motívum és anomália

A Matrix Profile két alapvető bányászati művelete:

| Érték | Interpretáció | Alkalmazás |
|:------|:--------------|:-----------|
| Globális **minimum** | Legismétlődőbb minta | Motívumkeresés |
| Globális **maximum** | Legszokatlanabb szakasz | Anomáliadetektálás |

---

## 3. dia -- z-normalizálás: miért szükséges?

Amplitúdófüggetlen összehasonlítás:

$$\\hat{T}_i = \\frac{T_i - \\mu}{\\sigma}$$

- Azonos alakú, különböző léptékű részsorozatok → hasonlónak ítélve ✓
- Nyers euklideszi távolság: amplitúdókülönbség dominál ✗

---

## 4. dia -- STOMP vs. Brute Force

| Algoritmus | Időkomplexitás | Memória |
|:-----------|:---------------|:--------|
| Brute Force | $O(n^2 m)$ | $O(n^2)$ |
| **STOMP** | $O(n^2)$ | $O(n)$ |

5 év adat brute force-szal: **4,4 év** számítási idő, **11,1 PB** memória.

---

## 5. dia -- [MSc] STUMPY: párhuzamos implementáció

- Numba JIT + Dask: CPU/GPU párhuzamosítás
- Akár 256 CPU mag vagy több GPU
- SCRUMP: közelítő, sebesség-kritikus esetekre

---

## 6. dia -- Alkalmazások

- **Motívumkeresés:** ismétlődő gépviselkedés-minták
- **Anomáliadetektálás:** ritkán előforduló hibaminták
- **[MSc] Szemantikus szegmentáció:** viselkedésállapot-váltások automatikus azonosítása

---

## 7. dia -- Összefoglalás

1. Matrix Profile = távolságvektor + Profile Index
2. z-normalizálás → amplitúdófüggetlen összehasonlítás
3. STOMP: $O(n^2)$, egzakt, párhuzamosítható (STUMPY)
4. Min → motívum; Max → anomália
""",
    "2_dft": """\
## 1. dia -- DFT: idő- és frekvenciatartomány

Az idő→frekvencia transzformáció alapja:

$$\\hat{X}(k) = \\sum_{j=0}^{N-1} X(j) \\cdot W_N^{jk}, \\quad W_N = e^{2\\pi i/N}$$

- $N$ komplex szám → $N$ frekvenciakomponens
- Mátrixszorzatként: $\\hat{X} = W_N \\cdot X$

---

## 2. dia -- FFT: az algoritmikus forradalom

Közvetlen DFT vs. FFT:

| Módszer | Műveletek |
|:--------|:----------|
| Közvetlen DFT | $N^2$ |
| **FFT (Cooley-Tukey)** | $N \\log N$ |

$N = 10^6$: $10^{12}$ → $2 \\cdot 10^7$ művelet (**50 000-szeres gyorsulás**).

---

## 3. dia -- Cooley-Tukey: rekurzív felbontás

$N$-pontos DFT → két $N/2$-pontos DFT:

$$\\hat{X}(k) = \\hat{X}_{\\text{páros}}(k) + W_N^k \\cdot \\hat{X}_{\\text{páratlan}}(k)$$

- "Oszd meg és uralkodj" elv
- **[MSc]** Butterfly-diagram vizualizálja az adatfolyamot

---

## 4. dia -- Alkalmazások: mérnöki területek

| Terület | Példa |
|:--------|:------|
| Jelanalízis | Rezgésdiagnosztika, spektrumelemzés |
| Hang/kép | MP3 tömörítés, MRI rekonstrukció |
| Geofizika | Szeizmológia, nukleáris teszt-detektálás |
| **[MSc]** Csillagászat | LIGO gravitációs hullámok, interferometria |

---

## 5. dia -- [MSc] Konvolúciós tétel

Időtartomány konvolúció $\\leftrightarrow$ frekvenciatartomány szorzat:

$$(f * g)(t) \\xrightarrow{\\mathcal{F}} F(\\omega) \\cdot G(\\omega)$$

**Szűrés $O(N^2)$ helyett $O(N \\log N)$-re csökkentve.**

---

## 6. dia -- Összefoglalás

1. DFT: $N$ pont → $N$ frekvenciakomponens; $O(N^2)$
2. FFT: ugyanaz, $O(N \\log N)$; Cooley-Tukey 1965
3. IDFT: visszatranszformálás; számítása = DFT($\\hat{X}(-k)$)
4. **[MSc]** Konvolúciós tétel → gyors digitális szűrés alapja
""",
    "3_termografia": """\
## 1. dia -- Bevezetés: az IR termográfia elve

Minden $T > 0\\ K$ hőmérsékletű test elektromágneses sugárzást bocsát ki.

- Érintésmentes és roncsolásmentes mérés
- Infravörös tartomány: $0{,}75$--$1000\\ \\mu$m
- Valós időben alkalmazható

---

## 2. dia -- Stefan-Boltzmann: sugárzási teljesítmény

$$W = \\varepsilon \\sigma T^4$$

| Jelölés | Jelentés | Érték |
|:--------|:---------|:------|
| $\\varepsilon$ | emisszivitás | $0$--$1$ |
| $\\sigma$ | Stefan-Boltzmann állandó | $5{,}67 \\cdot 10^{-8}\\ \\text{W/m}^2\\text{K}^4$ |
| $T$ | abszolút hőmérséklet | [K] |

---

## 3. dia -- Emisszivitás: anyagspecifikus korrekció

- Fekete test: $\\varepsilon = 1$
- Csiszolt acél: $\\varepsilon \\approx 0{,}1$
- Emberi bőr: $\\varepsilon \\approx 0{,}98$

**Alacsony $\\varepsilon$ → a visszavert környezeti sugárzás dominálja a mért értéket!**

---

## 4. dia -- Hőkamera felépítése: főegységek

- **Objektív**: germániumlencse (IR-áteresztő, látható fényre átlátszatlan)
- **Detektor**: mikrobolométer (nem hűtött) vagy hűtött rendszer
- **Jelfeldolgozó**: NUC kalibráció, hőmérsékletté alakítás

---

## 5. dia -- [MSc] Hűtött vs. nem hűtött detektor

| | Mikrobolométer | Hűtött (InSb/MCT) |
|:--|:---------------|:------------------|
| Ár | Olcsó | Drága |
| Érzékenység | Közepes | Magas |
| Hűtés | Nincs | LN₂ / Peltier |
| Tartomány | LWIR ($8$--$14\\ \\mu$m) | MWIR/LWIR |

---

## 6. dia -- Atmoszférikus ablakok

A levegő csak bizonyos hullámhosszokon áteresztő:

- **$1$--$5\\ \\mu$m** (MWIR): magas hőmérsékletű tárgyakhoz
- **$8$--$14\\ \\mu$m** (LWIR): szobahőmérsékletű tárgyakhoz

Üveg $>5\\ \\mu$m-en átlátszatlan → speciális optika szükséges.

---

## 7. dia -- Alkalmazások: ipari termográfia

- **Villamos diagnosztika**: kontakthiba, túlterhelés-detekció
- **Épületgépészet**: hőszigetelési hiányok azonosítása
- **[MSc] Megelőző karbantartás (PM)**: rendszeres hőtérképes trendkövetés

---

## 8. dia -- Összefoglalás: mérési elvek

1. Emisszivitás helyes beállítása kötelező
2. Reflexiós korrekció: $\\varepsilon = 1 - \\rho$ (átlátszatlan testeknél)
3. Atmoszférikus ablak: $8$--$14\\ \\mu$m szobahőmérsékletű tárgyakhoz
4. **[MSc]** Planck-görbe csúcsa: $\\lambda_m = b/T$ → Wien-törvény
""",
}

JEGYZET = {
    "1_matrixprofil": """\
## Tanulási célok

1. Megérteni a Matrix Profile definícióját és térkomplexitásának előnyét.
2. Megmagyarázni a z-normalizálás szerepét a részsorozat-hasonlóság számításában.
3. Azonosítani a motívum és az anomália fogalmát a Matrix Profile alapján.
4. Összehasonlítani a STOMP és Brute Force algoritmus komplexitását.
5. [MSc] Bemutatni a SCRUMP közelítő megközelítés alkalmazási körét.


<!-- Q:1 -->
## 2. Definíció és adatstruktúra

A **Matrix Profile** egy $O(n)$ méretű vektor, amely minden $m$ hosszú részsorozathoz tárolja a legközelebbi szomszéd z-normalizált euklideszi távolságát [1].

> **💡 Lényeg:** A Matrix Profile csak a távolságmátrix minimumait tartja meg -- az $O(n^2)$ mátrix helyett $O(n)$ vektort. Ez teszi lehetővé a nagy idősorok hatékony kezelését.

<!-- Q:2 -->
## 3. z-normalizált euklideszi távolság

A hasonlóság alapmértéke: $D_{i,j} = \\sqrt{\\sum_{k=0}^{m-1}(\\hat{T}_{i+k} - \\hat{T}_{j+k})^2}$, ahol $\\hat{T}$ z-normalizált. [1]

> **💡 Lényeg:** A z-normalizálás amplitúdófüggetlen összehasonlítást tesz lehetővé. Azonos formájú, de különböző méretű részsorozatok is hasonlónak minősülnek.

> **🗺️ Fejezet összegzés -- 3. z-normalizálás**

<!-- Q:3 -->
## 4. Motívum és anomália

A Matrix Profile **globális minimuma** a leghasonlóbb részsorozat-párt (motívum) jelöli; **globális maximuma** a legritkább, legszokatlanabb részsorozatot (anomália / discord) azonosítja. [1]

> **💡 Lényeg:** Egyetlen Matrix Profile számítással mind a motívumkeresés, mind az anomáliadetektálás elvégezhető -- nincs szükség külön modellekre.

> **[MSc]** A Profile Index kísérőtömb minden elemhez tárolja a legközelebbi szomszéd indeksét, lehetővé téve a gyors visszakeresést. [1]

> **🗺️ Fejezet összegzés -- 4. Motívum és anomália**

<!-- Q:4 -->
## 5. Algoritmusok

| Algoritmus | Időkomplexitás | Memória | Megjegyzés |
|:-----------|:---------------|:--------|:-----------|
| Brute Force | $O(n^2 m)$ | $O(n^2)$ | Naiv; 5 év adat: 4,4 év gépidő [1] |
| **STOMP** | $O(n^2)$ | $O(n)$ | Egzakt; STUMPY magja; GPU/Dask [1] |
| SCRUMP | $O(n^2)$ közelítő | $O(n)$ | Gyors közelítő; sebesség-kritikus esetekre [1] |

> **💡 Lényeg:** A STOMP a Brute Force belső hurkát vektorizálással váltja ki, drasztikusan csökkentve a számítási időt.

> **🗺️ Fejezet összegzés -- 5. Algoritmusok**


---

## Tárgymutató

- [2. Definíció és adatstruktúra](#2-definicio-es-adatstruktura)
- [3. z-normalizált euklideszi távolság](#3-z-normalizalt-euklideszi-tavolsag)
- [4. Motívum és anomália](#4-motivum-es-anomalia)
- [5. Algoritmusok](#5-algoritmusok)

---

## Hivatkozások

<a name="ref-1"></a>[1] STUMPY Documentation (2024). *STUMPY Basics Tutorial*. stumpy2024_webpage.
""",
    "2_dft": """\
## Tanulási célok

1. Leírni a DFT matematikai definícióját és a Fourier-mátrix kapcsolatát.
2. Megmagyarázni az FFT számítási előnyét a közvetlen DFT-vel szemben.
3. Vázolni a Cooley-Tukey rekurzív felbontás elvét.
4. Felsorolni a DFT/FFT legalább 3 mérnöki alkalmazási területét.
5. [MSc] Bemutatni a konvolúciós tétel és a digitális szűrés kapcsolatát.


<!-- Q:1 -->
## 2. DFT definíciója és Fourier-mátrix

A DFT $N$ hosszú diszkrét jelet frekvenciatartományba transzformál: $\\hat{X}(k) = \\sum_{j=0}^{N-1} X(j) W_N^{jk}$, ahol $W_N = e^{2\\pi i/N}$. [1]

Mátrix formában: $\\hat{X} = W_N \\cdot X$, ahol $W_N$ az egységgyökök unitér Fourier-mátrixa. Az IDFT: $X(j) = \\frac{1}{N}\\sum_{k=0}^{N-1} \\hat{X}(k) W_N^{-jk}$. [1]

> **💡 Lényeg:** Az IDFT számítása lényegében megegyezik a DFT-ével (csak $W_N^{-jk}$ és $1/N$ faktorral). Ugyanaz az implementáció mindkét irányban használható.

<!-- Q:2 -->
## 3. FFT és Cooley-Tukey

Az FFT $O(N^2)$-ről $O(N \\log N)$-re csökkenti a DFT számítási igényét. A Cooley-Tukey (1965) algoritmus $N = N_1 N_2$ esetén az $N$-pontos DFT-t két $N/2$-pontos DFT-re bontja rekurzívan. [1]

> **💡 Lényeg:** Az FFT nem egy új transzformáció -- ugyanolyan eredményt ad, mint a közvetlen DFT. Csak a számítást csinálja gyorsabban.

> **[MSc]** A butterfly-diagram az FFT adatfolyam-grafikonja: megmutatja, mely elemeket kell összevonni az egyes rekurzív lépésekben. [1]

> **🗺️ Fejezet összegzés -- 3. FFT és Cooley-Tukey**

<!-- Q:3 -->
## 4. Alkalmazások

A DFT/FFT nélkülözhetetlen a következő területeken [1]:

- **Jelfeldolgozás**: rezgésdiagnosztika, modemek, MP3 kódolás
- **Képfeldolgozás**: MRI rekonstrukció, mintázatfelismerés
- **Geofizika**: szeizmológiai idősorok, nukleáris tesztek detektálása
- **[MSc]** Csillagászat: LIGO gravitációs hullámok, aszteroida-pályák interpolációja

> **💡 Lényeg:** A digitális jelfeldolgozás legtöbb ága közvetve az FFT hatékonyságára épül -- nélküle a modern kommunikáció és orvosi képalkotás nem lenne megvalósítható.

> **🗺️ Fejezet összegzés -- 4. Alkalmazások**

<!-- Q:4 -->
## 5. [MSc] Konvolúciós tétel

Időtartomány konvolúció $\\leftrightarrow$ frekvenciatartomány szorzat: $(f * g)(t) \\xrightarrow{\\mathcal{F}} F(\\omega) \\cdot G(\\omega)$. [1]

Ez lehetővé teszi a digitális szűrést $O(N^2)$ helyett $O(N \\log N)$-nel: FFT → szorzás → IFFT.

> **💡 Lényeg:** A konvolúciós tétel az oka, hogy az FFT a digitális szűrés (és így a rezgésdiagnosztika, audiofeldolgozás, képszűrés) alapeszközévé vált.

> **🗺️ Fejezet összegzés -- 5. Konvolúciós tétel**


---

## Tárgymutató

- [2. DFT definíciója és Fourier-mátrix](#2-dft-definicioja-es-fourier-matrix)
- [3. FFT és Cooley-Tukey](#3-fft-es-cooley-tukey)
- [4. Alkalmazások](#4-alkalmazasok)
- [5. Konvolúciós tétel](#5-konvolucios-tetel)

---

## Hivatkozások

<a name="ref-1"></a>[1] Rockmore, D. N. (1999). "The FFT -- An Algorithm the Whole Family Can Use." *Computing in Science & Engineering*, 1(1), 24--30. rockmore1999_article.pdf.
""",
    "3_termografia": """\
## Tanulási célok

1. Megérteni a Stefan-Boltzmann törvény fizikai tartalmát és a képlet tagjai szerepét.
2. Megmagyarázni az emisszivitás szerepét a pontos hőmérséklet-mérésben.
3. Azonosítani a hőkamera főegységeit (detektor, objektív, jelfeldolgozó).
4. Felsorolni tipikus ipari termográfiai alkalmazásokat.
5. [MSc] Összehasonlítani a hűtött és nem hűtött detektor műszaki paramétereit.


<!-- Q:1 -->
## 2. Fizikai alapok

Az infravörös termográfia alapelve: minden $T > 0\\ \\text{K}$ hőmérsékletű test elektromágneses sugárzást bocsát ki. A **Stefan-Boltzmann törvény**: $W = \\varepsilon \\sigma T^4$. <sup>[[1]](#ref-1)</sup>

| Fogalom | Képlet | Forrás |
|:--------|:-------|:-------|
| Stefan-Boltzmann (valós test) | $W = \\varepsilon \\sigma T^4$ | [1] |
| Stefan-Boltzmann állandó | $\\sigma = 5{,}67 \\cdot 10^{-8}\\ \\text{W m}^{-2}\\text{K}^{-4}$ | [1] |
| Wien eltolódási törvény | $\\lambda_m = 2897\\ \\mu\\text{m}\\cdot\\text{K} / T$ | [1] |
| Kirchhoff sugárzási törvénye | $\\alpha + \\rho + \\tau = 1$ | [1] |

> **💡 Lényeg:** Az emisszivitás ($\\varepsilon$) az anyagspecifikus korrekciós tényező -- helytelen beállítása szisztematikus mérési hibát okoz.

<!-- Q:2 -->
## 3. Emisszivitás és mérési hiba

Az **emisszivitás** a valódi test sugárzásának aránya az ideális fekete test sugárzásához képest ($\\varepsilon \\in [0,1]$). Felületi állapot-, szög- és hullámhossz-függése jelentős. <sup>[[1]](#ref-1)</sup>

Átlátszatlan testeknél: $\\tau = 0$ → $\\varepsilon = \\alpha = 1 - \\rho$.

> **💡 Lényeg:** Tükröző felületek (pl. csiszolt fém, $\\varepsilon < 0{,}1$) esetén a visszavert környezeti sugárzás dominálhatja a mért értéket -- ez a leggyakoribb mérési hiba forrása.

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
""",
}

# ─── FILE WRITER ──────────────────────────────────────────────────────────────

def write_file(path: pathlib.Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode('utf-8'))
    print(f"  ✓ {path.relative_to(ROOT)}")

def bsc_filter(text: str) -> str:
    """Eltávolítja az [MSc] blokkokat és sorokat."""
    lines = text.split('\n')
    out = []
    skip_block = False
    for line in lines:
        if '[MSc]' in line and line.strip().startswith('>'):
            skip_block = True
            continue
        if skip_block and line.strip().startswith('>'):
            continue
        if skip_block and not line.strip().startswith('>'):
            skip_block = False
        if '[MSc]' in line:
            continue
        out.append(line)
    return '\n'.join(out)

# ─── GENERATE ALL FILES ───────────────────────────────────────────────────────

for week_dir, meta in WEEKS.items():
    n, tema, ref1, uuid = meta['n'], meta['tema'], meta['ref1'], meta['uuid']
    base = ROOT / "haromhetes_teszt" / week_dir
    bsc  = base / "bsc"
    print(f"\n=== {week_dir} ({tema}) ===")

    # --- SZÓJEGYZÉK ---
    szozedet_content = f"""\
---
title: {n}_SZOZEDET.MD -- {tema}
type: output
het: {n}
updated: {DATE}
status: DRAFT
---

# {n}. Szójegyzék -- {tema}

**Hét:** {n}. hét | **Dátum:** {DATE} | **Státusz:** DRAFT

{SZOZEDET[week_dir]}
## Irodalomjegyzék

{ref1}

# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| {DATE} | 1.1 | Újragenerálva -- ékezetek javítva (04_citations_maker) |
"""
    write_file(base / f"{n}_Szozedet.md", szozedet_content)
    write_file(bsc  / f"{n}_Szozedet.md", bsc_filter(szozedet_content))

    # --- MINDMAP ---
    mindmap_content = f"""\
---
title: {n}_MINDMAP.MD -- {tema}
type: output
het: {n}
updated: {DATE}
status: DRAFT
notebook: {uuid}
---

# {n}. Mindmap -- {tema}

{MINDMAP[week_dir]}

## Forrás

- Generálta: `nlm_query.py` (2026-05-24)
- Notebook: {uuid}
- Raw: `clean_sources/nlm_q1_raw.txt`

# Változásnapló

- {DATE} -- 1.1: Újragenerálva -- ékezetek javítva (05_mindmap_manager)
"""
    write_file(base / f"{n}_Mindmap.md", mindmap_content)
    write_file(bsc  / f"{n}_Mindmap.md", bsc_filter(mindmap_content))

    # --- KÉRDÉSEK ---
    kerdesek_content = f"""\
---
title: {n}_KERDESEK.MD -- {tema}
type: output
het: {n}
updated: {DATE}
status: DRAFT
---

# {n}. Kérdések -- {tema}

**Hét:** {n}. hét | **Dátum:** {DATE} | **Státusz:** DRAFT

{KERDESEK[week_dir]}

# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| {DATE} | 1.1 | Újragenerálva -- ékezetek javítva (09_question_bank_collector) |
"""
    write_file(base / f"{n}_Kerdesek.md", kerdesek_content)
    write_file(bsc  / f"{n}_Kerdesek.md", bsc_filter(kerdesek_content))

    # --- PREZENTÁCIÓ ---
    prez_content = f"""\
---
title: {n}_PREZENTACIO.MD -- {tema}
type: output
het: {n}
updated: {DATE}
status: DRAFT
notebook: {uuid}
---

# {n}. Prezentáció -- {tema}

**Hét:** {n}. hét | **Dátum:** {DATE} | **Státusz:** DRAFT

{PREZENTACIO[week_dir]}

# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| {DATE} | 1.1 | Újragenerálva -- ékezetek javítva (08_presentation_maker) |
"""
    write_file(base / f"{n}_Prezentacio.md", prez_content)
    write_file(bsc  / f"{n}_Prezentacio.md", bsc_filter(prez_content))

    # --- JEGYZET ---
    jegyzet_content = f"""\
---
title: {n}_JEGYZET.MD -- {tema}
type: output
het: {n}
updated: {DATE}
status: DRAFT
notebook: {uuid}
---

# {n}. Heti Jegyzet -- {tema}

**Hét:** {n}. hét | **Dátum:** {DATE} | **Státusz:** DRAFT

{JEGYZET[week_dir]}

# Változásnapló

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| {DATE} | 1.1 | Újragenerálva -- ékezetek javítva (01-07 pipeline) |
"""
    write_file(base / f"{n}_Jegyzet.md", jegyzet_content)
    write_file(bsc  / f"{n}_Jegyzet.md", bsc_filter(jegyzet_content))

print("\n=== KÉSZ: mind a 15+15 fájl újragenerálva ===")
