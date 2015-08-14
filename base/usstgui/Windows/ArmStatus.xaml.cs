using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Threading;
using System.Diagnostics;

namespace usstgui
{
    public partial class ArmStatus : Window
    {

        public ArmStatus()
        {
            InitializeComponent();
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
    }
}
