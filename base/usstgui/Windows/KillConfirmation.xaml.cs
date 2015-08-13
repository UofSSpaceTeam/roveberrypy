using System;
using System.Windows;
using System.Windows.Controls;

namespace usstgui
{
    public partial class KillConfirmation : Window
    {
		public KillConfirmation()
        {
            InitializeComponent();
        }

		private void CloseWindow(object sender, RoutedEventArgs e)
		{
			this.Close();
		}

        private void KillApplication(object sender, RoutedEventArgs e)
        {
			try
			{
				Environment.Exit(0);
			}
			catch(Exception ex){}
        }
    }
}
