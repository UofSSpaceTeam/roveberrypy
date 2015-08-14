using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace usstgui
{
    public partial class DrillStatus : Window
    {
        public DrillStatus()
        {
            InitializeComponent();
        }

        private void feedSet(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            SharedState.set("drillTranslation", DrillFeed.Value);
        }

		private void feedStop(object sender, MouseEventArgs e)
		{
			SharedState.set("drillTranslation", 0.0);
			this.Dispatcher.Invoke((Action)(() => { DrillFeed.Value = 0.0; }));
		}

		private void drillSet(object sender, RoutedPropertyChangedEventArgs<double> e)
		{
			if((bool)Cw.IsChecked)
				SharedState.set("drillRotation", DrillSpeed.Value);
			else if ((bool)Ccw.IsChecked)
				SharedState.set("drillRotation", -DrillSpeed.Value);
			else
				drillStop(null, null);
		}

		private void drillStop(object sender, RoutedEventArgs e)
		{
			SharedState.set("drillRotation", 0.0);
			this.Dispatcher.Invoke((Action)(() => { DrillSpeed.Value = 0.0; }));
		}		
	}
}
