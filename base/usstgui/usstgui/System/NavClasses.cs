using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GMap.NET.WindowsPresentation;

namespace usstgui
{
    public class GeoAngle
    {
        public bool IsNegative { get; set; }
        public int Degrees { get; set; }
        public int Minutes { get; set; }
        public int Seconds { get; set; }
        public int Milliseconds { get; set; }
        public double DecimalDegrees { get; set; }
        public double DecimalMinutes { get; set; }

        public static GeoAngle FromDouble(double angleInDegrees)
        {
            //ensure the value will fall within the primary range [-180.0..+180.0]
            while (angleInDegrees < -180.0)
                angleInDegrees += 360.0;

            while (angleInDegrees > 180.0)
                angleInDegrees -= 360.0;

            var result = new GeoAngle();

            //gets decimal degrees
            result.DecimalDegrees = Math.Round(angleInDegrees, 8);

            //gets decimal minutes
            result.DecimalMinutes = Math.Round((angleInDegrees - Math.Truncate(angleInDegrees)) * 60, 8);

            //switch the value to positive for further calcs
            result.IsNegative = angleInDegrees < 0;
            angleInDegrees = Math.Abs(angleInDegrees);

            //gets the degree
            result.Degrees = (int)Math.Floor(angleInDegrees);
            var delta = angleInDegrees - result.Degrees;

            //gets minutes and seconds
            var seconds = (int)Math.Floor(3600.0 * delta);
            result.Seconds = seconds % 60;
            result.Minutes = (int)Math.Floor(seconds / 60.0);
            delta = delta * 3600.0 - seconds;

            //gets fractions
            result.Milliseconds = (int)(10000.0 * delta);


            return result;
        }

        public static GeoAngle FromDMS(string angleInDMS)
        {
            string[] angle = angleInDMS.Split(null);
            int degrees = Convert.ToInt32(angle[0]);
            int minutes = Convert.ToInt32(angle[1]);
            double seconds = Convert.ToDouble(angle[2]);

            double angleInDegrees = degrees + (minutes / 60) + (seconds / 3600);

            return GeoAngle.FromDouble(angleInDegrees);
        }
        
        public static GeoAngle FromDMD(string angleInDMD)
        {
            string[] angle = angleInDMD.Split(null);
            int degrees = Convert.ToInt32(angle[0]);
            double minutes = Convert.ToDouble(angle[1]);

            double angleInDegrees = degrees + (minutes / 60);
            return GeoAngle.FromDouble(angleInDegrees);
        }

        public static GeoAngle FromDD(string angleInDD)
        {
            System.Diagnostics.Debug.WriteLine(Convert.ToDouble(angleInDD));
            return GeoAngle.FromDouble(Convert.ToDouble(angleInDD));
        }
        
        public override string ToString()
        {
            var degrees = this.IsNegative
                ? -this.Degrees
                : this.Degrees;

            return string.Format(
                "{0}° {1:00}' {2:00}\"",
                degrees,
                this.Minutes,
                this.Seconds);
        }

        public string ToString(string format)
        {
            switch (format)
            {
                case "DMSNS":
                    return string.Format(
                        "{0}° {1:00}' {2:00}\".{3:0000} {4}",
                        this.Degrees,
                        this.Minutes,
                        this.Seconds,
                        this.Milliseconds,
                        this.IsNegative ? 'S' : 'N');

                case "DMSWE":
                    return string.Format(
                        "{0}° {1:00}' {2:00}\".{3:0000} {4}",
                        this.Degrees,
                        this.Minutes,
                        this.Seconds,
                        this.Milliseconds,
                        this.IsNegative ? 'W' : 'E');

                case "DDNS":
                    return string.Format(
                        "{0}° {1}",
                        this.DecimalDegrees,
                        this.IsNegative ? 'S' : 'N');

                case "DDWE":
                    return string.Format(
                        "{0}° {1}",
                        this.DecimalDegrees,
                        this.IsNegative ? 'W' : 'E');

                case "DMDNS":
                    return string.Format(
                        "{0}° {1}' {2}",
                        this.Degrees,
                        this.DecimalMinutes,
                        this.IsNegative ? 'S' : 'N');

                case "DMDWE":
                    return string.Format(
                        "{0}° {1}' {2}",
                        this.Degrees,
                        this.DecimalMinutes,
                        this.IsNegative ? 'W' : 'E');

                default:
                    throw new NotImplementedException();
            }
        }
    }

    public class WaypointStorage
    {
        public GeoAngle Lat { get; set; }
        public GeoAngle Lng { get; set; }
        public string Name { get; set; }
        public string JsonString { get; set; }
        public GMapMarker Marker { get; set; }

        public static WaypointStorage FromStrings(string name, string lat, string lng, string type)
        {
            WaypointStorage result = new WaypointStorage();

            if(type == "DD")
            {
                result.Lat = GeoAngle.FromDD(lat);
                result.Lng = GeoAngle.FromDD(lng);
                
            }

            if(type == "DMS")
            {
                result.Lat = GeoAngle.FromDMS(lat);
                result.Lng = GeoAngle.FromDMS(lng);
            }

            if(type == "DMD")
            {
                result.Lat = GeoAngle.FromDMD(lat);
                result.Lng = GeoAngle.FromDMD(lng);
            }

            result.Name = name;
            result.Marker = null;

            return result;

        }

        public override string ToString()
        {
            return this.Name;
        }

        public void UpdatePosDD(double lat, double lon)
        {
            this.Lat = GeoAngle.FromDouble(lat);
            this.Lng = GeoAngle.FromDouble(lon);
        }


    }
}
