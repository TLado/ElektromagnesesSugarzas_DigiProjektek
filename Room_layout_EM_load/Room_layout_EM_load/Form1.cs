using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Text;
using System.Windows.Forms;

namespace Room_layout_EM_load
{
    public partial class Form1 : Form
    {
        private GridCell[,] grid;

        private int cellSizePx = 25;

        private double gridSizeM = 0.5;
        private const double ExportCellSizeM = 0.25;

        private int innerWidthCells;
        private int innerHeightCells;

        private int totalWidthCells;
        private int totalHeightCells;

        private string currentTool = "monitor";

        private Dictionary<string, string> toolMapping = new Dictionary<string, string>()
        {
            { "Számítógép monitor", "monitor" },
            { "Asztali számítógép", "desktop_pc" },
            { "Laptop", "laptop" },
            { "Mobiltelefon (használat közben, asztalon)", "phone_active" },
            { "Irodai WiFi router", "wifi_router" },
            { "Nyomtató / multifunkciós gép (működés közben)", "printer_active" },
            { "Fluoreszkáló / LED lámpa (mennyezeti)", "lamp" },
            { "Irodai konnektor / hosszabbító", "power_strip" },
            { "Szkenner / fénymásoló", "scanner" }
        };

        private Dictionary<string, string> specialToolMapping = new Dictionary<string, string>()
        {
            { "Fal", "wall" },
            { "Személy", "person" },
            { "Radír", "erase" }
        };

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            cmbGrid.SelectedIndex = 1; // 0.5

            lstTools.DataSource = new BindingSource(toolMapping, null);
            lstTools.DisplayMember = "Key";
            lstTools.ValueMember = "Value";

            lstSpecialTools.DataSource = new BindingSource(specialToolMapping, null);
            lstSpecialTools.DisplayMember = "Key";
            lstSpecialTools.ValueMember = "Value";

            if (lstTools.Items.Count > 0)
            {
                lstTools.SelectedIndex = 0;
            }
        }

        private void CreateRoom(int innerWidthCells, int innerHeightCells)
        {
            this.innerWidthCells = innerWidthCells;
            this.innerHeightCells = innerHeightCells;

            totalWidthCells = innerWidthCells + 2;
            totalHeightCells = innerHeightCells + 2;

            grid = new GridCell[totalWidthCells, totalHeightCells];

            for (int x = 0; x < totalWidthCells; x++)
            {
                for (int y = 0; y < totalHeightCells; y++)
                {
                    grid[x, y] = new GridCell();

                    if (x == 0 || y == 0 || x == totalWidthCells - 1 || y == totalHeightCells - 1)
                    {
                        grid[x, y].IsWall = true;
                    }
                }
            }

            canvasPanel.Width = totalWidthCells * cellSizePx + 1;
            canvasPanel.Height = totalHeightCells * cellSizePx + 1;
        }

        private void btnGenerate_Click(object sender, EventArgs e)
        {
            double widthM = (double)numWidth.Value;
            double heightM = (double)numHeight.Value;

            if (cmbGrid.SelectedItem == null)
            {
                MessageBox.Show("Válassz grid méretet.");
                return;
            }

            gridSizeM = double.Parse(cmbGrid.SelectedItem.ToString(), CultureInfo.InvariantCulture);

            int innerWidth = (int)Math.Round(widthM / gridSizeM);
            int innerHeight = (int)Math.Round(heightM / gridSizeM);

            if (innerWidth < 1 || innerHeight < 1)
            {
                MessageBox.Show("A szoba mérete túl kicsi a választott gridhez.");
                return;
            }

            CreateRoom(innerWidth, innerHeight);
            canvasPanel.Invalidate();
        }

        private void btnExport_Click(object sender, EventArgs e)
        {
            if (grid == null)
            {
                MessageBox.Show("Először hozz létre egy szobát.");
                return;
            }

            saveFileDialog1.Filter = "CSV files (*.csv)|*.csv";
            saveFileDialog1.FileName = "room_layout.csv";

            if (saveFileDialog1.ShowDialog() != DialogResult.OK)
                return;

            try
            {
                int subdiv = (int)Math.Round(gridSizeM / ExportCellSizeM);

                if (Math.Abs(subdiv * ExportCellSizeM - gridSizeM) > 0.0001)
                {
                    MessageBox.Show("A jelenlegi grid méret nem exportálható pontosan 0.25 m-es cellákra.");
                    return;
                }

                using (StreamWriter sw = new StreamWriter(saveFileDialog1.FileName, false, Encoding.UTF8))
                {
                    sw.WriteLine("x;y;is_wall;items");

                    for (int x = 0; x < totalWidthCells; x++)
                    {
                        for (int y = 0; y < totalHeightCells; y++)
                        {
                            GridCell cell = grid[x, y];
                            string items = string.Join(",", cell.Items);

                            for (int subX = 0; subX < subdiv; subX++)
                            {
                                for (int subY = 0; subY < subdiv; subY++)
                                {
                                    int exportX = x * subdiv + subX;
                                    int exportY = y * subdiv + subY;

                                    sw.WriteLine($"{exportX};{exportY};{(cell.IsWall ? 1 : 0)};{items}");
                                }
                            }
                        }
                    }
                }

                MessageBox.Show("CSV export kész.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Hiba export közben: " + ex.Message);
            }
        }

