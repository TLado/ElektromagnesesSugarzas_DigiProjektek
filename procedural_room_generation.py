import math
import random
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.prompt import Prompt
from rich import box

# ---------------------------------------------------------------------------
# Konstansok
# ---------------------------------------------------------------------------
EXPORT_CELL_SIZE_M = 0.25
WALL_THICKNESS = 1

# Asztal fizikai mérete cellában
DESK_W = 6   # ~1.5 m
DESK_H = 3   # ~0.75 m

DESK_BUNDLES = {
    "Developer (PC + 2 Monitor + Telefon)": {
        "computer": 1, "monitor": 2, "phone": 1, "person": 1,
    },
    "Standard (PC + Monitor + Telefon)": {
        "computer": 1, "monitor": 1, "phone": 1, "person": 1,
    },
    "Recepció (PC + Monitor + Telefon, nincs person)": {
        "computer": 1, "monitor": 1, "phone": 1, "person": 0,
    },
    "Tárgyaló asztal (csak Telefon)": {
        "computer": 0, "monitor": 0, "phone": 1, "person": 0,
    },
}

ITEM_STYLE = {
    "wall":     ("##", "white on grey23"),
    "table":    ("__", "bold white on dark_orange3"),
    "computer": ("PC", "bold white on blue"),
    "monitor":  ("MO", "bold white on green4"),
    "phone":    ("PH", "bold white on dark_red"),
    "person":   ("US", "bold white on purple"),
    "empty":    ("..", "grey50"),
}

console = Console()


# ---------------------------------------------------------------------------
# Asztal-blokk elhelyezési sablon
# ---------------------------------------------------------------------------
# A DESK_W x DESK_H-as blokkban megmondjuk, melyik (dx, dy) cellába
# kerül az adott eszköz. dx: 0..DESK_W-1, dy: 0..DESK_H-1
# dy=0 = hátsó sor (fal felőli), dy=DESK_H-1 = elülső (szék)

def desk_item_layout(bundle: dict) -> dict:
    """
    Visszaad egy {(dx, dy): item_name} szótárt a blokkon belüli
    eszköz-pozíciókhoz. Az asztal ("table") az összes cellát kitölti
    háttérként – az eszközök felülírják.
    """
    layout = {}

    items_to_place = []
    for item in ["monitor", "monitor", "computer", "phone", "person"]:
        if bundle.get(item, 0) > 0 and item not in [v for v in items_to_place]:
            items_to_place.append(item)
        elif item == "monitor" and bundle.get("monitor", 0) >= 2:
            # 2. monitor is kell
            if items_to_place.count("monitor") < bundle["monitor"]:
                items_to_place.append("monitor")

    # Pozíciók rögzített sablonban (DESK_W=6, DESK_H=3)
    # Hátsó sor (dy=0): monitorok balra + computer jobbra
    monitor_positions = [(0, 0), (1, 0), (2, 0)]
    computer_position = (4, 0)
    phone_position    = (2, 1)
    person_position   = (1, 2)

    # Asztal háttér – minden cella "table"
    for dy in range(DESK_H):
        for dx in range(DESK_W):
            layout[(dx, dy)] = "table"

    # Eszközök felülírják a table-t
    mon_count = 0
    for item in ["monitor", "monitor", "computer", "phone", "person"]:
        if item == "monitor" and mon_count < bundle.get("monitor", 0):
            if mon_count < len(monitor_positions):
                layout[monitor_positions[mon_count]] = "monitor"
            mon_count += 1
        elif item == "computer" and bundle.get("computer", 0):
            layout[computer_position] = "computer"
        elif item == "phone" and bundle.get("phone", 0):
            layout[phone_position] = "phone"
        elif item == "person" and bundle.get("person", 0):
            layout[person_position] = "person"

    return layout


# ---------------------------------------------------------------------------
# Generálási logika
# ---------------------------------------------------------------------------

def meters_to_cells(meters: float) -> int:
    return max(1, int(round(meters / EXPORT_CELL_SIZE_M)))


