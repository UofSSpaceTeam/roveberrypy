using System;
using System.Windows;
using System.Windows.Controls;
using System.Threading;
using System.Diagnostics;

namespace usstgui
{
    public partial class OptionsController1 : Window
    {
        private bool windowOpen = true;

		public OptionsController1()
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
					displayJoystickAxis("inputOneLeftX", LeftXInvert, LeftXScale, LeftXDeadband, LeftXResult);
					displayJoystickAxis("inputOneLeftY", LeftYInvert, LeftYScale, LeftYDeadband, LeftYResult);
					displayJoystickAxis("inputOneRightX", RightXInvert, RightXScale, RightXDeadband, RightXResult);
					displayJoystickAxis("inputOneRightY", RightYInvert, RightYScale, RightYDeadband, RightYResult);
				}));
				while (windowOpen)
				{
					this.Dispatcher.Invoke((Action)(() =>
					{
						updateResultBar("inputOneLeftX", LeftXResult);
						updateResultBar("inputOneLeftY", LeftYResult);
						updateResultBar("inputOneRightX", RightXResult);
						updateResultBar("inputOneRightY", RightYResult);
						updateResultBar("inputOneLeftTrigger", LeftTriggerResult);
						updateResultBar("inputOneRightTrigger", RightTriggerResult);
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
			StateManager.setShared("inputOne" + box.Name, box.IsChecked);
        }

		private void sliderChanged(object sender, RoutedEventArgs e)
		{
			Slider slider = (Slider)sender;
			StateManager.setShared("inputOne" + slider.Name, slider.Value);
        }

		private void Close(object sender, RoutedEventArgs e)
		{
			this.Close();
		}
    }
}
