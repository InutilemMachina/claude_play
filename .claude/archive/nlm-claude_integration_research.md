---
title: NLM_CLAUDE_INTEGRATION.MD — NLM-Claude integrációs útmutató
type: meta
tags: [meta, reference]
updated: 2026-05-21
description: Kutatási összefoglaló a NotebookLM+Claude integrációs lehetőségekről. Eszközök, MCP setup, meta-prompt architektúra (6. fejezet), tesztelési státusz.
---
# **A Google NotebookLM és az Anthropic Claude Rendszerintegrációs Architektúrája: Kétoldalú Adatcsere, Hierarchikus Lekérdezések és Munkafolyamat-Automatizáció**

A modern tudásmenedzsment és kutatási munkafolyamatok egyik legjelentősebb kihívása a célspecifikus mesterséges inteligenciát használó eszközök közötti fragmentáció felszámolása. A Google NotebookLM kiemelkedő képességekkel rendelkezik a szigorúan dokumentumokhoz kötött visszakeresés (Retrieval-Augmented Generation – RAG) és a zárt világ feltételezésén alapuló, hallucinációmentes információ-visszanyerés terén. Ezzel szemben az Anthropic Claude modellek – különösen a Sonnet és a készülő fejlettebb változatok – kimagasló kognitív szintetizáló, strukturáló és kódolási képességeket mutatnak fel a lokális és felhőalapú környezetekben.  
A két rendszer összekapcsolása egy olyan szinergicus architektúrát hoz létre, ahol a NotebookLM működik strukturált, zéró tokenköltségű memóriarétegként, míg a Claude a végrehajtó és elemző motor szerepét tölti be. Ez a jelentés részletesen bemutatja azokat a közvetlen és áthidaló megoldásokat, amelyek lehetővé teszik a két platform közötti kétoldalú adatcserét, a hivatkozások átvételét, a gondolattérképek exportálását, a Claude által vezérelt, egyedi hierarchia szerinti automatizált lekérdezéseket, valamint a teljes mértékben auditálható forrás- és ábrahivatkozási rendszert.

## **1\. A NotebookLM-ből származó válaszok és hivatkozások átvétele**

A NotebookLM egyik alapvető strukturális korlátja, hogy az adatok és hivatkozások alapértelmezetten a Google ökoszisztémájában maradnak, a chat-előzmények közvetlen exportálására pedig a platform nem biztosít natív funkciót. A válaszok és a hozzájuk kapcsolódó pontos forrásattribúciók kinyerésére és Claude-ba történő átvitelére több szoftveres áthidaló megoldás áll rendelkezésre, amelyek eltérő integrációs szinteket képviselnek.  
A hivatkozások strukturált exportálására alkalmas megoldásokat az alábbi összehasonlító táblázat rendszerezi:

| Megoldás megnevezése | Típus | Kivitelezés bonyolultsága | Fő kimeneti formátum | Citációs képességek és sajátosságok |
| :---- | :---- | :---- | :---- | :---- |
| **Markdown Capturer \- BibCit (v2.5)** | Chrome / Firefox kiterjesztés | Alacsung | Markdown, Word (.docx), PDF | A NotebookLM által adott számozott hivatkozásokat automatikusan átalakítja szabványos tudományos in-text hivatkozásokká (APA, Harvard, MLA, IEEE és további 10 000+ stílusban), valamint a dokumentum végén teljes bibliográfiát generál. Csak az extension telepítése után létrehozott új notebookok esetén működik megfelelően. |
| **NotebookLM Export Pro** | Chrome kiterjesztés | Alacsung | Markdown, PDF, LaTeX, Notion | Egyetlen kattintással kimenti a kijelölt forrásokat, a chat-előzményeket a pontos citációkkal együtt, valamint a személyes és AI-generált Studio jegyzeteket. Közvetlen Notion szinkronizációval rendelkezik. |
| **Apify NotebookLM API Actor** | Felhőalapú programozott API | Közepes | JSON, CSV, Markdown, Excel | Teljesen automatizált, RAG csővezetékekbe illeszthető megoldás. Google App Password használatával lép be, és strukturált formában adja vissza a teljes beszélgetési történetet, a források metaadatait és a citációs leképezéseket. |

A kiterjesztésalapú megközelítések (például a BibCit) működési mechanizmusa a böngésző DOM-struktúrájának valós idejű leolvasásán alapul. Amikor a NotebookLM generál egy választ, a BibCit rögzíti a számozott szürke indexeket, lekéri a hozzájuk tartozó forrásszöveg-részleteket és metaadatokat, majd a kiválasztott akadémiai stílusnak megfelelően átformázza azokat. Ez a folyamat kiküküszöböli a manuális másolás-beillesztés során fellépő formázási hibákat és a hivatkozások elvesztését.

## **2\. A NotebookLM mindmap (gondolattérkép) hierarchiájának átvétele**

A NotebookLM képes SVG/PNG-alapú gondolattérképeket generálni az feltöltött dokumentumokból a Studio panelen belül, azonban ezek közvetlen szerkesztésére a felület nem biztosít lehetőséget. A hierarchikus struktúra kinyerésére és Claude-ba vagy külső szerkesztőkbe való átvitelére az alábbi két fő áthidaló megoldás alkalmazható.

### **A. Közvetlen Markdown másolási és finomítási munkafolyamat**

A legegyszerűbb, kiterjesztés nélküli megoldás a NotebookLM beépített exportálási funkciójára épül :

1. A NotebookLM Studio paneljén meg kell nyitni a generált gondolattérképet.  
2. Manuálisan ki kell bontani a kívánt ágakat a részletességi szint beállításához.  
3. A jobb felső sarokban található **Copy as Markdown** (Másolás Markdownként) gombra kattintva a vágólapra másolható a strukturált hierarchia.  
4. Ez a hierarchikus szöveg közvetlenül beilleszthető a Claude-ba további elemzésre, vagy olyan online eszközökbe, mint az Xmind Markdown-to-Mindmap konvertere, amely azonnal szerkeszthető vizuális struktúrává alakítja a tabulátorokkal tagolt szöveget.

