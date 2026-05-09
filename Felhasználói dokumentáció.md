➤ [README](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/README.md)

➤ Felhasználói dokumentáció

➤ [Fejlesztői dokumentáció](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/Fejleszt%C5%91i%20dokument%C3%A1ci%C3%B3.md)

----

# Tartalomjegyzék

- [1. Telepítés és eltávolítás](#1-telepítés-és-eltávolítás)
  - [1.1. Telepítési lépések](#11-telepítési-lépések)
    - [1.1.1. Fontos telepítési megjegyzés](#111-fontos-telepítési-megjegyzés)
  - [1.2. Eltávolítás](#12-eltávolítás)
- [2. A program indítása](#2-a-program-indítása)
- [3. Felhasználói felület áttekintése](#3-felhasználói-felület-áttekintése)
  - [3.1. Magasság és szélesség beállítása](#31-magasság-és-szélesség-beállítása)
  - [3.2. Rácsfelbontás kiválasztása](#32-rácsfelbontás-kiválasztása)
  - [3.3. Szoba generálása](#33-szoba-generálása)
  - [3.4. Korábban mentett layout betöltése](#34-korábban-mentett-layout-betöltése)
  - [3.5. Fal és radír](#35-fal-és-radír)
  - [3.6. Eszközlista szűrése](#36-eszközlista-szűrése)
  - [3.7. Elhelyezhető eszközök listája](#37-elhelyezhető-eszközök-listája)
  - [3.8. Rajzterület](#38-rajzterület)
  - [3.9. Layout helyi mentése és vizualizáció megnyitása](#39-layout-helyi-mentése-és-vizualizáció-megnyitása)
  - [3.10. Layout exportálása saját helyre](#310-layout-exportálása-saját-helyre)
- [4. Gyakori hibák](#4-gyakori-hibák)
  - [4.1. A hőtérkép nem indul el](#41-a-hőtérkép-nem-indul-el)
  - [4.2. Az eszközlista üres](#42-az-eszközlista-üres)
  - [4.3. A mentés nem működik](#43-a-mentés-nem-működik)
  - [4.4. Javasolt megoldás](#44-javasolt-megoldás)
  
<a id="1-telepítés-és-eltávolítás"></a>
# 1. Telepítés és eltávolítás

A program telepítője a GitHub repositoryban, az alábbi útvonalon található:
    [ElektromagnesesSugarzas_DigiProjektek/Room_layout_EM_load/EMLPredictorSetup/Release/EMLPredictorSetup.msi](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/Room_layout_EM_load/EMLPredictorSetup/Release/EMLPredictorSetup.msi)
   
   A telepítő varázsló a jobb felső sarokban a lefele mutató nyíl ⤓ ikonra tölthető le.

<a id="11-telepítési-lépések"></a>
## 1.1. Telepítési lépések

1.  Töltse le az `.msi` telepítőt.
2.  Indítsa el a telepítési varázslót.
3.  Kövesse a telepítő lépéseit.

<a id="111-fontos-telepítési-megjegyzés"></a>
### 1.1.1. Fontos telepítési megjegyzés

A program működéséhez írási jogosultság szükséges, ezért:
 ❌ **NE** ide telepítse:
```
C:\Program Files (x86)\
```
vagy
```
C:\Program Files\
```

Mivel ezekben a mappákban a Windows korlátozhatja a fájlírást.

✔ Javasolt telepítési helyek:
Meghajtó gyökere:
```
D:\RoomLayout\
```
```
C:\RoomLayout\
```
Új mappa létrehozásával:
```
D:\RoomLayout\EMLPredictor\
```
```
C:\RoomLayout\EMLPredictor\
```

A telepítési varázslóban a telepítési mappa szabadon módosítható.


![Telepítő varázsló](https://i.imgur.com/UYgymPP.png)

<a id="12-eltávolítás"></a>
## 1.2. Eltávolítás
A telepítő varázsló újrafuttatásával távolítható el a program.

----------

<a id="2-a-program-indítása"></a>
# 2. A program indítása

A telepítés után az alkalmazás az asztali ikonról:
<p>
  <img src="https://i.imgur.com/lV9cnTS.png" width="100">
</p>

Vagy a telepítési mappából indítható:
```C:\EMLPredictor\Room_layout_EM_load.exe```

Indítás után a program automatikusan betölti az eszközadatbázist a `Resources` mappából.

<a id="3-felhasználói-felület-áttekintése"></a>
# 3. Felhasználói felület áttekintése

A felület fő részei:
![Kezelőfelület](https://i.imgur.com/imKzKQH.png)

|Sorszám| Funkció |
|--|--|
| 1. | Szoba szélességének és magasságának megadása |
| 2. | Rácsfelbontás kiválasztása (méterben) |
| 3. | Szoba generálása |
| 4. | Korábban mentett layout betöltése |
| 5. | Fal és radír |
| 6. | Eszközlista szűrése |
| 7. | Elhelyezhető eszközök listája |
| 8. | Rajzterület |
| 9. | Layout helyi mentése, vizualizáció megnyitása |
| 10. | Layout exportálása, mentése saját helyre |

<a id="31-magasság-és-szélesség-beállítása"></a>
## 3.1. Magasság és szélesség beállítása

A kezelőfelület bal felső részén található mezők segítségével adható meg a szoba szélessége és magassága méterben.

A program a megadott értékek alapján számolja ki a szükséges rácsméretet és a létrehozandó cellák számát. A méretek a kiválasztott grid felbontással együtt határozzák meg a generált szoba részletességét.

A túl nagy méreteket a rendszer automatikusan a támogatott maximális értékre csökkenti.

---
<a id="32-rácsfelbontás-kiválasztása"></a>
## 3.2. Rácsfelbontás kiválasztása

A rácsfelbontás meghatározza, hogy egy cella mekkora valós területet reprezentál.

Jelenleg támogatott értékek:

- `0.25 m`
- `0.5 m`
- `1 m`

A kisebb rácsméret részletesebb szerkesztést tesz lehetővé, azonban jelentősen növeli a létrejövő cellák számát és a rendszer terhelését.

A kiválasztott rácsméret a CSV exportban is eltárolásra kerül.

---
<a id="33-szoba-generálása"></a>
## 3.3. Szoba generálása

A `Szoba generálása` gomb hozza létre a szerkeszthető gridet.

A generálás során a program:

- létrehozza a megfelelő méretű rácsot
- automatikusan elhelyezi a külső falakat
- előkészíti a szerkesztőfelületet

A korábbi grid minden generáláskor felülírásra kerül, amennyiben ezt szeretnénk használni a későbbiekben, a csv export gomb segítségével (1.4.10.) elmenthető.

---
<a id="34-korábban-mentett-layout-betöltése"></a>
## 3.4. Korábban mentett layout betöltése

Az `Import` gomb segítségével korábban exportált vagy mentett CSV fájl tölthető vissza.

A program ellenőrzi a fájl formátumát, és hibás szerkezet esetén figyelmeztetést jelenít meg.

---
<a id="35-fal-és-radír"></a>
## 3.5. Fal és radír

A speciális szerkesztői eszközök külön listában találhatók.

### Fal

A `Fal` eszközzel a kiválasztott cella fal státusza kapcsolható.

A fal cellák:

- nem tartalmazhatnak eszközt
- a vizualizáció során akadályként működnek

### Radír

A `Radír` a kiválasztott cella teljes tartalmát törli, beleértve:

- az eszközöket
- a fal státuszt

---

<a id="36-eszközlista-szűrése"></a>
## 3.6. Eszközlista szűrése

A keresőmező segítségével az eszközlista gyorsan szűrhető.

---
<a id="37-elhelyezhető-eszközök-listája"></a>
## 3.7. Elhelyezhető eszközök listája

Az eszközlista tartalmazza az összes elhelyezhető elektromos eszközt.

Az adatok a `cleaned_magnetic_data.csv` fájlból töltődnek be, ezért az eszközlista adatvezérelt módon működik.

Az eszköz kiválasztása után a felhasználó a rajzterületen kattintással helyezheti el azt.

Egy cella több eszközt is tartalmazhat.

---
<a id="38-rajzterület"></a>
## 3.8. Rajzterület

A rajzterület jeleníti meg a generált szobát és annak celláit.

A grid sakktáblaszerű mintázatot használ a jobb olvashatóság érdekében. A különböző cellatípusok eltérő színnel jelennek meg:

- fal → sötétszürke
- eszközt tartalmazó cella → világoskék
- üres cella → fehér / világosszürke

A szerkesztés egérkattintással történik.

---
<a id="39-layout-helyi-mentése-és-vizualizáció-megnyitása"></a>
## 3.9. Layout helyi mentése és vizualizáció megnyitása

A `Mentés és vizualizálás` gomb a layoutot automatikusan a program `Resources` mappájába menti `room_layout.csv` néven.

A mentés után a rendszer automatikusan elindítja a `heatmap.exe` alkalmazást, amely elkészíti és megjeleníti a mágneses tér vizualizációját.

Ez a funkció a teljes szimulációs folyamat gyors elindítására szolgál.

---
<a id="310-layout-exportálása-saját-helyre"></a>
## 3.10. Layout exportálása saját helyre

Az `Export` gomb segítségével a felhasználó tetszőleges helyre mentheti a layoutot CSV formátumban.

Ez a funkció elsősorban:

- archiválásra
- megosztásra
- későbbi importálásra
- külső feldolgozásra

használható.

Az exportált fájl kompatibilis az alkalmazás import funkciójával.

<a id="4-gyakori-hibák"></a>
# 4. Gyakori hibák
<a id="41-a-hőtérkép-nem-indul-el"></a>
## 4.1. A hőtérkép nem indul el

Lehetséges okok:

-   hiányzik a `heatmap.exe`
-   hiányzik a `Resources` mappa
-   a program nem tud írni a telepítési könyvtárba

<a id="42-az-eszközlista-üres"></a>
## 4.2. Az eszközlista üres

Valószínűleg hiányzik:

```
cleaned_magnetic_data.csv
```

a `Resources` mappából.


<a id="43-a-mentés-nem-működik"></a>
## 4.3. A mentés nem működik

Ez leggyakrabban akkor történik, ha a program a `Program Files` vagy `Program Files (x86)` mappába lett telepítve.

<a id="44-javasolt-megoldás"></a>
## 4.4. Javasolt megoldás
A felmerülő hibák esetében az újratelepítés a javasolt, legegyszerűbb megoldás.
