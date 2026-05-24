<!-- Q3 answer -->
A hőkamerás mérőeszközök technológiája és a mérések pontosságát meghatározó tényezők összetett fizikai és mérnöki alapokon nyugszanak. Az alábbiakban a forrásdokumentumok alapján részletezem az eszközök típusait és a legfontosabb befolyásoló paramétereket.

### Hőkamerás mérőeszközök típusai

A hőkamerákat alapvetően a detektor működési elve és a használt spektrális tartomány alapján csoportosítjuk.

#### 1. Hűtött (Quantum) vs. Hűtetlen (Thermal) detektorok
*   **Hűtetlen detektorok (Mikrobolométer):** A legelterjedtebb ipari megoldás. Rácsszerkezetű vanádium-oxid (VOx) vagy amorf szilícium (a-Si) hőérzékelőkből állnak (Mikrobolométer technológia - Thermo Delta Kft.). Működésük alapja, hogy az infravörös sugárzás hatására megváltozik a detektorelemek elektromos ellenállása, amit a kiolvasó áramkör (ROIC) mér és hőtérképpé alakít (Mikrobolométer technológia - Thermo Delta Kft., IR Thermography: How It Works (FLIR 2024)). Előnyük az alacsonyabb ár és a robusztus kialakítás, de érzékenységük és sebességük elmarad a hűtött típusokétól (IR Thermography: How It Works (FLIR 2024)).
*   **Hűtött (Kvantum) detektorok:** Különböző félvezető anyagokból (pl. InSb, InGaAs, HgCdTe) készülnek. Működésük a kristályszerkezet elektronjainak állapotváltozásán alapul a beérkező fotonok hatására (IR Thermography: How It Works (FLIR 2024)). Ezek a detektorok rendkívül gyorsak és érzékenyek, de működésükhöz kriogenikus hűtésre (pl. Stirling-hűtő vagy folyékony nitrogén) van szükség, ami drágábbá és szervizigényesebbé teszi őket (IR Thermography: How It Works (FLIR 2024)).

#### 2. Spektrális tartományok
A hőkamerák az infravörös spektrum meghatározott "ablakaiban" mérnek:
*   **LWIR (Long Wave IR - Hosszúhullámú):** 7,5–14 μm közötti tartomány. Ipari és épületdiagnosztikai célokra leginkább ezt használják, mivel a légkör itt rendelkezik a legjobb átviteli tulajdonságokkal (IR Thermography: How It Works (FLIR 2024), Termografiai vizsgalatok (Haraszti 2013)).
*   **MWIR (Mid Wave IR - Középhullámú):** 3–5 μm közötti tartomány. Főként tudományos kutatásban, katonai alkalmazásoknál és magas hőmérsékletű (400 °C feletti) ipari folyamatoknál alkalmazzák (IR Thermography: How It Works (FLIR 2024), Termografiai vizsgalatok (Haraszti 2013)).
*   **SWIR (Short Wave IR - Rövidhullámú):** Kb. 0,9–2,5 μm tartomány. Speciális esetekben, igen magas hőmérsékletek detektálására használják (Termografiai vizsgalatok (Haraszti 2013)).

---

### A mérési pontosságot befolyásoló tényezők

A hőkamera nem közvetlenül hőmérsékletet mér, hanem sugárzási teljesítményt, amelyből szoftveresen számítja ki a hőmérsékletet (d1_lecturenotes.docx, IR Thermography: How It Works (FLIR 2024)). Ezért a következő tényezők kritikusak a pontosság szempontjából:

#### 1. Emissziófüggőség
Az emissziós tényező ($\varepsilon$) az objektum sugárzási képességét mutatja a fekete testhez képest (Emissivity - Wikipedia, Infrared Energy, Emissivity, Reflection & Transmission (FLIR)).
*   **Helytelen megválasztása:** Akár nagyságrendi mérési hibát is okozhat (Termografiai vizsgalatok (Haraszti 2013)).
*   **Befolyásoló tényezők:** Az anyagi minőség mellett az érdesség, az oxidáció foka és a mérés szöge is számít. A mérés szöge ideálisan a felületre merőlegeshez közeli (60 fokos kúpon belül), ennél nagyobb szögnél az emisszió drasztikusan csökkenhet (Infrared Energy, Emissivity, Reflection & Transmission (FLIR)).

#### 2. Reflexió (Visszaverődés)
Alacsony emissziójú (pl. fényes fém) felületek esetén a kamera a környező tárgyak és a kezelő hősugárzását is érzékeli, amely visszaverődik a célfelületről (Termografiai vizsgalatok (Haraszti 2013), Infrared Energy, Emissivity, Reflection & Transmission (FLIR)).
*   A szoftveres korrekcióhoz meg kell adni a **visszavert háttérhőmérsékletet** ($T_{refl}$ vagy $T_{amb}$), hogy a kamera le tudja vonni ezt a zavaró komponenst a mért értékből (IR Thermography: How It Works (FLIR 2024), Termografiai vizsgalatok (Haraszti 2013)).

#### 3. Kalibráció és szoftveres korrekció
A hőkamerák gyári kalibrálása fekete test sugárzókkal történik (d1_lecturenotes.docx, Infrared Energy, Emissivity, Reflection & Transmission (FLIR)). A mérési egyenletben a szoftver figyelembe veszi az alábbiakat a pontos eredményhez:
*   A légkör transzmisszióját ($\tau_{atm}$) és hőmérsékletét ($T_{atm}$) (IR Thermography: How It Works (FLIR 2024)).
*   Az objektum távolságát, mivel a levegőben lévő vízpára és $CO_2$ elnyeli a sugárzás egy részét (Termografiai vizsgalatok (Haraszti 2013)).

**A források nem tartalmaznak információt a következőre: NUC (Non-Uniformity Correction) kalibráció.** A források említik a detektorok integrált kiolvasó áramköreit (ROIC) és a vákuum fontosságát a mikrobolométereknél (Mikrobolométer technológia - Thermo Delta Kft.), de a specifikus "NUC" rövidítést nem részletezik.

### Összefoglaló a mérést befolyásoló adatokról

| Paraméter | Hatása a mérésre | Releváns forrás |
| :--- | :--- | :--- |
| **Emisszió ($\varepsilon$)** | Meghatározza a saját sugárzás arányát. | Termografiai vizsgalatok (Haraszti 2013) |
| **Visszavert hőmérséklet** | A tükröződő felületek "ál-hőmérsékletét" okozza. | IR Thermography: How It Works (FLIR 2024) |
| **Légköri transzmisszió** | A távolság és páratartalom miatti jelveszteséget korrigálja. | IR Thermography: How It Works (FLIR 2024) |
| **Mérési szög** | Túl lapos szögben az emisszió lecsökken, a reflexió megnő. | Emissivity - Wikipedia, flir_emissivity_guide.pdf |