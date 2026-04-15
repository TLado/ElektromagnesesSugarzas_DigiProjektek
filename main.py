import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
from matplotlib.patches import Rectangle
from skimage.draw import line

# CSV beolvasása
df = pd.read_csv('cleaned_magnetic_data.csv')

# Dictionary létrehozása: { 'id': [sugárzás, távolság] }
devices_and_values = {
    row['id']: [row['magneses_sugarzas_mikrotesla'], row['meresi_tavolsag_meterben']] 
    for _, row in df.iterrows()
}
devices_and_ids = {row['id']: row['eszkoz_neve'] for _, row in df.iterrows()}
RES = 0.125                     # felbontás (12.5 cm), ez a heatmap felbontása - ENNEK OSZTÓJÁNAK KELL LENNIE 0.25-EL!
MAGYAR_LAKOSSAGI_MAXIMUM = 100 # lakossági helyeken ekkora fluxussűrűség fogadható el (azért alacsonyabb, mint a foglalkozási maximum, mivel itt akár a nap 24 órájában is tartózkodhatnak)
MAGYAR_ALACSONY_AL = 1000 # ekkora fluxussűrűség felett már intézkedni kell a munkavállaló védelmére, de még szabad benne dolgozni (AL egyébként Action Level)
MAGYAR_MAGAS_AL = 6000 # ez a maximális határ, amit még óvintézkedés esetén is engedélyezni lehet emberi munkára


def calculate_combined_heatmap_old(dev_types, dxs, dys, width_m, height_m):
    # ARCHIVÁLT FÜGGVÉNY, SUGÁR KÖVETÉS NÉLKÜL, TEHÁT FALAKAT NEM VESZI FIGYELEMBE, CSAK A TÁVOLSÁGOT
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

def calculate_combined_heatmap(dev_types, dxs, dys, width_m, height_m, walls, cell_size_m):
    # Az itt használt sugárkövetés lényegében azt jelenti, hogy minden pixelnél megnézzük, hogy a forrástól a pixelig húzott egyenes vonal metszi-e a falakat. 
    # Ha igen, akkor az adott forrás nem járul hozzá a térerősséghez azon a ponton, ha nem, akkor pedig a távolság alapján számoljuk a hozzájárulást.
    x = np.arange(0, width_m + RES, RES)
    y = np.arange(0, height_m + RES, RES)
    X, Y = np.meshgrid(x, y)
    Z_total = np.zeros_like(X)

    # 1. Fal-maszk mátrix létrehozása
    wall_mask = np.zeros(Z_total.shape, dtype=bool)
    ratio = int(cell_size_m / RES)
    for w in walls:
        wr, wc = int(w[1]/RES), int(w[0]/RES)
        if 0 <= wr < wall_mask.shape[0] and 0 <= wc < wall_mask.shape[1]:
            wall_mask[wr:wr+ratio, wc:wc+ratio] = True

    # 2. Számítás sugárkövetéssel
    for i in range(len(dev_types)):
        B_ref = devices_and_values[dev_types[i]][0]
        dev_dist = devices_and_values[dev_types[i]][1]
        sr, sc = int(dys[i]/RES), int(dxs[i]/RES) # Forrás mátrix indexei
        
        for r in range(Z_total.shape[0]):
            for c in range(Z_total.shape[1]):
                # Vonalhúzás a forrás és a vizsgált pont közé
                rr, cc = line(sr, sc, r, c)
                
                # Ha a vonal nem érint egyetlen "True" (fal) pontot sem
                if not np.any(wall_mask[rr, cc]):
                    dist = max(np.sqrt((X[r, c] - dxs[i])**2 + (Y[r, c] - dys[i])**2), 0.05)
                    Z_total[r, c] += B_ref * (dev_dist / dist)**3

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
    # ARCHIVÁLT FÜGGVÉNY
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

def import_csv_efficient():
    room_layout_efficient = pd.read_csv("room_layout.csv", sep=";")
    # FONTOS MEGJEGYEZNI, hogy 2*25 cm-el nagyobb maga szoba, mint amit beírtunk az applikációba, mert a falakat ott nem számolta bele
    # a heatmapekben viszont már a falak is egy cellaként vannak értelmezve

    dev_types = []
    dxs = []
    dys = []
    walls = []

    for index, row in room_layout_efficient.iterrows():
        if row["device_id"] == "wall":
            walls.append((row["x_m"], row["y_m"]))
        elif row["device_id"] != "":
            device_id = row["device_id"]
            dx = row["x_m"]
            dy = row["y_m"]
            dev_types.append(device_id)
            dxs.append(dx)
            dys.append(dy)

    cell_size_m = room_layout_efficient['cell_size_m'].iloc[0]
    
    width_m = room_layout_efficient['x_m'].max() + cell_size_m
    height_m = room_layout_efficient['y_m'].max() + cell_size_m

    return dev_types, dxs, dys, width_m, height_m, cell_size_m, walls

