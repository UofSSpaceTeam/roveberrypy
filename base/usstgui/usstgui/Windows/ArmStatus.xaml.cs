using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Threading;
using System.Diagnostics;
using System.Windows.Media;
using System.Windows.Shapes;

namespace usstgui
{
    public partial class ArmStatus : Window
    {

        public ArmStatus()
        {
            InitializeComponent();
            m_stepSize = 10;
        }

        private void updateArmLimits()
        {
            int xCur, yCur;
            int xMin, xMax, yMin, yMax;
            float xNorm, yNorm;
            string xLbl, yLbl;

            xCur = Convert.ToInt32(IK_XVal.Text);
            yCur = Convert.ToInt32(IK_YVal.Text);

            yMin = -232;
            yMax = 655;
            
            double z = yCur;

            double max_radius = 1718.0 * Math.Sin(0.004439 * z + 0.4935) + 1817.0 * Math.Sin(0.006403 * z + 3.064) + 728.2 * Math.Sin(0.007664 * z - 0.4486);
            double min_radius;
            if (z > 204)
            {
                min_radius = 415.4 * Math.Sin(0.002591 * z + 0.4629);
            }
            else
            {
                min_radius = 364.8 * Math.Sin(0.003055 * z + 1.303);
            }

            xMax = Convert.ToInt32(max_radius);
            xMin = Convert.ToInt32(min_radius);


            xNorm = (float)(xCur - xMin) / (xMax - xMin);
            yNorm = (float)(yCur - yMin) / (yMax - yMin);

            xLbl = xMax.ToString() + "/" + xMin.ToString();
            yLbl = yMax.ToString() + "/" + yMin.ToString();

            ArmXMaxLbl.Content = xLbl;
            ArmYMaxLbl.Content = yLbl;

            ArmXStat.Value = xNorm;
            ArmYStat.Value = yNorm;

            try
            {
                updateArmDrawing();
            }
            catch (Exception)
            {
                ArmDrawing.Children.Clear();                
            }
            

        }

        protected override void OnClosing(System.ComponentModel.CancelEventArgs e)
        {
            base.OnClosing(e);
        }

        //Slider only for base rotation
        private void sliderChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            Slider baseSlider = (Slider)sender;
            //Debug.WriteLine(test.Value);
            SharedState.set("ArmBaseSpeed", baseSlider.Value * 2 - 10);
        }

        // Probably doesn't work like we expected, do not use
        private void textBoxChanged(object sender, TextChangedEventArgs e)
        {
            TextBox InvKinVal = (TextBox)sender;
            if (InvKinVal.Text != "")
            {
                SharedState.set(InvKinVal.Name, InvKinVal.Text);
                try
                {
                    updateArmLimits();
                }
                catch
                {
                }
            }
            
        }

        // Scroll Wheel makes it easy to nudge values
        private void textBoxWheel(object sender, MouseWheelEventArgs e)
        {
            TextBox InvKinBox = (TextBox)sender;
            int curVal = Convert.ToInt32(InvKinBox.Text);
            if (e.Delta > 0) curVal++;
            else curVal--;
            InvKinBox.Text = curVal.ToString();
        }

