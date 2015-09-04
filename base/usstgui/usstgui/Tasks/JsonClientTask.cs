using System;
using System.Text;
using System.IO;
using System.Threading;
using System.Diagnostics;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using Newtonsoft.Json;

using StateElement = System.Collections.Generic.KeyValuePair<string, dynamic>;
using StateDict = System.Collections.Generic.Dictionary<string, dynamic>;

namespace usstgui
{
	public class JsonClientTask : BaseTask
	{
		StateDict outData = new StateDict();
		UdpClient sender = new UdpClient();
		UdpClient receiver = new UdpClient();
		int period;

		public JsonClientTask(int period)
		{
			this.period = period;
			receiver.Client.SetSocketOption(
				SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
			receiver.Client.Bind(new IPEndPoint(IPAddress.Any, (int)getShared("jsonPort")));
		}

		public static void receiveFromFile(string filename)
		{
			StreamReader reader = new StreamReader(filename, ASCIIEncoding.ASCII);
			StateDict inData = parseJson(reader.ReadToEnd());
			foreach (StateElement e in inData)
				SharedState.set(e.Key, e.Value);
			reader.Close();
		}

		private static StateDict parseJson(string rawData)
		{
			StateDict inData = new StateDict();
			try
			{
				inData = JsonConvert.DeserializeObject<StateDict>(rawData);
			}
			catch
			{
				Debug.WriteLine("Got bad JSON: " + rawData);
			}
			return inData;
		}

		public override void start()
		{
			base.start();
			new Thread(new ThreadStart(netListenerFunction)).Start();
		}

		private void netListenerFunction()
		{

            IPEndPoint remote = new IPEndPoint(IPAddress.Any, 34567);
            while (true)
            {
                //IPEndPoint remote = null;
                while (receiver.Available > 0)
                {
                    StateDict inData = parseJson(Encoding.ASCII.GetString(receiver.Receive(ref remote)));
                    Debug.WriteLine(inData);
                    foreach (StateElement e in inData)
                        setShared(e.Key, e.Value);
                }
                Debug.WriteLine("loop");

                Thread.Sleep(100);
            }
        }

		protected override void messageTrigger(string key, dynamic value)
		{
			if(key.Equals("jsonPort"))
			{
                receiver.Client.Bind(new IPEndPoint(IPAddress.Any, getShared("jsonPort")));
			}
			else
			{
				lock(outData)
				{
					if(outData.ContainsKey(key))
						outData[key] = value;
					else
						outData.Add(key, value);
				}
			}
		}

		protected override void taskFunction()
		{
			byte[] dgram = null;
			while(true)
			{
				lock(outData)
				{
					if (outData.Count > 0)
					{
						dgram = Encoding.ASCII.GetBytes(
							JsonConvert.SerializeObject(outData));
                        outData.Clear();
					}
				}
				if (dgram != null)
				{
					sender.Send(dgram, dgram.GetLength(0), new IPEndPoint(
						IPAddress.Parse(getShared("roverIP")), (int)getShared("jsonPort")));
					dgram = null;
				}
				Thread.Sleep(period);
			}
		}
	}
}
