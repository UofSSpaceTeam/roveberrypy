using System;
using System.Collections.Generic;
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
    /// Interaction logic for DrillConfig.xaml
    /// </summary>
    public partial class DrillConfig : Window
    {
        public DrillConfig()
        {
            InitializeComponent();
        }

        private void drillCw(object sender, RoutedEventArgs e)
        {
            StateManager.setShared("drillCw", true.ToString());
            StateManager.setShared("drillCcw", false.ToString());
        }

        private void drillCcw(object sender, RoutedEventArgs e)
        {
            StateManager.setShared("drillCw", false.ToString());
            StateManager.setShared("drillCcw", true.ToString());
        }

        private void buttonTouch(object sender, MouseButtonEventArgs e)
        {
            Button pressed = (Button)sender;
            StateManager.setShared(pressed.Name, (e.ButtonState == MouseButtonState.Pressed).ToString());
        }

        private void sliderChanged(object sender,RoutedPropertyChangedEventArgs<double> e)
        {
            Slider slider = (Slider)sender;
            StateManager.setShared(slider.Name, slider.Value);
        }
    }
}