        private void textBoxKeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return)
            {

                TextBox InvKinVal = (TextBox)sender;
                if (InvKinVal.Text != "")
                {
                    int val = Convert.ToInt32(InvKinVal.Text);
                    SharedState.set(InvKinVal.Name, val.ToString());
                    try
                    {
                        updateArmLimits();
                    }
                    catch
                    {
                    }
                }

                TraversalRequest request = new TraversalRequest(FocusNavigationDirection.Next);
                ((TextBox)sender).MoveFocus(request);
            }
        }

        private void buttonTouch(object sender, MouseButtonEventArgs e)
        {
            Button pressed = (Button)sender;
            SharedState.set(pressed.Name, (e.ButtonState==MouseButtonState.Pressed).ToString());
        }

        private void updateArmDrawing()
        {
            double r = Convert.ToDouble(IK_XVal.Text)/1000.0;
            double z = Convert.ToDouble(IK_YVal.Text)/1000.0;

            double L1 = 0.33595;
            double L2 = 0.36085;
            double phi1 = Math.Acos(1.0/(2 * L1*L1 * (r*r + z*z)) * (L1 * L1 * L1 * z + L1 * z * (-L2 * L2 + r * r + z * z) 
                            + (r * r + z * z) * Math.Sqrt(-(L1 * L1 * r * r * (L1 * L1 * L1 * L1 + (-L2 * L2 + r * r + z * z) 
                            * (-L2 * L2 + r * r + z * z) - 2 * L1 * L1 * (L2 * L2 + r * r + z * z))) / ((r * r + z * z) * (r * r + z * z)))));
            double phi2 = -Math.Acos(1.0/((-2 * L1 * L2 * (r*r + z*z))) * (L1*L1*L1 * z - L1 * z * (L2*L2 + r*r + z*z) 
                            + (r*r + z*z) * Math.Sqrt(-(L1*L1 * r*r * (L1*L1*L1*L1 + (-L2*L2 + r*r + z*z)* (-L2 * L2 + r * r + z * z) 
                            - 2 * L1*L1 * (L2*L2 + r*r + z*z))) / ((r*r + z*z)* (r * r + z * z)))));
            ArmDrawing.Children.Clear();

            // get coordinates in meters
            double pivX = Math.Abs(L1 * Math.Sin(phi1)); 
            double pivY = Math.Abs(L1 * Math.Cos(phi1));

            const double ppm = 667.1899529; // pixels per meter

            Line bar1 = new Line();
            bar1.X1 = 110;
            bar1.Y1 = 450;
            bar1.X2 = 110 + pivX * ppm;
            bar1.Y2 = 450 - pivY * ppm;
            SolidColorBrush lineColor = new SolidColorBrush();
            lineColor.Color = Colors.Black;
            bar1.StrokeThickness = 3;
            bar1.Stroke = lineColor;
            Line bar2 = new Line();
            bar2.X1 = bar1.X2;
            bar2.Y1 = bar1.Y2;
            bar2.X2 = 110 + r * ppm;
            bar2.Y2 = 450 - z * ppm;
            bar2.StrokeThickness = 3;
            bar2.Stroke = lineColor;
            ArmDrawing.Children.Add(bar1);
            ArmDrawing.Children.Add(bar2);

        }

        double m_stepSize;
        /*private void ArmDrawing_KeyDown(object sender, KeyEventArgs e)
        {
            switch (e.Key) {
                // wasd controls for when using the figure
                case Key.W:
                    IK_YVal.Text = Convert.ToString(Convert.ToDouble(IK_YVal.Text) + m_stepSize);
                    break;
                case Key.S:
                    IK_YVal.Text = Convert.ToString(Convert.ToDouble(IK_YVal.Text) - m_stepSize);
                    break;
                case Key.A:
                    IK_XVal.Text = Convert.ToString(Convert.ToDouble(IK_XVal.Text) - m_stepSize);
                    break;
                case Key.D:
                    IK_XVal.Text = Convert.ToString(Convert.ToDouble(IK_XVal.Text) + m_stepSize);
                    break;
                    // ik controls for use with cameras
                case Key.I:
                    IK_XVal.Text = Convert.ToString(Convert.ToDouble(IK_XVal.Text) + m_stepSize);
                    break;
                case Key.K:
                    IK_XVal.Text = Convert.ToString(Convert.ToDouble(IK_XVal.Text) - m_stepSize);
                    break;
                case Key.PageUp:
                    if(m_stepSize < 100 && Math.Abs(m_stepSize - 100) > 0.0001)
                    {
                        m_stepSize *= 10; 
                    }
                    break;
                case Key.PageDown:
                    if(Math.Abs(m_stepSize - 0.1) > 0.0001 && m_stepSize > 0.1)
                    {
                        m_stepSize /= 10;
                    }
                    break;
            }
            try
            {
                updateArmDrawing();
            }
            catch (Exception)
            {
                ArmDrawing.Children.Clear();
            }
        }*/
    }
}
