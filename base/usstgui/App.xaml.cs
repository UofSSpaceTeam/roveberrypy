using System;
using System.Windows;
using System.Threading;
using System.Diagnostics;
using System.Collections.Generic;

namespace usstgui
{
	public partial class App : Application
	{
		public App()
		{
			StateQueue downlink;
			
			ExampleTask exampleTask;
			JsonClientTask jsonTask;
			ControllerTask controllerTask;

			Debug.WriteLine("System Build");

			downlink = new StateQueue();
			exampleTask = new ExampleTask(downlink, 34);
			StateManager.addObserver("exampleTime", downlink);

			downlink = new StateQueue();
			jsonTask = new JsonClientTask(downlink, 34568, 34567, "192.168.1.103", 150);
            // Joystick 1 (Drive) Messages
            StateManager.addObserver("inputOneLeftY", downlink);
            StateManager.addObserver("inputOneRightY", downlink);

            // Joytstick 2 (Arm) Messages
            StateManager.addObserver("inputTwoLeftY", downlink);
            StateManager.addObserver("inputTwoRightY", downlink);

            // Arm Inverse-Kinematics Controls
            StateManager.addObserver("armBaseSlider", downlink);
            StateManager.addObserver("IK_XVal", downlink);
            StateManager.addObserver("IK_YVal", downlink);
            StateManager.addObserver("IK_WristVal", downlink);
            StateManager.addObserver("armWristCw",downlink);
            StateManager.addObserver("armWristCcw", downlink);
            StateManager.addObserver("armGrpClose", downlink);
            StateManager.addObserver("armGrpOpen", downlink);

            // Drill Controls
            StateManager.addObserver("DrillFeed", downlink);
            StateManager.addObserver("DrillSpeed", downlink);
            StateManager.addObserver("DrillUp", downlink);
            StateManager.addObserver("DrillDn", downlink);
            StateManager.addObserver("DrillCw", downlink);
            StateManager.addObserver("DrillCcw", downlink);

            
            // Video Controls
            StateManager.addObserver("ArmVideo", downlink);
            StateManager.addObserver("DriveVideo", downlink);
            StateManager.addObserver("MastVideo", downlink);
            StateManager.addObserver("StopVideo", downlink);

            downlink = new StateQueue();
			controllerTask = new ControllerTask(downlink);

			Debug.WriteLine("System Load");

			jsonTask.receiveFromFile("initial.json");
			Debug.WriteLine("Initial " + StateManager.ToString());

            Debug.WriteLine("System Start");
			
			jsonTask.start();
			controllerTask.start();
			exampleTask.start();
		}
	}
}
