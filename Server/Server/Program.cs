using System.Net.Sockets;
using System.Net;
using System.Text;

namespace Server
{
    internal class Program
    {
        static async Task Main(string[] args)
        {
            IPEndPoint ipPoint = new IPEndPoint(IPAddress.Any, 8888);
            using Socket tcpListner = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            try
            {
                tcpListner.Bind(ipPoint);
                tcpListner.Listen(1000);
                Console.WriteLine("Server started...");

                using Socket client = await tcpListner.AcceptAsync();
                Console.WriteLine($"The client {client.RemoteEndPoint} connected");
                byte[] buffer = new byte[512];
                while (true)
                {
                    int reciveBytes = await client.ReceiveAsync(buffer);
                    string clientMessage = Encoding.UTF8.GetString(buffer, 0, reciveBytes);
                    Console.WriteLine($"The client sent message {clientMessage}");
                    if (clientMessage.Equals("exit"))
                    {
                        Console.WriteLine($"The client turn of");
                        break;
                    }
                    Console.WriteLine("You: ");
                    string serverMessage = Console.ReadLine() ?? string.Empty;
                    byte[] data = Encoding.UTF8.GetBytes(serverMessage);
                    await client.SendAsync(data);
                    if (serverMessage.Equals("exit"))
                    {
                        Console.WriteLine("End works the server");
                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Exeption {ex.Message}");
            }
        }
    }
}
