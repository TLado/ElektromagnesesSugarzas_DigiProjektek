➤ [README](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/README.md)

➤ Felhasználói dokumentáció

➤ [Fejlesztői dokumentáció](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/Fejleszt%C5%91i%20dokument%C3%A1ci%C3%B3.md)

----

# Tartalomjegyzék



# Telepítés és futtatás

A program telepítője a GitHub repositoryban, az alábbi útvonalon található:
    [ElektromagnesesSugarzas_DigiProjektek/Room_layout_EM_load/EMLPredictorSetup/Release/EMLPredictorSetup.msi](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/Room_layout_EM_load/EMLPredictorSetup/Release/EMLPredictorSetup.msi)
   
   A telepítő varázsló a jobb felső sarokban a lefele mutató nyíl ⤓ ikonra tölthető le.

## Telepítési lépések

1.  Töltse le az `.msi` telepítőt.
2.  Indítsa el a telepítési varázslót.
3.  Kövesse a telepítő lépéseit.

### Fontos telepítési megjegyzés

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

----------
## A program indítása

A telepítés után az alkalmazás az asztali ikonról:
<p>
  <img src="https://i.imgur.com/lV9cnTS.png" width="100">
</p>

Vagy a telepítési mappából indítható:
```C:\EMLPredictor\Room_layout_EM_load.exe```

Indítás után a program automatikusan betölti az eszközadatbázist a `Resources` mappából.

# Felhasználói felület áttekintése

A felület fő részei:
![Kezelőfelület](https://i.imgur.com/imKzKQH.png)

|Sorszám| Funkció |
|--|--|
| 1. | Szoba szélességének és magasságának megadása |
| 2. | Rácsfelbontás kiválasztása |
| 3. | Szoba generálása |
| 4. | Korábban mentett layout betöltése |
| 5. | Fal és radír |
| 6. | Eszközlista szűrése |
| 7. | Elhelyezhető eszközök listája |
| 8. | Rajzterület |
| 9. | Layout helyi mentése, vizualizáció megnyitása |
| 10. | Layout exportálása, mentése saját helyre |
