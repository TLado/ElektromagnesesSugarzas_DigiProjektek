# Room Layout EM Load – Room Layout editor
## C# alkalmazás dokumentáció

## Áttekintés

Ez a dokumentáció a C# alapú Windows Forms alkalmazás működésére és felépítésére fókuszál. A Python komponens csak annyiban kerül említésre, amennyiben az alkalmazás működéséhez szükséges.

Az alkalmazás célja egy irodai környezet vizuális modellezése rácsalapú (grid) megközelítéssel. A felhasználó egy grafikus felületen helyezheti el az elektromágneses sugárzást kibocsátó eszközöket, majd az így létrehozott elrendezést egy strukturált CSV fájlba mentheti.

Ez a CSV fájl később más rendszerek (pl. Python alapú számítási modul) számára szolgál bemenetként.

---

## Alkalmazás működése

<em>Megjegyzés: ez egy rövid összefoglaló, a használathoz olvassa el a **felhasználói dokumentációt**.</em>

A felhasználó először megadja a szoba méretét méterben, valamint kiválasztja a grid felbontását. Ez alapján a rendszer egy diszkrét rácsot generál, amelyben minden cella egy meghatározott fizikai területet reprezentál.

A grid létrehozásakor a rendszer automatikusan falakat helyez el a szoba határain, így biztosítva, hogy a felhasználó csak a belső területen dolgozhasson.

A felhasználó ezután különböző eszközöket helyezhet el a grid celláiban. Egy cella több eszközt is tartalmazhat, ami lehetővé teszi sűrűbb elrendezések modellezését.

A mentés során az aktuális állapot CSV formátumba kerül exportálásra. A mentési folyamat után az alkalmazás képes elindítani egy külső Python scriptet, amely a további feldolgozást végzi.

---

## Architektúra és fő komponensek

Az alkalmazás egyszerű, de jól elkülönített komponensekből épül fel.

A központi elem a **Form1 osztály**, amely a teljes alkalmazás vezérléséért felel. Ez tartalmazza a felhasználói felület eseménykezelőit, a grid kezelését, az eszközök elhelyezésének logikáját, valamint az export és külső folyamat indítás funkciókat.

A grid belső reprezentációját egy kétdimenziós tömb biztosítja (`GridCell[,]`). Ez egy mátrix, ahol minden elem egy cellát reprezentál.

A **GridCell osztály** feladata egyetlen cella állapotának tárolása. Egy cella két fontos információt tartalmaz:
- fal-e (`IsWall`)
- milyen eszközök találhatók benne (`Items` lista)

Az eszközök adatait a **DeviceInfo osztály** reprezentálja, amely a külső CSV fájlból kerül feltöltésre. Ez lehetővé teszi, hogy az eszközlista dinamikusan változtatható legyen.

---

## Grid működése

A grid a program egyik legfontosabb eleme, mivel ez biztosítja a tér reprezentációját.

A grid létrehozása a `CreateRoom()` metódusban történik. A felhasználó által megadott méretek alapján a rendszer kiszámolja, hogy hány cellára van szükség, majd létrehoz egy kétdimenziós tömböt.

A grid szélein automatikusan fal cellák jönnek létre. Ez azt jelenti, hogy a felhasználó nem tud a szoba határain kívül eszközöket elhelyezni.

Fontos tulajdonság, hogy egy cellában több eszköz is elhelyezhető. Ez egy lista segítségével van megvalósítva, így nincs korlátozva az eszközök száma cellánként.

---

## Rajzolás és vizualizáció

A grid megjelenítése a `canvasPanel_Paint` eseménykezelőben történik.

Minden cella külön kerül kirajzolásra, a következő logika szerint:
- fal cellák → sötétszürke szín
- eszközt tartalmazó cellák → kiemelt szín
- üres cellák → sakktábla mintázat

A cellákba szöveges jelölés is kerül, amely az eszköz típusát rövidített formában jeleníti meg.

---

## Felhasználói interakció

Az interakció alapja az egérkattintás, amelyet a `canvasPanel_MouseClick` kezel.

A kattintás hatása attól függ, hogy milyen eszköz van kiválasztva:
- normál eszköz → hozzáadás vagy eltávolítás
- fal → cella fal státuszának váltása
- radír → cella teljes törlése

A rendszer megakadályozza, hogy falra eszközt lehessen elhelyezni.

---

## Adatkezelés és CSV export

A mentés során a grid teljes állapota exportálásra kerül egy CSV fájlba.

Ezt a `SaveCsvToPath()` metódus végzi. A metódus végigiterál az összes cellán, és minden releváns információt kiír.

A CSV formátum célja, hogy egyértelműen és egyszerűen feldolgozható legyen más rendszerek számára.

A fájl tartalmazza:
- rácskoordináták
- valós pozíciók méterben
- cellaméret
- fal információ
- eszköz azonosítók

A személyek külön azonosítóval kerülnek mentésre (pl. `p001`), hogy egyedileg kezelhetők legyenek.

---

## Külső Python script indítása

A mentési folyamat után az alkalmazás képes automatikusan elindítani egy Python scriptet.

Ez a `RunPythonScript()` metódusban történik, amely egy új folyamatot indít a `ProcessStartInfo` segítségével.

Fontos, hogy a script a megfelelő munkakönyvtárból induljon, mivel a bemeneti fájlokat relatív elérési úttal olvassa be.

---

## Karbantartás

Az alkalmazás felépítése lehetővé teszi a célzott és gyors módosításokat.

Az eszközlista teljes mértékben adatvezérelt, így új eszközök hozzáadása a CSV fájl módosításával történik.

A grid működésével kapcsolatos módosítások jól elkülönülnek a `CreateRoom`, rajzolási és kattintáskezelő metódusokban.

A Python integráció külön metódusban található, így annak módosítása nem érinti a többi részt.

---

## Bővíthetőség és továbbfejlesztés

A program átadása után több irányban is könnyen továbbfejleszthető.

Új eszközök hozzáadásához elegendő a megfelelő CSV fájlt bővíteni, nincs szükség a C# kód módosítására.

A grid működése bővíthető például új cellatípusokkal vagy komplexebb interakciókkal. A felhasználói felület fejleszthető további kényelmi funkciókkal, mint például drag & drop vagy zoom.

Az adatkezelés bővíthető Excel támogatással is. A jelenlegi CSV alap könnyen kiterjeszthető `.xlsx` fájlok kezelésére, ami lehetővé teszi az adatok kényelmesebb szerkesztését és megosztását. Ez különösen hasznos lehet olyan felhasználók számára, akik nem technikai háttérrel rendelkeznek.

A kód szerkezete lehetővé teszi, hogy a projektet átvevő fejlesztők gyorsan átlássák a működést, és célzottan bővítsék a szükséges részeket.