def build_empty_grid(total_w: int, total_h: int) -> list:
    grid = []
    for y in range(total_h):
        row = []
        for x in range(total_w):
            is_wall = (
                x < WALL_THICKNESS or y < WALL_THICKNESS
                or x >= total_w - WALL_THICKNESS
                or y >= total_h - WALL_THICKNESS
            )
            row.append({"wall": is_wall, "items": []})
        grid.append(row)
    return grid


def place_desk_block(grid, origin_x, origin_y, bundle):
    """
    Elhelyez egy DESK_W × DESK_H méretű asztal-blokkot a rácsban.
    origin_x, origin_y: a blokk bal felső sarka.
    """
    layout = desk_item_layout(bundle)
    for dy in range(DESK_H):
        for dx in range(DESK_W):
            cx = origin_x + dx
            cy = origin_y + dy
            if cy >= len(grid) or cx >= len(grid[0]):
                continue
            cell = grid[cy][cx]
            if cell["wall"]:
                continue
            item = layout.get((dx, dy), "table")
            # items lista: az első elem a megjelenített, többi a CSV-hez
            # CSV-kompatibilis oszlopok szempontjából minden asztal-cella
            # megkapja a "table" flagot, az eszközök csak a saját cellájukba
            cell["items"] = [item]
            # CSV-hez: ha az eszköz-cella tartalmaz device-t, annak is
            # legyen "table" flagje (az asztal fizikai részén van)
            if item != "table":
                cell["items"] = [item, "table"]


