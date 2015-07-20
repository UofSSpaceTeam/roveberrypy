using System;
using System.Threading;
using System.Diagnostics;

namespace usstgui
{
	public class ExampleTask : BaseTask
	{
		int exampleArg;

		public ExampleTask(StateQueue downlink, int exampleArg)
			: base(downlink)
		{
			this.exampleArg = exampleArg;
		}

		protected override void messageTrigger(string key, dynamic value)
		{
			if (key.Equals("exampleTime"))
			{
				string tmp = value.ToString();
				Debug.WriteLine("Time is: " + tmp);
			}
		}

		protected override void taskFunction()
		{
			Debug.WriteLine("arg is " + exampleArg.ToString());
			while (true)
			{
				StateManager.setShared("exampleKey", DateTime.Now.ToLongTimeString());
				Thread.Sleep(2000);
				Debug.WriteLine(StateManager.ToString());
			}
		}
	}
}
