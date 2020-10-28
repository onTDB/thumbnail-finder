using System;
using System.IO;
using System.Net;
using System.Text;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {
            string text = "test";
            StringBuilder postParams = new StringBuilder();
            postParams.Append("?id=" + text);

            Encoding utfenc = Encoding.UTF8;
            byte[] result = utfenc.GetBytes(postParams.ToString());

            string url = "http://xnglwmx.purl.zz.am/akc";
            HttpWebRequest wReq = (HttpWebRequest)WebRequest.Create(url);

            wReq.Method = "POST";
            wReq.ContentType = "application/x-www-form-urlencoded";
            wReq.ContentLength = result.Length;

            Stream postDataStream = wReq.GetRequestStream();
            postDataStream.Write(result, 0, result.Length);
            postDataStream.Close();
        }
    }
}
