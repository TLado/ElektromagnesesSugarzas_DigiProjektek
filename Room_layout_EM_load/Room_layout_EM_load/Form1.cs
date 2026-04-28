using System;
using System.Collections.Generic;
using System.Diagnostics;
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
        private List<DeviceInfo> filteredDevices = new List<DeviceInfo>();

        private int cellSizePx = 25;
        private double gridSizeM = 0.5;

        private int innerWidthCells;
        private int innerHeightCells;
        private int totalWidthCells;
        private int totalHeightCells;

        private string currentTool = "";

        private Dictionary<string, string> specialToolMapping = new Dictionary<string, string>()
        {
            { "Fal", "wall" },
            { "Radír", "erase" }
        };

        public Form1()
        {
            InitializeComponent();
            this.MinimumSize = new Size(1280, 805);
        }

        private string GetResourcesFolder()
        {
            return Path.Combine(Application.StartupPath, "Resources");
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            cmbGrid.SelectedIndex = 1; // 0.5

            string csvPath = Path.Combine(GetResourcesFolder(), "cleaned_magnetic_data.csv");
            devices = LoadDevicesFromCsv(csvPath);
            filteredDevices = new List<DeviceInfo>(devices);

            BindDeviceList(filteredDevices);

            lstSpecialTools.DataSource = null;
            lstSpecialTools.DisplayMember = "Key";
            lstSpecialTools.ValueMember = "Value";
            lstSpecialTools.DataSource = new BindingSource(specialToolMapping, null);

            if (lstTools.Items.Count > 0)
                lstTools.SelectedIndex = 0;
        }

        private List<DeviceInfo> LoadDevicesFromCsv(string filePath)
        {
            List<DeviceInfo> result = new List<DeviceInfo>();

            if (!File.Exists(filePath))
            {
                MessageBox.Show("A cleaned_magnetic_data.csv fájl nem található:\n" + filePath);
                return result;
            }

            string[] lines = File.ReadAllLines(filePath, Encoding.UTF8);

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

        private void BindDeviceList(List<DeviceInfo> source)
        {
            lstTools.DataSource = null;
            lstTools.DisplayMember = "EszkozNeve";
            lstTools.ValueMember = "Id";
            lstTools.DataSource = source;
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
                        grid[x, y].IsWall = true;
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

            double maxWidthM;
            double maxHeightM;

            if (gridSizeM == 0.25)
            {
                maxWidthM = 8;
                maxHeightM = 6;
            }
            else if (gridSizeM == 0.5)
            {
                maxWidthM = 16;
                maxHeightM = 12;
            }
            else if (gridSizeM == 1)
            {
                maxWidthM = 34;
                maxHeightM = 26;
            }
            else
            {
                MessageBox.Show("Ismeretlen grid méret.");
                return;
            }

            if (widthM > maxWidthM)
            {
                widthM = maxWidthM;
                numWidth.Value = (decimal)maxWidthM;
            }

            if (heightM > maxHeightM)
            {
                heightM = maxHeightM;
                numHeight.Value = (decimal)maxHeightM;
            }


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
                SaveCsvToPath(saveFileDialog1.FileName);
                MessageBox.Show("CSV export kész.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Hiba export közben: " + ex.Message);
            }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            if (grid == null)
            {
                MessageBox.Show("Először hozz létre egy szobát.");
                return;
            }

            try
            {
                string resourcesFolder = GetResourcesFolder();
                Directory.CreateDirectory(resourcesFolder);

                string csvPath = Path.Combine(resourcesFolder, "room_layout.csv");
                string heatmapExePath = Path.Combine(resourcesFolder, "heatmap.exe");

                SaveCsvToPath(csvPath);

                if (!File.Exists(heatmapExePath))
                {
                    MessageBox.Show("A heatmap.exe nem található:\n" + heatmapExePath);
                    return;
                }

                ProcessStartInfo start = new ProcessStartInfo
                {
                    FileName = heatmapExePath,
                    WorkingDirectory = resourcesFolder,
                    UseShellExecute = true
                };

                Process.Start(start);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Hiba mentés vagy indítás közben: " + ex.Message);
            }
        }

        private void SaveCsvToPath(string filePath)
        {

            using (StreamWriter sw = new StreamWriter(filePath, false, Encoding.UTF8))
            {
                sw.WriteLine("x;y;x_m;y_m;cell_size_m;is_wall;device_id");

                for (int x = 0; x < totalWidthCells; x++)
                {
                    for (int y = 0; y < totalHeightCells; y++)
                    {
                        GridCell cell = grid[x, y];

                        double xM = x * gridSizeM;
                        double yM = y * gridSizeM;

                        if (cell.IsWall)
                        {
                            sw.WriteLine(
                                $"{x};{y};" +
                                $"{xM.ToString(CultureInfo.InvariantCulture)};" +
                                $"{yM.ToString(CultureInfo.InvariantCulture)};" +
                                $"{gridSizeM.ToString(CultureInfo.InvariantCulture)};" +
                                "1;wall");
                            continue;
                        }

                        if (cell.Items.Count == 0)
                            continue;

                        foreach (string item in cell.Items)
                        {
                            string exportId = item;

                            sw.WriteLine(
                                $"{x};{y};" +
                                $"{xM.ToString(CultureInfo.InvariantCulture)};" +
                                $"{yM.ToString(CultureInfo.InvariantCulture)};" +
                                $"{gridSizeM.ToString(CultureInfo.InvariantCulture)};" +
                                $"0;{exportId}");
                        }
                    }
                }
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

        private void tbFilter_TextChanged(object sender, EventArgs e)
        {
            string filterText = tbFilter.Text.Trim();

            if (string.IsNullOrWhiteSpace(filterText))
            {
                filteredDevices = new List<DeviceInfo>(devices);
            }
            else
            {
                filteredDevices = devices
                    .Where(d =>
                        d.EszkozNeve.IndexOf(filterText, StringComparison.OrdinalIgnoreCase) >= 0 ||
                        d.Id.IndexOf(filterText, StringComparison.OrdinalIgnoreCase) >= 0)
                    .ToList();
            }

            BindDeviceList(filteredDevices);

            if (lstTools.Items.Count > 0)
                lstTools.SelectedIndex = 0;
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

                        fillColor = (meterBlockX + meterBlockY) % 2 == 0
                            ? Color.White
                            : Color.LightGray;
                    }

                    using (Brush brush = new SolidBrush(fillColor))
                        g.FillRectangle(brush, rect);

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
                    cell.IsWall = !cell.IsWall;
            }
            else
            {
                if (cell.IsWall || string.IsNullOrWhiteSpace(currentTool))
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
                DeviceInfo device = devices.FirstOrDefault(d => d.Id == itemId);

                if (device != null)
                {
                    string name = device.EszkozNeve;
                    labels.Add(name.Length <= 3 ? name.ToUpper() : name.Substring(0, 3).ToUpper());
                }
                else
                {
                    labels.Add(itemId.ToUpper());
                }
            }

            return string.Join(",", labels);
        }

        private void btnImport_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Filter = "CSV files (*.csv)|*.csv";

            if (ofd.ShowDialog() != DialogResult.OK)
                return;

            try
            {
                ImportFromCsv(ofd.FileName);
                canvasPanel.Invalidate();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Hibás fájl:\n" + ex.Message);
            }
        }

        private void ImportFromCsv(string filePath)
        {
            var lines = File.ReadAllLines(filePath);

            if (lines.Length < 2)
                throw new Exception("Üres vagy hibás CSV.");

            // fejléc ellenőrzés
            string header = lines[0].Trim().ToLower();
            if (!header.Contains("x;y;x_m;y_m;cell_size_m;is_wall;device_id"))
                throw new Exception("Hibás CSV fejléc.");

            List<(int x, int y, double size, int isWall, string id)> data =
                new List<(int, int, double, int, string)>();

            foreach (var line in lines.Skip(1))
            {
                if (string.IsNullOrWhiteSpace(line))
                    continue;

                var parts = line.Split(';');

                if (parts.Length < 7)
                    throw new Exception("Hibás sor a CSV-ben.");

                int x = int.Parse(parts[0]);
                int y = int.Parse(parts[1]);
                double size = double.Parse(parts[4], CultureInfo.InvariantCulture);
                int isWall = int.Parse(parts[5]);
                string id = parts[6];

                data.Add((x, y, size, isWall, id));
            }

            if (data.Count == 0)
                throw new Exception("Nincs adat a CSV-ben.");

            // grid méret
            gridSizeM = data.First().size;

            // UI sync
            cmbGrid.SelectedItem = gridSizeM.ToString(CultureInfo.InvariantCulture);

            int maxX = data.Max(d => d.x);
            int maxY = data.Max(d => d.y);

            // mivel van fal körben → -2
            int innerWidth = maxX - 1;
            int innerHeight = maxY - 1;

            CreateRoom(innerWidth, innerHeight);

            // reset
            for (int x = 0; x < totalWidthCells; x++)
            {
                for (int y = 0; y < totalHeightCells; y++)
                {
                    grid[x, y].IsWall = false;
                    grid[x, y].Items.Clear();
                }
            }

            // visszatöltés
            foreach (var item in data)
            {
                if (item.x >= totalWidthCells || item.y >= totalHeightCells)
                    continue;

                var cell = grid[item.x, item.y];

                if (item.isWall == 1)
                {
                    cell.IsWall = true;
                }
                else if (!string.IsNullOrWhiteSpace(item.id))
                {
                    if (!cell.Items.Contains(item.id))
                        cell.Items.Add(item.id);
                }
            }
        }
    }
}