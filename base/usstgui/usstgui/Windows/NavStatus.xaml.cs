using System;
using System.Windows;
using System.Windows.Controls;
using System.Text;
using GMap.NET;
using GMap.NET.MapProviders;
using GMap.NET.WindowsPresentation;
using GMap.NET.Internals;
using GMap.NET.Projections;
using GMap.NET.CacheProviders;
using System.Net.NetworkInformation;
using System.Diagnostics;
using usstgui;
using System.Collections.Generic;
using System.Threading;

namespace usstgui
{
    public partial class NavStatus : Window
    {
        bool windowOpen = true;
        bool NMEA = true;
        public NavStatus()
        {
            InitializeComponent();
            Thread t = new Thread(new ThreadStart(NavDataMonitor));
            t.Start();

            if (!PingNetwork("pingtest.com"))
            {
                MainMap.Manager.Mode = AccessMode.CacheOnly;
                MessageBox.Show("No internet connection available, going to CacheOnly mode.");
            }

            MainMap.MapProvider = GMapProviders.OpenStreetMap;
            MainMap.Position = new PointLatLng(52.132452, -106.628350);
            
            // Add rover icon to list
            WaypointStorage roverLocation = new WaypointStorage();
            roverLocation = WaypointStorage.FromStrings("Rover", "52.132452", "-106.628350", "DD");
            ListViewItem item = new ListViewItem();
            item.Tag = roverLocation;
            PointsList.Items.Add(roverLocation);

            // Add to map
            PointLatLng initPosition = new PointLatLng(roverLocation.Lat.DecimalDegrees, roverLocation.Lng.DecimalDegrees); //Format for maps
            GMapMarker roverMarker = new GMapMarker(initPosition);
            RoverMarker roverIcon = new RoverMarker(roverMarker, "Rover");
            roverMarker.Shape = roverIcon;
            roverMarker.Offset = new Point(roverIcon.offesetX, roverIcon.offsetY);
            roverMarker.ZIndex = 1;
            MainMap.Markers.Add(roverMarker);
            roverLocation.Marker = roverMarker;


            // Test
            UpdateRoverPosition(20, 20, 49);

        }
        
        private void NavDataMonitor()
        {
            while (windowOpen)
            {
                this.Dispatcher.Invoke((Action)(() =>
                {
                    double lat = 0;
					double lng = 0;
					double hdg = 0;
				    if(NMEA)
				    {
						SharedState.set("gps_NMEA", "");
                        try { lat = Convert.ToDouble(SharedState.get("NMEAlat")); } catch { Debug.WriteLine("failed lat"); }
                        try { lng = Convert.ToDouble(SharedState.get("NMEA_lng")); } catch { Debug.WriteLine("failed lng"); }
                        try { hdg = Convert.ToDouble(SharedState.get("NMEA_hdg")); } catch { Debug.WriteLine("failed hdg"); }
				    }
					else
					{
						SharedState.set("gps_pos_lat", "");
						try { lat = Convert.ToDouble(SharedState.get("lattitude")); } catch { Debug.WriteLine("failed lat"); }

						SharedState.set("gps_pos_lon", "");
						try { lng = Convert.ToDouble(SharedState.get("longitude")); } catch { Debug.WriteLine("failed lng"); }

						SharedState.set("gps_heading", "");
						try { hdg = Convert.ToDouble(SharedState.get("heading")); } catch { Debug.WriteLine("failed hdg"); }
	
					}
					UpdateRoverPosition(lat, lng, hdg);
					Debug.WriteLine("GPS Update Passed");
                }));
                Thread.Sleep(500);
            }
        }

        //Kinda dumb helper to check if connected.. could be better?
        public static bool PingNetwork(string hostNameOrAddress)
        {
            bool pingStatus = false;

            using (Ping p = new Ping())
            {
                byte[] buffer = Encoding.ASCII.GetBytes("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
                int timeout = 4444; // 4s

                try
                {
                    PingReply reply = p.Send(hostNameOrAddress, timeout, buffer);
                    pingStatus = (reply.Status == IPStatus.Success);
                }
                catch (Exception)
                {
                    pingStatus = false;
                }
            }

            return pingStatus;
        }

        protected override void OnClosing(System.ComponentModel.CancelEventArgs e)
        {
            windowOpen = false;
            base.OnClosing(e);
        }

        // Map manipulation stuff
        private void ZoomSliderChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            Slider slider = (Slider)sender;
            MainMap.Zoom = slider.Value;
        }

        private void MainMap_OnMapZoomChanged()
        {
            ZoomSlider.Value = MainMap.Zoom;
        }

