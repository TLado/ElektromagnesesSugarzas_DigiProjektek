import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd

# Konstansok
devices_and_values = {"computer": 9, "monitor": 3, "phone": 5}
DISTANCE_WHEN_MEASURED = 0.1  # méter, amikor az alapvető értékeket mértük meg az eszközöknél ennyi méterre voltunk
RES = 0.1                     # felbontás (10 cm), ez a heatmap felbontása
MAGYAR_LAKOSSAGI_MAXIMUM = 100 # lakossági helyeken ekkora fluxussűrűség fogadható el (azért alacsonyabb, mint a foglalkozási maximum, mivel itt akár a nap 24 órájában is tartózkodhatnak)
MAGYAR_ALACSONY_AL = 1000 # ekkora fluxussűrűség felett már intézkedni kell a munkavállaló védelmére, de még szabad benne dolgozni (AL egyébként Action Level)
MAGYAR_MAGAS_AL = 6000 # ez a maximális határ, amit még óvintézkedés esetén is engedélyezni lehet emberi munkára


def calculate_combined_heatmap(dev_types, dxs, dys, width_m, height_m):
    # Rács létrehozása
    x = np.arange(0, width_m + RES, RES)
    y = np.arange(0, height_m + RES, RES)
    X, Y = np.meshgrid(x, y)
    
    # Kezdeti térerősség mindenhol nulla
    Z_total = np.zeros_like(X)

    # Minden eszköz térerősségének hozzáadása
    for i in range(len(dev_types)):
        dist = np.sqrt((X - dxs[i])**2 + (Y - dys[i])**2) # Pitagorasz tétel
        dist = np.maximum(dist, 0.05)  # Nullával osztás elkerülése
        
        B_ref = devices_and_values[dev_types[i]]
        # Inverz köbös törvény (pontszerű forrás)
        Z_total += B_ref * (DISTANCE_WHEN_MEASURED / dist)**3

    return X, Y, Z_total

def format_coord(x, y):
    # Koordináta indexek mellé a mágneses térerősséget is kiírjuk a jobb felső sarokba

    # Kiszámoljuk a mátrix indexeit a koordinátákból
    col = int(round(x / RES))
    row = int(round(y / RES))
    
    # Ellenőrizzük, hogy a szobán belül van-e az egér
    if 0 <= col < Z.shape[1] and 0 <= row < Z.shape[0]:
        z = Z[row, col]
        return f'x={x:.2f}, y={y:.2f}, B={z:.4f} \u03bcT'
    return f'x={x:.2f}, y={y:.2f}'

def import_csv(): 
    room_layout = pd.read_csv("room_layout.csv", sep=";")

    """
    CSV oszlopainak jelentése: 
    x           : A cella oszlopindexe a rácsban (egész szám).
    y           : A cella sorindexe a rácsban (egész szám).
    x_m         : A cella vízszintes középpontja méterben kifejezve.
    y_m         : A cella függőleges középpontja méterben kifejezve.
    cell_size_m : Egy cella oldalhossza méterben (felbontás).
    is_wall     : Bináris (0/1); 1-es, ha a cella egy fal része.
    items       : Ez bevallom nem tudom mi (Alexet kéne kérdezni)
    table       : Bináris (0/1); 1-es, ha asztal található a cellában.
    computer    : Bináris (0/1); 1-es, ha számítógép található a cellában.
    monitor     : Bináris (0/1); 1-es, ha monitor található a cellában.
    phone       : Bináris (0/1); 1-es, ha telefon található a cellában.
    person      : Bináris (0/1); 1-es, ha személy tartózkodik a cellában.

    """

    dev_types = []
    dxs = []
    dys = []

    computers = room_layout[room_layout["computer"] == 1]
    monitors = room_layout[room_layout["monitor"] == 1]
    phones = room_layout[room_layout["phone"] == 1]


    for item in computers.itertuples():
        dev_types.append("computer")
        dxs.append(item.x_m)
        dys.append(item.y_m)

    for item in monitors.itertuples():
        dev_types.append("monitor")
        dxs.append(item.x_m)
        dys.append(item.y_m)

    for item in phones.itertuples():
        dev_types.append("phone")
        dxs.append(item.x_m)
        dys.append(item.y_m)

    # A legnagyobb koordináták megkeresése
    max_x_m = room_layout['x_m'].max()
    max_y_m = room_layout['y_m'].max()
    cell_size_m = room_layout['cell_size_m'].iloc[0]

    # A szoba szélessége és hossza méterben (még falak nélkül, ezért vonok ki egyet-egyet)
    width_m = max_x_m + cell_size_m - 1
    height_m = max_y_m + cell_size_m - 1


    return dev_types, dxs, dys, width_m, height_m, cell_size_m


if __name__ == "__main__":
    # 1. Adatok bekérése
    dev_types, dxs, dys, width_m, height_m, cell_size_m = import_csv()
    print(dev_types)
    print(dxs)
    print(dys)

    # 2. Számítás
    X, Y, Z = calculate_combined_heatmap(dev_types, dxs, dys, width_m, height_m)

    # 3. Megjelenítés
    plt.figure(figsize=(10, 8))
    
    # Logaritmikus skála a jobb láthatóságért
    # vmin-t érdemes alacsonyra venni, hogy a távoli gyenge mezők is látszódjanak
    norm = LogNorm(vmin=0.0001, vmax=max(Z.max(), 10))
    
    cp = plt.pcolormesh(X, Y, Z, shading='auto', cmap='magma', norm=norm)
    
    # Színskála és feliratok (r'' a SyntaxWarning elkerüléséhez)
    plt.colorbar(cp, label=r'Mágneses térerősség ($\mu T$)')
    
    # Eszközök bejelölése a térképen
    for i in range(len(dev_types)):
        plt.scatter(dxs[i], dys[i], color='white', marker='x', s=100)
        plt.text(dxs[i]+0.2, dys[i]+0.2, dev_types[i], color='white', fontsize=9)

    plt.title('Kombinált mágneses hőtérkép a szobában')
    plt.xlabel('X távolság (m)')
    plt.ylabel('Y távolság (m)')
    plt.grid(True, linestyle='--', alpha=0.3)

    plt.gca().format_coord = format_coord 
    
    plt.show()