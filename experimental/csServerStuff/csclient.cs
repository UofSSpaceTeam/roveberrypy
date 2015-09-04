/// TO DO: Add Json Packet Support

using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

public struct Received
{
    public IPEndPoint Sender;
    public string Message;
}

class Udp
{
    protected UdpClient Client;

    protected Udp()
    {
        Client = new UdpClient();
    }

    public async Task<Received> Receive()
    {
        var result = await Client.ReceiveAsync();
        return new Received()
        {
            Message = Encoding.ASCII.GetString(result.Buffer, 0, result.Buffer.Length),
            Sender = result.RemoteEndPoint
        };
    }
	
	public static Udp ConnectTo(string hostname, int port)
    {
        var connection = new Udp();
        connection.Client.Connect(hostname, port);
        return connection;
    }
	
	public void Send(string message)
    {
        var datagram = Encoding.ASCII.GetBytes(message);
        Client.Send(datagram, datagram.Length);
    }
}


class Program
{
    static void Main()
    {
        var client = Udp.ConnectTo("192.168.1.103", 34567);

        // Here is a small threaded task
		// It uses the async keyword to block until Receive runs (which again blocks until data)
		Task.Factory.StartNew(async () => {
            while (true)
            {            
				var received = await client.Receive();
				Console.WriteLine(received.Message);
            }
        });

        // Console stuff to play with
		//tring read;
        //while (true)
        //{
        //    read = Console.ReadLine();
        //    client.Send(read);
        //}
    }
}
