using System.Windows;
using SharpDX.XInput;
using System;
using System.Threading;

namespace usstgui
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public Gamepad xbox;
        Controller controller;
        double scale = 1;
        private bool running = true;
        private int xinversion = 1;
        private int yinversion = 1;
        public MainWindow()
        {
            controller = new SharpDX.XInput.Controller(SharpDX.XInput.UserIndex.One);
            InitializeComponent();
            Thread t = new Thread(new ThreadStart(XboxController));
            t.Start();

            //this.OnClosing += Cleanup;
        }
        protected override void OnClosing(System.ComponentModel.CancelEventArgs e)
        {
            Cleanup();
            base.OnClosing(e);
        }

        protected void Cleanup()
        {
            running = false;
        }

        private void XboxController()
        {
            double x;
            double y;
            try
            {
                while(running)
                {
                    xbox = controller.GetState().Gamepad;
                    y = (-2 + (xbox.LeftThumbY - (-32768)) * (2 + 2) / (32767 + 32768))*scale*yinversion;
                    x = (-2 + (xbox.LeftThumbX - (-32768)) * (2 + 2) / (32767 + 32768))*scale*xinversion;
                    Console.WriteLine("Y = " + y);
                    Console.WriteLine("X = " +x);
                    Thread.Sleep(1000);
                }
            }
            catch (Exception ex)
            {
                Console.Write(ex);
            }
        }
        private void InvertX_Checked(object sender, RoutedEventArgs e)
        {
            xinversion = xinversion * (-1);

        }

        private void InvertY_Checked(object sender, RoutedEventArgs e)
        {
            yinversion = yinversion * (-1);
        }

        private void slider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            scale = scaler.Value;
        }
    }
}