### **B. Automatizált strukturális kinyerés kiterjesztéssel**

Ha mélyebb, géppel olvasható hierarchiára van szükség, a **NotebookLM Mindmap Extractor** kiterjesztés alkalmazható :

1. A gondolattérkép megnyitása és teljes kibontása után a kiterjesztés a DOM-ból kiolvassa az SVG csomópontok X-koordinátáit és összeköttetéseit.  
2. A hierarchikus összefüggéseket elemző algoritmus segítségével rekonstruálja a szülő-gyermek kapcsolatokat.  
3. A kimenet letölthető **FreeMind (.mm)**, **OPML** vagy **XML** formátumban. Az OPML és.mm fájlok közvetlenül beolvashatók mind vizuális gondolattérkép-szerkesztőkbe, mind pedig XML-ként a Claude környezetébe, megőrizve a pontos nódus-hierarchiát.

A kinyert hierarchia tisztításához és strukturálásához az alábbi szabályrendszer követése javasolt a Claude felületén történő feldolgozás előtt :

* **Értelmes címkék alkalmazása**: Az olyan általános csomópontokat, mint az "Áttekintés" vagy "Részletek", át kell nevezni specifikus kifejezésekre, például "Kulcsfontosságú megállapítások" vagy "Korlátozások".  
* **Csomópontok minimalizálása**: Minden csomópont csak egyetlen állítást vagy fogalmat tartalmazhat. A hosszú mondatokat gyermekcsomópontokra kell bontani.  
* **Hierarchia-korrekció**: A támogató részleteket mélyebb szintekre kell süllyeszteni, míg az ismétlődő koncepciókat egyetlen közös szülőcsomópont alatt kell egyesíteni.

## **3\. Lekérdezések futtatása egyedi Markdown-hierarchia alapján a Claude által**

Ahhoz, hogy a Claude képes legyen a felhasználó által definiált, egyedi Markdown-hierarchia (például egy részletes tartalomjegyzék, kutatási vázlat vagy kérdésstruktúra) mentén szisztematikusan lekérdezni a NotebookLM-et, egy kétirányú Model Context Protocol (MCP) hidat kell kiépíteni.

### **A működési elv és adatfolyam**

A Claude nem képes közvetlenül böngészni a NotebookLM felületét hivatalos API-kulcsok hiányában. A megoldás egy helyi MCP szerver futtatása (notebooklm-mcp-cli), amely cookie-alapú hitelesítéssel, böngésző-automatizáción keresztül szimulálja a lekérdezéseket.  
Az MCP architektúra alkalmazása jelentős token-megtakarítást eredményez a Claude oldalon. Ahelyett, hogy a teljes dokumentációt beolvasnánk a Claude kontextusába, a lekérdezés a helyi MCP szerveren keresztül fut le. A Google Gemini motorja végzi el a dokumentumok közötti keresést (RAG), és csak a szintetizált választ küldi vissza a Claude-nak. A token-megtakarítás aránya a következőképpen modellezhető:  
ahol T\_{\\text{forrás}} a NotebookLM-be feltöltött összes dokumentum szószáma (amely notebookonként akár 25 millió szó is lehet) , míg T\_{\\text{szintetizált}} a Claude által fogadott, citációkkal ellátott válasz hossza (jellemzően 1500–3000 token).

### **Az integráció lépései és konfigurációja**

