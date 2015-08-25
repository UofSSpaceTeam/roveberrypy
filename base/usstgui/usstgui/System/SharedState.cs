using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

using StateElement = System.Collections.Generic.KeyValuePair<string, dynamic>;
using StateDict = System.Collections.Generic.Dictionary<string, dynamic>;

namespace usstgui
{
	public static class SharedState
	{
		private static StateDict state = new StateDict();
		private static Dictionary<string, List<StateQueue>> observerMap;

		static SharedState()
		{
			state = new StateDict();
			observerMap = new Dictionary<string, List<StateQueue>>();
		}

		public static void addObserver(string key, StateQueue downlink)
		{
			lock (observerMap)
			{
				if (!observerMap.ContainsKey(key))
					observerMap.Add(key, new List<StateQueue>());
				observerMap[key].Add(downlink);
			}
		}

		public static dynamic get(string key)
		{
			dynamic result = null;
			lock(state)
			{
				if(state.ContainsKey(key))
					result = state[key];
			}
			return result;
		}

		public static void set(string key, dynamic value)
		{
			set(key, value, null);
		}

		public static void set(string key, dynamic value, StateQueue ignoredDownlink)
		{
			lock(state)
			{
				if (state.ContainsKey(key))
					state[key] = value;
				else
					state.Add(key, value);
			}
			notifyObservers(key, ignoredDownlink);
		}

		private static void notifyObservers(string key, StateQueue ignoredDownlink)
		{
			StateElement element;

			lock(observerMap)
				if (observerMap.ContainsKey(key))
				{
					lock(state)
						element = new StateElement(key, state[key]);
					foreach(StateQueue q in observerMap[key])
					{
						if(!StateQueue.ReferenceEquals(q, ignoredDownlink))
							q.put(element);
					}
				}
		}

		public static new string ToString()
		{
			string result = "Shared State:\n";
			lock (state)
			{
				foreach (StateElement e in state)
					result += "<" + e.Key + ">:<" + e.Value.ToString() + ">, ";
			}
			return result + "\n";
		}
	}
}
