# Elektromágneses Sugárzás Projekt a Digitális Projektek tárgyhoz

**Cél**: egy olyan program létrehozása, amely képes megbecsülni a beltéri elektromágneses terhelést, tehát egy olyan futtatható python fájl, ami a bemeneti változók megadása után (laptopok száma stb.) a terhelési mutatót dobja ki.  

**Feladat részletesebben**: 
- Bemeneti változók: környezet leírása (pl. hány laptop van, milyen közel vannak egymáshoz stb.) 
- Kimeneti változó: összegző terhelési mutató (0-1-ig; az 1 feletti érték már a biztonságos határérték felett van) és egy közvetlen terhelési érték (Volt per méter (V/m) vagy Watt per négyzetméter (W/m^2)) 
- Amennyiben indokolt, a programkód kibővíthető egy tanuló modellé. 

**Pár fontos infó (még csak a mágneses térről, mivel azt az excelt kaptuk csak meg)**
- Hz = Frekvencia, azt adja meg, milyen gyorsan rezeg a tér (milyen ütemben változik az iránya)
- muT = Azt adja meg, milyen erős a mágneses tér, milyen a fluxussűrűsége (a mu egy görög betű, csak ebben a karakterkódolásban nincs benne)
- Lakossági Maximum = lakossági helyeken ekkora fluxussűrűség fogadható el (azért alacsonyabb, mint a foglalkozási maximum, mivel itt akár a nap 24 órájában is tartózkodhatnak)
- Foglalkozási Maximum = munkahelyen a maximális fluxussűrűség (ebben van az alacsony AL és a magas AL)
- alacsony AL = ekkora fluxussűrűség esetén már intézkedni kell a munkavállaló védelmére, de még szabad benne dolgozni (AL egyébként Action Level)
- magas AL = ez a maximális határ, amit még óvintézkedés esetén is engedélyezni lehet emberi munkára