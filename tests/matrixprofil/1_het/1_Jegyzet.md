---
title: 1_JEGYZET.MD -- Matrix Profile: Alapok es Alkalmazasok
type: output
het: 1
updated: 2026-05-22
status: DRAFT
notebook: ff49ac69-0750-4773-bd4d-42536e96be3f
---

# 1. Heti Jegyzet -- Matrix Profile: Alapok es Alkalmazasok

**Het:** 1. het | **Datum:** 2026-05-22 | **Statusz:** DRAFT

## Tanulasi celok

1. Megerteni a Matrix Profile (MP) matematikai definiciojat es alapfogalmait.
2. Azonositani az MP vektor es index felepteset es szerepet.
3. Osszehasonlitani a STAMP, STOMP es SCRIMP++ algoritmusokat komplexitas es felhasznalasi eset szerint.
4. Felsorolni az MP fo alkalmazasi teruletek (motifum, diszkord, szegmentacio).
5. [MSc] Megerteni a multidimenzios es streaming MP varianst.

<!-- Q:1 -->
## 2. Alapfogalmak es MP struktura

A Matrix Profile (MP) alapfogalmai a következők szerint határozhatók meg a források alapján:

### 1. Idősor (Time Series)
*   **Matematikai definíció**: Az idősor ($T$) valós számok sorozata: $T = [t_1, t_2, \dots, t_n]$, ahol $n$ az idősor hossza és $T \in \mathbb{R}^n$ <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup>.
*   **Fizikai értelem**: Egy fizikai folyamat vagy jelenség időbeli lefolyását rögzítő adatsor, mint például szívritmus (EKG), szeizmikus rezgések vagy egy gép energiafogyasztása <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.

> **💡 Lényeg:** Az idősor ($T$) valós számok rendezett sorozata, amelyet diszkrét időpontokban rögzítenek. Hossza $n$, matematikailag $T \in \mathbb{R}^n$. Az összes MP-algoritmus ezen az adatstruktúrán operál.

