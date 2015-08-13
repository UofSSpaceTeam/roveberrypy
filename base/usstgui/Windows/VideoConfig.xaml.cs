using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using MjpegProcessor;

namespace usstgui
{
    /// <summary>
    /// Interaction logic for VideoConfig.xaml
    /// </summary>
    public partial class VideoConfig : Window
    {
        readonly MjpegDecoder VideoFb;

        public VideoConfig()
        {
            InitializeComponent();
            VideoFb = new MjpegDecoder();
            VideoFb.FrameReady += mjpeg_FrameReady;
            VideoFb.Error += _mjpeg_Error;
        }

        private void startStream(object sender, RoutedEventArgs e)
        {
            Button pressed = (Button)sender;
            StateManager.setShared(pressed.Name, "start");
            VideoFb.ParseStream(new Uri("http://192.168.1.103:40000/?action=stream"));
            
        }

        private void stopStream(object sender, RoutedEventArgs e)
        {
            VideoFb.StopStream();
            Button pressed = (Button)sender;
            StateManager.setShared("StopVideo", "all");
            BitmapImage image = new BitmapImage(new Uri("../Resources/noStream.jpg", UriKind.Relative));
            VideoCanvas.Source = image;
        }

        private void mjpeg_FrameReady(object sender, FrameReadyEventArgs e)
        {
            VideoCanvas.Source = e.BitmapImage;
        }

        void _mjpeg_Error(object sender, ErrorEventArgs e)
        {
            MessageBox.Show(e.Message);
        }
    }
}