def _layout_rows(n, x_start, x_end, y_start, y_end):
    """Asztalok sorokban, DESK_W + gap közzel."""
    positions = []
    gap_x = meters_to_cells(0.8)   # asztalok közötti folyosó
    gap_y = meters_to_cells(1.2)   # sorok közötti folyosó
    step_x = DESK_W + gap_x
    step_y = DESK_H + gap_y
    cols = max(1, (x_end - x_start) // step_x)
    for i in range(n):
        col = i % cols
        row = i // cols
        x = x_start + col * step_x
        y = y_start + row * step_y
        positions.append((x, y))
    return positions


def _layout_facing(n, x_start, x_end, y_start, y_end):
    """
    Páros elrendezés: 2 asztal egymással szemben, monitorok középen.
    Az egyik sor normál irányban, a szemközti 'tükrözve' (de pozíció szintjén
    csak az y-t toljuk el egy asztal + kis résnyivel).
    """
    positions = []
    gap_x   = meters_to_cells(0.8)
    gap_mid = meters_to_cells(0.3)   # monitor-monitor rés középen
    step_x  = DESK_W + gap_x

    cols = max(1, (x_end - x_start) // step_x)
    pair_h  = DESK_H * 2 + gap_mid + meters_to_cells(1.5)  # pár magassága
    mid_y   = y_start + (y_end - y_start) // 2

    desk_index = 0
    block = 0
    while desk_index < n:
        for col in range(cols):
            if desk_index >= n:
                break
            x = x_start + col * step_x + block * (cols * step_x)
            pair_top_y    = mid_y - DESK_H - gap_mid // 2
            pair_bottom_y = mid_y + gap_mid // 2

            positions.append((x, pair_top_y))
            desk_index += 1
            if desk_index >= n:
                break
            positions.append((x, pair_bottom_y))
            desk_index += 1
        block += 1
        if block > 10:
            break
    return positions


def generate_layout(inner_w_m, inner_h_m, bundle_counts, layout_style):
    inner_w = meters_to_cells(inner_w_m)
    inner_h = meters_to_cells(inner_h_m)
    total_w = inner_w + 2 * WALL_THICKNESS
    total_h = inner_h + 2 * WALL_THICKNESS
    grid = build_empty_grid(total_w, total_h)

    desks_to_place = []
    for bundle_name, count in bundle_counts.items():
        for _ in range(count):
            desks_to_place.append(DESK_BUNDLES[bundle_name])

    if not desks_to_place:
        return grid, total_w, total_h

    margin = meters_to_cells(1.0)
    x_start = WALL_THICKNESS + margin
    x_end   = total_w - WALL_THICKNESS - margin
    y_start = WALL_THICKNESS + margin
    y_end   = total_h - WALL_THICKNESS - margin

    if x_end - x_start <= 0 or y_end - y_start <= 0:
        x_start = WALL_THICKNESS + 1
        x_end   = total_w - WALL_THICKNESS - 1
        y_start = WALL_THICKNESS + 1
        y_end   = total_h - WALL_THICKNESS - 1

    n = len(desks_to_place)

    if layout_style == "rows":
        positions = _layout_rows(n, x_start, x_end, y_start, y_end)
    elif layout_style == "facing":
        positions = _layout_facing(n, x_start, x_end, y_start, y_end)
    else:
        positions = _layout_rows(n, x_start, x_end, y_start, y_end)

    for i, (px, py) in enumerate(positions[:n]):
        if 0 <= py < len(grid) and 0 <= px < len(grid[0]):
            place_desk_block(grid, px, py, desks_to_place[i])

    return grid, total_w, total_h


def grid_to_dataframe(grid, total_w, total_h):
    rows = []
    for y in range(total_h):
        for x in range(total_w):
            cell = grid[y][x]
            items = cell["items"]
            rows.append({
                "x": x, "y": y,
                "x_m": round(x * EXPORT_CELL_SIZE_M, 4),
                "y_m": round(y * EXPORT_CELL_SIZE_M, 4),
                "cell_size_m": EXPORT_CELL_SIZE_M,
                "is_wall": int(cell["wall"]),
                "items": ",".join(items) if items else "",
                "table":    int("table"    in items),
                "computer": int("computer" in items),
                "monitor":  int("monitor"  in items),
                "phone":    int("phone"    in items),
                "person":   int("person"   in items),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Rich megjelenítés
# ---------------------------------------------------------------------------

def render_map(grid, total_w, total_h, title: str, max_w=72):
    max_cells_x = min(total_w, max_w)
    max_cells_y = min(total_h, 30)

    lines = []
    truncated_x = total_w > max_cells_x
    truncated_y = total_h > max_cells_y

    for y in range(max_cells_y):
        line = Text()
        for x in range(max_cells_x):
            cell = grid[y][x]
            if cell["wall"]:
                sym, style = ITEM_STYLE["wall"]
            elif not cell["items"]:
                sym, style = ITEM_STYLE["empty"]
            else:
                top_item = cell["items"][0]
                sym, style = ITEM_STYLE.get(top_item, ITEM_STYLE["table"])
            line.append(sym, style=style)
        if truncated_x:
            line.append("→", style="grey50 dim")
        lines.append(line)

    if truncated_y:
        lines.append(Text("↓ (levágva)", style="grey50 dim"))

    combined = Text("\n").join(lines)
    return Panel(combined, title=f"[bold]{title}[/bold]",
                 border_style="bright_blue", padding=(0, 1), expand=False)


def render_legend():
    t = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    t.add_column()
    t.add_column()
    labels = {
        "wall": "Fal", "table": "Asztal lap", "computer": "Számítógép",
        "monitor": "Monitor", "phone": "Telefon", "person": "Személy",
    }
    for key, (sym, style) in ITEM_STYLE.items():
        if key == "empty":
            continue
        t.add_row(Text(f" {sym} ", style=style), labels[key])
    return Panel(t, title="Jelölések", border_style="dim", expand=False)


# ---------------------------------------------------------------------------
# CLI user flow
# ---------------------------------------------------------------------------

def ask_float(prompt_text: str, default: float) -> float:
    while True:
        raw = Prompt.ask(prompt_text, default=str(default))
        try:
            val = float(raw.replace(",", "."))
            if val > 0:
                return val
            console.print("[red]Pozitív számot adj meg![/red]")
        except ValueError:
            console.print("[red]Érvénytelen szám![/red]")


def ask_bundle_counts() -> dict:
    console.print("\n[bold cyan]Asztal-kosarak – hány darabot szeretnél?[/bold cyan]")
    counts = {}
    for i, name in enumerate(DESK_BUNDLES.keys(), 1):
        while True:
            raw = Prompt.ask(f"  [{i}] {name}", default="0")
            try:
                n = int(raw)
                if n >= 0:
                    counts[name] = n
                    break
                console.print("[red]Nemnegatív számot adj meg![/red]")
            except ValueError:
                console.print("[red]Egész számot adj meg![/red]")
    return {k: v for k, v in counts.items() if v > 0}


def main():
    console.print(Panel(
        "[bold white]IRODAI SZOBAGENERÁTOR[/bold white]\n"
        "[dim]Procedurális elrendezés → room_layout.csv[/dim]\n"
        f"[dim]Asztal mérete: {DESK_W * EXPORT_CELL_SIZE_M:.2f} m × "
        f"{DESK_H * EXPORT_CELL_SIZE_M:.2f} m  |  "
        f"Felbontás: {EXPORT_CELL_SIZE_M} m/cella[/dim]",
        style="bold bright_blue", expand=False
    ))

    console.print("\n[bold cyan]Szoba méretei[/bold cyan]")
    width_m  = ask_float("  Szélesség (m)", 10.0)
    height_m = ask_float("  Hosszúság (m)", 8.0)

    bundle_counts = ask_bundle_counts()
    if not bundle_counts:
        console.print("[red]Legalább 1 asztalt adj meg![/red]")
        return

    total_desks = sum(bundle_counts.values())
    console.print(f"\n[bold green]Generálás... ({total_desks} asztal, "
                  f"egyenként {DESK_W}×{DESK_H} cella)[/bold green]")

    items_shuffled = list(bundle_counts.items())
    random.shuffle(items_shuffled)

    configs = [
        (bundle_counts,        "rows",   "A – Sorok"),
        (bundle_counts,        "facing", "B – Szemközti párok"),
        (dict(items_shuffled), "rows",   "C – Sorok (véletlen sorrend)"),
    ]

    options = []
    for bc, style, label in configs:
        grid, tw, th = generate_layout(width_m, height_m, bc, style)
        options.append((grid, tw, th, label))

    console.print()
    maps = [render_map(grid, tw, th, label) for grid, tw, th, label in options]
    console.print(Columns(maps, equal=False, expand=False))
    console.print(render_legend())

    # Statisztika
    stat = Table(title="Összefoglaló", box=box.ROUNDED, border_style="dim cyan")
    stat.add_column("Opció", style="bold")
    stat.add_column("Stílus")
    stat.add_column("Asztal cellák")
    stat.add_column("Szoba (m)")
    for grid, tw, th, label in options:
        desk_cells = sum(
            1 for row in grid for cell in row if "table" in cell["items"]
        )
        letter = label.split("–")[0].strip()
        style_name = label.split("–")[1].strip() if "–" in label else label
        stat.add_row(letter, style_name, str(desk_cells),
                     f"{width_m:.1f} × {height_m:.1f}")
    console.print(stat)

    console.print()
    choice = Prompt.ask(
        "[bold yellow]Melyik opciót exportáljuk?[/bold yellow]",
        choices=["A", "B", "C", "a", "b", "c"], default="A"
    ).upper()
    idx = {"A": 0, "B": 1, "C": 2}[choice]

    filename = Prompt.ask("Fájlnév", default="room_layout.csv")
    if not filename.endswith(".csv"):
        filename += ".csv"

    grid, total_w, total_h, label = options[idx]
    df = grid_to_dataframe(grid, total_w, total_h)
    df.to_csv(filename, sep=";", index=False, encoding="utf-8-sig")

    console.print(Panel(
        f"[bold green]✅ Elmentve:[/bold green] {filename}\n"
        f"[dim]Opció: {label}  |  Sorok: {len(df)}  |  "
        f"Asztalméret: {DESK_W * EXPORT_CELL_SIZE_M} m × "
        f"{DESK_H * EXPORT_CELL_SIZE_M} m[/dim]",
        border_style="green", expand=False
    ))


if __name__ == "__main__":
    main()
