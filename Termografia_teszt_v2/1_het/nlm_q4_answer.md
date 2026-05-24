<!-- Q4 answer -->
Az infravörös termográfia az ipari diagnosztika egyik legsokoldalúbb eszköze, mivel lehetővé teszi a berendezések üzem közbeni, érintésmentes vizsgálatát, feltárva a szemmel nem látható hőtani anomáliákat. Az alábbiakban részletezem az alkalmazási területeket a forrásdokumentumok alapján:

### 1. Általános karbantartás és állapotfüggő diagnosztika
A termográfia alapvető eleme a számítógéppel támogatott megelőző karbantartásnak (*Computer-Aided Predictive Maintenance*), ahol a cél a gépek ideális üzemi hőmérsékletétől való eltérések korai detektálása (D1 Lecture Notes (Termografia).docx).
*   **Trendfigyelés:** A karbantartók évente legalább egyszer hőtérképet készítenek a kritikus egységekről, és az új képeket összehasonlítják a korábbi állapotokkal (Hoterkep-keszites a karbantarto szemszogebol.pdf).
*   **Hiba-beazonosítás:** Ha egy forró pont (*hot spot*) jelenik meg ott, ahol korábban nem volt, az közeledő meghibásodást jelez, így a javítás még a leállás előtt ütemezhető (Hoterkep-keszites a karbantarto szemszogebol.pdf).
*   **Előnyök:** Üzem közben végezhető, nincs kényszerű leállás, és biztonságos távolságból ellenőrizhetők a nehezen elérhető (pl. mennyezeti) alkatrészek is (Hoterkep-keszites a karbantarto szemszogebol.pdf).

### 2. Villamosipari alkalmazások
A villamosiparban nincsenek kötelező szabványok, de szigorú irányelvek (pl. NETA) szabályozzák a mérést, ahol a környezeti hőmérséklethez vagy a fázisok közötti különbséghez (*ΔT*) viszonyítanak (Hőkamerák villamos szakembereknek).
*   **Kötéshibák:** A laza vagy korrodált csatlakozások megnövekedett ellenállása hőt termel. Például egy meglazult kötés 48,7 °C-os felmelegedést is mutathat (Hőkamerák villamos szakembereknek).
*   **Túlterhelés:** A túlterhelt vezetékek vagy kismegszakítók jól láthatóan magasabb hőmérsékletűek; egy túlterhelt kismegszakító hőmérséklete elérheti a 41,9 °C-ot (Hőkamerák villamos szakembereknek).
*   **Alkatrészek öregedése:** Az elöregedett kerámiaszigetelések vagy kötőelemek túlhevülése (pl. 49,7 °C-os érték) időben jelezheti a tűzveszélyt (Hőkamerák villamos szakembereknek).
*   **Napelemes rendszerek:** A cellák állapotának ellenőrzésekor kimutatható az ún. *HotSpot* effektus, amelyet például árnyékhatás is okozhat, és a cella 53,8 °C-ra való hevülését eredményezheti (Hőkamerák villamos szakembereknek).

### 3. Gépészeti diagnosztika
A gépészetben a súrlódás és a kenési elégtelenségek okozta hőmérséklet-emelkedés a legfontosabb jelzőszám (Hoterkep-keszites a karbantarto szemszogebol.pdf).
*   **Forgógépek:** Motorok, szivattyúk, ventilátorok és kompresszorok csapágyainak ellenőrzése. A forró pontok jelzik a csapágykopást vagy a tengelyirányú beállítási hibákat (Hoterkep-keszites a karbantarto szemszogebol.pdf).
*   **Erőátvitel:** Hajtóművek, fogaskerék-házak és konvejorok (szállítószalagok) hőeloszlásának vizsgálata (Hoterkep-keszites a karbantarto szemszogebol.pdf).
*   **Folyamatműszerezés:** Szelepek, gőzcsapdák és csővezetékek elzáródásának vagy szivárgásának detektálása (Hoterkep-keszites a karbantarto szemszogebol.pdf).

### 4. Épületdiagnosztika és építészet
Az építészetben a termográfia a szerkezeti integritás és az energiahatékonyság vizsgálatára szolgál (D1 Lecture Notes (Termografia).docx).
*   **Hőszigetelés ellenőrzése:** A szigetelési hiányosságok és hőhidak pontos helye beazonosítható a falak külső felületének termális elváltozásai alapján (D1 Lecture Notes (Termografia).docx).
*   **Nedvesség detektálása:** A vízzel átitatott lapos tető éjszaka tovább tartja a nappali meleget, mint a száraz részek, így a szivárgások helye éjszakai méréssel pontosan meghatározható (D1 Lecture Notes (Termografia).docx).
*   **Nyílászárók:** Az alacsony emissziós (Low-E) bevonattal ellátott ablakok hatékonysága mérhető; ezek télen akár felére is csökkenthetik a hőveszteséget a bevonat nélküli üvegekhez képest (Emissivity - Wikipedia).
*   **HVAC rendszerek:** A fűtési, szellőztetési és légkondicionáló berendezések, valamint a padlófűtés csővezetékeinek roncsolásmentes keresése (Hoterkep-keszites a karbantarto szemszogebol.pdf).

### Összefoglaló táblázat a diagnosztikai példákról

| Terület | Vizsgált jelenség | Konkrét példa / Érték | Forrás |
| :--- | :--- | :--- | :--- |
| **Villamosipar** | Túlterhelt alkatrész | 41,9 °C-os kismegszakító | Hőkamerák villamos szakembereknek |
| **Villamosipar** | Napelem hiba | 53,8 °C-os HotSpot (árnyék miatt) | Hőkamerák villamos szakembereknek |
| **Építészet** | Tetőszivárgás | Nedves szigetelés hővisszatartása éjjel | D1 Lecture Notes (Termografia).docx |
| **Gépészet** | Csapágyhiba | Rendellenes melegedés a motorháznál | Hoterkep-keszites a karbantarto szemszogebol.pdf |
| **Építészet** | Low-E üvegezés | 50%-os hőveszteség-csökkenés | Emissivity - Wikipedia |