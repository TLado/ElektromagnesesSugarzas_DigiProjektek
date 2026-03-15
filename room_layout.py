import matplotlib
matplotlib.use("QtAgg")

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button, TextBox, RadioButtons
import pandas as pd
import numpy as np
EXPORT_CELL_SIZE_M = 0.25

ITEM_COLORS = {
    "wall": "#4a4a4a",
    "table": "#d9b38c",
    "computer": "#9fc5e8",
    "monitor": "#b6d7a8",
    "phone": "#f9cb9c",
    "person": "#d5a6bd"
}

ITEM_LABELS = {
    "table": "T",
    "computer": "PC",
    "monitor": "M",
    "phone": "P",
    "person": "U"
}

TOOLS = ["wall", "table", "computer", "monitor", "phone", "person", "erase"]


class NotebookRoomDesigner:
    def __init__(self):
        self.inner_width_m = 10.0
        self.inner_height_m = 8.0
        self.cell_size_m = 0.5
        self.current_tool = "table"
        self.grid = []
        self.last_export_path = None

        self.inner_width_cells = self._meters_to_cells(self.inner_width_m, self.cell_size_m)
        self.inner_height_cells = self._meters_to_cells(self.inner_height_m, self.cell_size_m)

        self.total_width_cells = self.inner_width_cells + 2
        self.total_height_cells = self.inner_height_cells + 2

        self.fig = plt.figure(figsize=(14, 8))
        self.ax_grid = self.fig.add_axes([0.05, 0.08, 0.62, 0.84])

        self.ax_width = self.fig.add_axes([0.73, 0.90, 0.08, 0.05])
        self.ax_height = self.fig.add_axes([0.84, 0.90, 0.08, 0.05])
        self.ax_cellsize = self.fig.add_axes([0.73, 0.82, 0.19, 0.05])
        self.ax_generate = self.fig.add_axes([0.73, 0.73, 0.19, 0.06])

        self.ax_tools = self.fig.add_axes([0.73, 0.37, 0.19, 0.30])

        self.ax_filename = self.fig.add_axes([0.73, 0.22, 0.19, 0.05])
        self.ax_export = self.fig.add_axes([0.73, 0.14, 0.19, 0.06])

        self.width_box = TextBox(self.ax_width, "Width m", initial=str(self.inner_width_m))
        self.height_box = TextBox(self.ax_height, "Height m", initial=str(self.inner_height_m))
        self.cellsize_box = TextBox(self.ax_cellsize, "Grid size m", initial=str(self.cell_size_m))

        self.generate_button = Button(self.ax_generate, "Generate Room")
        self.tools_radio = RadioButtons(self.ax_tools, TOOLS, active=1)
        self.filename_box = TextBox(self.ax_filename, "CSV file", initial="room_layout.csv")
        self.export_button = Button(self.ax_export, "Export CSV")

        self.generate_button.on_clicked(self.generate_room)
        self.tools_radio.on_clicked(self.set_tool)
        self.export_button.on_clicked(self.export_csv)
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)

        self._create_room(self.inner_width_cells, self.inner_height_cells)
        self.draw()

    def _meters_to_cells(self, meters, cell_size):
        return max(1, int(round(meters / cell_size)))

    def _empty_cell(self):
        return {"wall": False, "items": []}

    def _create_room(self, inner_width_cells, inner_height_cells):
        self.inner_width_cells = inner_width_cells
        self.inner_height_cells = inner_height_cells

        self.total_width_cells = self.inner_width_cells + 2
        self.total_height_cells = self.inner_height_cells + 2

        self.grid = [
            [self._empty_cell() for _ in range(self.total_width_cells)]
            for _ in range(self.total_height_cells)
        ]

        for y in range(self.total_height_cells):
            for x in range(self.total_width_cells):
                if (
                    x == 0
                    or y == 0
                    or x == self.total_width_cells - 1
                    or y == self.total_height_cells - 1
                ):
                    self.grid[y][x]["wall"] = True
                    self.grid[y][x]["items"] = []

    def generate_room(self, event=None):
        try:
            width_m = float(self.width_box.text.replace(",", "."))
            height_m = float(self.height_box.text.replace(",", "."))
            cell_size_m = float(self.cellsize_box.text.replace(",", "."))
        except ValueError:
            print("A width, height és grid size mezőkbe számot írj.")
            return

        if width_m <= 0 or height_m <= 0 or cell_size_m <= 0:
            print("Minden méret legyen pozitív.")
            return

        if cell_size_m < 0.25:
            print("A grid mérete legalább 0.25 m legyen.")
            return

        inner_width_cells = self._meters_to_cells(width_m, cell_size_m)
        inner_height_cells = self._meters_to_cells(height_m, cell_size_m)

        if inner_width_cells < 1 or inner_height_cells < 1:
            print("A szoba túl kicsi ehhez a felbontáshoz.")
            return

        if inner_width_cells + 2 > 200 or inner_height_cells + 2 > 200:
            print("A grid túl nagy lenne, válassz nagyobb cellaméretet.")
            return

        self.inner_width_m = width_m
        self.inner_height_m = height_m
        self.cell_size_m = cell_size_m

        self._create_room(inner_width_cells, inner_height_cells)
        self.draw()

    def set_tool(self, label):
        self.current_tool = label
        self.draw()

    def on_click(self, event):
        if event.inaxes != self.ax_grid:
            return
        if event.xdata is None or event.ydata is None:
            return

        x = int(event.xdata)
        y = int(event.ydata)

        if x < 0 or y < 0 or x >= self.total_width_cells or y >= self.total_height_cells:
            return

        cell = self.grid[y][x]
        tool = self.current_tool

        if tool == "erase":
            cell["wall"] = False
            cell["items"] = []
            self.draw()
            return

        if tool == "wall":
            if cell["items"]:
                print("Ebben a cellában már van objektum, ezért nem lehet fallá tenni.")
                return
            cell["wall"] = not cell["wall"]
            if cell["wall"]:
                cell["items"] = []
        else:
            if cell["wall"]:
                print("Ez a cella fal, ide más nem helyezhető.")
                return

            if tool in cell["items"]:
                cell["items"].remove(tool)
            else:
                cell["items"].append(tool)

        self.draw()

    def _is_outer_wall(self, x, y):
        return (
            x == 0
            or y == 0
            or x == self.total_width_cells - 1
            or y == self.total_height_cells - 1
        )

    def _empty_checker_color(self, x, y):
        # A sakktáblaminta csak a falon belüli térre vonatkozzon.
        # Ezért a belső koordinátát nézzük: (1,1) legyen a kezdőpont.
        inner_x = x - 1
        inner_y = y - 1

        meter_block_x = int((inner_x * self.cell_size_m) // 1.0)
        meter_block_y = int((inner_y * self.cell_size_m) // 1.0)

        if (meter_block_x + meter_block_y) % 2 == 0:
            return "#ffffff"
        return "#f2f2f2"

    def _cell_facecolor(self, cell, x, y):
        if cell["wall"]:
            return ITEM_COLORS["wall"]

        if cell["items"]:
            return ITEM_COLORS.get(cell["items"][0], "#ffffff")

        return self._empty_checker_color(x, y)

    def _cell_label(self, cell):
        if cell["wall"]:
            return "W"
        if not cell["items"]:
            return ""
        return ",".join(ITEM_LABELS.get(item, item[:1].upper()) for item in cell["items"])

    def draw(self):
        self.ax_grid.clear()
        self.ax_grid.set_xlim(0, self.total_width_cells)
        self.ax_grid.set_ylim(0, self.total_height_cells)
        self.ax_grid.set_aspect("equal")
        self.ax_grid.set_xticks(np.arange(0, self.total_width_cells + 1, 1))
        self.ax_grid.set_yticks(np.arange(0, self.total_height_cells + 1, 1))
        self.ax_grid.grid(True, linewidth=0.6)
        self.ax_grid.invert_yaxis()

        for y in range(self.total_height_cells):
            for x in range(self.total_width_cells):
                cell = self.grid[y][x]
                rect = patches.Rectangle(
                    (x, y),
                    1,
                    1,
                    facecolor=self._cell_facecolor(cell, x, y),
                    edgecolor="black",
                    linewidth=0.6
                )
                self.ax_grid.add_patch(rect)

                label = self._cell_label(cell)
                if label:
                    self.ax_grid.text(
                        x + 0.5,
                        y + 0.5,
                        label,
                        ha="center",
                        va="center",
                        fontsize=8,
                        color="white" if cell["wall"] else "black"
                    )

        self.ax_grid.set_title(
            f"Szobarajzoló | Aktív elem: {self.current_tool} | "
            f"Belső szoba: {self.inner_width_m:.2f}m x {self.inner_height_m:.2f}m | "
            f"Belső grid: {self.inner_width_cells}x{self.inner_height_cells} | "
            f"Teljes grid fallal: {self.total_width_cells}x{self.total_height_cells} | "
            f"Cella: {self.cell_size_m:.2f}m | Export: {EXPORT_CELL_SIZE_M:.2f}m"
        )

        self.fig.canvas.draw_idle()

    def export_dataframe(self):
        subdiv = int(round(self.cell_size_m / EXPORT_CELL_SIZE_M))

        if not math.isclose(subdiv * EXPORT_CELL_SIZE_M, self.cell_size_m, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError(
                f"A jelenlegi grid size ({self.cell_size_m}) nem bontható pontosan "
                f"{EXPORT_CELL_SIZE_M}-es exportcellákra."
            )

        rows = []

        for y in range(self.total_height_cells):
            for x in range(self.total_width_cells):
                cell = self.grid[y][x]

                for sub_y in range(subdiv):
                    for sub_x in range(subdiv):
                        export_x = x * subdiv + sub_x
                        export_y = y * subdiv + sub_y

                        rows.append({
                            "x": export_x,
                            "y": export_y,
                            "x_m": export_x * EXPORT_CELL_SIZE_M,
                            "y_m": export_y * EXPORT_CELL_SIZE_M,
                            "cell_size_m": EXPORT_CELL_SIZE_M,
                            "is_wall": int(cell["wall"]),
                            "items": ",".join(cell["items"]) if cell["items"] else "",
                            "table": int("table" in cell["items"]),
                            "computer": int("computer" in cell["items"]),
                            "monitor": int("monitor" in cell["items"]),
                            "phone": int("phone" in cell["items"]),
                            "person": int("person" in cell["items"])
                        })

        return pd.DataFrame(rows)

    def export_csv(self, event=None):
        filename = self.filename_box.text.strip()
        if not filename:
            print("Adj meg fájlnevet.")
            return

        if not filename.endswith(".csv"):
            filename += ".csv"

        try:
            df = self.export_dataframe()
        except ValueError as e:
            print(str(e))
            return

        df.to_csv(filename, sep=";", index=False, encoding="utf-8-sig")
        self.last_export_path = filename
        print(f"CSV elmentve: {filename}")
        print(f"Export felbontás: {EXPORT_CELL_SIZE_M} m x {EXPORT_CELL_SIZE_M} m")
        print(f"Exportált sorok száma: {len(df)}")


designer = NotebookRoomDesigner()
plt.show()
