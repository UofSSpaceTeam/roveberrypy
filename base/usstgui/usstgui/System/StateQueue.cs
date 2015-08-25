using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

using StateElement = System.Collections.Generic.KeyValuePair<string, dynamic>;
using StateDict = System.Collections.Generic.Dictionary<string, dynamic>;

namespace usstgui
{
	public class StateQueue : Object
	{
		private Queue<StateElement> queue;
		private SemaphoreSlim signal;

		public StateQueue()
		{
			queue = new Queue<StateElement>();
			signal = new SemaphoreSlim(0, 1);
		}

		public StateElement get()
		{
			StateElement item;

			signal.Wait();
			lock (queue)
			{
				item = queue.Dequeue();
				if (queue.Count > 0)
					signal.Release();
			}
			return item;
		}

		public void put(StateElement item)
		{
			lock (queue)
			{
				queue.Enqueue(item);
				if (queue.Count == 1)
					signal.Release();
			}
		}
	}
}
