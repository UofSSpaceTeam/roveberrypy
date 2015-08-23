using System;
using System.Threading;
using System.Diagnostics;
using System.Collections.Generic;

namespace usstgui
{
	public class LidarTask : BaseTask
	{
		int[] topDistances;
		int[] bottomDistances;

		public LidarTask()
		{
			topDistances = new int[720];
			bottomDistances = new int[720];
		}

		protected override void messageTrigger(string key, dynamic value)
		{
			if(key.Equals("lidarData"))
			{
				string[] data = ((string)value).Split(',');
				int i = Int32.Parse(data[2]);
				topDistances[i] = Int32.Parse(data[0]);
				bottomDistances[i] = Int32.Parse(data[1]);
			}
		}

		protected override void taskFunction()
		{
			while (true)
			{

			}
		}
	}
}