import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd

# CSV beolvasása
df = pd.read_csv('cleaned_magnetic_data.csv')

# Konstansok

# Dictionary létrehozása: { 'eszköz neve': [sugárzás, távolság] }
devices_and_values = {
    row['eszkoz_neve']: [row['magneses_sugarzas_mikrotesla'], row['meresi_tavolsag_meterben']] 
    for _, row in df.iterrows()
}
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
        
        B_ref = devices_and_values[dev_types[i]][0]
        # Inverz köbös törvény (pontszerű forrás)
        Z_total += B_ref * (devices_and_values[dev_types[i]][1] / dist)**3

    return X, Y, Z_total

def format_coord(x, y, Z):
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
    # CSV beolvasása (figyelj a szeparátorra!)
    room_layout = pd.read_csv("room_layout.csv", sep=";")

    dev_types = []
    dxs = []
    dys = []

    # Azokat az oszlopokat keressük, amik szerepelnek a mágneses adatbázisban is
    available_devices = [col for col in room_layout.columns if col in devices_and_values]

    for dev in available_devices:
        # Kiválasztjuk azokat a sorokat, ahol az adott eszköz jelen van (1-es érték)
        active_items = room_layout[room_layout[dev] == 1]
        for item in active_items.itertuples():
            dev_types.append(dev)
            dxs.append(item.x_m)
            dys.append(item.y_m)

    # Paraméterek kinyerése
    cell_size_m = room_layout['cell_size_m'].iloc[0]
    
    width_m = room_layout['x_m'].max() + cell_size_m - 1
    height_m = room_layout['y_m'].max() + cell_size_m - 1

    return dev_types, dxs, dys, width_m, height_m, cell_size_m


def show_regular_heatmap():
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

    plt.gca().format_coord = lambda x, y: format_coord(x, y, Z)
    
    plt.show()

def show_limit_heatmap():
    # 1. Adatok bekérése
    dev_types, dxs, dys, width_m, height_m, cell_size_m = import_csv()

    # 2. Számítás
    X, Y, Z = calculate_combined_heatmap(dev_types, dxs, dys, width_m, height_m)

    # 3. Kategorizálás: szín alapján a határértékek szerint
    # Zöld: 0 - MAGYAR_LAKOSSAGI_MAXIMUM
    # Sárga: MAGYAR_LAKOSSAGI_MAXIMUM - MAGYAR_ALACSONY_AL
    # Narancssárga: MAGYAR_ALACSONY_AL - MAGYAR_MAGAS_AL
    # Piros: MAGYAR_MAGAS_AL felett
    
    Z_colored = np.zeros((*Z.shape, 3))  # RGB mátrix
    
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            value = Z[i, j]
            
            if value <= MAGYAR_LAKOSSAGI_MAXIMUM:
                # Zöld
                Z_colored[i, j] = [0, 1, 0]
            elif value <= MAGYAR_ALACSONY_AL:
                # Sárga
                Z_colored[i, j] = [1, 1, 0]
            elif value <= MAGYAR_MAGAS_AL:
                # Narancssárga
                Z_colored[i, j] = [1, 0.647, 0]
            else:
                # Piros
                Z_colored[i, j] = [1, 0, 0]

    # 4. Megjelenítés
    plt.figure(figsize=(10, 8))
    
    plt.imshow(Z_colored, extent=[X.min(), X.max(), Y.min(), Y.max()], 
               origin='lower', aspect='auto')
    
    # Eszközök bejelölése a térképen
    for i in range(len(dev_types)):
        plt.scatter(dxs[i], dys[i], color='white', marker='x', s=100)
        plt.text(dxs[i]+0.2, dys[i]+0.2, dev_types[i], color='black', fontsize=9, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='black', linewidth=0.5))

    plt.title('Mágneses térerősség kategóriák (határértékek szerint)')
    plt.xlabel('X távolság (m)')
    plt.ylabel('Y távolság (m)')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Jelmagyarázat
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=[0, 1, 0], label=f'0 - {MAGYAR_LAKOSSAGI_MAXIMUM} µT (Biztonságos)'),
        Patch(facecolor=[1, 1, 0], label=f'{MAGYAR_LAKOSSAGI_MAXIMUM} - {MAGYAR_ALACSONY_AL} µT (Lakossági határt átlépte)'),
        Patch(facecolor=[1, 0.647, 0], label=f'{MAGYAR_ALACSONY_AL} - {MAGYAR_MAGAS_AL} µT (Alacsony foglalkozási határt)'),
        Patch(facecolor=[1, 0, 0], label=f'{MAGYAR_MAGAS_AL} µT felett (Magas foglalkozási határt)')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.show(block=False)

if __name__ == "__main__":
    plt.ion()  # Interaktív mód bekapcsolása
    show_regular_heatmap() # sima heatmap
    show_limit_heatmap() # határértékek szerinti kategorizált heatmap
    plt.show(block=True)  # Mindkét ablak nyitva marad, lehet navigálni közöttük