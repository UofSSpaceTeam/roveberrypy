﻿using System;
using System.Threading;
using System.Diagnostics;
using SharpDX.XInput;

namespace usstgui
{
	public class ControllersTask : BaseTask
	{
		Gamepad input;
        Controller controller1, controller2;

		public ControllersTask()
		{
			controller1 = new SharpDX.XInput.Controller(SharpDX.XInput.UserIndex.One);
			controller2 = new SharpDX.XInput.Controller(SharpDX.XInput.UserIndex.Two);
		}

		protected override void messageTrigger(string key, dynamic value) {}

		protected override void taskFunction()
		{
			while(true)
			{
				Thread.Sleep(50);
				if(controller1.IsConnected)
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
					setShared("controller1Heartbeat", true);
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
					setShared("controller2Heartbeat", true);
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
			setShared(name, Math.Round(value * scale, 2));
		}

		private void processJoystickAxis(string name, short inputValue)
		{
			processAxis(name,
						(double)inputValue / 32767.0,
						(bool)getShared(name + "Invert"),
						(float)getShared(name + "Scale"),
						(float)getShared(name + "Deadband"));
		}

		private void processTriggerAxis(string name, short inputValue)
		{
			processAxis(name,
						(double)inputValue / 255.0,
						(bool)false,
						(float)getShared(name + "Scale"),
						(float)getShared(name + "Deadband"));
		}

		private void processButton(string name, GamepadButtonFlags button)
		{

			setShared(name, input.Buttons.HasFlag(button).ToString());
		}

		private void setDefaultValues(string prefix)
		{
			setShared(prefix + "LeftX", 0.0);
			setShared(prefix + "LeftY", 0.0);
			setShared(prefix + "RightX", 0.0);
			setShared(prefix + "RightY", 0.0);
			setShared(prefix + "LeftTrigger", 0.0);
			setShared(prefix + "RightTrigger", 0.0);
			setShared(prefix + "AButton", false);
			setShared(prefix + "BButton", false);
			setShared(prefix + "XButton", false);
			setShared(prefix + "YButton", false);
		}
	}
}