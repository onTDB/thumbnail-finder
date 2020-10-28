using System;
using System.IO;
using System.Net;
using System.Net.Sockets;

namespace ConsoleApp1server
{
    class Program
    {
        static void Main(string[] args)
        {
            RunServer();
            Console.ReadLine();
        }
        async static void RunServer()
        {
            int buf_size = 1024;
            TcpListener listener = new TcpListener(IPAddress.Any, 1234);
            listener.Start();

            while (true)
            {
                TcpClient tc = await listener.AcceptTcpClientAsync();
                NetworkStream stream = tc.GetStream();

                // 데이터 크기 수신
                byte[] bytes = new byte[4];
                int nb = await stream.ReadAsync(bytes, 0, bytes.Length);
                if (nb != 4)
                {
                    throw new ApplicationException("Invalid size");
                }
                int total = BitConverter.ToInt32(bytes, 0);

                // 실제 데이터 수신
                string filename = Guid.NewGuid().ToString("N") + ".png";
                using (var fs = new FileStream(filename, FileMode.CreateNew))
                {
                    var buff = new byte[buf_size];
                    int received = 0;
                    while (received < total)
                    {
                        int n = total - received >= buf_size ? buf_size : total - received;
                        nb = await stream.ReadAsync(buff, 0, n);
                        received += nb;

                        await fs.WriteAsync(buff, 0, nb);
                    }
                }
                byte[] result = new byte[1];
                result[0] = 1;
                await stream.WriteAsync(result, 0, result.Length);
                stream.Close();
                tc.Close();
            }
        }
    }
}
