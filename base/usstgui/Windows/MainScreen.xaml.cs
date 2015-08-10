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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace usstgui
{
    /// <summary>
    /// Interaction logic for Window1.xaml
    /// </summary>
    public partial class MainScreen : Window
    {
        public MainScreen()
        {
            InitializeComponent();
        }

		protected override void OnClosing(System.ComponentModel.CancelEventArgs e)
		{
			e.Cancel = true;
			OpenWindow(KillConfirmation, null);
		}

		private void OpenWindow(object sender, RoutedEventArgs e)
		{
			try
			{
				((Window)Activator.CreateInstance(null, "usstgui." + ((Button)sender).Name).Unwrap()).Show();
			}
			catch(Exception ex)
			{
				Debug.WriteLine("Couldn't open window: " + ex.Message);
			}
		}

        private void KillAll(object sender, RoutedEventArgs e)
        {
            Environment.Exit(0);
        }
    }
}
