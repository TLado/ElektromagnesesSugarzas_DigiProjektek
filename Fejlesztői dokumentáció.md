➤ [README](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/README.md)

➤ [Felhasználói dokumentáció](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/Felhaszn%C3%A1l%C3%B3i%20dokument%C3%A1ci%C3%B3.md)

---
  
 **Számítógépre klónozás:**  `git clone https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek.git`

---

 ## Tartalomjegyzék
  A **fejlesztői dokumentáció** három részre oszlik: a szobatervező és hőtérkép-generáló modul, valamint továbbfejlesztés esetén .py fájlból futtatható EXE áálomány készítésére.

1. [Szobatervező modul](#szobatervezo-modul)
   - [1.1. Áttekintés](#szobatervezo-attekintes)
   - [1.2. Fájlok és erőforrások](#szobatervezo-fajlok)
   - [1.3. Fő architektúra](#szobatervezo-architektura)
   - [1.4. Form1](#form1)
   - [1.5. GridCell](#gridcell)
   - [1.6. DeviceInfo](#deviceinfo)
   - [1.7. Eszközlista betöltése](#eszkozlista-betoltese)
   - [1.8. Eszközlista szűrése](#eszkozlista-szurese)
   - [1.9. Szoba generálása](#szoba-generalasa)
   - [1.10. Grid kirajzolása](#grid-kirajzolasa)
   - [1.11. Szerkesztői eszközök](#szerkesztoi-eszkozok)
   - [1.12. Felhasználói interakció](#felhasznaloi-interakcio)
   - [1.13. CSV export](#csv-export)
   - [1.14. Export és mentés közötti különbség](#export-es-mentes)
   - [1.15. Hőtérkép-generáló EXE indítása](#heatmap-exe-inditasa)
   - [1.16. CSV import](#csv-import)
   - [1.17. Karbantartás](#karbantartas)

2. [Hőtérkép-generáló modul](#hoterkep-modul)
   - [2.1. Fájlok leírása](#hoterkep-fajlok)
   - [2.2. A szkript függvényeinek hívási hierarchiája](#hivasi-hierarchia)
     - [2.2.1. Fő belépési pont](#fo-belepesi-pont)
     - [2.2.2. Megjelenítő függvények](#megjelenito-fuggvenyek)
     - [2.2.3. Független Worker függvények](#worker-fuggvenyek)
     - [2.2.4. Archivált függvények](#archivalt-fuggvenyek)

3. [Futtatható EXE állomány készítése](#exe-keszitese)
   - [3.1. Kód módosítása](#kod-modositasa)
   - [3.2. Modul telepítése](#modul-telepitese)
   - [3.3. Belépés a projekt mappájába](#projekt-mappa)
   - [3.4. EXE készítése](#exe-build)
   - [3.5. Szükséges CSV fájlok](#szukseges-csv-fajlok)
   - [3.6. Gyakori hibák](#gyakori-hibak)
     - [3.6.1. pyinstaller is not recognized](#pyinstaller-not-recognized)
     - [3.6.2. Hiányzó skimage modul](#hianyzo-skimage-modul)

<a id="szobatervezo-modul"></a>
# 1. SZOBATERVEZŐ MODUL
<a id="szobatervezo-attekintes"></a>
## 1.1. Áttekintés

Ez a fejezet a C# alapú Windows Forms szobatervező modul működését és felépítését mutatja be. A **hőtérkép-generáló modul** külön komponensként működik, ezért annak részletes leírása a dokumentáció második részében található.

A szobatervező modul célja, hogy a felhasználó egy grafikus felületen létrehozhasson egy rácsalapú szobaelrendezést, majd abban elektromágneses sugárzást kibocsátó eszközöket helyezhessen el. Az elkészült elrendezést a program CSV formátumban menti, amelyet a hőtérkép-generáló modul bemenetként használ.

A Forms alkalmazás fő feladatai (részletesebben a [felhasználói dokumentációban](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/Felhaszn%C3%A1l%C3%B3i%20dokument%C3%A1ci%C3%B3.md)):

- szoba méretének és rácsméretének megadása,
- szoba automatikus legenerálása külső falakkal,
- eszközök elhelyezése cellákban,
- korábban mentett szobaelrendezések importálása,
- szobaelrendezés exportálása CSV fájlba,
- a hőtérkép-generáló `heatmap.exe` elindítása.

---
<a id="szobatervezo-fajlok"></a>
## 1.2. Fájlok és erőforrások

A Forms alkalmazás a futási könyvtárban található `Resources` mappából dolgozik. Fejlesztői környezetben és telepített alkalmazásként is ugyanaz a logika használható.

A `Resources` mappában található fő fájlok:

- `cleaned_magnetic_data.csv`  
  Az eszközök adatbázisa. A Forms alkalmazás ebből tölti be az eszközlistát.

- `heatmap.exe`  
  A Python scriptből készült futtatható állomány. A szobaterv mentése után ezt indítja el a Forms alkalmazás.

- `room_layout.csv`  
  A Forms alkalmazás által generált fájl. Ez tartalmazza az aktuális szobaelrendezést.

---
<a id="szobatervezo-architektura"></a>
## 1.3. Fő architektúra

A szobatervező modul egyszerű, eseményvezérelt Windows Forms architektúrát használ.

A fő komponensek:

- `Form1`
- `GridCell`
- `DeviceInfo`

A program központi része a `Form1` osztály, amely kezeli a felület eseményeit, a grid állapotát, az eszközök betöltését, az import/export funkciókat és a külső `heatmap.exe` indítását.

A szoba belső állapotát egy kétdimenziós tömb tárolja:
`private GridCell[,] grid;`
Ez a mátrix reprezentálja a teljes szobaelrendezést. 

<a id="form1"></a>
## 1.4. Form1

A `Form1` a szobatervező alkalmazás fő vezérlőosztálya. Ez tartalmazza a felhasználói felülethez kapcsolódó eseménykezelőket, a grid létrehozását, a cellák rajzolását, az eszközlista kezelését, valamint a CSV import/export logikát.

Fontosabb felelősségei:

-   a felület inicializálása,
-   eszközlista betöltése CSV-ből,
-   eszközlista szűrése keresőmező alapján,
-   szobagrid létrehozása,
-   cellák kirajzolása,
-   kattintások kezelése,
-   CSV export és import,
-   `heatmap.exe` indítása.

A `Form1` tartalmazza az alkalmazás legtöbb működési logikáját, ezért továbbfejlesztés esetén ez az elsődleges kiindulási pont.

<a id="gridcell"></a>
## 1.5. GridCell

A `GridCell` osztály egyetlen rácscellát reprezentál.

Fő tulajdonságai:

```
public bool IsWall { get; set; }public List<string> Items { get; set; }
```

Az `IsWall` azt tárolja, hogy az adott cella fal-e.  
Az `Items` lista tartalmazza az adott cellában elhelyezett eszközök azonosítóit.

Egy cellában több eszköz is lehet, ezért az `Items` lista típusú. Ez lehetővé teszi például, hogy ugyanazon a pozíción több elektromos eszköz is szerepeljen.

Fal cellára nem lehet eszközt elhelyezni.

<a id="deviceinfo"></a>
## 1.6 .DeviceInfo

A `DeviceInfo` osztály egy eszköz alapadatait tárolja, amelyeket a program a `cleaned_magnetic_data.csv` fájlból olvas be.

Fő mezői:

```
public string EszkozNeve { get; set; }public string Id { get; set; }
```

Az `EszkozNeve` jelenik meg a felhasználói felületen az eszközlistában.  
Az `Id` kerül eltárolásra a grid celláiban és a kiexportált `room_layout.csv` fájlban.

----------

<a id="eszkozlista-betoltese"></a>
## 1.7. Eszközlista betöltése

Az eszközlista betöltése a `LoadDevicesFromCsv()` metódusban történik.

A program a következő fájlból dolgozik:

```
Resources/cleaned_magnetic_data.csv
```

A CSV elvárt oszlopai:

```
eszkoz_neve,magneses_sugarzas_mikrotesla,meresi_tavolsag_meterben,id
```

A Forms alkalmazás ebből jelenleg az első és a negyedik oszlopot használja:

-   `eszkoz_neve` → megjelenített név,
-   `id` → belső azonosító.

A betöltött eszközök a `devices` listába kerülnek, majd ebből készül a szűrt lista (`filteredDevices`), amely az `lstTools` vezérlő adatforrása.

----------

<a id="eszkozlista-szurese"></a>
## 1.8. Eszközlista szűrése

Az eszközök keresése a `tbFilter_TextChanged()` eseménykezelőben történik.

A keresés az alábbi mezőkben történik:

-   eszköz neve,
-   eszköz azonosítója.

A keresés nem kis- és nagybetű érzékeny. Minden szövegbevitel után a program újraszűri az eszközlistát, majd újraköti az `lstTools` vezérlőhöz.

Ez lehetővé teszi, hogy nagyobb eszközadatbázis esetén is gyorsan megtalálható legyen a keresett elem.

----------

<a id="szoba-generalasa"></a>
## 1.9. Szoba generálása

A szoba létrehozása a `btnGenerate_Click()` eseményből indul, a tényleges grid létrehozását pedig a `CreateRoom()` metódus végzi.

A felhasználó megadja:

-   a szoba szélességét méterben,
-   a szoba magasságát méterben,
-   a rácsméretet.

Támogatott rácsméretek:

-   `0.25 m`
-   `0.5 m`
-   `1 m`

A program a megadott fizikai méretekből kiszámolja a szükséges cellaszámot.

Például:

```
Szoba szélessége: 10 mRácsméret: 0.5 mBelső cellaszám: 20
```

A grid köré a program automatikusan falat generál, ezért a teljes cellaszám mindig nagyobb kettővel a belső cellaszámnál.


### Maximális szobaméret

Teljesítményoptimalizálás miatt a program rácsmérettől függő maximális szobaméretet használ.

Jelenlegi limitek:
| Rácsméret | Maximális szélesség | Maximális magasság |
|--|--|--|
| 0.25 m | 8 m | 6 m |
| 0.5 m | 16 m | 12 m |
| 1 m | 34 m | 26 m |


Ha a felhasználó ennél nagyobb méretet ad meg, a program automatikusan visszaállítja az értéket a megengedett maximumra.

----------

<a id="grid-kirajzolasa"></a>
## 1.10. Grid kirajzolása

A grid megjelenítését a `canvasPanel_Paint()` eseménykezelő végzi.

A kirajzolás cellánként történik. A cellák színe az állapotuktól függ:

-   fal cella → sötétszürke,
-   eszközt tartalmazó cella → világoskék,
-   üres cella → fehér / világosszürke sakktábla mintázat.

A sakktábla mintázat segíti a térbeli tájékozódást. A mintázat a falon belüli területen indul, és méteralapú blokkok szerint számolódik.

A cellákba szöveges jelölés is kerül. A fal jelölése:

```
W
```

Az eszközök esetében a program az eszköz nevéből képez rövidítést. Ez a megjelenítés csak vizuális segítség, az exportált fájlban az eszköz ID-ja szerepel.

----------
<a id="szerkesztoi-eszkozok"></a>
## 1.11. Szerkesztői eszközök

A normál eszközlista mellett külön szerkesztői eszközlista is található.

Jelenlegi speciális eszközök:

-   `Fal`
-   `Radír`

----------
<a id="felhasznaloi-interakcio"></a>
## 1.12. Felhasználói interakció

A cellák szerkesztését a `canvasPanel_MouseClick()` eseménykezeli.

A kattintás működése az aktuálisan kiválasztott eszköztől függ.

Normál eszköz esetén:

-   ha az eszköz még nincs a cellában, bekerül,
-   ha már szerepel a cellában, eltávolításra kerül.

Fal esetén:

-   a cella fal státusza kapcsolható,
-   csak akkor állítható fallá, ha nincs benne eszköz.

Radír esetén:

-   a cella tartalma törlődik,
-   a fal státusz is törlődik.

A program nem engedi, hogy fal cellára eszköz kerüljön.

----------
<a id="csv-export"></a>
## 1.13. CSV export

A CSV exportot a `SaveCsvToPath()` metódus végzi.

A kimeneti fájl neve tipikusan:

```
room_layout.csv
```

Az exportált formátum:

```
x;y;x_m;y_m;cell_size_m;is_wall;device_id
```

Az oszlopok jelentése:
|Oszlop| Jelentés |
|--|--|
| `x` | cella X koordinátája a gridben |
| `y` | cella Y koordinátája a gridben |
| `x_m` | cella X koordinátája méterben |
| `y_m` | cella Y koordinátája méterben |
| `cell_size_m` | aktuális rácsméret méterben |
| `is_wall` | `1`, ha fal; különben `0` |
| `device_id` | eszköz azonosítója vagy `wall` |




Normál eszköz esetén a `device_id` a `cleaned_magnetic_data.csv` fájlban szereplő eszközazonosító.

A program nem számolja át az exportot másik rácsméretre, hanem mindig az aktuálisan kiválasztott rácsméretet használja. Ez azért fontos, mert a diagramkészítő komponens is ebből az értékből dolgozik.

----------
<a id="export-es-mentes"></a>
## 1.14. Export és mentés közötti különbség

A program kétféle mentési logikát használ.

A `btnExport_Click()` egy felhasználó által kiválasztott helyre menti a CSV fájlt. Ez főként kézi exportálásra vagy ellenőrzésre használható.

A `btnSave_Click()` a `Resources` mappába menti a `room_layout.csv` fájlt, majd elindítja a `heatmap.exe` programot.

Ez a működés azért fontos, mert a `heatmap.exe` ugyanebből a mappából olvassa be a szükséges fájlokat.

----------
<a id="heatmap-exe-inditasa"></a>
## 1.15. Hőtérkép-generáló EXE indítása

A `btnSave_Click()` mentés után elindítja a `Resources` mappában található futtatható állományt:

```
Resources/heatmap.exe
```

Az indítás `ProcessStartInfo` segítségével történik.

Ez biztosítja, hogy a `heatmap.exe` a saját mappájában keresse a bemeneti fájlokat, például:

-   `room_layout.csv`
-   `cleaned_magnetic_data.csv`

----------
<a id="csv-import"></a>
## 1.16. CSV import

A program képes korábban exportált szobaelrendezések visszatöltésére is.

Az importálás a `btnImport_Click()` eseményből indul, a tényleges feldolgozást az `ImportFromCsv()` metódus végzi.

Az importálás lépései:

1.  a felhasználó kiválaszt egy CSV fájlt,
2.  a program ellenőrzi a fejlécet,
3.  beolvassa a cellaadatokat,
4.  meghatározza a rácsméretet,
5.  újragenerálja a gridet,
6.  visszaállítja a falakat és az eszközöket.

Az importált fájlnak az alábbi fejlécet kell tartalmaznia:

```
x;y;x_m;y_m;cell_size_m;is_wall;device_id
```

Ha a formátum hibás, a program hibaüzenetet jelenít meg, és nem tölti be a fájlt.

----------
<a id="karbantartas"></a>
## 1.17. Karbantartás

A szobatervező modul karbantartása elsősorban három területen történhet.

Az eszközlista módosítása a `cleaned_magnetic_data.csv` fájlban végezhető el. Új eszköz hozzáadásához elegendő új sort felvenni a CSV-be, megfelelő ID-val.

A grid működését érintő módosítások főként az alábbi metódusokat érintik:

-   `CreateRoom()`
-   `canvasPanel_Paint()`
-   `canvasPanel_MouseClick()`

Az export/import formátum módosítása esetén az alábbi metódusokat kell együtt kezelni:

-   `SaveCsvToPath()`
-   `ImportFromCsv()`

Fontos, hogy ha a CSV struktúrája változik, akkor a diagramkészítő komponens beolvasási logikáját is hozzá kell igazítani.

----------
<a id="hoterkep-modul"></a>
# 2. HŐTÉRKÉP-GENERÁLÓ MODUL

Megjegyzés: A hőtérkép generáló modulból futtatható EXE állomány készült, felhasználói szinten nem szükséges a függőségek telepítése. Amennyiben új EXE fájlt szeretnénk készíteni, az erre vonatkozó információk a **3. fejezetben** találhatóak.

*  **Függőségek letöltése:**  `pip install -r requirements.txt`

*  **Diagramok kiírása** (tesztelésre, mert ugye alapvetően a C# applikáción keresztül tudjuk elindítani): `python main.py`


<a id="hoterkep-fajlok"></a>
## 2.1. Fájlok leírása:

*  **`cleaned_magnetic_data.csv`**: Itt vannak az eszközök adatai. Oszlopok: `eszkoz_neve`, `magneses_sugarzas_mikrotesla`, `meresi_tavolsag_meterben`, `id`

*  **`main.py`**: Ezzel a python kóddal dolgozzuk fel és írjuk ki a `room_layout.csv` által létrehozott szobának a sugárzástérképét.

*  **`requirements.txt`**: Függőségek a `main.py`-hoz.

*  **`room_layout.csv`**: Ebben vannak a C# program által létrehozott szoba adatai.

  
<a id="hivasi-hierarchia"></a>
## 2.2. A szkript függvényeinek hívási hierarchiája és kapcsolati hálója a következőképpen épül fel:

  
<a id="fo-belepesi-pont"></a>
### 2.2.1. Fő belépési pont:

*  **`display_heatmaps()`**: A program indulásakor hívódik meg. Elindítja a két fő vizualizációs folyamatot:

1. Meghívja a `show_regular_heatmap()` függvényt.

2. Meghívja a `show_limit_heatmap()` függvényt.

  
<a id="megjelenito-fuggvenyek"></a>
### 2.2.2. Megjelenítő függvények (A vezérlők):

Mindkét függvény felépítése azonos: lekérik az adatokat, elvégeztetik a számítást, majd kirajzolják a grafikont.

*  **`show_regular_heatmap()`** és **`show_limit_heatmap()`**:

*  **Meghívja:**  `import_csv_efficient()` -> Visszakapja a szoba és az eszközök adatait (falak, koordináták).

*  **Meghívja:**  `calculate_combined_heatmap(...)` -> Átadja a beolvasott adatokat, és visszakapja a kiszámolt mágneses térerősség-mátrixot (Z).

*  **Referál (Callback):** A `show_regular_heatmap` a `format_coord` függvényt köti be a Matplotlib felületéhez a kurzor adatainak kiírásához.

*  **Belső (Nested) függvény:** Mindkettő definiál egy helyi `hover(event)` függvényt, amely az egeres interakciókat (eszköznevek felugró ablakai) kezeli.

  
<a id="worker-fuggvenyek"></a>
### 2.2.3. Független "Worker" (munkavégző) függvények:

Ezek a függvények végzik a tényleges munkát, de ők maguk nem hívnak meg más saját függvényt a szkriptből.

*  **`import_csv_efficient()`**: Önmagában lekezeli a `room_layout.csv` beolvasását és az adatszerkezetek (listák) felépítését.

*  **`calculate_combined_heatmap()`**: Átveszi az adatokat, és külső könyvtárak (`numpy`, `skimage.draw.line`) segítségével legenerálja a hőtérkép értékeit.

*  **`format_coord(x, y, Z)`**: Szimpla formázó függvény, a Matplotlib hívja meg automatikusan, amikor az egeret mozgatjuk a grafikonon.

  
<a id="archivalt-fuggvenyek"></a>
### 2.2.4. Archivált (jelenleg nem hívott) függvények:

*  **`import_csv()`**: A beolvasás régebbi, elavult verziója. Nincs meghívva sehol.

*  **`calculate_combined_heatmap_old()`**: A fizikai számítás régebbi (sugárkövetés és fal-árnyékolás nélküli) verziója. Szintén nincs meghívva az aktív kódban.

<a id="exe-keszitese"></a>
# 3. FUTTATHATÓ EXE ÁLLOMÁNY KÉSZÍTÉSE
 A `main.py` fájlban taláható kód egyes esetekben eltér a futtatható EXE által hasznát kódtól. Amennyiben továbbfejlesztést követően futtatható EXE-t szeretnénk készíteni a következő lépéseket szükséges megtenni:
 
 <a id="kod-modositasa"></a>
## 3.1. Kód módosítása
  Kód elejére beillesztendő:
  ```
  import  os  
import  sys  
  
def  app_path(filename):  
	if  getattr(sys, 'frozen', False):  
		base_path  =  os.path.dirname(sys.executable)  
	else:  
		base_path  =  os.path.dirname(os.path.abspath(__file__))  
  
return  os.path.join(base_path, filename)
```

Csere:
Ez:```
df = pd.read_csv('cleaned_magnetic_data.csv')```
Erre:```
df = pd.read_csv(app_path('cleaned_magnetic_data.csv'))```

Ez:```
room_layout_efficient = pd.read_csv("room_layout.csv", sep=";")```
Erre:```
room_layout_efficient = pd.read_csv(app_path("room_layout.csv"), sep=";")```

<a id="modul-telepitese"></a>
## 3.2. Modul telepítése
 Az EXE állománnyá alakításhoz a következő modulra van szükség: **pyinstaller**
 A terminálban a következő parancs segítségével telepíthető:
```
 pip install numpy pandas matplotlib scikit-image pyinstaller
```
Belépés a projekt mappájába
## 3.3. Belépés a projekt mappájába
 A parancssorban abba a mappába kell navigálni, ahol a `main.py` fájl található:
```
cd "C:\...\projekt_mappa"
```

A mappában szerepeljen az ikonfájl is:
```
favicon.ico
```
<a id="exe-build"></a>
## 3.4. EXE készítése
A buildelés után a kész fájl a következő mappában található:
```
dist\main.exe
```
<a id="szukseges-csv-fajlok"></a>
## 3.5. Szükséges CSV fájlok

A program külső CSV fájlokat használ, ezért ezeknek az EXE mellett kell lenniük:

```
main.exe
cleaned_magnetic_data.csv
room_layout.csv
```
Ezeket nem érdemes beépíteni az EXE-be, mert a program mindig az aktuális, felülírt CSV fájlokat olvassa be.

<a id="gyakori-hibak"></a>
## 3.6. Gyakori hibák
<a id="pyinstaller-not-recognized"></a>
### 3.6.1. `pyinstaller is not recognized`

Ha a következő hiba jelenik meg:

```
'pyinstaller' is not recognized as an internal or external command
```

akkor a PyInstaller parancs nincs a PATH változóban. Ilyenkor a biztonságosabb megoldás a következő forma használata:

```
python -m PyInstaller ...
```

Ezért a dokumentációban is ezt a formát használjuk.

<a id="hianyzo-skimage-modul"></a>
### 3.6.2. Hiányzó `skimage` modul

Ha indításkor ehhez hasonló hiba jelenik meg:

```
No module named 'skimage._shared.geometry'
```

akkor a PyInstaller nem csomagolta be automatikusan a `scikit-image` egyik belső modulját. Ezt a következő kapcsoló oldja meg:

```
--collect-all skimage
```
