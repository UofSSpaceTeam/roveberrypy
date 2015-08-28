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
using usstgui.Windows;
using System.Collections.Generic;
using usstgui.NavMarkers;

namespace usstgui
{
    public partial class NavStatus : Window
    {
        public NavStatus()
        {
            InitializeComponent();

            if (!PingNetwork("pingtest.com"))
            {
                MainMap.Manager.Mode = AccessMode.CacheOnly;
                MessageBox.Show("No internet connection available, going to CacheOnly mode.");
            }

            MainMap.MapProvider = GMapProviders.BingHybridMap;
            MainMap.Position = new PointLatLng(52.132452, -106.628350);

           
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

                // Memory leaks galore.. doesn't really matter though :P
                WaypointStorage point = new WaypointStorage();
                point = WaypointStorage.FromStrings(Name, Lat, Lng, mode);
                ListViewItem item = new ListViewItem();
                item.Tag = point;
                PointsList.Items.Add(point);

                Debug.WriteLine(point.Lng.DecimalDegrees);

                PointLatLng enteredPosition = new PointLatLng(point.Lat.DecimalDegrees, point.Lng.DecimalDegrees);

                GMapMarker marker = new GMapMarker(enteredPosition);
                marker.Shape = new WaypointMarker(marker, Name);
                marker.Offset = new Point(-15, -30);
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


    }
}
