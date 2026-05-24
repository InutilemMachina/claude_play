<!-- Q1 answer -->
Az infravörös termográfia egy olyan érintésmentes mérési eljárás, amely a tárgyak által kibocsátott láthatatlan infravörös sugárzást elektronikus jelekké, majd vizuális képpé – hőtérképpé vagy termogrammává – alakítja (d1_lecturenotes.docx, flir2024_howworks.pdf). Ez a technológia lehetővé teszi a felületi hőmérséklet-különbségek detektálását és a pontos hőmérsékletértékek meghatározását anélkül, hogy a mérőműszer érintkezne a vizsgált felülettel (flir2024_howworks.pdf, haraszti2013_termografia.pdf).

### Alkalmazási területek
A termográfiát széles körben alkalmazzák a diagnosztika és a karbantartás területén:
*   **Villamos diagnosztika:** Kötéshibák, korrodált csatlakozások, túlterhelt vezetékek és aszimmetrikus terhelések keresése transzformátorokban, kapcsolószekrényekben és napelemes rendszerekben (Hőkamerák villamos szakembereknek, Hoterkep-keszites a karbantarto szemszogebol.pdf).
*   **Gépészeti karbantartás:** Motorok, csapágyak, szivattyúk és hajtóművek rendellenes felmelegedésének ellenőrzése (Hoterkep-keszites a karbantarto szemszogebol.pdf).
*   **Épületdiagnosztika:** Hőszigetelési hiányosságok, hőhidak, nedvesedés és tetőszivárgások felderítése (d1_lecturenotes.docx, Hoterkep-keszites a karbantarto szemszogebol.pdf).
*   **Tudományos és környezeti vizsgálatok:** Planetáris hőmérséklet-mérések, űreszközök hővédelmének ellenőrzése és a globális felmelegedéssel kapcsolatos kutatások (Emissivity - Wikipedia).

### Fizikai alapelvek
A termográfia működése a hősugárzás (radiáció) jelenségén és alapvető fizikai törvényeken nyugszik:
1.  **Emisszió:** Minden test, amelynek hőmérséklete meghaladja az abszolút nulla fokot (0 K vagy -273,15 °C), elektromágneses sugárzást bocsát ki (d1_lecturenotes.docx, flir2024_howworks.pdf).
2.  **Stefan-Boltzmann törvény:** Kimondja, hogy a fekete test által kisugárzott összes energia a test abszolút hőmérsékletének negyedik hatványával arányos (d1_lecturenotes.docx, haraszti2013_termografia.pdf).
3.  **Planck-féle sugárzási törvény:** Leírja a sugárzás spektrális eloszlását a hullámhossz függvényében egy adott hőmérsékleten (d1_lecturenotes.docx, flir2024_howworks.pdf).
4.  **Wien-féle eltolódási törvény:** Megmutatja, hogy a hőmérséklet emelkedésével a sugárzás intenzitásának maximuma a rövidebb hullámhosszak felé tolódik (d1_lecturenotes.docx, flir2024_howworks.pdf).
5.  **Kirchhoff-féle sugárzási törvény:** Megállapítja, hogy egy test emissziós képessége és abszorpciós (elnyelő) képessége egy adott hullámhosszon és hőmérsékleten megegyezik (d1_lecturenotes.docx, flir_emissivity_guide.pdf).

### Leglényegesebb jellemzők és paraméterek

| Jellemző | Meghatározás | Forrás |
| :--- | :--- | :--- |
| **Emissziós tényező (ε)** | A tárgy sugárzási hatékonysága az ideális fekete testhez képest (értéke 0 és 1 között mozog). | flir_emissivity_guide.pdf, haraszti2013_termografia.pdf |
| **Sugárzási egyenleg** | A beeső sugárzás sorsa: emisszió + reflexió (visszaverődés) + transzmisszió (áteresztés) = 1. | d1_lecturenotes.docx, flir2024_howworks.pdf |
| **Atmoszferikus ablakok** | Azon spektrális tartományok (3-5 μm és 8-14 μm), ahol a légkör jól átereszti az infravörös sugárzást. | flir2024_howworks.pdf, haraszti2013_termografia.pdf |
| **Hőkamera detektor** | Eszköz, amely a sugárzást elektromos jellé alakítja; leggyakoribb a hűtés nélküli mikrobolométer. | flir2024_howworks.pdf, Mikrobolométer technológia - Thermo Delta Kft. |
| **NETD (Termikus érzékenység)** | A legkisebb hőmérsékletkülönbség, amelyet a kamera még érzékelni képes (mK-ben megadva). | Hőkamerák villamos szakembereknek |