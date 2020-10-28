using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace ConsoleApp2
{
    class Program
    {
        static void Main(string[] args)
        {
            Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            IPEndPoint ep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 9999);
            socket.Bind(ep);

            socket.Listen(10);

            Socket clientSocket = socket.Accept();
            if(clientSocket.Connected)
            {
                Console.WriteLine("client가 sv에 접속");
            }
            while (!Console.KeyAvailable)
            {
                try
                {
                    byte[] buff = new byte[2048];
                    int n = 0;
                
                    n = clientSocket.Receive(buff);
                    buff = Encoding.UTF8.GetBytes("null");
                    string result = Encoding.UTF8.GetString(buff, 0, n);
                    Console.WriteLine(result);
                }catch
                {
                    break;
                }
            }

        }
    }
}
