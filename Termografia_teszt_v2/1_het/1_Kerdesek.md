---
title: 1_Kerdesek -- Infravörös Termográfia
type: output
status: ready
updated: 2026-05-24
description: BSc (4 db) + MSc (2 db) vizsgakérdések -- NLM Q5 alapján.
---
# 1_Kerdesek -- Infravörös Termográfia

_Forrás: NLM Termografia\_teszt\_v2 Q5 lekérdezés_

Alább olvasható négy BSc és két MSc szintű vizsgakérdés az infravörös termográfia témaköréből, a megadott források alapján összeállítva:

### BSc szintű vizsgakérdések (Alapelvek)

**1. Kérdés: Definiálja az infravörös termográfia fogalmát és nevezze meg a három alapvető hőközlési módot!**
*   **Elvárt válasz fő pontjai:**
    *   Az infravörös termográfia egy érintésmentes mérési eljárás, amely a tárgyak láthatatlan infravörös sugárzását vizuális képpé (hőtérképpé) alakítja (d1_lecturenotes.docx).
    *   Hővezetés (kondukció): energiaátadás részecskék elmozdulása nélkül, főleg szilárd testekben (d1_lecturenotes.docx).
    *   Hőszállítás (konvekció): energiaszállítás folyadékok vagy gázok részecskéinek áramlása útján (d1_lecturenotes.docx).
    *   Hősugárzás (radiáció): elektromágneses hullámok útján történő terjedés, amelyhez nincs szükség közvetítő közegre (d1_lecturenotes.docx, haraszti2013_termografia.pdf).
*   **SZINT:** BSc

**2. Kérdés: Ismertesse az emissziós tényező fogalmát és a mérést befolyásoló legfontosabb tényezőket!**
*   **Elvárt válasz fő pontjai:**
    *   Az emissziós tényező ($\varepsilon$) egy arányszám (0 és 1 között), amely megmutatja, hogy egy felület milyen hatékonysággal sugároz az ideális fekete testhez képest (flir_emissivity_guide.pdf, Emissivity - Wikipedia).
    *   Befolyásolja az anyagi minőség, a felület érdessége és oxidációs foka (flir_emissivity_guide.pdf, haraszti2013_termografia.pdf).
    *   Függ a mérési szögtől: a merőlegestől való jelentős eltérés (pl. 60° felett) drasztikusan csökkentheti az emissziót (flir_emissivity_guide.pdf).
    *   Helytelen megválasztása jelentős mérési hibához, akár nagyságrendi hőmérsékleti eltéréshez vezethet (haraszti2013_termografia.pdf).
*   **SZINT:** BSc

**3. Kérdés: Magyarázza el a Wien-féle eltolódási törvény lényegét és annak gyakorlati jelentőségét a hőkamerák kiválasztásakor!**
*   **Elvárt válasz fő pontjai:**
    *   A törvény kimondja, hogy a sugárzási maximumhoz tartozó hullámhossz ($\lambda_{max}$) fordítottan arányos a test abszolút hőmérsékletével (d1_lecturenotes.docx, flir2024_howworks.pdf).
    *   A hőmérséklet emelkedésével a kisugárzott energia maximuma a rövidebb hullámhosszak felé tolódik (d1_lecturenotes.docx).
    *   Gyakorlati jelentőség: alacsony hőmérsékletű mérésekhez (pl. épületdiagnosztika) hosszúhullámú (LWIR), míg magas hőmérsékletű ipari folyamatokhoz középhullámú (MWIR) kamera az optimális (flir2024_howworks.pdf, haraszti2013_termografia.pdf).
*   **SZINT:** BSc

**4. Kérdés: Mutasson be két konkrét ipari alkalmazási példát, ahol a termográfia a megelőző karbantartást segíti!**
*   **Elvárt válasz fő pontjai:**
    *   Villamos hálózatok: laza kötések, túlterhelt vezetékek vagy aszimmetrikus fázisterhelések detektálása a tűzkárok megelőzése érdekében (Hőkamerák villamos szakembereknek).
    *   Gépészeti berendezések: motorok vagy szivattyúk csapágyainak ellenőrzése; a rendellenes melegedés kopást vagy kenési hibát jelezhet (Hoterkep-keszites a karbantarto szemszogebol.pdf).
    *   Trendfigyelés: a rendszeres mérések során készült hőképek összehasonlítása a korábbi állapotokkal (Hoterkep-keszites a karbantarto szemszogebol.pdf).
*   **SZINT:** BSc

---

### MSc szintű vizsgakérdések (Matematikai összefüggések és méréstechnika)

**5. Kérdés: Vezesse le a hőkamera által érzékelt teljes sugárzási teljesítmény (W_tot) összetevőit a sugárzási egyenleg és a Kirchhoff-törvény alapján!**
*   **Elvárt válasz fő pontjai:**
    *   A sugárzási egyenleg alapja: $\varepsilon + \rho + \tau = 1$ (emisszió + reflexió + transzmisszió) (d1_lecturenotes.docx, flir2024_howworks.pdf).
    *   A Kirchhoff-törvény értelmében az emissziós tényező megegyezik az abszorpciós tényezővel ($\varepsilon = \alpha$) (d1_lecturenotes.docx).
    *   A kamera által mért teljes sugárzás három fő forrásból adódik: a tárgy saját sugárzása ($\varepsilon \cdot \tau_{atm} \cdot W_{obj}$), a környezet visszavert sugárzása ($\rho \cdot \tau_{atm} \cdot W_{amb}$) és a légkör saját sugárzása ($(1-\tau_{atm}) \cdot W_{atm}$) (flir2024_howworks.pdf).
    *   Átlátszatlan testek esetén ($\tau=0$), a reflexió kifejezhető az emisszióval: $\rho = 1 - \varepsilon$ (flir2024_howworks.pdf).
*   **SZINT:** MSc

**6. Kérdés: Elemezze az emisszió irányfüggését leíró koszinusz-modell matematikai hátterét és annak hatását a kvantitatív termográfiára!**
*   **Elvárt válasz fő pontjai:**
    *   A felületi emisszió nem izotróp; az irányfüggést gyakran az $\varepsilon(\alpha) = \varepsilon_0 \cdot \cos^n(\alpha)$ modell írja le, ahol $\varepsilon_0$ a felületre merőleges emisszió (Emissivity - Wikipedia).
    *   Az '$n$' kitevő jellemzi a diffúz viselkedéstől való eltérést; nagyobb '$n$' érték esetén az emisszió meredekebben csökken a látószög növekedésével (Emissivity - Wikipedia).
    *   Méréstechnikai következmény: nagy látószögnél a detektált sugárzásban megnő a visszavert háttérsugárzás aránya, ami jelentős alulmérést eredményezhet a valós hőmérséklethez képest (Emissivity - Wikipedia).
    *   A mérés pontossága érdekében a geometriai tényezőt (optogeometriai faktor) be kell építeni a kvantitatív termográfiai egyenletbe (Emissivity - Wikipedia).
*   **SZINT:** MSc