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
using Vlc.DotNet.Core;
using Vlc.DotNet.Wpf;

namespace usstgui.Tasks
{
    /// <summary>
    /// Interaction logic for VideoConfig.xaml
    /// </summary>
    public partial class VideoConfig : Window
    {
        public VideoConfig()
        {
            VlcContext.LibVlcDllsPath = CommonStrings.LIBVLC_DLLS_PATH_DEFAULT_VALUE_AMD64;
            VlcContext.LibVlcPluginsPath = CommonStrings.PLUGINS_PATH_DEFAULT_VALUE_AMD64;

            VlcContext.StartupOptions.IgnoreConfig = true;

            VlcContext.Initialize();

            InitializeComponent();

            var vlcPlayer = new VlcControl();
            var media = new LocationMedia("rtsp://admin:12345@192.168.42.200:554/MediaInput/h264");

            Grid1.Children.Add(vlcPlayer);

            var vlcBinding = new Binding("VideoSource");
            vlcBinding.Source = vlcPlayer;

            var vImage = new Image();
            vImage.SetBinding(Image.SourceProperty, vlcBinding);

            var vBrush = new VisualBrush();
            vBrush.TileMode = TileMode.None;
            vBrush.Stretch = Stretch.Uniform;
            vBrush.Visual = vImage;

            Grid1.Background = vBrush;

            vlcPlayer.Play();

        }

    }
}
