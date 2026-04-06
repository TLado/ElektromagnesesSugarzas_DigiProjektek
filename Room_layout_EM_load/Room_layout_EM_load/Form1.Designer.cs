namespace Room_layout_EM_load
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            splitContainer1 = new SplitContainer();
            tableLayoutPanel1 = new TableLayoutPanel();
            RoomSettings = new GroupBox();
            btnGenerate = new Button();
            cmbGrid = new ComboBox();
            label3 = new Label();
            numHeight = new NumericUpDown();
            numWidth = new NumericUpDown();
            label2 = new Label();
            label1 = new Label();
            groupBox1 = new GroupBox();
            lstSpecialTools = new ListBox();
            lstTools = new ListBox();
            groupBox2 = new GroupBox();
            btnExport = new Button();
            canvasPanel = new Panel();
            saveFileDialog1 = new SaveFileDialog();
            groupBox3 = new GroupBox();
            ((System.ComponentModel.ISupportInitialize)splitContainer1).BeginInit();
            splitContainer1.Panel1.SuspendLayout();
            splitContainer1.Panel2.SuspendLayout();
            splitContainer1.SuspendLayout();
            tableLayoutPanel1.SuspendLayout();
            RoomSettings.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)numHeight).BeginInit();
            ((System.ComponentModel.ISupportInitialize)numWidth).BeginInit();
            groupBox1.SuspendLayout();
            groupBox2.SuspendLayout();
            groupBox3.SuspendLayout();
            SuspendLayout();
            // 
            // splitContainer1
            // 
            splitContainer1.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            splitContainer1.Location = new Point(0, 0);
            splitContainer1.Name = "splitContainer1";
            // 
            // splitContainer1.Panel1
            // 
            splitContainer1.Panel1.Controls.Add(tableLayoutPanel1);
            // 
            // splitContainer1.Panel2
            // 
            splitContainer1.Panel2.Controls.Add(canvasPanel);
            splitContainer1.Size = new Size(1263, 758);
            splitContainer1.SplitterDistance = 294;
            splitContainer1.TabIndex = 0;
            // 
            // tableLayoutPanel1
            // 
            tableLayoutPanel1.AutoScroll = true;
            tableLayoutPanel1.ColumnCount = 1;
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableLayoutPanel1.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 50F));
            tableLayoutPanel1.Controls.Add(RoomSettings, 0, 0);
            tableLayoutPanel1.Controls.Add(groupBox1, 0, 1);
            tableLayoutPanel1.Controls.Add(groupBox2, 0, 3);
            tableLayoutPanel1.Controls.Add(groupBox3, 0, 2);
            tableLayoutPanel1.Dock = DockStyle.Fill;
            tableLayoutPanel1.Location = new Point(0, 0);
            tableLayoutPanel1.Name = "tableLayoutPanel1";
            tableLayoutPanel1.RowCount = 4;
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 66.0493851F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Percent, 33.95062F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 340F));
            tableLayoutPanel1.RowStyles.Add(new RowStyle(SizeType.Absolute, 89F));
            tableLayoutPanel1.Size = new Size(294, 758);
            tableLayoutPanel1.TabIndex = 0;
            // 
            // RoomSettings
            // 
            RoomSettings.Controls.Add(btnGenerate);
            RoomSettings.Controls.Add(cmbGrid);
            RoomSettings.Controls.Add(label3);
            RoomSettings.Controls.Add(numHeight);
            RoomSettings.Controls.Add(numWidth);
            RoomSettings.Controls.Add(label2);
            RoomSettings.Controls.Add(label1);
            RoomSettings.Dock = DockStyle.Fill;
            RoomSettings.Location = new Point(3, 3);
            RoomSettings.Name = "RoomSettings";
            RoomSettings.Size = new Size(288, 211);
            RoomSettings.TabIndex = 0;
            RoomSettings.TabStop = false;
            RoomSettings.Text = "Szoba";
            // 
            // btnGenerate
            // 
            btnGenerate.Location = new Point(141, 149);
            btnGenerate.Name = "btnGenerate";
            btnGenerate.Size = new Size(128, 51);
            btnGenerate.TabIndex = 6;
            btnGenerate.Text = "Szoba generálása";
            btnGenerate.UseVisualStyleBackColor = true;
            btnGenerate.Click += btnGenerate_Click;
            // 
            // cmbGrid
            // 
            cmbGrid.FormattingEnabled = true;
            cmbGrid.Items.AddRange(new object[] { "0.25", "0.5", "1" });
            cmbGrid.Location = new Point(118, 106);
            cmbGrid.Name = "cmbGrid";
            cmbGrid.Size = new Size(151, 28);
            cmbGrid.TabIndex = 5;
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new Point(9, 109);
            label3.Name = "label3";
            label3.Size = new Size(108, 20);
            label3.TabIndex = 4;
            label3.Text = "Rácsméret (m):";
            // 
            // numHeight
            // 
            numHeight.Location = new Point(118, 67);
            numHeight.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            numHeight.Name = "numHeight";
            numHeight.Size = new Size(150, 27);
            numHeight.TabIndex = 3;
            numHeight.Value = new decimal(new int[] { 1, 0, 0, 0 });
            // 
            // numWidth
            // 
            numWidth.Location = new Point(118, 32);
            numWidth.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            numWidth.Name = "numWidth";
            numWidth.Size = new Size(150, 27);
            numWidth.TabIndex = 2;
            numWidth.Value = new decimal(new int[] { 1, 0, 0, 0 });
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(9, 67);
            label2.Name = "label2";
            label2.Size = new Size(106, 20);
            label2.TabIndex = 1;
            label2.Text = "Magasság (m):";
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(9, 34);
            label1.Name = "label1";
            label1.Size = new Size(103, 20);
            label1.TabIndex = 0;
            label1.Text = "Szélesség (m):";
            // 
            // groupBox1
            // 
            groupBox1.Controls.Add(lstSpecialTools);
            groupBox1.Dock = DockStyle.Fill;
            groupBox1.Location = new Point(3, 220);
            groupBox1.Name = "groupBox1";
            groupBox1.Size = new Size(288, 105);
            groupBox1.TabIndex = 1;
            groupBox1.TabStop = false;
            groupBox1.Text = "Szerkesztő eszköztár";
            // 
            // lstSpecialTools
            // 
            lstSpecialTools.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            lstSpecialTools.FormattingEnabled = true;
            lstSpecialTools.Location = new Point(6, 35);
            lstSpecialTools.Name = "lstSpecialTools";
            lstSpecialTools.Size = new Size(276, 64);
            lstSpecialTools.TabIndex = 1;
            lstSpecialTools.SelectedIndexChanged += lstSpecialTools_SelectedIndexChanged;
            // 
            // lstTools
            // 
            lstTools.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            lstTools.FormattingEnabled = true;
            lstTools.Location = new Point(6, 26);
            lstTools.Name = "lstTools";
            lstTools.Size = new Size(276, 304);
            lstTools.TabIndex = 0;
            lstTools.SelectedIndexChanged += lstTools_SelectedIndexChanged;
            // 
            // groupBox2
            // 
            groupBox2.Controls.Add(btnExport);
            groupBox2.Dock = DockStyle.Fill;
            groupBox2.Location = new Point(3, 671);
            groupBox2.Name = "groupBox2";
            groupBox2.Size = new Size(288, 84);
            groupBox2.TabIndex = 2;
            groupBox2.TabStop = false;
            groupBox2.Text = "Műveletek";
            // 
            // btnExport
            // 
            btnExport.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            btnExport.Location = new Point(154, 24);
            btnExport.Name = "btnExport";
            btnExport.Size = new Size(128, 51);
            btnExport.TabIndex = 7;
            btnExport.Text = "CSV Export";
            btnExport.UseVisualStyleBackColor = true;
            btnExport.Click += btnExport_Click;
            // 
            // canvasPanel
            // 
            canvasPanel.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            canvasPanel.BackColor = Color.White;
            canvasPanel.BorderStyle = BorderStyle.FixedSingle;
            canvasPanel.Location = new Point(17, 12);
            canvasPanel.Name = "canvasPanel";
            canvasPanel.Size = new Size(936, 734);
            canvasPanel.TabIndex = 0;
            canvasPanel.Paint += canvasPanel_Paint;
            canvasPanel.MouseClick += canvasPanel_MouseClick;
            // 
            // groupBox3
            // 
            groupBox3.Controls.Add(lstTools);
            groupBox3.Dock = DockStyle.Fill;
            groupBox3.Location = new Point(3, 331);
            groupBox3.Name = "groupBox3";
            groupBox3.Size = new Size(288, 334);
            groupBox3.TabIndex = 3;
            groupBox3.TabStop = false;
            groupBox3.Text = "Eszközlista";
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1263, 758);
            Controls.Add(splitContainer1);
            Name = "Form1";
            Text = "EML Predictor - Room Layout editor";
            Load += Form1_Load;
            splitContainer1.Panel1.ResumeLayout(false);
            splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)splitContainer1).EndInit();
            splitContainer1.ResumeLayout(false);
            tableLayoutPanel1.ResumeLayout(false);
            RoomSettings.ResumeLayout(false);
            RoomSettings.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)numHeight).EndInit();
            ((System.ComponentModel.ISupportInitialize)numWidth).EndInit();
            groupBox1.ResumeLayout(false);
            groupBox2.ResumeLayout(false);
            groupBox3.ResumeLayout(false);
            ResumeLayout(false);
        }

        #endregion

        private SplitContainer splitContainer1;
        private TableLayoutPanel tableLayoutPanel1;
        private GroupBox RoomSettings;
        private Label label2;
        private Label label1;
        private ComboBox cmbGrid;
        private Label label3;
        private NumericUpDown numHeight;
        private NumericUpDown numWidth;
        private Button btnGenerate;
        private GroupBox groupBox1;
        private GroupBox groupBox2;
        private Button btnExport;
        private ListBox lstTools;
        private Panel canvasPanel;
        private SaveFileDialog saveFileDialog1;
        private ListBox lstSpecialTools;
        private GroupBox groupBox3;
    }
}
