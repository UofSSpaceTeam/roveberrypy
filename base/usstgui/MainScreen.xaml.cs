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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace usstgui
{
    /// <summary>
    /// Interaction logic for Window1.xaml
    /// </summary>
    public partial class Window1 : Window
    {
        public Window1()
        {
            InitializeComponent();
            OptionsController1.Tag = new OptionsController1();

        }

        private void OpenConfigWindow(object sender, RoutedEventArgs e)
        {
            // Can this be simplified? I couldn't see anything to fix it
            Button pressedConfigButton = (Button)sender;
            string target = pressedConfigButton.Name;

            if(target == "OptionsController1")
            {
                Window newWindow = new OptionsController1();
                newWindow.Show();
            }

            if(target == "ArmConfig")
            {
                Window newWindow = new ArmConfig();
                newWindow.Show();
            }
            

        }
    }
}
