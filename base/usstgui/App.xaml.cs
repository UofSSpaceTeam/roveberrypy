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
			// Load initial state information
			JsonClientTask.receiveFromFile("initial.json");
			Debug.WriteLine("Initial " + SharedState.ToString());

			// Task to read the xbox controllers
			ControllersTask controllers = new ControllersTask();

			// Communications task
			JsonClientTask jsonClient = new JsonClientTask(150);
			jsonClient.subscribe(new string[] {"commsHeartbeat", // Rover task heartbeat messages
											"driveHeartbeat",
											"armHeartbeat",
											"drillHeartbeat",
											"gpsHeartbeat",
											"lidarHeartbeat",
											"inputOneLeftY", // Joystick 1 (Drive) Messages
											"inputOneRightY",
											"inputTwoLeftY", // Joystick 2 (Arm) Messages
											"inputTwoLeftX",
											"inputTwoRightY",
											"inputTwoRightX",
                                            "inputTwoAButton",
                                            "inputTwoBButton",
                                            "inputTwoXButton",
                                            "inputTwoYButton",
                                            "armBaseSlider", // Arm Inverse-Kinematics Controls
											"IK_XVal",
											"IK_YVal",
											"IK_WristVal",
											"wristRotation",
											"gripperOpenClose",
											"DrillFeedPower", // Drill Controls
											"DrillTranslation",
											"DrillRotation",
											"DrillPower",
											"VideoState"}); // Video
			
			// start all the tasks
			jsonClient.start();
			controllers.start();
		}
	}
}
