---
marp: true
theme: default
paginate: true
backgroundColor: "#ffffff"
---

# Mátrix Profil: Elmélet és Alkalmazások
### 1. hét
**Rezgésdiagnosztika és idősor-elemzés**
2026

---

## Áttekintés: Mi a Mátrix Profil?

A Mátrix Profil egy **meta-idősor**, amely tárolja:
- **$P$ (profil):** minden alszekvencia legközelebbi szomszédjának $z$-normált euklideszi távolsága
- **$I$ (index):** a legközelebbi szomszéd helye (indexe)

> "Svájci bicska" az idősor-elemzésben -- egyetlen adatszerkezetből megoldható a legtöbb feladat.

---

## Miért áttörő?

| Tulajdonság | Leírás |
|:---|:---|
| **Egzakt** | Nincs hamis pozitív/negatív |
| **Paramétermentes** | Csak $m$ (ablakméret) kell |
| **$O(n)$ memória** | Lineáris tárigény |
| **Anytime** | Megszakítható, közelítő megoldás |
| **Inkrementális** | Streaming adatokon frissíthető |
| **Párhuzamosítható** | GPU-gyorsítás lehetséges |

---

## Alapfogalmak

$$T = t_1, t_2, \ldots, t_n \quad \text{(Idősor)}$$

$$T_{i,m} = t_i, t_{i+1}, \ldots, t_{i+m-1} \quad \text{(Alsor)}$$

$$P[i] = \min_{j} \, d(T_{i,m},\, T_{j,m}), \quad |i-j| > \frac{m}{2} \quad \text{(Mátrix Profil)}$$

**Kizárási zóna ($m/2$):** triviális, átfedő egyezések szűrése

---

## Mátrix Profil tulajdonságai

- **Legalacsonyabb pontok** → legjobb **motívum** pár
- **Legmagasabb pont** → **diszkordia** (anomália)
- **Variancia** → az idősor komplexitásának mértéke
- **Hisztogram** → sűrűségbecslés

---

## Algoritmusok áttekintése

```
MASS  →  STAMP  →  STOMP  →  GPU-STOMP
O(nlogn)   O(n²logn)   O(n²)    O(n²) párhuzamos
szubrutin   anytime    logn gyorsabb  GPU CUDA
```

---

## STAMP és STOMP

**STAMP** ($O(n^2 \log n)$):
- MASS szubrutin minden alszekvenciára
- Véletlenszerű sorrend → **anytime** tulajdonság
- STAMPI: inkrementális streaming változat

**STOMP** ($O(n^2)$, $O(\log n)$ gyorsulás):
$$QT_{i,j} = QT_{i-1,j-1} - t_{i-1}t_{j-1} + t_{i+m-1}t_{j+m-1}$$
- $O(1)$ frissítés → rendezett keresés → maximális párhuzamosíthatóság

---

<!-- MSc -->
## [MSc] GPU-STOMP: Skálázhatóság

| Adathossz | STAMP | STOMP | GPU-STOMP |
|:---|:---:|:---:|:---:|
| $2^{17}$ (~131 K) | 15,1 perc | 4,2 perc | **10 mp** |
| $2^{21}$ (~2,1 M) | 4,2 nap | 0,87 nap | **9,3 perc** |
| 100 millió | 25,5 év | 5,4 év | **12,1 nap** |

NVIDIA Tesla K80, $m = 256$, Tesla K80
<!-- /MSc -->

---

## Alkalmazás 1: Motívumkeresés

**Motívum** = ismétlődő alsor, az MP **minimuma** jelöli

Példák:
- Szeizmológia: ismétlődő földrengés-sorozatok
- EKG: szívritmus-minták azonosítása
- Pingvin-telemetria: merülési minták
- Ipari: azonos üzemi rezsimek

---

## Alkalmazás 2: Anomáliadetektálás

**Diszkordia** = az MP **maximuma** -- a legkevésbé tipikus szakasz

Példák:
- EKG: premature ventrikuláris kontrakció
- Adatközpont: hűtési anomália
- Gépi diagnosztika: meghibásodás-előjel

> Az MP diszkordia-detektálás paramétermentes és egzakt -- nincs küszöbérték-beállítás.

---

## Alkalmazás 3 & 4

**Szemantikai szegmentálás** (ívszámlálás):
- MP Index ívstrukturája → rezsimhatárok
- Példa: járás/futás váltás detektálása emberi mozgássoron

**Hasonlósági join** ($J_{AB}$):
- Két idősor közös mintái → pl. zenei mintavétel detektálás
- TSD: mi van $T_A$-ban, ami $T_B$-ben nincs → összehasonlító diagnózis

---

## Összefoglalás

1. **Mátrix Profil** = meta-idősor ($P$, $I$), egyetlen adatszerkezet
2. **Paramétermentes, egzakt** -- csak $m$ ablakméret kell
3. **Algoritmusok:** MASS → STAMP → STOMP → GPU-STOMP (mind egzakt)
4. **Alkalmazások:** motívum, anomália, szegmentálás, join
5. **MATLAB primitív** óta könyvtártámogatott (STUMPY, SCAMP)

---

## Kérdések az anyaghoz

1. Mi a különbség a Mátrix Profil ($P$) és a Mátrix Profil Index ($I$) között?
2. Miért szükséges a kizárási zóna? Mi történne nélküle?
3. Melyik algoritmus alkalmas 10 millió adatpontos streaming adatra?
4. Hogyan azonosítható anomália az MP alapján?

---

## Irodalom

[1] C.-C. M. Yeh et al., "Matrix Profile I," *IEEE ICDM*, 2016.
[2] Y. Zhu et al., "Matrix Profile II," *IEEE ICDM*, 2016.
[3] MathWorks, *matrixProfile dokumentáció*, MATLAB R2024b.
[4] UCR Matrix Profile Page: cs.ucr.edu/~eamonn/MatrixProfile.html
