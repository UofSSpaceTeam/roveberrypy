using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace usstgui
{
    /// <summary>
    /// Interaction logic for ArmConfig.xaml
    /// </summary>
    public partial class ArmConfig : Window
    {
        public ArmConfig()
        {
            InitializeComponent();
        }

        private void slider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            Slider test = (Slider)sender;
            Debug.WriteLine(test.Value);
        }
    }
}
