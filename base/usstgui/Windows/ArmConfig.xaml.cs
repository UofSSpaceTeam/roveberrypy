using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Threading;
using System.Diagnostics;

namespace usstgui
{
    /// <summary>
    /// Interaction logic for ArmConfig.xaml
    /// </summary>
    public partial class ArmConfig : Window
    {

        public ArmConfig()
        {
            InitializeComponent();
        }

        private void updateArmLimits()
        {
            // Needs code here to set up the label and progress bar
            int xCur, yCur;
            float xMin, xMax, yMin, yMax;
            float xNorm, yNorm;
            string xLbl, yLbl;

            xCur = Convert.ToInt32(IK_XVal.Text);
            yCur = Convert.ToInt32(IK_YVal.Text);

            xMin = 200;
            xMax = 1000;
            yMin = 200;
            yMax = 1000;

            xNorm = (xCur - xMin) / (xMax - xMin);
            yNorm = (yCur - yMin) / (yMax - yMin);

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
            StateManager.setShared("ArmBaseSpeed", baseSlider.Value * 2 - 10);
        }

        // Probably doesn't work like we expected, do not use
        private void textBoxChanged(object sender, TextChangedEventArgs e)
        {
            TextBox InvKinVal = (TextBox)sender;
            if (InvKinVal.Text != "")
            {
                StateManager.setShared(InvKinVal.Name, InvKinVal.Text);
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
                    StateManager.setShared(InvKinVal.Name, InvKinVal.Text);
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
            StateManager.setShared(pressed.Name, (e.ButtonState==MouseButtonState.Pressed).ToString());
        }
    }
}
