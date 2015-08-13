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

        private void drillForward(object sender, RoutedEventArgs e)
        {
			SharedState.set("drillRotation", "forward");
        }

		private void drillReverse(object sender, RoutedEventArgs e)
		{
			SharedState.set("drillRotation", "reverse");
		}

		private void feedUp(object sender, RoutedEventArgs e)
		{
			SharedState.set("drillTranslation", "forward");
		}

		private void feedDown(object sender, RoutedEventArgs e)
		{
			SharedState.set("drillTranslation", "reverse");
		}

        private void feedSet(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            SharedState.set("DrillFeedPower", ((Slider)sender).Value);
        }

		private void drillSet(object sender, RoutedPropertyChangedEventArgs<double> e)
		{
			SharedState.set("DrillPower", ((Slider)sender).Value);
		}

		private void feedStop(object sender, MouseButtonEventArgs e)
		{
			SharedState.set("DrillFeedPower", 0.0);
		}

	}
}
