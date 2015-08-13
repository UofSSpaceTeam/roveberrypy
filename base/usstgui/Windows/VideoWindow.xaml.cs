using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;
using MjpegProcessor;

namespace usstgui
{
    public partial class VideoWindow : Window
    {
        readonly MjpegDecoder VideoFb = new MjpegDecoder();

        public VideoWindow()
        {
            InitializeComponent();
            VideoFb.FrameReady += mjpeg_FrameReady;
            VideoFb.Error += _mjpeg_Error;
			stopStream(null, null);
        }

		private Uri getCameraUri()
		{
			return new Uri("http://" + SharedState.get("roverIP") + ":" +
				SharedState.get("cameraPort").ToString() + "/?action=stream");
		}

        private void startStream(object sender, RoutedEventArgs e)
        {
			SharedState.set("videoState", "start" + ((Button)sender).Name);
			VideoFb.ParseStream(getCameraUri());
        }

        private void stopStream(object sender, RoutedEventArgs e)
        {
            VideoFb.StopStream();
            SharedState.set("videoState", "stop");
            BitmapImage image = new BitmapImage(new Uri("../Resources/noStream.jpg", UriKind.Relative));
            VideoCanvas.Source = image;
        }

        private void mjpeg_FrameReady(object sender, FrameReadyEventArgs e)
        {
            VideoCanvas.Source = e.BitmapImage;
        }

        void _mjpeg_Error(object sender, ErrorEventArgs e)
        {
			if(this.IsActive)
			{
				MessageBox.Show(this, e.Message, "Video Error");
			}
        }
    }
}
