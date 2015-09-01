using GMap.NET.WindowsPresentation;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace usstgui
{
    /// <summary>
    /// Interaction logic for RoverMarker.xaml
    /// </summary>
    public partial class RoverMarker : UserControl
    {
        Label Label;
        GMapMarker Marker;
        double angle;
        public int offesetX = -16;
        public int offsetY = -18;

        public RoverMarker(GMapMarker marker, string title)
        {
            InitializeComponent();

            this.Marker = marker;
            Label = new Label();

            this.Loaded += new RoutedEventHandler(Marker_Loaded);
        }

        private void Marker_Loaded(object sender, RoutedEventArgs e)
        {
            if (icon.Source.CanFreeze)
            {
                icon.Source.Freeze();
            }
        }

        public void MarkerArrowHeading(double setAngle)
        {
            this.angle = setAngle;

            RotateTransform imgRotate = (RotateTransform)arrow.RenderTransform;
            imgRotate.Angle = setAngle;
        }
    }
}