        private void MainMap_OnPositionChanged(PointLatLng point)
        {
            GeoAngle geoLat = new GeoAngle();
            geoLat = GeoAngle.FromDouble(point.Lat);

            GeoAngle geoLng = new GeoAngle();
            geoLng = GeoAngle.FromDouble(point.Lng);

            string output = geoLat.ToString("DDNS") + ", " + geoLng.ToString("DDWE");
            DDLabel.Content = "DD: " + output;

            output = geoLat.ToString("DMSNS") + ", " + geoLng.ToString("DMSWE");
            DMSLabel.Content = "DMS: " + output;

            output = geoLat.ToString("DMDNS") + ", " + geoLng.ToString("DMDWE");
            DMDLabel.Content = "DMD: " + output;
        }

        // Data Management
        private void AddPt_Click(object sender, RoutedEventArgs e)
        {
            try {
                string Name = NameBox.Text;
                string Lat = LatBox.Text;
                string Lng = LngBox.Text;
                string mode;

                if ((bool)SelectDD.IsChecked)
                {
                    mode = "DD";
                }
                else if ((bool)SelectDMS.IsChecked)
                {
                    mode = "DMS";
                }
                else if ((bool)SelectDMD.IsChecked)
                {
                    mode = "DMD";
                }
                else return;
                
                WaypointStorage point = new WaypointStorage();
                point = WaypointStorage.FromStrings(Name, Lat, Lng, mode);
                ListViewItem item = new ListViewItem();
                item.Tag = point;
                PointsList.Items.Add(point);
                
                PointLatLng enteredPosition = new PointLatLng(point.Lat.DecimalDegrees, point.Lng.DecimalDegrees);
                 
                GMapMarker marker = new GMapMarker(enteredPosition);
                WaypointMarker icon = new WaypointMarker(marker, Name);
                marker.Shape = icon;
                marker.Offset = new Point(icon.offesetX, icon.offsetY);
                marker.ZIndex = 1;
                MainMap.Markers.Add(marker);
                point.Marker = marker;

            }
            catch
            {
                MessageBox.Show("Hold on Cowboy!\n\nMust be in format D M S etc...");
                return;
            }
        }

        private void PtHere_Click(object sender, RoutedEventArgs e)
        {
            PointLatLng point = MainMap.Position;
            LatBox.Text = point.Lat.ToString();
            LngBox.Text = point.Lng.ToString();
            SelectDD.IsChecked = true;
        }

        // Visualization
        // Helpers for Haversine formula
        private static double ToRadian(double val) { return val * (Math.PI / 180); }
        private static double DiffRadian(double val1, double val2) { return ToRadian(val2) - ToRadian(val1); }

        public static string GetDelta(GeoAngle[] A, GeoAngle[] B)
        {
            double EarthRadius = 6364843; // meters in poland

            double lat1 = A[0].DecimalDegrees;
            double lat2 = B[0].DecimalDegrees;

            double lng1 = A[1].DecimalDegrees;
            double lng2 = B[1].DecimalDegrees;

            return (EarthRadius * 2 * Math.Asin(Math.Min(1, Math.Sqrt((Math.Pow(Math.Sin((DiffRadian(lat1, lat2)) / 2.0), 2.0)
                + Math.Cos(ToRadian(lat1)) * Math.Cos(ToRadian(lat2)) * Math.Pow(Math.Sin((DiffRadian(lng1, lng2)) / 2.0), 2.0)))))).ToString();
        }

        public void UpdateRoverPosition(double lat, double lng, double hdg)
        {
            WaypointStorage rover = PointsList.Items.GetItemAt(0) as WaypointStorage;
            RoverMarker roverIcon = rover.Marker.Shape as RoverMarker;
            roverIcon.MarkerArrowHeading(hdg);
            rover.UpdatePosDD(lat, lng);
            rover.Marker.Position = new PointLatLng(rover.Lat.DecimalDegrees, rover.Lng.DecimalDegrees);
        }

        private void CenterMap_Click(object sender, RoutedEventArgs e)
        {
            WaypointStorage rover = PointsList.Items.GetItemAt(0) as WaypointStorage;
            MainMap.Position = new PointLatLng(rover.Lat.DecimalDegrees, rover.Lng.DecimalDegrees);
        }

        private void radioButton1_Checked(object sender, RoutedEventArgs e)
        {

        }

        private void GPSMode_Checked(object sender, RoutedEventArgs e)
        {
            RadioButton selected = sender as RadioButton;
            if(selected.Name == "SelectSBP")
            {
                NMEA = false;
                Debug.WriteLine("RTK GPS Enabled");
            }
            else
            {
                NMEA = true;
                Debug.WriteLine("NMEA GPS Enabled");
            }
        }
    }
}
