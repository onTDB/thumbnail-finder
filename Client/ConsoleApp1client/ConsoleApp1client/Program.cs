using System;
using System.ComponentModel.Design;
using System.Net.Sockets;
using System.Text;

namespace ConsoleApp1client
{
    class Program
    {
        static void Main(string[] args)
        {
            Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            socket.Connect("127.0.0.1", 9999);

            if (socket.Connected)
            {
                Console.WriteLine("연결");
            }
            string message = string.Empty;  

            while((message=Console.ReadLine()) != "exit")
            {
                byte[] buff = Encoding.UTF8.GetBytes(message);
                socket.Send(buff);
            }
            byte[] endbuff = Encoding.UTF8.GetBytes("exit");
            socket.Send(endbuff);
        }
    }
}