### 2. Részsorozat (Subsequence)
*   **Matematikai definíció**: $T_{i,m}$ az idősor egy folytonos szakasza $m$ hosszal, amely az $i$. pozíciótól kezdődik: $T_{i,m} = [t_i, t_{i+1}, \dots, t_{i+m-1}]$, ahol $1 \leq i \leq n-m+1$ <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup> <sup>[[2]](#ref-2)</sup>.
*   **Fizikai értelem**: Az idősor egy rövid "ablaka", amely egy konkrét lokális eseményt, mintát vagy viselkedést reprezentál (például egyetlen szívverést vagy egy lépést a járás során) <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup> <sup>[[4]](#ref-4)</sup>.

> **💡 Lényeg:** A részsorozat ($T_{i,m}$) az idősor egy $m$ hosszú folytonos ablaka, amely az $i$. pozíciótól indul. Az MP minden ilyen ablakot összehasonlít az összes többivel -- ez az összehasonlítás alapja.

### 3. Z-normalizált Euklideszi távolság
*   **Matematikai definíció**: Két részsorozat közötti távolság, miután mindkettőt 0 átlagra és 1 szórásra skáláztuk. A Matrix Profile algoritmusok (pl. MASS) ezt hatékonyan, skaláris szorzatok útján számítják ki: $D[i] = \sqrt{2m(1 - \frac{QT_i - m\mu_Q M_T[i]}{m\sigma_Q \Sigma_T[i]})}$ <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Fizikai értelem**: Lehetővé teszi két minta alakbeli hasonlóságának összehasonlítását függetlenül azok amplitúdójától vagy eltolódásától. Ezzel kiküszöbölhető a "vándorló alapvonal" és a különböző skálázású jelek zavaró hatása <sup>[[1]](#ref-1)</sup>.

> **💡 Lényeg:** A z-normalizálás 0 átlagra és 1 szórásra transzformálja az ablakokat, így az amplitúdó és DC-eltolás nem befolyásolja a hasonlóságot. A MASS algoritmus FFT segítségével $O(n \log n)$ alatt számítja ki a teljes távolságprofilt.

### 4. Távolságprofil (Distance Profile)
*   **Matematikai definíció**: Egy $D_i$ vektor, amely tartalmazza az idősor egy kiválasztott részsorozata ($T_{i,m}$) és az összes többi azonos hosszúságú részsorozat közötti távolságot: $D_i = [d_{i,1}, d_{i,2}, \dots, d_{i,n-m+1}]$ <sup>[[3]](#ref-3)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup> <sup>[[1]](#ref-1)</sup>.
*   **Fizikai értelem**: Megmutatja, hogy egy konkrét minta mennyire elterjedt vagy egyedi az egész adatsorban. A lokális minimumok jelzik a minta ismétlődéseit <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup> <sup>[[4]](#ref-4)</sup>.

> **💡 Lényeg:** A távolságprofil ($D_i$) egy vektor, amely egyetlen kiválasztott ablak távolságát mutatja az összes többi azonos hosszú ablaktól. Minimuma adja a legközelebbi szomszéd távolságát -- ezt tárolja a Matrix Profile.

### 5. Kizárási zóna (Exclusion Zone)
*   **Matematikai definíció**: Egy tartomány a lekérdezett részsorozat indexe ($i$) körül, ahol a távolságértékeket végtelenre ($\infty$) állítják, hogy elkerüljék az önmagával való egyezést. Mértéke jellemzően $m/2$ vagy $m/4$ <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Fizikai értelem**: Megakadályozza a "triviális egyezések" megtalálását, azaz hogy egy részsorozat önmagát vagy a közvetlen, jelentős átfedésben lévő szomszédait találja meg mint legközelebbi partnert <sup>[[4]](#ref-4)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[4]](#ref-4)</sup>.

> **💡 Lényeg:** A kizárási zóna (jellemzően $\pm m/4$) megakadályozza, hogy egy részsorozat önmagát vagy erősen átfedő szomszédait találja meg. Nélküle az MP triviális egyezéseket adna vissza, amelyek nem hordoznak információt.

### 6. Matrix Profile vektor ($P$)
*   **Matematikai definíció**: Egy $P$ vektor, amely minden részsorozathoz eltárolja a kizárási zónán kívüli legkisebb távolságértéket: $P = [\min(D_1), \min(D_2), \dots, \min(D_{n-m+1})]$ <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Fizikai értelem**: Az adatsor "meta-leírása". Az alacsony értékek ismétlődő mintákat (motívumokat - *motifs*), a magas értékek pedig egyedi anomáliákat (diszkordokat - *discords*) reprezentálnak <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup> <sup>[[4]](#ref-4)</sup>.

> **💡 Lényeg:** A $P$ vektor minden részsorozathoz eltárolja a kizárási zónán kívüli legkisebb távolságot. Alacsony értékek ismétlődő mintákra (motívum), magas értékek egyedi anomáliákra (diszkord) utalnak -- ez az MP két legfontosabb alkalmazásának alapja.

### 7. Matrix Profile Index ($I$)
*   **Matematikai definíció**: Egy egész számokat tartalmazó vektor, ahol $I[i] = j$, ha a $T_{j,m}$ részsorozat a $T_{i,m}$ legközelebbi nem-triviális szomszédja <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Fizikai értelem**: Pontos "mutatót" ad arra, hogy egy adott minta párja hol található az idősorban. Ez az alapja az összefüggő események (láncok) és a strukturális váltások (szegmentáció) azonosításának <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.

> **💡 Lényeg:** Az $I$ vektor minden részsorozathoz megmutatja, hogy legközelebbi szomszédja hol helyezkedik el az idősorban. Az ívek alapján azonosíthatók a rezsimváltások (FLUSS szegmentáció) és az összefüggő motívum-láncok.

> **🗺️ Fejezet összegzés -- 2. Alapfogalmak es MP struktura**

## Tárgymutató

- [2. Alapfogalmak es MP struktura](#2-alapfogalmak-es-mp-struktura)
  - [1. Idősor (Time Series)](#1-idősor-time-series)
  - [2. Részsorozat (Subsequence)](#2-részsorozat-subsequence)
  - [3. Z-normalizált Euklideszi távolság](#3-z-normalizált-euklideszi-távolság)
  - [4. Távolságprofil (Distance Profile)](#4-távolságprofil-distance-profile)
  - [5. Kizárási zóna (Exclusion Zone)](#5-kizárási-zóna-exclusion-zone)
  - [6. Matrix Profile vektor ($P$)](#6-matrix-profile-vektor-p)
  - [7. Matrix Profile Index ($I$)](#7-matrix-profile-index-i)
- [3. Algoritmusok](#3-algoritmusok)
  - [1. MASS (Mueen’s ultra-fast Algorithm for Similarity Search)](#1-mass-mueen’s-ultra-fast-algorithm-for-similarity-search)
  - [2. STAMP (Scalable Time series Anytime Matrix Profile)](#2-stamp-scalable-time-series-anytime-matrix-profile)
  - [3. STOMP (Scalable Time series Ordered-search Matrix Profile)](#3-stomp-scalable-time-series-ordered-search-matrix-profile)
  - [4. SCRIMP++](#4-scrimp++)
- [4. Fo alkalmazasok](#4-fo-alkalmazasok)
  - [1. Motívum keresés (Motif Discovery)](#1-motívum-keresés-motif-discovery)
  - [2. Diszkord keresés (Discord / Anomaly Discovery)](#2-diszkord-keresés-discord-/-anomaly-discovery)
  - [3. Szemantikai szegmentáció (FLUSS)](#3-szemantikai-szegmentáció-fluss)
  - [4. Shapelet felfedezés](#4-shapelet-felfedezés)
- [5. Osszefoglalo](#5-osszefoglalo)

>
> A fejezet hét alapfogalma az MP teljes adatstruktúráját definiálja.

> **Idősor / Részsorozat** -- az adatreprezentáció két szintje. **Z-normalizált távolság / Távolságprofil** -- a hasonlóságmérés eszközei. **Kizárási zóna** -- a triviális egyezések kiszűrése. **$P$ vektor** -- az összes legközelebbi szomszéd távolsága (motívum/diszkord olvasható belőle). **$I$ vektor** -- a szomszédok indexe (szegmentáció és láncok alapja).

> Összességében: az MP mint adatstruktúra $O(n)$ tárban, egzakt módon kódolja az összes pár-hasonlósági információt.

<!-- Q:2 -->
## 3. Algoritmusok

A Matrix Profile kiszámítására szolgáló legfontosabb algoritmusok a források alapján az alábbiak:

### 1. MASS (Mueen’s ultra-fast Algorithm for Similarity Search)
*   **Alapelv**: Ez az algoritmus a távolságprofilok kiszámításának alapvető szubrutinja <sup>[[3]](#ref-3)</sup>.

A MASS a Gyors Fourier-transzformációt (FFT) használja a lekérdező részsorozat és az idősor közötti skaláris szorzatok (sliding dot products) kiszámításához <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.

A z-normalizáláshoz szükséges statisztikai mutatókat (átlag, szórás) $O(1)$ idő alatt számítja ki előre meghatározott kumulatív összegek segítségével <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Időkomplexitás**: $O(n \log n)$ egyetlen távolságprofil esetén <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Előnyök**: Ultra-gyors; a futási ideje független az adatok tulajdonságaitól és a részsorozat hosszától ($m$); nem igényel indexelést, így elkerüli a hagyományos módszerek "legrosszabb eseteit" <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Hátrányok**: Önmagában csak egy távolságprofilt ad vissza; a teljes Matrix Profile előállításához (STAMP-be ágyazva) lassabb, mint a STOMP <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.

> **💡 Lényeg:** A MASS az FFT-alapú skaláris szorzatszámítást és a z-normalizáláshoz szükséges előre kiszámított kumulatív összegeket kombinálja, így egyetlen távolságprofilt $O(n \log n)$ alatt ad vissza. Minden magasabb szintű MP-algoritmus ezt hívja szubrutinként.

### 2. STAMP (Scalable Time series Anytime Matrix Profile)
*   **Alapelv**: Egy iteratív algoritmus, amely az idősor minden részsorozatára meghívja a MASS szubrutint, de **véletlenszerű sorrendben** <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.

Minden iterációban frissíti a Matrix Profile-t az eddigi legjobb (legkisebb távolságú) értékekkel <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Időkomplexitás**: $O(n^2 \log n)$ <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Előnyök**: "Anytime" tulajdonság: a teljes futási idő töredéke alatt (pl. 0,25%-nál) már vizuálisan megbízható közelítő eredményt ad <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>; paramétermentes és könnyen párhuzamosítható <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Hátrányok**: Elméletileg lassabb a STOMP-nál egy $O(\log n)$ szorzóval <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.

> **💡 Lényeg:** A STAMP véletlenszerű sorrendben hívja a MASS-t minden részsorozatra, és folyamatosan frissíti az eddigi legjobb értékeket. Anytime jellege miatt már a futási idő töredékénél megbízható közelítő eredményt ad ($O(n^2 \log n)$ teljes futás).

### 3. STOMP (Scalable Time series Ordered-search Matrix Profile)
*   **Alapelv**: Ez az algoritmus **rendezett (egymást követő) keresést** végez. Kihasználja, hogy ha ismert egy részsorozat dot-product vektora, akkor a következő (egy eltolással lévő) részsorozaté $O(1)$ idő alatt frissíthető egy matematikai összefüggés alapján <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup>.

Létezik GPU-gyorsított változata (**GPU-STOMP**), amely tömegesen párhuzamosítja a számításokat <sup>[[2]](#ref-2)</sup>.
*   **Időkomplexitás**: $O(n^2)$ <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup>.
*   **Előnyök**: Gyorsabb, mint a STAMP; a GPU változat lehetővé tette 100 millió adatpont feldolgozását is elviselhető idő alatt <sup>[[2]](#ref-2)</sup>.
*   **Hátrányok**: Nem rendelkezik a STAMP hatékony "anytime" képességével, mivel a rendezett haladás miatt a motívumok felfedezése a futás végére is maradhat <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup>.

> **💡 Lényeg:** A STOMP rendezett keresést végez: mivel egymást követő ablakokra a dot-product $O(1)$ frissítéssel számítható, az összesített komplexitás $O(n^2)$ -- elméleti gyorsulás a STAMP-hez képest. GPU-STOMP változata 100 millió adatpont feldolgozását is lehetővé teszi.

### 4. SCRIMP++
*   **Alapelv**: A SCRIMP++ a STAMP gyors konvergenciáját (anytime jelleg) ötvözi a STOMP sebességével <sup>[[1]](#ref-1)</sup>.

Két fázisból áll: egy előzetes ritka mintavételezésből (Pre-SCRIMP), amely gyorsan azonosítja a potenciális motívumokat, és egy azt követő rendezett finomításból <sup>[[4]](#ref-4)</sup>.
*   **Időkomplexitás**: $O(n^2)$ az egzakt megoldáshoz, de a közelítő eredményt rendkívül gyorsan szolgáltatja <sup>[[1]](#ref-1)</sup>.
*   **Előnyök**: Jelenleg a legkorszerűbb egyensúly a válaszkészség ("anytime" működés) és az abszolút számítási sebesség között <sup>[[4]](#ref-4)</sup>.
*   **Hátrányok**: Az implementációja bonyolultabb, mint az alap STAMP vagy STOMP algoritmusoké <sup>[[4]](#ref-4)</sup>.

> **💡 Lényeg:** A SCRIMP++ a STAMP gyors konvergenciáját (Pre-SCRIMP közelítő fázis) és a STOMP sebességét ötvözi. Jelenleg ez a legjobb egyensúly az interaktív válaszkészség és a precíz egzakt eredmény között, bár implementációja a legösszetettebb a három közül.

> **🗺️ Fejezet összegzés -- 3. Algoritmusok**
>
> A fejezet három MP-algoritmust mutat be növekvő hatékonysággal.

> **MASS** -- $O(n \log n)$ szubrutin, minden algoritmus alapja. **STAMP** -- véletlenszerű, anytime, $O(n^2 \log n)$. **STOMP** -- rendezett, $O(n^2)$, GPU-val skálázható. **SCRIMP++** -- Pre-SCRIMP közelítő + rendezett finomítás, legjobb válaszkészség.

> Összességében: STAMP interaktív felfedezésre, STOMP/SCRIMP++ nagy adathalmazok egzakt feldolgozására ajánlott.

<!-- Q:3 -->
## 4. Fo alkalmazasok

A Matrix Profile (MP) alkalmazási lehetőségei rendkívül szerteágazóak, mivel az adatszerkezet kinyerése után számos idősor-bányászati feladat triviálissá válik <sup>[[4]](#ref-4)</sup>.

A források alapján a négy fő alkalmazási terület a következő:

### 1. Motívum keresés (Motif Discovery)
*   **Definíció**: Az idősorban előforduló, egymáshoz nagyon hasonló, közelítőleg ismétlődő minták azonosítása <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup> <sup>[[5]](#ref-5)</sup>.
*   **Használat az MP-vel**: Az idősor legjelentősebb motívum-párját a Matrix Profile vektor globális minimum értékei jelölik ki <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.

Mivel a profil minden részsorozathoz eltárolja a legközelebbi szomszéd távolságát, a legkisebb értékek adják a legnagyobb hasonlóságot <sup>[[2]](#ref-2)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Gyakorlati példa**: Szeizmológiai adatokban a "doubletek" (ismétlődő földrengésjelek) azonosítása, amelyek ugyanazon a törésvonalon bekövetkező feszültségoldódást jeleznek <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup>.

További példa a pingvinek merülési mintázatának felismerése gyorsulásmérő adatokból <sup>[[2]](#ref-2)</sup>.

> **💡 Lényeg:** A motívum az idősor leggyakrabban ismétlődő mintája. Az MP-ben a $P$ vektor globális minimumai jelölik ki a motívum-párokat -- nincs szükség előzetes küszöbértékre vagy paraméterre. Alkalmazás: szeizmikus doubletek, pingvinek merülési ciklusa.

### 2. Diszkord keresés (Discord / Anomaly Discovery)
*   **Definíció**: Az adatsor legszokatlanabb, leginkább egyedi szakaszainak (anomáliáinak) megtalálása, amelyek a legkevésbé hasonlítanak az összes többi részsorozatra <sup>[[4]](#ref-4)</sup>.
*   **Használat az MP-vel**: A diszkordokat a Matrix Profile vektor globális maximum értékei reprezentálják <sup>[[4]](#ref-4)</sup>.

A magas érték azt jelzi, hogy a részsorozatnak még a legközelebbi szomszédja is távol van euklideszi értelemben <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Gyakorlati példa**: EKG jelekben a rendellenes szívverések (pl. PVC - korai kamrai összehúzódás) automatikus detektálása <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.

Szintén használható szenzorhibák vagy váratlan hálózati terhelési csúcsok azonosítására <sup>[[1]](#ref-1)</sup> <sup>[[2]](#ref-2)</sup>.

> **💡 Lényeg:** A diszkord az idősor legszokatlanabb szakasza, amelynek még a legközelebbi szomszédja is nagy távolságra van -- a $P$ vektor globális maximuma. Alkalmazás: EKG-anomáliák (PVC), szenzorhibák, terhelési csúcsok detektálása.

### 3. Szemantikai szegmentáció (FLUSS)
*   **Definíció**: Az idősor felosztása olyan szakaszokra (rezsimekre), amelyek különböző fizikai folyamatokat vagy viselkedési állapotokat tükröznek <sup>[[3]](#ref-3)</sup> <sup>[[5]](#ref-5)</sup>.
*   **Használat az MP-vel**: A Matrix Profile Index ($I$) értékeit használja fel. Ha minden részsorozatot összekötünk egy ívvel a legközelebbi szomszédjával, a rezsimváltások határán ezek az ívek ritkábban haladnak át <sup>[[3]](#ref-3)</sup>.

A FLUSS algoritmus kiszámítja az egyes pontokon áthaladó ívek számát (arc count), és ahol ez a szám alacsony, ott valószínűsíthető a váltás <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.
*   **Gyakorlati példa**: Emberi mozgásadatoknál (motion capture) a séta és a futás közötti váltás pontos pillanatának meghatározása <sup>[[3]](#ref-3)</sup>.

> **💡 Lényeg:** A FLUSS az MP Index ívein alapul: ahol kevesebb ív halad át, ott valószínű a rezsimváltás. Ez teljesen automatikus szegmentálást tesz lehetővé paraméter nélkül -- alkalmazás: mozgásadat-fázisok elkülönítése.

### 4. Shapelet felfedezés
*   **Definíció**: Olyan rövid szakaszok (alakzatok) kinyerése, amelyek maximálisan reprezentatívak egy adott osztályra nézve, így alkalmasak az idősorok osztályozására <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup> <sup>[[5]](#ref-5)</sup>.
*   **Használat az MP-vel**: Két különböző osztály Matrix Profile-jának összehasonlításával történik ($P_{AA}$ és $P_{AB}$ hasonlósági joinok). Ha egy minta megjelenik az egyik osztályban (alacsony $P_{AA}$), de hiányzik a másikból (magas $P_{AB}$), akkor az egy jó shapelet jelölt <sup>[[1]](#ref-1)</sup> <sup>[[3]](#ref-3)</sup>.

Az MP segítségével a shapeletek keresése nagyságrendekkel gyorsabb, mint a hagyományos brute-force módszerekkel <sup>[[3]](#ref-3)</sup>.
*   **Gyakorlati példa**: Gyenge címkékkel rendelkező adatok osztályozása, például rovarmegfigyelésnél (EPG adatok) annak elkülönítése, hogy az állat éppen táplálkozik vagy csak próbálkozik <sup>[[1]](#ref-1)</sup>.

> **💡 Lényeg:** A shapelet olyan rövid minta, amely maximálisan megkülönbözteti az osztályokat. Az MP a $P_{AA}$ vs $P_{AB}$ similarity join összehasonlításával nagyságrendekkel gyorsítja a shapelet-keresést a brute-force módszerekhez képest.

> **🗺️ Fejezet összegzés -- 4. Fo alkalmazasok**
>
> A fejezet négy fő alkalmazási területet tárgyal, amelyek mind közvetlenül az MP vektorból olvashatók.

> **Motívum keresés** -- $P$ minimum, ismétlődő minták. **Diszkord keresés** -- $P$ maximum, anomáliák. **FLUSS szegmentáció** -- $I$ ívei, rezsimváltások. **Shapelet felfedezés** -- join-alapú osztálydiszkrimináció.

> Összességében: az MP egyetlen előszámítással négy különböző elemzési feladatot old meg paraméter nélkül.

## 5. Osszefoglalo

A Matrix Profile egy univerzalis idosor-adatstruktura, amely minden reszsorozathoz
eltarolja a legkozelebbi nem-trivialis szomszed tav­olsagat (P vektor) es indexet
(I vektor). Elonyei: egzakt, parametermentes, O(n) tarigenyu es determinisztikus.
Az alapalgoritmus (STAMP) veletlen mintaveteleses anytime megkozelitese az FFT-alapu
MASS szubrutin segitsegevel szamitja a tavolsagprofilokat. A STOMP rendezett keresesse
gyorsitja ezt, a SCRIMP++ pedig interaktiv sebessegu kozeliteseket tesz lehetove.
Az MP egyseges feluletet nyujt motivum-, diszkord- es szegmentacios feladatokhoz.

## Forrasjegyzek

<a id="ref-1"></a>**[1]** Yeh, C-C. M. et al., "Matrix Profile XI: SCRIMP++," *arXiv preprint*, 2018

<a id="ref-2"></a>**[2]** Zhu, Y. et al., "Matrix Profile II: Exploiting a Novel Algorithm and GPUs," *IEEE ICDM 2016*, 2016. DOI: 10.1109/ICDM.2016.0096

<a id="ref-3"></a>**[3]** Yeh, C-C. M. et al., "Matrix Profile I: All Pairs Similarity Joins for Time Series," *IEEE ICDM 2016*, 2016. DOI: 10.1109/ICDM.2016.0069

<a id="ref-4"></a>**[4]** Law, S. M. (STUMPY contributors), "STUMPY Tutorial: The Matrix Profile," *stumpy.readthedocs.io*, 2024

<a id="ref-5"></a>**[5]** Law, S. M., "STUMPY: A Powerful and Scalable Python Library for Time Series Data Mining," *Journal of Open Source Software*, 2019. DOI: 10.21105/joss.01504


## Valtozasnaplo

- 2026-05-22 -- Letrehozva (01_nlm_query_runner, 3 query, CLI-alapu pipeline)