        private void lstTools_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (lstTools.SelectedItem is KeyValuePair<string, string> selected)
            {
                currentTool = selected.Value;
                lstSpecialTools.ClearSelected();
            }
        }

        private void lstSpecialTools_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (lstSpecialTools.SelectedItem is KeyValuePair<string, string> selected)
            {
                currentTool = selected.Value;
                lstTools.ClearSelected();
            }
        }

        private void canvasPanel_Paint(object sender, PaintEventArgs e)
        {
            if (grid == null)
                return;

            Graphics g = e.Graphics;

            for (int x = 0; x < totalWidthCells; x++)
            {
                for (int y = 0; y < totalHeightCells; y++)
                {
                    GridCell cell = grid[x, y];

                    Rectangle rect = new Rectangle(
                        x * cellSizePx,
                        y * cellSizePx,
                        cellSizePx,
                        cellSizePx);

                    Color fillColor;

                    if (cell.IsWall)
                    {
                        fillColor = Color.DarkGray;
                    }
                    else if (cell.Items.Count > 0)
                    {
                        fillColor = GetItemColor(cell.Items[0]);
                    }
                    else
                    {
                        int innerX = x - 1;
                        int innerY = y - 1;

                        int meterBlockX = (int)Math.Floor((innerX * gridSizeM) / 1.0);
                        int meterBlockY = (int)Math.Floor((innerY * gridSizeM) / 1.0);

                        if ((meterBlockX + meterBlockY) % 2 == 0)
                            fillColor = Color.White;
                        else
                            fillColor = Color.LightGray;
                    }

                    using (Brush brush = new SolidBrush(fillColor))
                    {
                        g.FillRectangle(brush, rect);
                    }

                    g.DrawRectangle(Pens.Black, rect);

                    string text = GetCellLabel(cell);
                    if (!string.IsNullOrEmpty(text))
                    {
                        TextRenderer.DrawText(
                            g,
                            text,
                            this.Font,
                            rect,
                            cell.IsWall ? Color.White : Color.Black,
                            TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter
                        );
                    }
                }
            }
        }

        private void canvasPanel_MouseClick(object sender, MouseEventArgs e)
        {
            if (grid == null)
                return;

            int x = e.X / cellSizePx;
            int y = e.Y / cellSizePx;

            if (x < 0 || y < 0 || x >= totalWidthCells || y >= totalHeightCells)
                return;

            GridCell cell = grid[x, y];

            if (currentTool == "erase")
            {
                cell.IsWall = false;
                cell.Items.Clear();
            }
            else if (currentTool == "wall")
            {
                if (cell.Items.Count == 0)
                {
                    cell.IsWall = !cell.IsWall;
                }
            }
            else
            {
                if (cell.IsWall)
                    return;

                if (cell.Items.Contains(currentTool))
                    cell.Items.Remove(currentTool);
                else
                    cell.Items.Add(currentTool);
            }

            canvasPanel.Invalidate();
        }

        private Color GetItemColor(string item)
        {
            switch (item)
            {
                case "monitor":
                    return Color.LightGreen;
                case "desktop_pc":
                    return Color.LightBlue;
                case "laptop":
                    return Color.CadetBlue;
                case "phone_active":
                    return Color.PeachPuff;
                case "wifi_router":
                    return Color.Khaki;
                case "printer_active":
                    return Color.Plum;
                case "lamp":
                    return Color.LightYellow;
                case "power_strip":
                    return Color.LightGray;
                case "scanner":
                    return Color.LightSalmon;
                case "person":
                    return Color.Pink;
                default:
                    return Color.White;
            }
        }

        private string GetCellLabel(GridCell cell)
        {
            if (cell.IsWall)
                return "W";

            if (cell.Items.Count == 0)
                return "";

            List<string> labels = new List<string>();

            foreach (string item in cell.Items)
            {
                switch (item)
                {
                    case "monitor":
                        labels.Add("MON");
                        break;
                    case "desktop_pc":
                        labels.Add("PC");
                        break;
                    case "laptop":
                        labels.Add("L");
                        break;
                    case "phone_active":
                        labels.Add("PH");
                        break;
                    case "wifi_router":
                        labels.Add("R");
                        break;
                    case "printer_active":
                        labels.Add("PR");
                        break;
                    case "lamp":
                        labels.Add("LMP");
                        break;
                    case "power_strip":
                        labels.Add("PS");
                        break;
                    case "scanner":
                        labels.Add("SC");
                        break;
                    case "person":
                        labels.Add("U");
                        break;
                    default:
                        labels.Add(item.Substring(0, Math.Min(2, item.Length)).ToUpper());
                        break;
                }
            }

            return string.Join(",", labels);
        }
    }
}