1. **Környezet előkészítése**: Telepíteni kell az Astral uv Python csomaggyűjtőt :  
   `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. **Az MCP CLI telepítése**:  
   `uv tool install notebooklm-mcp-cli`  
   Ez létrehozza az nlm parancssori eszközt és a notebooklm-mcp binárist.  
3. **Google-hitelesítés**:  
   `nlm login`  
   Ez megnyit egy Chrome vagy Brave ablakot, ahol be kell lépni a NotebookLM-et hosztoló Google-fiókba. A munkamenet-cookie-k helyben mentésre kerülnek, és 2-4 hétig érvényesek.  
4. **Claude konfigurálása**: A Claude Desktop konfigurációs fájljához (claude\_desktop\_config.json) hozzá kell adni az MCP szervert :  
   `{`  
     `"mcpServers": {`  
       `"notebooklm": {`  
         `"type": "stdio",`  
         `"command": "notebooklm-mcp",`  
         `"args":,`  
         `"env": {}`  
       `}`  
     `}`  
   `}`

### **Példa prompt a Claude számára a hierarchikus lekérdezés futtatásához**

Miután a Claude felülete jelzi az aktív MCP kapcsolatot, az alábbi prompt sablonnal utasítható a strukturált dokumentum elkészítésére:  
Olvasd be a következő Markdown struktúrát. Menj végig szisztematikusan minden egyes alfejezeten (H3-as szint), és a kapcsolódó kérdést küldd el lekérdezésként a NotebookLM MCP szervernek az 'Azure-Cert-Research' nevű notebookomban. A kapott válaszokat a pontos szövegközi forráshivatkozásokkal együtt integráld a megfelelő fejezet alá.  
Saját hierarchia:

# **Azure AI-900 Kutatási Jelentés**

## **1\. Gépi tanulási alapelvek**

### **1.1 Felügyelt vs. Felügyelet nélküli tanulás**

Kérdés a NotebookLM-hez: "Mi a különbség a felügyelt és felügyelet nélküli tanulás között a forrásaink szerint?"

### **1.2 Regressziós modellek alkalmazása**

Kérdés a NotebookLM-hez: "Milyen konkrét példákat említenek a dokumentumok a regressziós modellek használatára?"  
A Claude ezt követően egymás után végrehajtja a lekérdezéseket, majd az összesített, formázott Markdown fájlt menti a helyi könyvtárba.

## **4\. Képek és táblázatok kezelése a NotebookLM-ben és a szükséges promptok**

A NotebookLM multimodális képességei és bemeneti korlátai határozzák meg, hogyan képes a Claude-ból érkező képi vagy táblázatos információkat feldolgozni, és azokat hogyan adja vissza a lekérdezések során.

### **Képekkel ellátott Markdown fájlok támogatása**

A NotebookLM támogatja a helyi .md (Markdown) fájlok közvetlen feltöltését forrásként. Fontos korlátozás azonban, hogy a Markdown fájlokban lévő, külső szerverekre mutató kép-URL-eket vagy relatív hivatkozásokat a rendszer nem követi, és a képeket nem tölti le automatikusan a forrás nézetbe. Weboldal URL-importálásakor is kizárólag a HTML szöveges tartalom kerül lekaparásra, a beágyazott képek és videók nélkül.  
Ha képi információkat kell átadni, a képeket külön fájlként (támogatott foráshasználati formátumok: PNG, JPEG, WEBP, HEIC, GIF, BMP, TIFF) kell feltölteni a notebookba. A Gemini alapú motor kiváló OCR és vizuális értelmezési képességekkel rendelkezik; képes diagramok, grafikonok, folyamatábrák és kézzel írt jegyzetek értelmezésére, sőt ezeket össze tudja kapcsolni a környező szöveges forrásokkal. A legjobb RAG-eredmény elérése érdekében javasolt a képekhez részletes alt-text leírást vagy metaadatokat fűzni, mert a NotebookLM így sokkal pontosabban indexeli és rendeli hozzájuk a releváns szöveges kontextust.

### **Táblázatok kezelése és a natív "Data Tables" funkció**

A NotebookLM Pro és Ultra előfizetők számára elérhető a dedikált **Adattáblák (Data Tables)** funkció. Ez lehetővé teszi a kaotikus, strukturálatlan forrásokból származó adatok egyetlen strukturált, többforrásos szintézist tartalmazó táblázatba történő kimentését.

### **Promptolási stratégia a Claude általi felhasználáshoz**

Ahhoz, hogy a Claude az MCP-n keresztül olyan strukturált válaszokat kapjon a NotebookLM-től, amelyek pontosan tartalmazzák a táblázatokat, ábrahivatkozásokat és a hozzájuk tartozó citációkat, szigorú és direkt promptolási struktúrát kell alkalmazni. Az alábbi prompt sablont kell elküldeni a Claude-nak, hogy azt továbbítsa az MCP lekérdezés során:  
Feladat: Készíts egy részletes összehasonlító jelentést a kijelölt források alapján.  
Formázási és strukturális szabályok:

1. Minden numerikus adatot és strukturált összehasonlítást kizárólag szabványos Markdown táblázatként (GitHub Flavored Markdown) ábrázolj. Kerüld a folyószöveges felsorolást a strukturált adatok esetében.  
2. Ha a forrásokban ábrák, diagramok vagy vizuális sémák szerepelnek, hivatkozz rájuk explicit módon, megadva a forrásfájl nevét és az ábra sorszámát (pl. "\[Ábra: forrásfájl\_neve.ext \#1\]").  
3. Minden egyes táblázati cellában vagy állítás végén kötelezően helyezz el forrásattribúciót a NotebookLM belső hivatkozási rendszerével (számozott indexek formájában), hogy a Claude pontosan lássa a forrásdokumentum nevét és a hivatkozott bekezdést.

Lekérdezési cél: "Hozz létre egy strukturált Markdown adattáblázatot a versenytársak technikai paramétereiről. Oszlopok: Versenytárs neve, Algoritmus típusa \[Hivatkozás\], Késleltetési érték \[Hivatkozás\], Megjegyzés az ábrák alapján \[Hivatkozás\]."  
Ez a prompt biztosítja, hogy a NotebookLM által visszaadott szöveges válasz azonnal Markdown-kompatibilis táblázattá alakuljon, amelyet a Claude minimális tokenfelhasználással, formázási sérülés nélkül tud integrálni a végső dokumentumba.

## **5\. Claude Cowork és NotebookLM interfész-integráció**

A felhasználói felületek szintjén két alapvető megközelítés létezik a Claude és a NotebookLM összekapcsolására: a **közvetlen, ágensalapú lokális munkatér** (Claude Cowork plugin) és a **böngésző-automatizációs terminálos áthidalás** (Claude Code CLI plugin).  
A két integrációs felület összehasonlítása az alábbi táblázatban látható:

| Jellemző | Claude Cowork \+ notebooklm-cowork | Claude Code \+ notebooklm-connector |
| :---- | :---- | :---- |
| **Elsődleges felület** | Claude Cowork (lokális ágens és virtuális gép) | Terminál / Parancssor (CLI) |
| **Működési mechanizmus** | MCP szerver hibrid API-hívásokkal | Chrome böngésző-automatizáció (Patchright) |
| **Kommunikációs csatorna** | 39 natív ágens-eszköz (playbook) | Böngésző szimuláció / /notebook slash parancsok |
| **Lekérdezési sebesség** | Gyors (\~10-15 másodperc) | Lassú (\~30-60 másodperc lekérdezésenként) |
| **Automatikus javítás** | Manuális utasításra épülő javítás | Automatikus lefedettség-ellenőrzés (3 körös követés) |
| *Licenc / Követelmény* | Ingyenes / lokálisan futtatható | Anthropic Pro/Max/Teams előfizetés szükséges |

### **A. A közvetlen megközelítés: Claude Cowork \+ notebooklm-cowork plugin**

A Claude Cowork asztali alkalmazás lehetővé teszi, hogy a mesterséges intelligencia ágensként hajtson végre több lépésből álló feladatokat egy kijelölt helyi mappában. A notebooklm-cowork plugin segítségével a Claude Cowork teljes felügyeletet kap a NotebookLM környezet felett.  
A plugin egy 39 eszközből álló eszköztárat (playbook) ad át a Claude-nak, amellyel az alábbi műveletek végezhetők el közvetlenül a beszélgetési felületen keresztül :

* **Notebookok kezelése**: Új notebookok létrehozása, átnevezése, törlése és rendszerezése.  
* **Forráskezelés**: Helyi PDF, DOCX, TXT fájlok, Google Drive dokumentumok vagy webes URL-ek tömeges importálása és szinkronizálása.  
* **Studio-leletek előállítása**: 9-féle különböző formátum (audio podcast, videó vázlat, slide deck stb.) generálása és letöltése.  
* **Kereszt-notebook lekérdezések**: Egyidejű keresés futtatása több különböző notebook forrásanyagaiban.

### **B. Az áthidaló megközelítés: Claude Code \+ Chrome automatizáció**

Ha a munkafolyamat elsősorban parancssori környezetben zajlik, a Claude Code CLI eszköz használható a notebooklm-connector kiterjesztéssel együtt. Ez a megoldás nem igényel bonyolult MCP konfigurációt, hanem a hivatalos Claude Chrome-kiterjesztésen keresztül hajt végre böngésző-automatizációt :

1. El kell indítani a Claude Code-ot a következő paranccsal: claude \--chrome.  
2. Telepíteni kell a plugint:  
   `/plugin marketplac[span_113](start_span)[span_113](end_span)[span_121](start_span)[span_121](end_span)e add LeeJuOh/claude-code-zero`  
   `/plugin install notebooklm-connector@claude-code-zero`

3. Regisztrálni kell a cél-notebook URL-jét, és megkezdhető a lekérdezés.

A megoldás legnagyobb előnye az automatikus lefedettség-ellenőrzés (coverage check). Ha a NotebookLM egy összetett kérdésre csak részleges választ ad vissza, a plugin ezt automatikusan észleli, és célzott pontosító kérdéseket küld vissza (maximum 3 körben), amíg a teljes információ ki nem nyerhető.

## **6\. Auditálhatósági és kétoldalú nyomonkövetési meta-prompt architektúra**

A NotebookLM és a Claude integrációja során a legnagyobb hibaforrás a citációk elvesztése vagy pontatlanná válása. Különösen igaz ez akkor, ha a források nem követik a szigorú akadémiai formázási szabályokat, azaz nincsenek folyószöveges hivatkozások az ábrákhoz, nincsenek sorszámok, vagy a források nevei csupán kaotikus fájlnevek (például tavak2004.pdf).  
A NotebookLM forráslistájában a helyi fájlok **nativan megtartják a kiterjesztésüket** (pl. .pdf, .docx), míg a webes URL-ek a lap címét veszik fel kiterjesztés nélkül. Ahhoz, hogy az emberi ellenőr és mindkét mesterséges intelligencia számára transzparens és auditálható legyen az adatfolyam, egy kétirányú meta-prompt protokollt kell alkalmazni.

### **A. NotebookLM szintű meta-prompt (Custom Instructions)**

Ezt a promptot a NotebookLM **"Configure Chat" (Chat konfigurálása)** felületén, a notebook-szintű egyedi utasításokhoz (Custom Instructions) kell bemásolni. Ez a scope legfeljebb 10 000 karaktert engedélyez, így alkalmas összetett logikai szabályok rögzítésére.

# **SZEREPKÖR ÉS CÉL**

Te egy rendkívül precíz, akadémiai szintű kutatási és adatintegrációs asszisztens vagy. Kizárólag a feltöltött forrásokból dolgozol. Ha egy információ nem található meg a forrásokban, jelöld meg, hogy "A források nem tartalmaznak információt a következőre: \[téma\]".

# **CITÁCIÓS ÉS AUDITÁLÁSI SZABÁLYOK**

1. KÖTELEZŐ FORRÁSMEGJELÖLÉS: Minden egyes állítás, numerikus adat, következtetés vagy megállapítás végén helyezz el szövegközi hivatkozást. Használd a NotebookLM natív számozott szürke indexeit, de a generált folyószövegbe írd bele a pontos forrásfájl nevét a kiterjesztésével együtt (pl. "tavak2004.pdf").  
2. FORRÁSNÉV-KONVENCIÓ: A forrásokra kizárólag a Sources (Források) panelen látható pontos nevükvel és kiterjesztésükkel hivatkozz (pl. "tavak2004.pdf", "report\_clean.docx"). Ha a forrás kiterjesztés nélküli (pl. webes kaparás), használd az ott látható pontos címet. Ne rövidíts és ne változtass a neveken.

# **ÁBRÁK ÉS TÁBLÁZATOK REKONSTRUKCIÓS HEURISZTIKÁJA**

Mivel a forrásokban az ábrák és táblázatok sokszor nem rendelkeznek explicit számozással, címmel vagy folyószöveges hivatkozással, alkalmazd az alábbi kontextuális heurisztikát:

1. VIZUÁLIS ÉS TÁBLÁZATOCR INTEGRÁCIÓ: Ha a PDF vagy kép formátumú forrásban ábra, diagram vagy táblázat található, de nincs sorszáma, elemezd a vizuális tartalmat és a közvetlenül felette/alatta elhelyezkedő 3 bekezdést.  
2. REKONSTRUÁLT HORGONYZÁS: Ha adatot vagy ábra-információt idézel, de az ábra "névtelen", generálj hozzá egy egyedi, kontextusból levezetett horgonyt az alábbi formában: \`\`  
3. IMPLICIT HORGONYOK JELÖLÉSE: Ha a folyószöveg nem hivatkozik egy ábrára, de a felette lévő bekezdésben tárgyalt adatok megegyeznek az ábrán látható értékekkel, kapcsold össze őket, és jelezd explicit módon: "Az adatok vélhetően a forrásban található cím nélküli diagramból származnak: \[Inferred Figure: tavak2004.pdf | Anchored to: '...' text segment\]."

# **KIMENETI FORMÁTUM**

* Válaszaidat strukturált Markdown formátumban add meg.  
* A táblázatokat szabványos GFM (GitHub Flavored Markdown) formában generáld. Minden sor végén és minden cellában szerepeljen a pontos forrásattribúció és a kontextuális horgony, ha nem szabványos ábráról van szó.

### **B. Claude szintű meta-prompt (Claude Project Custom Instructions)**

Ezt az utasításcsomagot a Claude felületén lévő **Project Instructions** (Projekt egyedi utasításai) vagy a Claude Cowork rendszerszintű promptjában kell megadni. Ez segít a Claude-nak abban, hogy a NotebookLM által visszaküldött válaszokat értelmezze, a kiterjesztéssel ellátott fájlneveket valódi szakcikkekként rekonstruálja, és felépítse a teljes mértékben nyomonkövethető audit-ösvényt (audit trail).

# **SYSTEM ROLE & ARCHITECTURAL INSTRUCTIONS**

You are the Chief Synthesis Analyst working in tandem with a Google NotebookLM backend connected via MCP. Your primary task is to take RAG-generated, cited outputs from NotebookLM and compile them into fully synthesized, academic and audit-ready Markdown documents.

# **SOURCE RECONCILIATION & FILE EXTENSION POLICY**

1. EXTENSION MAPPING: NotebookLM natively preserves file extensions for uploaded documents (e.g., "tavak2004.pdf") and strips them for web URLs. You must maintain a strict "Source Mapping Table" in your system memory.  
2. RESOLVE SHORTHAND NAMES: When NotebookLM returns a source name like "tavak2004.pdf", you must cross-reference this with your project knowledge base or use your general reasoning to expand it into a full, professional bibliographic citation in the final Bibliography section.  
   * *Example:* tavak2004.pdf \-\> **Kovács, J. & Nagy, L. (2004). Magyarországi tavak ökológiai állapotfelmérése. Hidrológiai Közlöny, 34(2), 112-125.**

# **INFERRED VISUALS & AUDIT TRAIL RECONSTRUCTION**

You must construct a bulletproof audit trail for figures and tables that lack formal academic anchoring in the source text:

1. HEURISTIC PROCESSING: If NotebookLM returns an implicit horgony (e.g., \`\`), do not discard this metadata. Instead, translate it into a readable, traceable reference in your final document.  
2. DUAL-INDEX CITATION SYSTEM: Format the citations in the final document to include both the human-readable citation and the machine-verifiable source link:  
   * *Format in text:* "...a Balaton foszforterhelése ugrásszerűen megnőtt (tavak2004.pdf, \[Inferred Figure near paragraph: '...'\])."  
3. MISSING CONTEXT DETECTOR (3-ROUND RECOVERY): If NotebookLM returns a table but the source text surrounding it is vague, you must automatically use your MCP tool (notebook\_query) to ask a targeted follow-up question specifically querying the context of that table (e.g., "Analyze the 3 paragraphs surrounding the table containing Balaton phosphorus values in tavak2004.pdf"). Do this for up to 3 rounds to guarantee context completeness before compiling the final document.

# **FINAL OUTPUT VERIFICATION**

Ensure that every table cell containing numerical data, and every mention of an image/chart, has a direct, explicit path mapped back to:

* The exact source filename (with extension, e.g., tavak2004.pdf).  
* The specific page, paragraph, or contextual anchor identified by NotebookLM.  
* The corresponding entry in the consolidated bibliography at the end of the Markdown file.

### **C. A kétoldalú nyomonkövetés működése a gyakorlatban (Példa munkafolyamat)**

1. **Feltöltés és indexelés**: A kutató feltölti a tavak2004.pdf fájlt a NotebookLM-be. A rendszer rögzíti ezt a fájlnevet és kiterjesztést.  
2. **Kérdésküldés a Claude-tól**: A Claude az MCP-n keresztül elküldi a lekérdezést : *"Milyen foszforszintet mértek a tavakban?"*  
3. **Kontextuális elemzés a NotebookLM-ben**: A Gemini motor észleli a tavak2004.pdf fájlban lévő táblázatot. Bár a táblázatnak nincs címe, a NotebookLM Custom Instructions-ben megadott szabályok alapján a modell azonosítja a táblázat melletti bekezdést ("...a méréseket 2004 augusztusában végezték..."), és az alábbi választ generálja:"A tavak foszforszintje 0.45 mg/l volt."  
4. **Végső szintetizálás a Claude-ban**: A Claude fogadja ezt a strukturált választ, és az alábbi formában menti a végső Markdown dokumentumba: A Balaton foszforterhelése a nyári időszakban elérte a 0.45 mg/l értéket (Kovács & Nagy, 2004; tavak2004.pdf, kontextuális horgony: 'a méréseket 2004 augusztusában végezték').  
5. **Eredmény**: Az emberi olvasó számára a szöveg teljesen érthető és tudományosan megalapozott, míg egy későbbi audit során a hivatkozott rész pontosan visszakereshető a NotebookLM-ben a tavak2004.pdf fájl bekezdés-szintű egyezése alapján.

## **7\. Integrációs Eszközök Beszerzési Forrásai és Telepítési Útmutatója**

A fent bemutatott integrációk és kiterjesztések gyakorlati megvalósításához az alábbiakban találhatóak meg a szükséges csomagok, szoftverek hivatalos beszerzési helyei és lépésről lépésre követhető telepítési folyamatai.

### **A. Claude Cowork és a notebooklm-cowork plugin telepítése**

Ez az architektúra helyi ágensként, virtuális gépben futtatja a Claude-ot, és közvetlen elérést biztosít a fájlrendszeredhez.

#### **1\. lépés: Az Astral uv telepítése**

Az uv egy ultragyors Python csomag- és környezetkezelő, amely elengedhetetlen a CLI és az MCP szerver futtatásához.

* **macOS / Linux** terminálban:  
  `curl -LsSf https://astral.sh/uv/install.sh | sh`

