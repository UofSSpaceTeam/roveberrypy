using System;
using System.Threading;
using System.Diagnostics;
using SharpDX.XInput;

namespace usstgui
{
	public class ControllerTask : BaseTask
	{
		Gamepad input;
        Controller controller1, controller2;

		public ControllerTask(StateQueue downlink) : base(downlink)
		{
			controller1 = new SharpDX.XInput.Controller(SharpDX.XInput.UserIndex.One);
			controller2 = new SharpDX.XInput.Controller(SharpDX.XInput.UserIndex.Two);
		}

		protected override void messageTrigger(string key, dynamic value)
		{
		}

		protected override void taskFunction()
		{
			while (true)
			{
				Thread.Sleep(50);
				if (controller1.IsConnected)
				{
					input = controller1.GetState().Gamepad;
					processJoystickAxis("inputOneLeftX", input.LeftThumbX);
					processJoystickAxis("inputOneLeftY", input.LeftThumbY);
					processJoystickAxis("inputOneRightX", input.RightThumbX);
					processJoystickAxis("inputOneRightY", input.RightThumbY);
					processTriggerAxis("inputOneLeftTrigger", input.LeftTrigger);
					processTriggerAxis("inputOneRightTrigger", input.RightTrigger);
					processButton("inputOneAButton", GamepadButtonFlags.A);
					processButton("inputOneBButton", GamepadButtonFlags.B);
					processButton("inputOneXButton", GamepadButtonFlags.X);
					processButton("inputOneYButton", GamepadButtonFlags.Y);
					StateManager.setShared("controller1Heartbeat", true);
                }
                else
                    setDefaultValues("inputOne");

                if (controller2.IsConnected)
                {
                    input = controller2.GetState().Gamepad;
                    processJoystickAxis("inputTwoLeftX", input.LeftThumbX);
                    processJoystickAxis("inputTwoLeftY", input.LeftThumbY);
                    processJoystickAxis("inputTwoRightX", input.RightThumbX);
                    processJoystickAxis("inputTwoRightY", input.RightThumbY);
                    processTriggerAxis("inputTwoLeftTrigger", input.LeftTrigger);
                    processTriggerAxis("inputTwoRightTrigger", input.RightTrigger);
                    processButton("inputTwoAButton", GamepadButtonFlags.A);
                    processButton("inputTwoBButton", GamepadButtonFlags.B);
                    processButton("inputTwoXButton", GamepadButtonFlags.X);
                    processButton("inputTwoYButton", GamepadButtonFlags.Y);
					StateManager.setShared("controller2Heartbeat", true);
                }
                else
                    setDefaultValues("inputTwo");
			}
		}

		private void processAxis(string name, double inputValue, bool invert,
								float scale, float deadband)
		{
			double value = inputValue;
			if (value < deadband && value > -deadband)
				value = 0.0;
			if (invert)
				value = -value;
			StateManager.setShared(name, Math.Round(value * scale, 2));
		}

		private void processJoystickAxis(string name, short inputValue)
		{
			processAxis(name,
						(double)inputValue / 32767.0,
						(bool)StateManager.getShared(name + "Invert"),
						(float)StateManager.getShared(name + "Scale"),
						(float)StateManager.getShared(name + "Deadband"));
		}

		private void processTriggerAxis(string name, short inputValue)
		{
			processAxis(name,
						(double)inputValue / 255.0,
						(bool)false,
						(float)StateManager.getShared(name + "Scale"),
						(float)StateManager.getShared(name + "Deadband"));
		}

		private void processButton(string name, GamepadButtonFlags button)
		{
			StateManager.setShared(name, input.Buttons.HasFlag(button));
		}

		private void setDefaultValues(string prefix)
		{
			StateManager.setShared(prefix + "LeftX", 0.0);
			StateManager.setShared(prefix + "LeftY", 0.0);
			StateManager.setShared(prefix + "RightX", 0.0);
			StateManager.setShared(prefix + "RightY", 0.0);
			StateManager.setShared(prefix + "LeftTrigger", 0.0);
			StateManager.setShared(prefix + "RightTrigger", 0.0);
			StateManager.setShared(prefix + "AButton", false);
			StateManager.setShared(prefix + "BButton", false);
			StateManager.setShared(prefix + "XButton", false);
			StateManager.setShared(prefix + "YButton", false);
		}
	}
}
