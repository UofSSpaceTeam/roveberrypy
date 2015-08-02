using System;
using System.Windows;
using System.Configuration;
using System.Data;
using System.Linq;
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
				downlink, 34568, 34567, "127.0.0.1", 1000);
			StateManager.addObserver("exampleKey", downlink);

			downlink = new StateQueue();
			controllerTask = new ControllerTask(downlink);

			Debug.WriteLine("System Start");

			exampleTask.start();
			jsonTask.start();
			controllerTask.start();
		}
	}
}