def show_regular_heatmap():
    # FONTOS MEGJEGYEZNI, hogy a pcolormesh a kapott koordinátákat mindig a cella közepének tekinti
    # 1. Adatok bekérése
    # dev_types, dxs, dys, width_m, height_m, cell_size_m = import_csv()
    dev_types, dxs, dys, width_m, height_m, cell_size_m, walls = import_csv_efficient()
    print(f"dev_types: {dev_types}")
    print(f"dxs: {dxs}")
    print(f"dys: {dys}")
    print(f"width_m: {width_m}")
    print(f"height_m: {height_m}")

    # 2. Számítás
    X, Y, Z = calculate_combined_heatmap(dev_types, dxs, dys, width_m, height_m, walls, cell_size_m)
    Z[Z == 0] = 0.0001  # A pontosan 0 értékek felhúzása a színskála aljára, hogy ne fehér legyen

    # 3. Megjelenítés
    plt.figure(figsize=(10, 8))
    
    # Logaritmikus skála a jobb láthatóságért
    # vmin-t érdemes alacsonyra venni, hogy a távoli gyenge mezők is látszódjanak
    norm = LogNorm(vmin=0.0001, vmax=max(Z.max(), 10))
    
    cp = plt.pcolormesh(X + RES/2, Y + RES/2, Z, shading='auto', cmap='magma', norm=norm) # egy kicsit eltoljuk a koordinátákat, hogy a cellák közepére kerüljenek a színek
    # Falak rárajzolása új rétegként
    for w in walls:
        plt.gca().add_patch(Rectangle((w[0], w[1]), cell_size_m, cell_size_m, 
                                      facecolor='gray', edgecolor='black', alpha=1.0, zorder=5))
    
    # Színskála és feliratok (r'' a SyntaxWarning elkerüléséhez)
    plt.colorbar(cp, label=r'Mágneses térerősség ($\mu T$)')
    
    # Eszközök bejelölése a térképen
    for i in range(len(dev_types)):
        plt.scatter(dxs[i]+RES/2, dys[i]+RES/2, color='white', edgecolors='grey', marker='o', s=100)
        # plt.text(dxs[i], dys[i], devices_and_ids[dev_types[i]], color='white', fontsize=9)

    plt.title('Kombinált mágneses hőtérkép a szobában')
    plt.xlabel('X távolság (m)')
    plt.ylabel('Y távolság (m)')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Y tengely invertálása, hogy a szobaszerkesztővel megegyezzen
    plt.gca().invert_yaxis()

    plt.gca().format_coord = lambda x, y: format_coord(x, y, Z)
    # Kilógó perem levágása
    plt.xlim(0, width_m)
    plt.ylim(height_m, 0) # Elöl a nagyobb érték az invertált Y tengely miatt

    # Hover effect: amikor az egér egy eszköz közelébe kerül, megjelenik egy címke a névvel
    annot = plt.gca().annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9, edgecolor="black"), 
                               color="black", fontsize=9, zorder=10)
    annot.set_visible(False)

    def hover(event):
        if event.inaxes == plt.gca() and len(dxs) > 0:
            # Távolságok kiszámítása az egér és az összes eszköz között
            dists = np.sqrt((np.array(dxs) - event.xdata)**2 + (np.array(dys) - event.ydata)**2)
            idx = np.argmin(dists)
            
            # Ha 0.5 méternél közelebb van az egér az eszközhöz, mutassa a címkét
            if dists[idx] < 0.5:
                annot.xy = (dxs[idx], dys[idx])
                annot.set_text(devices_and_ids[dev_types[idx]])
                # Irányváltás, ha a plot jobb oldalán vagyunk, hogy ne lógjon ki a címke
                if event.xdata > width_m / 2:
                    annot.set_ha('right')         # Szöveg igazítása balra felé
                    annot.set_position((-5, 5)) # Doboz eltolása balra és fel
                else:
                    annot.set_ha('left')          # Szöveg igazítása jobbra felé
                    annot.set_position((5, 5))
                annot.set_visible(True)
            else:
                annot.set_visible(False)
            plt.gcf().canvas.draw_idle()

    plt.gcf().canvas.mpl_connect("motion_notify_event", hover)

    plt.show()

