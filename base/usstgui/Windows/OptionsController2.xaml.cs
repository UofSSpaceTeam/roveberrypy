using System.Windows;
using System.Windows.Controls;
using System;
using System.Threading;
using System.Diagnostics;

namespace usstgui
{
    public partial class OptionsController2 : Window
    {
        private bool windowOpen = true;

		public OptionsController2()
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
			}
        }

		private void displayJoystickAxis(string name, CheckBox invert, Slider scale,
			Slider deadband, ProgressBar resultBar)
		{
			displayTriggerAxis(name, scale, deadband, resultBar);
			invert.IsChecked = StateManager.getShared(name + "Invert");
		}

		private void displayTriggerAxis(string name, Slider scale,
			Slider deadband, ProgressBar resultBar)
		{
			scale.Value = StateManager.getShared(name + "Scale");
			deadband.Value = StateManager.getShared(name + "Deadband");
			resultBar.Value = StateManager.getShared(name);
		}

		private void updateResultBar(string name, ProgressBar resultBar)
		{
			resultBar.Value = StateManager.getShared(name);
		}

		private void checkboxChanged(object sender, RoutedEventArgs e)
		{
			CheckBox box = (CheckBox)sender;
			StateManager.setShared("inputTwo" + box.Name, box.IsChecked);
        }

		private void sliderChanged(object sender, RoutedEventArgs e)
		{
			Slider slider = (Slider)sender;
			StateManager.setShared("inputTwo" + slider.Name, slider.Value);
        }

		private void Close(object sender, RoutedEventArgs e)
		{
			this.Close();
		}
    }
}
