using GMap.NET.WindowsPresentation;
using System.Windows;
using System.Windows.Controls;


namespace usstgui
{
    /// <summary>
    /// Interaction logic for WaypointMarker.xaml
    /// </summary>
    public partial class WaypointMarker : UserControl
    {
        Label Label;
        GMapMarker Marker;
        public int offesetX = -15;
        public int offsetY = -30;

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
