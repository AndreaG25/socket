using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Collections.Generic;


namespace server
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("SERVER 4 AGCHESS");
            Console.WriteLine("v0.1");
            Console.WriteLine("Enter port number: ");
            int port = Convert.ToInt32(Console.ReadLine());
            string myIP = Dns.GetHostByName(Dns.GetHostName()).AddressList[0].ToString();
            Console.WriteLine(myIP); //Problema: AddressList[0] mi ritorna uno degli indirizzi, non so però quale interfaccia di rete
            IPAddress ipAddress = System.Net.IPAddress.Parse(myIP);

            //Create TCP socket server
            IPEndPoint localEndPoint = new IPEndPoint(ipAddress, port);
            Socket listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            try
            {
                listener.Bind(localEndPoint);
                listener.Listen(10);
                Console.WriteLine("Waiting for a connection...");
                while (true)
                {
                    Socket handler = listener.Accept();
                    Client clientThread = new Client(handler);
                    Console.WriteLine("New Connection!");
                    
                    Thread t = new Thread(new ThreadStart(clientThread.doClient));
                    t.Start();


                }

            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }

        }
    }
    public class Client
    {

        Socket client;

        byte[] bytes = new Byte[1024];
        String data = "";

        public Client(Socket client)
        {
            this.client = client;
        }
        public bool checkEnd(string code, bool color)
        {
            if(code == "205")
            {
                //Console.WriteLine("Ha vinto il " + color.ToString());
                return true;
            }
            else if (code == "207")
            {
                //Console.WriteLine("Ripetizione di mosse dopo la mossa di " + color.ToString());
                return true;
            }
            else if (code == "208")
            {
                //Console.WriteLine("Pareggio per materiale insufficiente dopo la mossa di" + color.ToString());
                return true;
            }
            else if (code == "209")
            {
                //Console.WriteLine("Pareggio per stallo dopo la mossa di" + color.ToString());
                return true;
            }
            else if(code == "210")
            {
                //Console.WriteLine("Il " + color.ToString() + " mi arrendo");
                return true;
            }
            else
            {
                return false;
            }
        }
        public void startMatch(string codeMatch)
        {
            bool matchRun = true;
            MatchStruct match = dataGames.getMatch(codeMatch);
            Socket white = match.players[0];
            Socket black = match.players[1];
            sendMessage("201", white);
            string res = "";
            string[] resSplitted;
            while (matchRun)
            {
                res = wait4message(white);
                resSplitted = res.Split(':');
                if(checkEnd(resSplitted[1], true))
                {
                    matchRun = false;
                }
                sendMessage(res, black);
                if (matchRun == true)
                {
                    res = wait4message(black);
                    resSplitted = res.Split(':');

                    if (checkEnd(resSplitted[1], false))
                    {
                        matchRun = false;
                    }
                    sendMessage(res, white);
                }
                
            }
            //Console.WriteLine("Il match " + match.codeMatch + " è terminato");
            dataGames.deleteMatch(match);
        }
        public void sendMessage(string msg, Socket dest)
        {
            byte[] byte2Send = Encoding.ASCII.GetBytes(msg);
            dest.Send(byte2Send);
        }
        public string wait4message(Socket conn)
        {
            data = "";
            while (true)
            {

                while (data.IndexOf("$") == -1)
                {
                    int bytesRec = conn.Receive(bytes);
                    string arrivato = Encoding.ASCII.GetString(bytes, 0, bytesRec);
                    

                    data += Encoding.ASCII.GetString(bytes, 0, bytesRec);
                    bytes = new Byte[1024];

                }
                data = data.Remove(data.Length - 1, 1);
                return data;
            }
        }

        public static string RandomString()
        {
            var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            var stringChars = new char[5];
            var random = new Random();

            for (int i = 0; i < stringChars.Length; i++)
            {
                stringChars[i] = chars[random.Next(chars.Length)];
            }

            var finalString = new String(stringChars);
            return finalString;
        }
        public void doClient()
        {
            string msg = wait4message(client);
            if (msg == "!PLAY")
            {
                if (dataGames.getSinglePlayer() == null)
                {
                    dataGames.addPlayer(client);
                    sendMessage("1", client);
                }
                else
                {
                    MatchStruct m = new MatchStruct();
                    m.codeMatch = RandomString();


                    m.players.Add(dataGames.getSinglePlayer());
                    m.players.Add(client);

                    dataGames.addMatch(m);
                    sendMessage("2:" + m.codeMatch, client);
                    sendMessage("3:" + m.codeMatch, dataGames.getSinglePlayer());
                    Thread t = new Thread(new ThreadStart(() => startMatch(m.codeMatch)));
                    t.Start();
                    dataGames.removeSinglePlayer();
                }
            }
            else
            {
                Console.WriteLine("Error");
            }
        }
    }

    public class MatchStruct
    {
        public string codeMatch;
        public List<Socket> players;

        public MatchStruct()
        {
            players = new List<Socket>();
        }
    }

    public static class dataGames
    {

        private static List<MatchStruct> matches = new List<MatchStruct>();
        //private static List<MatchStruct> friendlyMatches = new List<MatchStruct>();
        private static Socket playerWithOutMatch = null;
        public static List<MatchStruct> getMatches()
        {
            return matches;
        }
        /*
        public static List<MatchStruct> getFriendlyMatches()
        {
            return friendlyMatches;
        }*/
        public static Socket getSinglePlayer()
        {
            return playerWithOutMatch;
        }

        public static void deleteMatch(MatchStruct m)
        {
            matches.Remove(m);
        }

        public static void addMatch(MatchStruct m)
        {
            matches.Add(m);
        }
        /*
        public static void addFriendlyMatch(MatchStruct m)
        {
            friendlyMatches.Add(m);
        }*/

        public static void addPlayer(Socket player)
        {
            playerWithOutMatch = player;
        }
        /*
        public static void addPlayerFriendlyMatch(Socket player, int index)
        {
            friendlyMatches[index].players.Add(player);

        }
        */
        public static void removeSinglePlayer()
        {
            playerWithOutMatch = null;
        }
        /*
        public static void deleteFriendlyMatch(int i)
        {
            friendlyMatches.RemoveAt(i);
        }
        */
        public static MatchStruct getMatch(string code)
        {
            for (int i = 0; i < matches.Count; i++)
            {
                if (matches[i].codeMatch == code)
                {
                    return matches[i];
                }
            }
            return null;
        }
    }
}














