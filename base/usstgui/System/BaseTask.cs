using System;
using System.Threading;

using StateElement = System.Collections.Generic.KeyValuePair<string, dynamic>;

namespace usstgui
{
	public class BaseTask
	{
		private StateQueue downlink = new StateQueue();

		public void subscribe(string[] keys)
		{
			foreach(string key in keys)
			{
				subscribe(key);
			}
		}

		public void subscribe(string key)
		{
			SharedState.addObserver(key, downlink);
		}

		protected dynamic getShared(string key)
		{
			return SharedState.get(key);
		}

		protected void setShared(string key, dynamic value)
		{
			SharedState.set(key, value, downlink);
		}

		public virtual void start()
		{
			new Thread(new ThreadStart(taskFunction)).Start();
			new Thread(new ThreadStart(listenerFunction)).Start();
		}

		private void listenerFunction()
		{
			StateElement data;
			while(true)
			{
				data = downlink.get();
				messageTrigger(data.Key, data.Value);
			}
		}

		protected virtual void messageTrigger(string key, dynamic value) {}

		protected virtual void taskFunction() {}
	}
}
