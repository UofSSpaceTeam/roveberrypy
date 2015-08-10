using System;
using System.Threading;

using StateElement = System.Collections.Generic.KeyValuePair<string, dynamic>;

namespace usstgui
{
	public class BaseTask
	{
		private Thread task;
		private Thread listener;
		private StateQueue downlink;

		public BaseTask(StateQueue downlink)
		{
			task = new Thread(new ThreadStart(taskFunction));
			listener = new Thread(new ThreadStart(listenerFunction));
			this.downlink = downlink;
		}

		public virtual void start()
		{
			task.Start();
			listener.Start();
		}

		public virtual void stop()
		{
			task.Abort();
			listener.Abort();
		}

		private void listenerFunction()
		{
			StateElement data;
			while (true)
			{
				data = downlink.get();
				messageTrigger(data.Key, data.Value);
			}
		}

		protected virtual void messageTrigger(string key, dynamic value) { }

		protected virtual void taskFunction() { }
	}
}
