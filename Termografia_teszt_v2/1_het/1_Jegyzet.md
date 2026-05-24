---
title: 1_Jegyzet -- Infravörös Termográfia
type: output
status: draft
version: 0.1
updated: 2026-05-24
description: Termografia_teszt_v2 -- 1. hét. NLM Q1-Q4 alapján összeállított tanulási segédlet.
---
# Tárgymutató

- [1. Áttekintés](#1-áttekintés)
    - [Alkalmazási területek](#alkalmazási-területek)
    - [Fizikai alapelvek](#fizikai-alapelvek)
    - [Leglényegesebb jellemzők és paraméterek](#leglényegesebb-jellemzők-és-paraméterek)
- [2. Sugárzásfizikai alaptörvények](#2-sugárzásfizikai-alaptörvények)
    - [1. Stefan–Boltzmann-törvény](#1-stefanboltzmann-törvény)
    - [2. Planck-féle sugárzási törvény](#2-planck-féle-sugárzási-törvény)
    - [3. Wien-féle eltolódási törvény](#3-wien-féle-eltolódási-törvény)
    - [4. Kirchhoff-féle sugárzási törvény](#4-kirchhoff-féle-sugárzási-törvény)
    - [Összefoglaló táblázat](#összefoglaló-táblázat)
- [3. Hőkamerák és méréstechnika](#3-hőkamerák-és-méréstechnika)
    - [Hőkamerás mérőeszközök típusai](#hőkamerás-mérőeszközök-típusai)
      - [1. Hűtött (Quantum) vs. Hűtetlen (Thermal) detektorok](#1-hűtött-quantum-vs-hűtetlen-thermal-detektorok)
      - [2. Spektrális tartományok](#2-spektrális-tartományok)
    - [A mérési pontosságot befolyásoló tényezők](#a-mérési-pontosságot-befolyásoló-tényezők)
      - [1. Emissziófüggőség](#1-emissziófüggőség)
      - [2. Reflexió (Visszaverődés)](#2-reflexió-visszaverődés)
      - [3. Kalibráció és szoftveres korrekció](#3-kalibráció-és-szoftveres-korrekció)
    - [Összefoglaló a mérést befolyásoló adatokról](#összefoglaló-a-mérést-befolyásoló-adatokról)
- [4. Gyakorlati alkalmazások](#4-gyakorlati-alkalmazások)
    - [1. Általános karbantartás és állapotfüggő diagnosztika](#1-általános-karbantartás-és-állapotfüggő-diagnosztika)
    - [2. Villamosipari alkalmazások](#2-villamosipari-alkalmazások)
    - [3. Gépészeti diagnosztika](#3-gépészeti-diagnosztika)
    - [4. Épületdiagnosztika és építészet](#4-épületdiagnosztika-és-építészet)
    - [Összefoglaló táblázat a diagnosztikai példákról](#összefoglaló-táblázat-a-diagnosztikai-példákról)

---

# 1_Jegyzet -- Infravörös Termográfia

_Forrás: NLM Termografia\_teszt\_v2 notebook, Q1-Q4 lekérdezések_

# 1. Áttekintés

<!-- Q:1 -->
Az infravörös termográfia egy olyan érintésmentes mérési eljárás, amely a tárgyak által kibocsátott láthatatlan infravörös sugárzást elektronikus jelekké, majd vizuális képpé – hőtérképpé vagy termogrammává – alakítja (d1_lecturenotes.docx, flir2024_howworks.pdf). Ez a technológia lehetővé teszi a felületi hőmérséklet-különbségek detektálását és a pontos hőmérsékletértékek meghatározását anélkül, hogy a mérőműszer érintkezne a vizsgált felülettel (flir2024_howworks.pdf, haraszti2013_termografia.pdf).

### Alkalmazási területek
A termográfiát széles körben alkalmazzák a diagnosztika és a karbantartás területén:
* **Villamos diagnosztika:** Kötéshibák, korrodált csatlakozások, túlterhelt vezetékek és aszimmetrikus terhelések keresése transzformátorokban, kapcsolószekrényekben és napelemes rendszerekben (Hőkamerák villamos szakembereknek, Hoterkep-keszites a karbantarto szemszogebol.pdf).
* **Gépészeti karbantartás:** Motorok, csapágyak, szivattyúk és hajtóművek rendellenes felmelegedésének ellenőrzése (Hoterkep-keszites a karbantarto szemszogebol.pdf).
* **Épületdiagnosztika:** Hőszigetelési hiányosságok, hőhidak, nedvesedés és tetőszivárgások felderítése (d1_lecturenotes.docx, Hoterkep-keszites a karbantarto szemszogebol.pdf).
* **Tudományos és környezeti vizsgálatok:** Planetáris hőmérséklet-mérések, űreszközök hővédelmének ellenőrzése és a globális felmelegedéssel kapcsolatos kutatások (Emissivity - Wikipedia).


> **💡 Lényeg:** Villamos diagnosztikától épületfizikáig széles spektrum.

### Fizikai alapelvek
A termográfia működése a hősugárzás (radiáció) jelenségén és alapvető fizikai törvényeken nyugszik:
1. **Emisszió:** Minden test, amelynek hőmérséklete meghaladja az abszolút nulla fokot (0 K vagy -273,15 °C), elektromágneses sugárzást bocsát ki (d1_lecturenotes.docx, flir2024_howworks.pdf).
2. **Stefan-Boltzmann törvény:** Kimondja, hogy a fekete test által kisugárzott összes energia a test abszolút hőmérsékletének negyedik hatványával arányos (d1_lecturenotes.docx, haraszti2013_termografia.pdf).
3. **Planck-féle sugárzási törvény:** Leírja a sugárzás spektrális eloszlását a hullámhossz függvényében egy adott hőmérsékleten (d1_lecturenotes.docx, flir2024_howworks.pdf).
4. **Wien-féle eltolódási törvény:** Megmutatja, hogy a hőmérséklet emelkedésével a sugárzás intenzitásának maximuma a rövidebb hullámhosszak felé tolódik (d1_lecturenotes.docx, flir2024_howworks.pdf).
5. **Kirchhoff-féle sugárzási törvény:** Megállapítja, hogy egy test emissziós képessége és abszorpciós (elnyelő) képessége egy adott hullámhosszon és hőmérsékleten megegyezik (d1_lecturenotes.docx, flir_emissivity_guide.pdf).


> **💡 Lényeg:** Stefan-Boltzmann, Planck, Wien és Kirchhoff törvények.

### Leglényegesebb jellemzők és paraméterek

| Jellemző | Meghatározás | Forrás |
| :--- | :--- | :--- |
| **Emissziós tényező (ε)** | A tárgy sugárzási hatékonysága az ideális fekete testhez képest (értéke 0 és 1 között mozog). | flir_emissivity_guide.pdf, haraszti2013_termografia.pdf |
| **Sugárzási egyenleg** | A beeső sugárzás sorsa: emisszió + reflexió (visszaverődés) + transzmisszió (áteresztés) = 1. | d1_lecturenotes.docx, flir2024_howworks.pdf |
| **Atmoszferikus ablakok** | Azon spektrális tartományok (3-5 μm és 8-14 μm), ahol a légkör jól átereszti az infravörös sugárzást. | flir2024_howworks.pdf, haraszti2013_termografia.pdf |
| **Hőkamera detektor** | Eszköz, amely a sugárzást elektromos jellé alakítja; leggyakoribb a hűtés nélküli mikrobolométer. | flir2024_howworks.pdf, Mikrobolométer technológia - Thermo Delta Kft. |
| **NETD (Termikus érzékenység)** | A legkisebb hőmérsékletkülönbség, amelyet a kamera még érzékelni képes (mK-ben megadva). | Hőkamerák villamos szakembereknek |


> **💡 Lényeg:** Hőmérséklet-érzékenység (NETD), térbeli felbontás és emissziós szám.

# 2. Sugárzásfizikai alaptörvények

<!-- Q:2 -->
Az infravörös termográfia elméleti hátterét négy alapvető fizikai sugárzási törvény határozza meg, amelyek leírják az objektumok hőmérséklete és az általuk kibocsátott elektromágneses sugárzás közötti összefüggéseket.

### 1. Stefan–Boltzmann-törvény

**Matematikai definíció:**
$$E_{(f)}(T) = \sigma \cdot T^4$$
vagy szürke testekre:
$$W = \varepsilon \cdot \sigma \cdot T^4$$
Ahol:
* **$E_{(f)}$** vagy **$W$**: A kisugárzott összes teljesítmény (sugárzási fluxus) egységnyi felületre vonatkoztatva [$W/m^2$] [1-3].
* **$\sigma$**: Stefan–Boltzmann-állandó ($5,67 \cdot 10^{-8} \ W/m^2K^4$) [2-4].
* **$T$**: Az objektum abszolút hőmérséklete [Kelvin] [1, 3, 5].
* **$\varepsilon$**: Emissziós tényező (fekete test esetén $\varepsilon = 1$) [2, 6].

**Fizikai értelmezés:**
A törvény kimondja, hogy egy fekete test által kibocsátott teljes sugárzási energia arányos az abszolút hőmérsékletének negyedik hatványával [1, 3]. Ez azt jelenti, hogy a hőmérséklet kismértékű emelkedése a kisugárzott energia jelentős növekedését eredményezi, ami lehetővé teszi a hőkamerák számára a pontos hőmérséklet-meghatározást [3, 7].


> **💡 Lényeg:** Az összsugárzás T⁴-tel arányos: E = εσT⁴.

### 2. Planck-féle sugárzási törvény

**Matematikai definíció:**
Planck törvénye megadja a fekete test spektrális emisszióképességét ($e_{\lambda,T}$) a hullámhossz ($\lambda$) és a hőmérséklet ($T$) függvényében [8, 9]. Bár a képlet komplex, alapja az energia kvantált természete:
$$E = h \cdot \nu$$
Ahol **$h$** a Planck-állandó ($6,626 \cdot 10^{-34} \ Js$), **$\nu$** pedig a frekvencia [10-12].

**Fizikai értelmezés:**
A Planck-törvény leírja a hősugárzás intenzitásának spektrális eloszlását egy adott hőmérsékleten [9, 13]. Kimutatja, hogy az energia nem folytonosan, hanem diszkrét adagokban (kvantumokban) adódik át [12, 14]. A törvény grafikus megjelenítése a Planck-görbék sorozata, amelyek megmutatják, hogy minden hőmérséklethez egy egyedi sugárzáseloszlási görbe tartozik [5, 9].


> **💡 Lényeg:** Spektrális eloszlást ír le; valós testnél ε szorzóval módosul.

### 3. Wien-féle eltolódási törvény

**Matematikai definíció:**
$$\lambda_{max} = \frac{b}{T}$$
vagy a forrásokban megadott állandóval:
$$\lambda_{max} = \frac{2898}{T}$$
Ahol:
* **$\lambda_{max}$**: Az a hullámhossz, ahol a sugárzás intenzitása maximális [$\mu m$] [5, 15].
* **$b$**: Wien-féle állandó ($2,9 \cdot 10^{-3} \ mK$) [16].
* **$T$**: Abszolút hőmérséklet [Kelvin] [5, 15].

**Fizikai értelmezés:**
A törvény szerint a sugárzó test hőmérsékletének növekedésével a sugárzási maximumhoz tartozó hullámhossz a rövidebb hullámhosszak felé tolódik [7, 15, 17]. Ez magyarázza meg, miért változik egy izzó test színe a hőmérséklet emelkedésével vörösről sárgára, majd fehérre [9, 15]. Környezeti hőmérsékleten ($300 \ K$) a maximum körülbelül $10 \ \mu m$ környékén (infravörös tartomány) található [5].


> **💡 Lényeg:** λ_max = b/T; magasabb hőmérsékletnél rövidebb csúcshullámhossz.

### 4. Kirchhoff-féle sugárzási törvény

**Matematikai definíció:**
$$\alpha = \varepsilon$$
vagy részletesebben:
$$\frac{e(\nu, T)}{a(\nu, T)} = E_{(f)}(\nu, T)$$
Ahol **$\alpha$** az abszorpciós képesség (elnyelés) és **$\varepsilon$** az emissziós tényező (kisugárzás) [18-20].

**Fizikai értelmezés:**
Kirchhoff törvénye kimondja, hogy egy adott hőmérsékleten és hullámhosszon egy test emissziós képessége megegyezik az abszorpciós képességével [20, 21]. Ez azt jelenti, hogy azok a testek, amelyek jól nyelik el a sugárzást, jó sugárzók is (pl. a korom), míg a rossz elnyelők (mint a fényes fémek) rossz sugárzók és jó visszaverők [18, 21].


> **💡 Lényeg:** ε = α: jó elnyelők egyben jó sugárzók.

### Összefoglaló táblázat

| Törvény | Fő üzenet | Releváns forrás |
| :--- | :--- | :--- |
| **Stefan–Boltzmann** | A teljes sugárzott energia a hőmérséklet negyedik hatványával arányos. | haraszti2013_termografia.pdf [3], d1_lecturenotes.docx [1] |
| **Planck** | A sugárzás spektrális eloszlása a kvantumelméleten alapul. | flir2024_howworks.pdf [13], d1_lecturenotes.docx [9] |
| **Wien** | A hőmérséklet emelkedésével a sugárzási csúcs a rövidebb hullámhosszak felé tolódik. | flir_emissivity_guide.pdf [7], d1_lecturenotes.docx [15] |
| **Kirchhoff** | Egy test ugyanolyan mértékben sugároz, mint amilyen mértékben elnyel ($\varepsilon = \alpha$). | flir2024_howworks.pdf [20], d1_lecturenotes.docx [19] |


> **💡 Lényeg:** Négy törvény összehasonlítva képlet, változók és forrás szerint.

# 3. Hőkamerák és méréstechnika

<!-- Q:3 -->
A hőkamerás mérőeszközök technológiája és a mérések pontosságát meghatározó tényezők összetett fizikai és mérnöki alapokon nyugszanak. Az alábbiakban a forrásdokumentumok alapján részletezem az eszközök típusait és a legfontosabb befolyásoló paramétereket.

### Hőkamerás mérőeszközök típusai

A hőkamerákat alapvetően a detektor működési elve és a használt spektrális tartomány alapján csoportosítjuk.

#### 1. Hűtött (Quantum) vs. Hűtetlen (Thermal) detektorok
* **Hűtetlen detektorok (Mikrobolométer):** A legelterjedtebb ipari megoldás. Rácsszerkezetű vanádium-oxid (VOx) vagy amorf szilícium (a-Si) hőérzékelőkből állnak (Mikrobolométer technológia - Thermo Delta Kft.). Működésük alapja, hogy az infravörös sugárzás hatására megváltozik a detektorelemek elektromos ellenállása, amit a kiolvasó áramkör (ROIC) mér és hőtérképpé alakít (Mikrobolométer technológia - Thermo Delta Kft., IR Thermography: How It Works (FLIR 2024)). Előnyük az alacsonyabb ár és a robusztus kialakítás, de érzékenységük és sebességük elmarad a hűtött típusokétól (IR Thermography: How It Works (FLIR 2024)).
* **Hűtött (Kvantum) detektorok:** Különböző félvezető anyagokból (pl. InSb, InGaAs, HgCdTe) készülnek. Működésük a kristályszerkezet elektronjainak állapotváltozásán alapul a beérkező fotonok hatására (IR Thermography: How It Works (FLIR 2024)). Ezek a detektorok rendkívül gyorsak és érzékenyek, de működésükhöz kriogenikus hűtésre (pl. Stirling-hűtő vagy folyékony nitrogén) van szükség, ami drágábbá és szervizigényesebbé teszi őket (IR Thermography: How It Works (FLIR 2024)).

#### 2. Spektrális tartományok
A hőkamerák az infravörös spektrum meghatározott "ablakaiban" mérnek:
* **LWIR (Long Wave IR - Hosszúhullámú):** 7,5–14 μm közötti tartomány. Ipari és épületdiagnosztikai célokra leginkább ezt használják, mivel a légkör itt rendelkezik a legjobb átviteli tulajdonságokkal (IR Thermography: How It Works (FLIR 2024), Termografiai vizsgalatok (Haraszti 2013)).
* **MWIR (Mid Wave IR - Középhullámú):** 3–5 μm közötti tartomány. Főként tudományos kutatásban, katonai alkalmazásoknál és magas hőmérsékletű (400 °C feletti) ipari folyamatoknál alkalmazzák (IR Thermography: How It Works (FLIR 2024), Termografiai vizsgalatok (Haraszti 2013)).
* **SWIR (Short Wave IR - Rövidhullámú):** Kb. 0,9–2,5 μm tartomány. Speciális esetekben, igen magas hőmérsékletek detektálására használják (Termografiai vizsgalatok (Haraszti 2013)).

---


> **💡 Lényeg:** Hűtött (jobb érzékenység) vs. hűtetlen (kisebb méret, ár).

### A mérési pontosságot befolyásoló tényezők

A hőkamera nem közvetlenül hőmérsékletet mér, hanem sugárzási teljesítményt, amelyből szoftveresen számítja ki a hőmérsékletet (d1_lecturenotes.docx, IR Thermography: How It Works (FLIR 2024)). Ezért a következő tényezők kritikusak a pontosság szempontjából:

#### 1. Emissziófüggőség
Az emissziós tényező ($\varepsilon$) az objektum sugárzási képességét mutatja a fekete testhez képest (Emissivity - Wikipedia, Infrared Energy, Emissivity, Reflection & Transmission (FLIR)).
* **Helytelen megválasztása:** Akár nagyságrendi mérési hibát is okozhat (Termografiai vizsgalatok (Haraszti 2013)).
* **Befolyásoló tényezők:** Az anyagi minőség mellett az érdesség, az oxidáció foka és a mérés szöge is számít. A mérés szöge ideálisan a felületre merőlegeshez közeli (60 fokos kúpon belül), ennél nagyobb szögnél az emisszió drasztikusan csökkenhet (Infrared Energy, Emissivity, Reflection & Transmission (FLIR)).

#### 2. Reflexió (Visszaverődés)
Alacsony emissziójú (pl. fényes fém) felületek esetén a kamera a környező tárgyak és a kezelő hősugárzását is érzékeli, amely visszaverődik a célfelületről (Termografiai vizsgalatok (Haraszti 2013), Infrared Energy, Emissivity, Reflection & Transmission (FLIR)).
* A szoftveres korrekcióhoz meg kell adni a **visszavert háttérhőmérsékletet** ($T_{refl}$ vagy $T_{amb}$), hogy a kamera le tudja vonni ezt a zavaró komponenst a mért értékből (IR Thermography: How It Works (FLIR 2024), Termografiai vizsgalatok (Haraszti 2013)).

#### 3. Kalibráció és szoftveres korrekció
A hőkamerák gyári kalibrálása fekete test sugárzókkal történik (d1_lecturenotes.docx, Infrared Energy, Emissivity, Reflection & Transmission (FLIR)). A mérési egyenletben a szoftver figyelembe veszi az alábbiakat a pontos eredményhez:
* A légkör transzmisszióját ($\tau_{atm}$) és hőmérsékletét ($T_{atm}$) (IR Thermography: How It Works (FLIR 2024)).
* Az objektum távolságát, mivel a levegőben lévő vízpára és $CO_2$ elnyeli a sugárzás egy részét (Termografiai vizsgalatok (Haraszti 2013)).

**A források nem tartalmaznak információt a következőre: NUC (Non-Uniformity Correction) kalibráció.** A források említik a detektorok integrált kiolvasó áramköreit (ROIC) és a vákuum fontosságát a mikrobolométereknél (Mikrobolométer technológia - Thermo Delta Kft.), de a specifikus "NUC" rövidítést nem részletezik.


> **💡 Lényeg:** Emissziós szám, reflexió és NUC kalibrációs hiba a fő hibaforrások.

### Összefoglaló a mérést befolyásoló adatokról

| Paraméter | Hatása a mérésre | Releváns forrás |
| :--- | :--- | :--- |
| **Emisszió ($\varepsilon$)** | Meghatározza a saját sugárzás arányát. | Termografiai vizsgalatok (Haraszti 2013) |
| **Visszavert hőmérséklet** | A tükröződő felületek "ál-hőmérsékletét" okozza. | IR Thermography: How It Works (FLIR 2024) |
| **Légköri transzmisszió** | A távolság és páratartalom miatti jelveszteséget korrigálja. | IR Thermography: How It Works (FLIR 2024) |
| **Mérési szög** | Túl lapos szögben az emisszió lecsökken, a reflexió megnő. | Emissivity - Wikipedia, flir_emissivity_guide.pdf |


> **💡 Lényeg:** Hőmérsékleti hiba emissziófüggésének kezelése szoftverrel.

# 4. Gyakorlati alkalmazások

<!-- Q:4 -->
Az infravörös termográfia az ipari diagnosztika egyik legsokoldalúbb eszköze, mivel lehetővé teszi a berendezések üzem közbeni, érintésmentes vizsgálatát, feltárva a szemmel nem látható hőtani anomáliákat. Az alábbiakban részletezem az alkalmazási területeket a forrásdokumentumok alapján:

### 1. Általános karbantartás és állapotfüggő diagnosztika
A termográfia alapvető eleme a számítógéppel támogatott megelőző karbantartásnak (*Computer-Aided Predictive Maintenance*), ahol a cél a gépek ideális üzemi hőmérsékletétől való eltérések korai detektálása (D1 Lecture Notes (Termografia).docx).
* **Trendfigyelés:** A karbantartók évente legalább egyszer hőtérképet készítenek a kritikus egységekről, és az új képeket összehasonlítják a korábbi állapotokkal (Hoterkep-keszites a karbantarto szemszogebol.pdf).
* **Hiba-beazonosítás:** Ha egy forró pont (*hot spot*) jelenik meg ott, ahol korábban nem volt, az közeledő meghibásodást jelez, így a javítás még a leállás előtt ütemezhető (Hoterkep-keszites a karbantarto szemszogebol.pdf).
* **Előnyök:** Üzem közben végezhető, nincs kényszerű leállás, és biztonságos távolságból ellenőrizhetők a nehezen elérhető (pl. mennyezeti) alkatrészek is (Hoterkep-keszites a karbantarto szemszogebol.pdf).


> **💡 Lényeg:** Prediktív karbantartás alapja: rendellenes felmelegedés korai felismerése.

### 2. Villamosipari alkalmazások
A villamosiparban nincsenek kötelező szabványok, de szigorú irányelvek (pl. NETA) szabályozzák a mérést, ahol a környezeti hőmérséklethez vagy a fázisok közötti különbséghez (*ΔT*) viszonyítanak (Hőkamerák villamos szakembereknek).
* **Kötéshibák:** A laza vagy korrodált csatlakozások megnövekedett ellenállása hőt termel. Például egy meglazult kötés 48,7 °C-os felmelegedést is mutathat (Hőkamerák villamos szakembereknek).
* **Túlterhelés:** A túlterhelt vezetékek vagy kismegszakítók jól láthatóan magasabb hőmérsékletűek; egy túlterhelt kismegszakító hőmérséklete elérheti a 41,9 °C-ot (Hőkamerák villamos szakembereknek).
* **Alkatrészek öregedése:** Az elöregedett kerámiaszigetelések vagy kötőelemek túlhevülése (pl. 49,7 °C-os érték) időben jelezheti a tűzveszélyt (Hőkamerák villamos szakembereknek).
* **Napelemes rendszerek:** A cellák állapotának ellenőrzésekor kimutatható az ún. *HotSpot* effektus, amelyet például árnyékhatás is okozhat, és a cella 53,8 °C-ra való hevülését eredményezheti (Hőkamerák villamos szakembereknek).


> **💡 Lényeg:** Kötéshibák, aszimmetria, transformer- és napelem-diagnosztika.

### 3. Gépészeti diagnosztika
A gépészetben a súrlódás és a kenési elégtelenségek okozta hőmérséklet-emelkedés a legfontosabb jelzőszám (Hoterkep-keszites a karbantarto szemszogebol.pdf).
* **Forgógépek:** Motorok, szivattyúk, ventilátorok és kompresszorok csapágyainak ellenőrzése. A forró pontok jelzik a csapágykopást vagy a tengelyirányú beállítási hibákat (Hoterkep-keszites a karbantarto szemszogebol.pdf).
* **Erőátvitel:** Hajtóművek, fogaskerék-házak és konvejorok (szállítószalagok) hőeloszlásának vizsgálata (Hoterkep-keszites a karbantarto szemszogebol.pdf).
* **Folyamatműszerezés:** Szelepek, gőzcsapdák és csővezetékek elzáródásának vagy szivárgásának detektálása (Hoterkep-keszites a karbantarto szemszogebol.pdf).


> **💡 Lényeg:** Csapágyak, szivattyúk, hajtóművek melegedésének nyomon követése.

### 4. Épületdiagnosztika és építészet
Az építészetben a termográfia a szerkezeti integritás és az energiahatékonyság vizsgálatára szolgál (D1 Lecture Notes (Termografia).docx).
* **Hőszigetelés ellenőrzése:** A szigetelési hiányosságok és hőhidak pontos helye beazonosítható a falak külső felületének termális elváltozásai alapján (D1 Lecture Notes (Termografia).docx).
* **Nedvesség detektálása:** A vízzel átitatott lapos tető éjszaka tovább tartja a nappali meleget, mint a száraz részek, így a szivárgások helye éjszakai méréssel pontosan meghatározható (D1 Lecture Notes (Termografia).docx).
* **Nyílászárók:** Az alacsony emissziós (Low-E) bevonattal ellátott ablakok hatékonysága mérhető; ezek télen akár felére is csökkenthetik a hőveszteséget a bevonat nélküli üvegekhez képest (Emissivity - Wikipedia).
* **HVAC rendszerek:** A fűtési, szellőztetési és légkondicionáló berendezések, valamint a padlófűtés csővezetékeinek roncsolásmentes keresése (Hoterkep-keszites a karbantarto szemszogebol.pdf).


> **💡 Lényeg:** Hőhidak, nedvesedés, tetőszivárgás non-destruktív feltárása.

### Összefoglaló táblázat a diagnosztikai példákról

| Terület | Vizsgált jelenség | Konkrét példa / Érték | Forrás |
| :--- | :--- | :--- | :--- |
| **Villamosipar** | Túlterhelt alkatrész | 41,9 °C-os kismegszakító | Hőkamerák villamos szakembereknek |
| **Villamosipar** | Napelem hiba | 53,8 °C-os HotSpot (árnyék miatt) | Hőkamerák villamos szakembereknek |
| **Építészet** | Tetőszivárgás | Nedves szigetelés hővisszatartása éjjel | D1 Lecture Notes (Termografia).docx |
| **Gépészet** | Csapágyhiba | Rendellenes melegedés a motorháznál | Hoterkep-keszites a karbantarto szemszogebol.pdf |
| **Építészet** | Low-E üvegezés | 50%-os hőveszteség-csökkenés | Emissivity - Wikipedia |


> **💡 Lényeg:** Iparágak × alkalmazás × hőkamera-típus mátrix.


> **🗺️ Fejezet összegzés — 4. Gyakorlati alkalmazások**
>
> A termográfia széles körű ipari alkalmazása a megelőző karbantartás kulcseszköze.