* **Windows (PowerShell)** terminálban:  
  `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

*(Megjegyzés: Telepítés után indítsd újra a terminált\!)*

#### **2\. lépés: A notebooklm-mcp-cli szerver telepítése és hitelesítése**

Ez a csomag tartalmazza az MCP protokollt és az nlm parancssori segédeszközt.

* **Telepítés**:  
  `uv tool install notebooklm-mcp-cli`

* **Google bejelentkezés és token-kinyerés**: Futtasd az alábbi parancsot, amely megnyit egy Chrome/Brave ablakot. Jelentkezz be a Google-fiókodba. A parancs automatikusan kinyeri és helyben elmenti a session cookie-kat (2–4 hétig érvényesek):  
  `nlm login`

* **Ellenőrzés** (opcionális, a meglévő notebookjaid listázása):  
  `nlm notebook list`

#### **3\. lépés: A n\[span\_141\](start\_span)\[span\_141\](end\_span)otebooklm-cowork plugin hozzáadása a Claude Cowork-höz**

* **Beszerzési forrás**: A plugin nyílt forráskódú GitHub repozitóriuma elérhető a https://github.com/gfsaaser24/notebooklm-cowork címen.  
* **Telepítés**:  
  1. Töltsd le a GitHub repozitóriumból a notebooklm-co\[span\_143\](start\_span)\[span\_143\](end\_span)work.plugin fájlt.  
  2. Nyisd meg a Claude Cowork asztali alkalmazást, és a beállításoknál húzd be vagy tallózd be a letöltött .plugin fájlt.  
  3. Fogadd el a biztonsági figyelmeztetést, majd indítsd újra a Cowork munkamenetet (session). Az MCP szerver automatikusan elindul a háttérben az nlm\[span\_146\](start\_span)\[span\_146\](end\_span) login során mentett profil használatával.

### **B. Claude Code és a notebooklm-connector plugin telepítése**

Ez a fejlesztői munkafolyamat a terminálból futó Claude Code CLI eszközt kapcsolja össze a NotebookLM felületével Chrome automatizáción keresztül.

#### **1\. lépés: Node.js és npm telepítése**

A Claude Code CLI futtatásához Node.js (v18+) környezetre van szükség.

* **Beszerzési forrás**: Töltsd le az operációs rendszerednek megfelelő telepítőt a hivatalos oldalról: https://nodejs.org  
* **Telepítés**: Futtasd az .msi (Windows) vagy .pkg (macOS) fájlt, és hagyd jóvá az alapértelmezett beállításokat.  
* **Ellenőrzés** a terminálban:  
  `node -v`  
  `npm -v`

#### **2\. lépés: Claude Code CLI telepítése és aktiválása**

* **Beszerzési forrás**: A hivatalos @anthropic-ai/claude-code npm csomag.  
* **Telepítés** globálisan a rendszereden (figyelem: ne használd a sudo parancsot a jogosultsági hibák elkerülése érdekében):  
  `npm install -g @anthropic-ai/claude-code`

* **Aktiválás**: Lépj be a projekt könyvtáradba, írd be a claude parancsot, és kövesd az OAuth bejelentkezési utasításokat az Anthropic fiókod összekapcsolásához.

#### **3\. lépés: Chrome integráció előkészítése**

* **Beszerzési forrás**: Telepítsd a hivatalos **Claude in Chrome** (v1.0.36+) böngészőbővítményt a Chrome Web Store-ból: https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn  
* **Futtatás**: Indítsd el a terminálban a Claude Code-ot úgy, hogy engedélyezed a Chrome automatizációt:  
  `claude --chrome`  
  *(Győződj meg róla, hogy a megnyíló Chrome böngészőben be vagy jelentkezve a Google-fiókodba a NotebookLM oldalon\!)*

#### **4\. lépés: A notebooklm-connector plugin letöltése**

* **Beszerzési forrás**: A LeeJuOh/claude-code-zero plugin-piactér GitHub repozitóriuma.  
* **Telepítés** (közvetlenül a futó Claude Code terminálon belül futtatandó slash parancsokkal): /plugin marketplace add LeeJuOh/claude-code-zero /plugin install notebooklm-connector@claude-code-zero  
* **Ellenőrzés**: Futtasd a /plugin parancsot a Claude Code-ban, és ellenőrizd az "Installed" fület.

### **C. Böngészőbővítmények manuális/félautomata exporthoz**

Amennyiben nem szeretnél helyi kódkörnyezetet és MCP szervert fenntartani, az alábbi böngészőbővítményekkel egyetlen kattintással kimentheted a NotebookLM válaszait Claude-kompatibilis Markdown fájlba.

#### **1\. Markdown Capturer \- BibCit (v2.5)**

Ez a kiterjesztés automatikusan átalakítja a NotebookLM számozott citációit szabványos akadémiai hivatkozásokká (APA, Harvard, IEEE stb.), és teljes bibliográfiát generál.

* **Beszerzési források**:  
  * **Chrome / Brave / Edge / Arc / Vivaldi**: https://chromewebstore.google.com/detail/markdown-capturer-bibcit/bbglkcgbhkhchpbbbcgpocnhplhdhnmc  
  * **Firefox**: https://addons.mozilla.org/en-GB/firefox/addon/markdown-capturer-bibcit/  
* **Telepítés**: Navigálj a fenti linkre, kattints az "Add to Chrome" / "Add to Firefox" gombra, majd rögzítsd (pin) az eszköztárra. Új válasz generálásakor a chat felületén megjelenő piros BibCit gombbal másolhatod ki a tökéletesen formázott Markdown/Word fájlt.

#### **2\. NotebookLM Export Pro**

Ez a bővítmény egy dedikált "Export" gombot helyez el a NotebookLM kezelőfelületén, amellyel a teljes chat-előzmény, a források metaadatai és a Studio jegyzetek menthetők el.

* **Beszerzési forrás**:  
  * **Chrome Web Store**: https://chromewebstore.google.com/detail/notebooklm-export-pro/fhplgheiijiledgfpabdiihe\[span\_46\](start\_span)\[span\_46\](end\_span)blmjoaog  
* **Telepítés és használat**: Telepítés után nyiss meg egy tetszőleges notebookot a NotebookLM-ben. Kattints a megjelenő "Export" gombra, és válaszd a "Markdown" vagy "Notion" integrációt a Claude-ba történő közvetlen beolvasáshoz.

## **8\. Következtetések és stratégiai ajánlások**

A Google NotebookLM és az Anthropic Claude integrációja jelentősen növeli a kutatási munkafolyamatok hatékonyságát, amennyiben a megfelelő architektúrát választják ki a technikai felkészültség és a kitűzött célok függvényében.

* **Nagy volumenű akadémiai és ipari kutatásokhoz** a helyi MCP szerverrel (notebooklm-mcp-cli) támogatott **Claude Cowork** architektúra javasolt, kiegészítve a kétoldalú meta-prompt rendszerrel. Ez a felépítés biztosítja a maximális sebességet, a kereszt-notebook kereséseket, valamint az egyedi Markdown-hierarchiák mentén történő teljesen automatizált, auditálható adatgyűjtést.  
* **Gyors, ad-hoc jellegű jegyzetelési feladatokhoz** – ahol a precíz, publikációkész hivatkozások megléte a legfontosabb szempont – a **Markdown Capturer \- BibCit** vagy a **NotebookLM Export Pro** kiterjesztések használata az optimális választás. Ezek minimális telepítési igénnyel működnek, és azonnal Claude-kompatibilis Markdown formátumba mentik a chat-előzményeket.  
* **Képek és táblázatok kezelésekor** szigorúan követni kell a kétlépcsős feltöltési szabályt (Markdown a szövegnek, külön képfájlok a vizuális elemeknek), a kontextuális horgonyzási promptokat, valamint a táblázat-orientált promptolási struktúrát, hogy a kapott adatok struktúrája és citációs leképezései hibátlanul épülhessenek be a Claude által generált végső jelentésekbe.

#### **Works cited**

- 1\. NotebookLM vs Claude (2026): Research Workflows Compared \- Atlas, https://www.atlasworkspace.ai/blog/notebooklm-vs-claude-projects 
- 2\. NotebookLM feels powerful until you try to do these 5 basic things \- XDA Developers, https://www.xda-developers.com/notebooklm-limitations/ 
- 3\. NotebookLM \+ Claude via MCP: Turning Two AI Giants Into One Research Machine | by Vinay Bhaskarla | Medium, https://medium.com/@vinayanand2/notebooklm-claude-via-mcp-turning-two-ai-giants-into-one-research-machine-8219dab9df86 
- 4\. Claude Cowork vs Kuse vs NotebookLM: A Deep Comparison for Real Workflows in 2026, https://www.kuse.ai/kuse-cowork/blog-post/claude-cowork-vs 
- 5\. Connect Claude Code to NotebookLM via MCP: 2026 Guide, https://pasqualepillitteri.it/en/news/1598/connect-claude-code-notebooklm-mcp-zero-tokens-2026 
- 6\. How to Export and Download Sources from NotebookLM, https://www.nlmtools.com/blog/notebooklm-export-sources 
- 7\. Export NotebookLM Responses as Formatted Word DOCX with Proper In-Text Citations & References in over 10000 Citation Styles \- Reddit, https://www.reddit.com/r/notebooklm/comments/1t7zrd3/export\_notebooklm\_responses\_as\_formatted\_word/ 
- 8\. Is Notebook able to understand images? : r/notebooklm \- Reddit, https://www.reddit.com/r/notebooklm/comments/1qb29pn/is\_notebook\_able\_to\_understand\_images/ 
- 9\. Markdown Capturer \- BibCit version history \- 4 versions – Add-ons for Firefox (en-GB), https://addons.mozilla.org/en-GB/firefox/addon/markdown-capturer-bibcit/versions/- 
- 10\. Export NotebookLM to Word DOCX with Proper In-Text Citations & References | BibCit Extension v2.5 \- YouTube, https://www.youtube.com/watch?v=mbchh6NvnEI 
- 11\. Use Mind Maps in NotebookLM \- Google Help, https://support.google.com/notebooklm/answer/16212283?hl=en 
- 12\. I use this Chrome extension to make NotebookLM's Mind Maps way more useful \- XDA Developers, https://www.xda-developers.com/notebooklm-mindmap-extractor-extension/ 
- 13\. How to export NotebookLM mind maps and edit them online (step ..., https://xmind.com/blog/export-notebooklm-mind-map 
- 14\. NotebookLM Mind Map Extractor – Free Online Tool \- Xmind, https://xmind.com/tools/notebooklm-mind-map-extractor 
- 15\. NotebookLM Mindmap Extractor \- Corrected Hierarchy \- Chrome Web Store, https://chromewebstore.google.com/detail/notebooklm-mindmap-extrac/ecikohbjgbjnlbldbjnceohmbhipipcp 
- 16\. Built a Claude Code plugin to query NotebookLM with automatic follow-ups on incomplete answers : r/ClaudeAI \- Reddit, https://www.reddit.com/r/ClaudeAI/comments/1r5znnl/built\_a\_claude\_code\_plugin\_to\_query\_notebooklm/ 
- 17\. Claude Cowork plugin for Google NotebookLM. 39 tools — notebooks, sources, AI queries, web research, studio artifacts, sharing, and batch operations. \- GitHub, https://github.com/gfsaaser24/notebooklm-cowork 
- 18\. NotebookLM Claude Integration | MCP Servers \- LobeHub, https://lobehub.com/mcp/ray-manaloto-notebooklm-claude-integration 
- 19\. Add or discover new sources for your notebook \- Computer \- NotebookLM Help, https://support.google.com/notebooklm/answer/16215270?hl=en\&co=GENIE.Platform%3DDesktop
- 20\. NotebookLM: A Guide With Practical Examples \- DataCamp, https://www.datacamp.com/tutorial/notebooklm 
- 21\. NotebookLM Data Tables: Transform Information Chaos \- Medium, https://medium.com/@kombib/notebooklm-data-tables-transform-information-chaos-e16f3ac1f518 
- 22\. NotebookLM: Convert Sources Into Data Tables | xFanatical, https://xfanatical.com/blog/what-is-notebooklm-how-to-convert-sources-into-data-tables/ 
- 23\. NotebookLM \+ Claude Code: built a plugin that connects them through Chrome automation, https://www.reddit.com/r/notebooklm/comments/1r605ja/notebooklm\_claude\_code\_built\_a\_plugin\_that/ 
- 24\. NotebookLM Export Pro \- Chrome Web Store \- Google, https://chromewebstore.google.com/detail/notebooklm-export-pro/fhplgheiijiledgfpabdiiheblmjoaog

---

# 9. Tesztelési státusz és nyitott kérdések

## 9.1. Teszteletlen eszközök

| Eszköz | Forrás | Státusz |
|--------|--------|---------|
| notebooklm-cowork plugin (39 tool) | github.com/gfsaaser24/notebooklm-cowork | ❔ teszteletlen |
| notebooklm-mcp (PleasePrompto) | github.com/PleasePrompto/notebooklm-mcp | ❔ teszteletlen |
| notebooklm-skill (PleasePrompto) | github.com/PleasePrompto/notebooklm-skill | ❔ teszteletlen |
| notebooklm-skill-claude-ai (mkll) | github.com/mkll/notebooklm-skill-claude-ai | ❔ teszteletlen |
| Apify NotebookLM API Actor | apify.com | ❔ teszteletlen |
| NLM Data Tables Studio prompt | minden tier | ✅ szabad tier-en is elérhető (2026 elején rolloutra); Studio → ceruza ikon; sablon: nlm_prompts.md C |

## 9.2. Nyitott módszertani kérdések
- MinerU + NLM kétlépcsős feltöltés: tesztelendő A4 szintű forráson.
- notebooklm-mcp cookie élettartama: 2-4 hét — megújítási folyamat tesztelendő.
- Cross-notebook lekérdezés (notebooklm-cowork): hasznos lehet többhetes tematikánál.

# 10. Linkgyűjtemény

## 10.1. GitHub repók (tesztelendő eszközök)
- https://github.com/PleasePrompto/notebooklm-mcp — MCP szerver
- https://github.com/PleasePrompto/notebooklm-skill — Cowork skill
- https://github.com/mkll/notebooklm-skill-claude-ai — alternatív skill
- https://github.com/gfsaaser24/notebooklm-cowork — 39-eszközös Cowork plugin
- https://mcpmarket.com/server/notebooklm-6 — MCP piactér bejegyzés

## 10.2. Cikkek, útmutatók
- https://aimaker.substack.com/p/notebooklm-mcp-claude-setup-guide-research-workflow — Setup guide
- https://aiblewmymind.substack.com/p/notebooklm-claude-code-use-cases — Claude Code use cases
- https://www.atlasworkspace.ai/blog/notebooklm-vs-claude-projects — összehasonlítás
- https://www.atlasworkspace.ai/blog/notebooklm-competitors — versenytársak
- https://medium.com/@vinayanand2/notebooklm-claude-via-mcp-turning-two-ai-giants-into-one-research-machine-8219dab9df86 — MCP integráció
- https://www.reddit.com/r/AISEOInsider/comments/1qbogok/the_secret_notebooklm_mcp_setup_that_turns_claude/ — Reddit thread
- https://www.xda-developers.com/notebooklm-connects-to-claude-through-mcp/ — XDA: MCP
- https://www.xda-developers.com/pairing-notebooklm-and-claude/ — XDA: párosítás
- https://www.xda-developers.com/my-best-ai-workflow-is-just-notebooklm-and-claude/ — XDA: workflow
- https://www.xda-developers.com/notebooklm-is-powerful-but-claude-better-at-handling-unorganized-notes/ — XDA: összehasonlítás

## 10.3. YouTube (referencia, nem fetchelt)
- https://www.youtube.com/watch?v=6t32nPxeJb8
- https://www.youtube.com/watch?v=PkOlfB3RY5Q
- https://www.youtube.com/watch?v=fV17ZkPBlAc
- https://www.youtube.com/watch?v=VtoD378U9Z0
- https://www.youtube.com/watch?v=Ml1TwnCkK4w
- https://www.youtube.com/watch?v=7sInxhTDA7U
- https://www.youtube.com/watch?v=gKc1Cgaocuw
- https://www.youtube.com/shorts/Lt0Zuyy2Ecw

# Változásjegyzék
- 2026-05-21 — YAML header és változásjegyzék hozzáadva; _claude/-ból .claude/-ba áthelyezve
