using GMap.NET.WindowsPresentation;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using usstgui.Windows;

namespace usstgui.NavMarkers
{
    /// <summary>
    /// Interaction logic for WaypointMarker.xaml
    /// </summary>
    public partial class WaypointMarker : UserControl
    {
        Label Label;
        GMapMarker Marker;

        public WaypointMarker(GMapMarker marker, string title)
        {
            InitializeComponent();

            this.Marker = marker;
            Label = new Label();

            this.Loaded += new RoutedEventHandler(Marker_Loaded);
        }

        void Marker_Loaded(object sender, RoutedEventArgs e)
        {
            if (icon.Source.CanFreeze)
            {
                icon.Source.Freeze();
            }
        }
    }
}
