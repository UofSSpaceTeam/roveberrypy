using System;
using System.Windows;
using System.Windows.Controls;
using System.Threading;
using System.Diagnostics;

namespace usstgui
{
    public partial class Controller2Status : Window
    {
        private bool windowOpen = true;

		public Controller2Status()
        {
            InitializeComponent();
            Thread t = new Thread(new ThreadStart(XboxController));
            t.Start();
        }

        protected override void OnClosing(System.ComponentModel.CancelEventArgs e)
        {
			windowOpen = false;
            base.OnClosing(e);
        }

        private void XboxController()
        {
            try
            {
				this.Dispatcher.Invoke((Action)(() =>
				{
					displayJoystickAxis("inputTwoLeftX", LeftXInvert, LeftXScale, LeftXDeadband, LeftXResult);
					displayJoystickAxis("inputTwoLeftY", LeftYInvert, LeftYScale, LeftYDeadband, LeftYResult);
					displayJoystickAxis("inputTwoRightX", RightXInvert, RightXScale, RightXDeadband, RightXResult);
					displayJoystickAxis("inputTwoRightY", RightYInvert, RightYScale, RightYDeadband, RightYResult);
				}));
				while (windowOpen)
				{
					this.Dispatcher.Invoke((Action)(() =>
					{
						updateResultBar("inputTwoLeftX", LeftXResult);
						updateResultBar("inputTwoLeftY", LeftYResult);
						updateResultBar("inputTwoRightX", RightXResult);
						updateResultBar("inputTwoRightY", RightYResult);
						updateResultBar("inputTwoLeftTrigger", LeftTriggerResult);
						updateResultBar("inputTwoRightTrigger", RightTriggerResult);
					}));
					Thread.Sleep(100);
				}
				Debug.WriteLine("done");
            }
            catch (Exception ex)
            {
                Debug.WriteLine(ex);
			}
        }

		private void displayJoystickAxis(string name, CheckBox invert, Slider scale,
			Slider deadband, ProgressBar resultBar)
		{
			displayTriggerAxis(name, scale, deadband, resultBar);
			invert.IsChecked = SharedState.get(name + "Invert");
		}

		private void displayTriggerAxis(string name, Slider scale,
			Slider deadband, ProgressBar resultBar)
		{
			scale.Value = SharedState.get(name + "Scale");
			deadband.Value = SharedState.get(name + "Deadband");
			resultBar.Value = SharedState.get(name);
		}

		private void updateResultBar(string name, ProgressBar resultBar)
		{
			resultBar.Value = SharedState.get(name);
		}

		private void checkboxChanged(object sender, RoutedEventArgs e)
		{
			CheckBox box = (CheckBox)sender;
			SharedState.set("inputTwo" + box.Name, box.IsChecked);
        }

		private void sliderChanged(object sender, RoutedEventArgs e)
		{
			Slider slider = (Slider)sender;
			SharedState.set("inputTwo" + slider.Name, slider.Value);
        }

		private void Close(object sender, RoutedEventArgs e)
		{
			this.Close();
		}
    }
}