def show_limit_heatmap():
    # 1. Adatok bekérése
    # dev_types, dxs, dys, width_m, height_m, cell_size_m = import_csv()
    dev_types, dxs, dys, width_m, height_m, cell_size_m, walls = import_csv_efficient()

    # 2. Számítás
    X, Y, Z = calculate_combined_heatmap(dev_types, dxs, dys, width_m, height_m, walls, cell_size_m)

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
    
    # A Z_colored mátrixot az Y tengely mentén invertáljuk az origin='upper' miatt
    plt.imshow(np.flipud(Z_colored), 
               extent=[X.min(), X.max()+RES, Y.min(), Y.max()+RES], # bevallom, nem tudom miért, de el kellett tolni a max értéket, hogy jó legyen az átfedés
               origin='upper', aspect='auto')
    # Falak rárajzolása új rétegként
    for w in walls:
        plt.gca().add_patch(Rectangle((w[0], w[1]), cell_size_m, cell_size_m, 
                                      facecolor='gray', edgecolor='black', alpha=1.0, zorder=5))
    
    # Eszközök bejelölése a térképen
    for i in range(len(dev_types)):
        plt.scatter(dxs[i]+RES/2, dys[i]+RES/2, color='white', edgecolors='grey', marker='o', s=100)
        # plt.text(dxs[i], dys[i], devices_and_ids[dev_types[i]], color='black', fontsize=9, 
                # bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='black', linewidth=0.5))

    plt.title('Mágneses térerősség kategóriák (határértékek szerint)')
    plt.xlabel('X távolság (m)')
    plt.ylabel('Y távolság (m)')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Y tengely invertálása, hogy a szobaszerkesztővel megegyezzen
    plt.gca().invert_yaxis()
    
    # Jelmagyarázat
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=[0, 1, 0], label=f'0 - {MAGYAR_LAKOSSAGI_MAXIMUM} µT (Biztonságos)'),
        Patch(facecolor=[1, 1, 0], label=f'{MAGYAR_LAKOSSAGI_MAXIMUM} - {MAGYAR_ALACSONY_AL} µT (Lakossági határt átlépte)'),
        Patch(facecolor=[1, 0.647, 0], label=f'{MAGYAR_ALACSONY_AL} - {MAGYAR_MAGAS_AL} µT (Alacsony foglalkozási határt)'),
        Patch(facecolor=[1, 0, 0], label=f'{MAGYAR_MAGAS_AL} µT felett (Magas foglalkozási határt)')
    ]
    # Jelmagyarázat kihelyezése a grafikon alá
    plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
    
    # Margók igazítása, hogy biztosan beférjen
    plt.tight_layout()
    
    # Kilógó perem levágása
    plt.xlim(0, width_m)
    plt.ylim(height_m, 0) # Elöl a nagyobb érték az invertált Y tengely miatt

    # Hover effect: amikor az egér egy eszköz közelébe kerül, megjelenik egy címke a névvel
    annot = plt.gca().annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9, edgecolor="black"), 
                               color="black", fontsize=9, zorder=10)
    annot.set_visible(False)

    def hover(event):
        if event.inaxes == plt.gca() and len(dxs) > 0:
            # Távolságok kiszámítása az egér és az összes eszköz között
            dists = np.sqrt((np.array(dxs) - event.xdata)**2 + (np.array(dys) - event.ydata)**2)
            idx = np.argmin(dists)
            
            # Ha 0.5 méternél közelebb van az egér az eszközhöz, mutassa a címkét
            if dists[idx] < 0.5:
                annot.xy = (dxs[idx], dys[idx])
                annot.set_text(devices_and_ids[dev_types[idx]])
                # Irányváltás, ha a plot jobb oldalán vagyunk, hogy ne lógjon ki a címke
                if event.xdata > width_m / 2:
                    annot.set_ha('right')         # Szöveg igazítása balra felé
                    annot.set_position((-5, 5)) # Doboz eltolása balra és fel
                else:
                    annot.set_ha('left')          # Szöveg igazítása jobbra felé
                    annot.set_position((5, 5))
                annot.set_visible(True)
            else:
                annot.set_visible(False)
            plt.gcf().canvas.draw_idle()

    plt.gcf().canvas.mpl_connect("motion_notify_event", hover)
    
    plt.show(block=False)

def display_heatmaps():
    """Megjeleníti mindkét hőtérképet (reguláris és kategorizált)."""
    plt.ion()  # Interaktív mód bekapcsolása
    show_regular_heatmap() # sima heatmap
    show_limit_heatmap() # határértékek szerinti kategorizált heatmap
    plt.show(block=True)  # Mindkét ablak nyitva marad, lehet navigálni közöttük

if __name__ == "__main__":
    # from room_layout import NotebookRoomDesigner
    # designer = NotebookRoomDesigner()
    # plt.show()
    display_heatmaps()