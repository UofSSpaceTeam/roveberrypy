using System.Windows;
using System.Windows.Controls;
using SharpDX.XInput;
using System;
using System.Threading;

namespace usstgui
{
    public partial class OptionsController1 : Window
    {
        public Gamepad input;
        Controller controller;
        private bool running = true;

		public OptionsController1()
        {
            controller = new SharpDX.XInput.Controller(SharpDX.XInput.UserIndex.One);
            InitializeComponent();
            Thread t = new Thread(new ThreadStart(XboxController));
            t.Start();
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
            try
            {
                while(running)
                {
					if (controller.IsConnected)
						input = controller.GetState().Gamepad;
					else
					{
						input.LeftThumbX = input.LeftThumbY = input.RightThumbX = input.RightThumbY = 0;
						input.LeftTrigger = input.RightTrigger = 0;
						input.Buttons = 0;
						this.Dispatcher.Invoke((Action)(() => this.Close()));
					}
					this.Dispatcher.Invoke((Action)(() =>
					{
						processJoystickAxis(input.LeftThumbX, LeftXInvert, LeftXScale, LeftXDeadband, LeftXInput, LeftXResult);
						processJoystickAxis(input.LeftThumbY, LeftYInvert, LeftYScale, LeftYDeadband, LeftYInput, LeftYResult);
						processJoystickAxis(input.RightThumbX, RightXInvert, RightXScale, RightXDeadband, RightXInput, RightXResult);
						processJoystickAxis(input.RightThumbY, RightYInvert, RightYScale, RightYDeadband, RightYInput, RightYResult);
						processTriggerAxis(input.LeftTrigger, LeftTriggerInvert, LeftTriggerScale, LeftTriggerDeadband,
											LeftTriggerInput, LeftTriggerResult);
						processTriggerAxis(input.RightTrigger, RightTriggerInvert, RightTriggerScale, RightTriggerDeadband,
											RightTriggerInput, RightTriggerResult);
					}));
                    Thread.Sleep(100);
                }
            }
            catch (Exception ex)
            {
                Console.Write(ex);
            }
        }

		private void processJoystickAxis(short inputValue, CheckBox invert, Slider scale, Slider deadband,
										ProgressBar inputBar, ProgressBar resultBar)
		{
			processAxis(inputValue / 32767.0, invert, scale, deadband, inputBar, resultBar);
		}

		private void processTriggerAxis(short inputValue, CheckBox invert, Slider scale, Slider deadband,
										ProgressBar inputBar, ProgressBar resultBar)
		{
			processAxis(inputValue / 255.0, invert, scale, deadband, inputBar, resultBar);
		}

		private void processAxis(double inputValue, CheckBox invert, Slider scale, Slider deadband,
								ProgressBar inputBar, ProgressBar resultBar)
		{
			inputBar.Value = inputValue;
			if (Math.Abs(inputValue) > deadband.Value)
				resultBar.Value = inputValue * scale.Value * ((bool)invert.IsChecked ? -1 : 1);
			else
				resultBar.Value = 0;
		}
    }
}
