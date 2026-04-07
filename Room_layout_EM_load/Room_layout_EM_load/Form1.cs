using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace Room_layout_EM_load
{
    public partial class Form1 : Form
    {
        private GridCell[,] grid;
        private List<DeviceInfo> devices = new List<DeviceInfo>();

        private int cellSizePx = 25;

        private double gridSizeM = 0.5;
        private const double ExportCellSizeM = 0.25;

        private int innerWidthCells;
        private int innerHeightCells;

        private int totalWidthCells;
        private int totalHeightCells;

        private string currentTool = "";

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

            string csvPath = Path.Combine(Application.StartupPath, "magnetic_data.csv");
            devices = LoadDevicesFromCsv(csvPath);

            lstTools.DataSource = null;
            lstTools.DisplayMember = "EszkozNeve";
            lstTools.ValueMember = "Id";
            lstTools.DataSource = devices;

            lstSpecialTools.DataSource = null;
            lstSpecialTools.DisplayMember = "Key";
            lstSpecialTools.ValueMember = "Value";
            lstSpecialTools.DataSource = new BindingSource(specialToolMapping, null);

            if (lstTools.Items.Count > 0)
            {
                lstTools.SelectedIndex = 0;
            }
        }

        private List<DeviceInfo> LoadDevicesFromCsv(string filePath)
        {
            List<DeviceInfo> result = new List<DeviceInfo>();

            if (!File.Exists(filePath))
            {
                MessageBox.Show("A magnetic_data.csv fájl nem található:\n" + filePath);
                return result;
            }

            string[] lines = File.ReadAllLines(filePath, Encoding.UTF8);

            if (lines.Length <= 1)
                return result;

            for (int i = 1; i < lines.Length; i++)
            {
                string line = lines[i].Trim();

                if (string.IsNullOrWhiteSpace(line))
                    continue;

                string[] parts = line.Split(',');

                // 0 = eszkoz_neve
                // 1 = magneses_sugarzas_mikrotesla
                // 2 = meresi_tavolsag_meterben
                // 3 = id
                if (parts.Length < 4)
                    continue;

                string eszkozNeve = parts[0].Trim();
                string id = parts[3].Trim();

                if (string.IsNullOrWhiteSpace(eszkozNeve) || string.IsNullOrWhiteSpace(id))
                    continue;

                result.Add(new DeviceInfo
                {
                    EszkozNeve = eszkozNeve,
                    Id = id
                });
            }

            return result;
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

                int personCounter = 1;

                using (StreamWriter sw = new StreamWriter(saveFileDialog1.FileName, false, Encoding.UTF8))
                {
                    sw.WriteLine("x;y;x_m;y_m;cell_size_m;is_wall;device_id");

                    for (int x = 0; x < totalWidthCells; x++)
                    {
                        for (int y = 0; y < totalHeightCells; y++)
                        {
                            GridCell cell = grid[x, y];

                            for (int subX = 0; subX < subdiv; subX++)
                            {
                                for (int subY = 0; subY < subdiv; subY++)
                                {
                                    int exportX = x * subdiv + subX;
                                    int exportY = y * subdiv + subY;

                                    double xM = exportX * ExportCellSizeM;
                                    double yM = exportY * ExportCellSizeM;

                                    // Fal export
                                    if (cell.IsWall)
                                    {
                                        sw.WriteLine($"{exportX};{exportY};{xM.ToString(CultureInfo.InvariantCulture)};{yM.ToString(CultureInfo.InvariantCulture)};{ExportCellSizeM.ToString(CultureInfo.InvariantCulture)};1;wall");
                                        continue;
                                    }

                                    // Üres cella: ne exportáljuk
                                    if (cell.Items.Count == 0)
                                        continue;

                                    // Egy cellában több eszköz esetén több sor
                                    foreach (string item in cell.Items)
                                    {
                                        string exportId;

                                        if (item == "person")
                                        {
                                            exportId = $"p{personCounter:D3}";
                                            personCounter++;
                                        }
                                        else
                                        {
                                            exportId = item; // pl. i001
                                        }

                                        sw.WriteLine($"{exportX};{exportY};{xM.ToString(CultureInfo.InvariantCulture)};{yM.ToString(CultureInfo.InvariantCulture)};{ExportCellSizeM.ToString(CultureInfo.InvariantCulture)};0;{exportId}");
                                    }
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
            if (lstTools.SelectedItem is DeviceInfo selected)
            {
                currentTool = selected.Id;
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

                if (string.IsNullOrWhiteSpace(currentTool))
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
            if (item == "person")
                return Color.Pink;

            return Color.LightBlue;
        }

        private string GetCellLabel(GridCell cell)
        {
            if (cell.IsWall)
                return "W";

            if (cell.Items.Count == 0)
                return "";

            List<string> labels = new List<string>();

            foreach (string itemId in cell.Items)
            {
                if (itemId == "person")
                {
                    labels.Add("U");
                }
                else
                {
                    DeviceInfo device = devices.FirstOrDefault(d => d.Id == itemId);

                    if (device != null)
                    {
                        string nev = device.EszkozNeve;

                        if (nev.Length <= 3)
                            labels.Add(nev.ToUpper());
                        else
                            labels.Add(nev.Substring(0, Math.Min(3, nev.Length)).ToUpper());
                    }
                    else
                    {
                        labels.Add(itemId.ToUpper());
                    }
                }
            }

            return string.Join(",", labels);
        }
    }
}