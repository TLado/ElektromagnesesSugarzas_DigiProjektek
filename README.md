
➤ README

➤ [Felhasználói dokumentáció](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/Felhaszn%C3%A1l%C3%B3i%20dokument%C3%A1ci%C3%B3.md)

➤ [Fejlesztői dokumentáció](https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek/blob/main/Fejleszt%C5%91i%20dokument%C3%A1ci%C3%B3.md)

----
  
 **Számítógépre klónozás:**  `git clone https://github.com/TLado/ElektromagnesesSugarzas_DigiProjektek.git`
Függőségek letöltése (parancssorban):
`pip install -r requirements.txt`

----

# Electromagnetic Load Predictor 

<p>
  <img src="https://i.imgur.com/lV9cnTS.png" width="100">
</p>

Az **EML Predictor** a Budapesti Corvinus Egyetem Digitalizációs projektek tárgya keretében fejlesztett alkalmazás, amely irodai környezetek elektromágneses terhelésének modellezésére és vizualizációjára szolgál.

## Projekt célja  
- irodai környezetek elektromágneses terhelésének modellezése  
- mágneses térerősség vizualizálása  
- különböző szobaelrendezések összehasonlítása  
- oktatási és demonstrációs célú szimuláció biztosítása  

## Az alkalmazás működése

Az alkalmazás két különböző hőtérképet generál az elkészített szoba layout alapján. Az első egy részletes mágneses térerősség-hőtérkép, amely folytonos színátmenettel jeleníti meg a tér erősségét a szoba különböző pontjain. A második egy kategorizált hőtérkép, amely előre definiált határértékek alapján színezi a területeket, így gyorsan azonosíthatók a biztonságos, figyelmeztető vagy potenciálisan veszélyes zónák.

## Számítás
A mágneses térerősség számítása pontszerű sugárforrás-modellen alapul.  
Minden elektromos eszköz egy mágneses teret kibocsátó forrásként kerül kezelésre, amelynek erőssége a távolság növekedésével csökken.

A számítás az inverz köbös törvényt használja:

<p>
  <img src="https://i.imgur.com/x2a8XgG.png" width="250">
</p>


ahol:

-   `B` → a számított mágneses térerősség
-   `B_ref` → az eszköz referencia mágneses értéke
-   `d_ref` → a referencia mérési távolság
-   `d` → a vizsgált pont távolsága az eszköztől

A teljes mágneses tér meghatározásához a rendszer minden egyes vizsgált pontban összeadja az összes eszköz hozzájárulását.

A számítás során a falak árnyékoló akadályként működnek.  
A rendszer sugárkövetés segítségével ellenőrzi, hogy az eszköz és a vizsgált pont közötti egyenes metszi-e valamely falat. Ha igen, az adott eszköz hozzájárulása az adott pontban nullának tekintendő.

Az eredmény egy kétdimenziós mágneses térerősség-eloszlás, amely hőtérképként jeleníthető meg.

## Mértékegységek jelentése
- Hz = Frekvencia, azt adja meg, milyen gyorsan rezeg a tér (milyen ütemben változik az iránya); ez minden elektromos eszköznél 50hz Európában, így ez állandó marad (Amerikában 60Hz)
- µT = Mikrotesla, azt adja meg, milyen erős a mágneses tér, milyen a fluxussűrűsége

## Határértékek jelentése
| Szín | Érték (µT) | Jelentés röviden | Kihez viszonyít | Tipikus jelentés |
|---|---:|---|---|---|
| 🟩 Zöld | 0–100 µT | Biztonságos | Lakosság | A legtöbb országban ez a lakossági ajánlott határ 50 Hz-en, hosszú távú tartózkodásra is elfogadott. |
| 🟨 Sárga | 100–1000 µT | Lakossági határt átlépte | Lakosság vs. munkahely | Már meghaladja a lakossági limitet, de még jellemzően a foglalkozási határ alatt marad. |
| 🟧 Narancs | 1000–6000 µT | Alacsony foglalkozási határ | Dolgozók | Olyan szint, amely tipikusan csak munkavállalóknak engedhető meg, munkavédelmi szabályok mellett. |
| 🟥 Piros | 6000 µT felett | Magas foglalkozási határ | Dolgozók | Nagyon erős mező, csak speciális ipari környezetben, korlátozott ideig, ellenőrzött körülmények között elfogadható. |

---

## Használt technológiák  
  
### C# / .NET Windows Forms  
A grafikus szobatervező felületért felel.  
  
Feladatai:  
- felhasználói interakció kezelése  
- grid generálás  
- eszközök elhelyezése  
- CSV export/import  
- Python alapú vizualizáció indítása  
  
### Python  
A mágneses tér számítását és vizualizációját végzi.  
  
Feladatai:  
- CSV feldolgozás  
- mágneses térerősség számítása  
- falak figyelembevétele sugárkövetéssel  
- hőtérképek generálása

---

## Készítette:

Ladomérszky Torda, Fekete Alex, Rutai Tamás, Jakab Gábor, Zátrok Balázs
2026
