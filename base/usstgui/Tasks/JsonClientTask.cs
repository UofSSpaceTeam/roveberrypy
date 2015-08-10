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
		StateDict outData;
		StateDict inData;
		Thread netListener;
		UdpClient sender;
		UdpClient receiver;
		IPEndPoint localEndPoint;
		IPEndPoint remoteEndPoint;
		int period;

		public JsonClientTask(
			StateQueue downlink,
			int localPort,
			int remotePort,
			string roverIP,
			int period)
			: base(downlink)
		{
			this.period = period;
			outData = new StateDict();
			netListener = new Thread(new ThreadStart(netListenerFunction));

			localEndPoint = new IPEndPoint(IPAddress.Any, localPort);
			remoteEndPoint = new IPEndPoint(IPAddress.Parse(roverIP), remotePort);

			sender = new UdpClient();
			receiver = new UdpClient();
			receiver.Client.SetSocketOption(
				SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
			receiver.Client.Bind(localEndPoint);
		}

		public void receiveFromFile(string filename)
		{
			StreamReader reader = new StreamReader(filename, ASCIIEncoding.ASCII);
			receiveJson(reader.ReadToEnd());
			reader.Close();
		}

		public override void start()
		{
			base.start();
			netListener.Start();
		}

		public override void stop()
		{
			base.stop();
			netListener.Abort();
		}

		private void netListenerFunction()
		{
			IPEndPoint remote = null;
			while (true)
			{
				receiveJson(Encoding.ASCII.GetString(receiver.Receive(ref remote)));
			}
		}

		private void receiveJson(string rawData)
		{
			inData = new StateDict();
			try
			{
				inData = JsonConvert.DeserializeObject<StateDict>(rawData);
			}
			catch
			{
				Debug.WriteLine("Got bad JSON: " + rawData);
			}
			foreach (StateElement e in inData)
				StateManager.setShared(e.Key, e.Value);
		}

		protected override void messageTrigger(string key, dynamic value)
		{
			lock (outData)
			{
				if (outData.ContainsKey(key))
					outData[key] = value;
				else
					outData.Add(key, value);
			}
		}

		protected override void taskFunction()
		{
			byte[] dgram = null;
			while (true)
			{
				lock (outData)
				{
					if (outData.Count > 0)
					{
						dgram = Encoding.ASCII.GetBytes(
							JsonConvert.SerializeObject(outData));
                        //Debug.Write("TX Packet: ");
                        //Debug.WriteLine(Encoding.Default.GetString(dgram));
                        outData.Clear();
					}
				}
				if (dgram != null)
				{
					sender.Send(dgram, dgram.GetLength(0), remoteEndPoint);
					dgram = null;
				}
				Thread.Sleep(period);
			}
		}
	}
}
