using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Room_layout_EM_load
{
    public class GridCell
    {
        public bool IsWall { get; set; }
        public List<string> Items { get; set; } = new List<string>();
    }
}
