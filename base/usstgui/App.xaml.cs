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
			jsonTask = new JsonClientTask(
				downlink, 34568, 34567, "192.168.1.103", 150);
            StateManager.addObserver("inputOneLeftY", downlink);
            StateManager.addObserver("inputOneRightY", downlink);
            StateManager.addObserver("inputTwoLeftY", downlink);
            StateManager.addObserver("inputTwoRightY", downlink);

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
