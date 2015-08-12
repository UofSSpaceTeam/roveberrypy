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
        readonly MjpegDecoder _mjpeg;

        public VideoConfig()
        {
            InitializeComponent();
            _mjpeg = new MjpegDecoder();
            _mjpeg.FrameReady += mjpeg_FrameReady;
            _mjpeg.Error += _mjpeg_Error;
        }

        private void Start_Click(object sender, RoutedEventArgs e)
        {
            _mjpeg.ParseStream(new Uri("http://webcam.sonoma.edu/mjpg/video.mjpg"));
        }

        private void mjpeg_FrameReady(object sender, FrameReadyEventArgs e)
        {
            image.Source = e.BitmapImage;
        }

        void _mjpeg_Error(object sender, ErrorEventArgs e)
        {
            MessageBox.Show(e.Message);
        }
    }
}
