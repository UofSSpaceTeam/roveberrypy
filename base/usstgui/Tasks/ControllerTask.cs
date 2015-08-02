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
			setInitialValues("inputOne");
			setDefaultValues("inputTwo");
		}

		protected override void messageTrigger(string key, dynamic value)
		{
		}

		protected override void taskFunction()
		{
			while (true)
			{
				Thread.Sleep(200);
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
				}
				else
					setDefaultValues("inputOne");
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


		private void setInitialValues(string prefix)
		{
			setDefaultValues(prefix);
			StateManager.setShared(prefix + "LeftXInvert", false);
			StateManager.setShared(prefix + "LeftXScale", 0.8);
			StateManager.setShared(prefix + "LeftXDeadband", 0.2);
			StateManager.setShared(prefix + "LeftYInvert", false);
			StateManager.setShared(prefix + "LeftYScale", 0.8);
			StateManager.setShared(prefix + "LeftYDeadband", 0.2);
			StateManager.setShared(prefix + "RightXInvert", false);
			StateManager.setShared(prefix + "RightXScale", 0.8);
			StateManager.setShared(prefix + "RightXDeadband", 0.2);
			StateManager.setShared(prefix + "RightYInvert", false);
			StateManager.setShared(prefix + "RightYScale", 0.8);
			StateManager.setShared(prefix + "RightYDeadband", 0.2);
			StateManager.setShared(prefix + "LeftTriggerScale", 0.8);
			StateManager.setShared(prefix + "LeftTriggerDeadband", 0.1);
			StateManager.setShared(prefix + "RightTriggerScale", 0.8);
			StateManager.setShared(prefix + "RightTriggerDeadband", 0.1);
		}
	}
}
