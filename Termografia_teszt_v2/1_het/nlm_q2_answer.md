<!-- Q2 answer -->
Az infravörös termográfia elméleti hátterét négy alapvető fizikai sugárzási törvény határozza meg, amelyek leírják az objektumok hőmérséklete és az általuk kibocsátott elektromágneses sugárzás közötti összefüggéseket.

### 1. Stefan–Boltzmann-törvény

**Matematikai definíció:**
$$E_{(f)}(T) = \sigma \cdot T^4$$
vagy szürke testekre:
$$W = \varepsilon \cdot \sigma \cdot T^4$$
Ahol:
*   **$E_{(f)}$** vagy **$W$**: A kisugárzott összes teljesítmény (sugárzási fluxus) egységnyi felületre vonatkoztatva [$W/m^2$] [1-3].
*   **$\sigma$**: Stefan–Boltzmann-állandó ($5,67 \cdot 10^{-8} \ W/m^2K^4$) [2-4].
*   **$T$**: Az objektum abszolút hőmérséklete [Kelvin] [1, 3, 5].
*   **$\varepsilon$**: Emissziós tényező (fekete test esetén $\varepsilon = 1$) [2, 6].

**Fizikai értelmezés:**
A törvény kimondja, hogy egy fekete test által kibocsátott teljes sugárzási energia arányos az abszolút hőmérsékletének negyedik hatványával [1, 3]. Ez azt jelenti, hogy a hőmérséklet kismértékű emelkedése a kisugárzott energia jelentős növekedését eredményezi, ami lehetővé teszi a hőkamerák számára a pontos hőmérséklet-meghatározást [3, 7].

### 2. Planck-féle sugárzási törvény

**Matematikai definíció:**
Planck törvénye megadja a fekete test spektrális emisszióképességét ($e_{\lambda,T}$) a hullámhossz ($\lambda$) és a hőmérséklet ($T$) függvényében [8, 9]. Bár a képlet komplex, alapja az energia kvantált természete:
$$E = h \cdot \nu$$
Ahol **$h$** a Planck-állandó ($6,626 \cdot 10^{-34} \ Js$), **$\nu$** pedig a frekvencia [10-12].

**Fizikai értelmezés:**
A Planck-törvény leírja a hősugárzás intenzitásának spektrális eloszlását egy adott hőmérsékleten [9, 13]. Kimutatja, hogy az energia nem folytonosan, hanem diszkrét adagokban (kvantumokban) adódik át [12, 14]. A törvény grafikus megjelenítése a Planck-görbék sorozata, amelyek megmutatják, hogy minden hőmérséklethez egy egyedi sugárzáseloszlási görbe tartozik [5, 9].

### 3. Wien-féle eltolódási törvény

**Matematikai definíció:**
$$\lambda_{max} = \frac{b}{T}$$
vagy a forrásokban megadott állandóval:
$$\lambda_{max} = \frac{2898}{T}$$
Ahol:
*   **$\lambda_{max}$**: Az a hullámhossz, ahol a sugárzás intenzitása maximális [$\mu m$] [5, 15].
*   **$b$**: Wien-féle állandó ($2,9 \cdot 10^{-3} \ mK$) [16].
*   **$T$**: Abszolút hőmérséklet [Kelvin] [5, 15].

**Fizikai értelmezés:**
A törvény szerint a sugárzó test hőmérsékletének növekedésével a sugárzási maximumhoz tartozó hullámhossz a rövidebb hullámhosszak felé tolódik [7, 15, 17]. Ez magyarázza meg, miért változik egy izzó test színe a hőmérséklet emelkedésével vörösről sárgára, majd fehérre [9, 15]. Környezeti hőmérsékleten ($300 \ K$) a maximum körülbelül $10 \ \mu m$ környékén (infravörös tartomány) található [5].

### 4. Kirchhoff-féle sugárzási törvény

**Matematikai definíció:**
$$\alpha = \varepsilon$$
vagy részletesebben:
$$\frac{e(\nu, T)}{a(\nu, T)} = E_{(f)}(\nu, T)$$
Ahol **$\alpha$** az abszorpciós képesség (elnyelés) és **$\varepsilon$** az emissziós tényező (kisugárzás) [18-20].

**Fizikai értelmezés:**
Kirchhoff törvénye kimondja, hogy egy adott hőmérsékleten és hullámhosszon egy test emissziós képessége megegyezik az abszorpciós képességével [20, 21]. Ez azt jelenti, hogy azok a testek, amelyek jól nyelik el a sugárzást, jó sugárzók is (pl. a korom), míg a rossz elnyelők (mint a fényes fémek) rossz sugárzók és jó visszaverők [18, 21].

### Összefoglaló táblázat

| Törvény | Fő üzenet | Releváns forrás |
| :--- | :--- | :--- |
| **Stefan–Boltzmann** | A teljes sugárzott energia a hőmérséklet negyedik hatványával arányos. | haraszti2013_termografia.pdf [3], d1_lecturenotes.docx [1] |
| **Planck** | A sugárzás spektrális eloszlása a kvantumelméleten alapul. | flir2024_howworks.pdf [13], d1_lecturenotes.docx [9] |
| **Wien** | A hőmérséklet emelkedésével a sugárzási csúcs a rövidebb hullámhosszak felé tolódik. | flir_emissivity_guide.pdf [7], d1_lecturenotes.docx [15] |
| **Kirchhoff** | Egy test ugyanolyan mértékben sugároz, mint amilyen mértékben elnyel ($\varepsilon = \alpha$). | flir2024_howworks.pdf [20], d1_lecturenotes.docx [19] |