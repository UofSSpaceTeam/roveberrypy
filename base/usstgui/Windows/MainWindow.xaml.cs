using System;
using System.Windows;
using System.Windows.Controls;
using System.Diagnostics;
using System.Threading;
using System.Windows.Media;

namespace usstgui
{
    public partial class MainWindow : Window
    {
        public MainWindow()
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
			Color alive = Colors.LightGreen;
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
			if(SharedState.get(key) == true)
				this.Dispatcher.Invoke((Action)(() => { button.Background = new SolidColorBrush(alive); }));
			else
				this.Dispatcher.Invoke((Action)(() => { button.Background = new SolidColorBrush(dead); }));
			SharedState.set(key, false);
		}
    }
}
