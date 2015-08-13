using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
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
    public partial class MainScreen : Window
    {
        public MainScreen()
        {
            InitializeComponent();
			new Thread(new ThreadStart(HeartbeatMonitor)).Start();
        }

		protected override void OnClosing(System.ComponentModel.CancelEventArgs e)
		{
			e.Cancel = true;
			new KillConfirmation().Show();
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

		private void HeartbeatMonitor()
		{
			Color alive = Colors.AliceBlue;
			Color dead = Colors.Coral;
			while(true)
			{
				processHeartbeat("commsHeartbeat", CommsStatus, alive, dead);
				processHeartbeat("driveHeartbeat", DriveStatus, alive, dead);
				processHeartbeat("armHeartbeat", ArmStatus, alive, dead);
				processHeartbeat("drillHeartbeat", DrillStatus, alive, dead);
				processHeartbeat("gpsHeartbeat", GpsStatus, alive, dead);
				processHeartbeat("lidarHeartbeat", LidarStatus, alive, dead);
				processHeartbeat("controller1Heartbeat", Controller1Status, alive, dead);
				processHeartbeat("controller2Heartbeat", Controller2Status, alive, dead);
				Thread.Sleep(2000);
			}
		}

		private void processHeartbeat(string key, Button button, Color alive, Color dead)
		{
			if(StateManager.getShared(key) == true)
				this.Dispatcher.Invoke((Action)(() => { button.Background = new SolidColorBrush(alive); }));
			else
				this.Dispatcher.Invoke((Action)(() => { button.Background = new SolidColorBrush(dead); }));
			StateManager.setShared(key, false);
		}
    }
}
