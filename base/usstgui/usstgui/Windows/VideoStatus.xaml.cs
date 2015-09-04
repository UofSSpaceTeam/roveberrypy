using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media.Imaging;
using MjpegProcessor;
using System.Threading;

namespace usstgui
{
    public partial class VideoStatus : Window
    {
        readonly MjpegDecoder VideoFb = new MjpegDecoder();

        public VideoStatus()
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
            SharedState.set("fps", fps.Text);
            SharedState.set("resX", resX.Text);
            SharedState.set("resY", resY.Text);
            SharedState.set("videoState", "start" + ((Button)sender).Name);
            Thread.Sleep(10000);
            VideoFb.ParseStream(getCameraUri());
        }

        private void stopStream(object sender, RoutedEventArgs e)
        {
            VideoFb.StopStream();
            SharedState.set("videoState", "stop");
            BitmapImage image = new BitmapImage(new Uri("../Resources/noStream.jpg", UriKind.Relative));
            VideoCanvas.Source = image;
        }

        private void CamCtl(object sender, RoutedEventArgs e)
        {
            Button pressed = (Button)sender;
            SharedState.set(pressed.Name, "Step");
        }

        private void TakePicture(object sender, RoutedEventArgs e)
        {
            string url = @"http://192.168.1.103:40000/?action=snapshot";
            //string file = System.IO.Path.GetFileName(url);
            System.Net.WebClient cln = new System.Net.WebClient();

            Microsoft.Win32.SaveFileDialog dlg = new Microsoft.Win32.SaveFileDialog();
            dlg.FileName = "Picture"; // Default file name
            dlg.DefaultExt = ".jpg"; // Default file extension

            // Show save file dialog box
            bool? result = dlg.ShowDialog();

            // Process save file dialog box results
            if(result == true)
            {
                // Save document
                string filename = dlg.FileName;
                cln.DownloadFile(url, filename);
            }
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
