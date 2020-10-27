using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.IO;
namespace WindowsFormsApp2
{
    public partial class Form1 : MetroFramework.Forms.MetroForm
    {
        public StringBuilder postParams = new StringBuilder();

        public Form1()
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.AutoSizeMode = AutoSizeMode.GrowAndShrink;
            this.FormBorderStyle = FormBorderStyle.None;
            this.TopMost = true;
        }
        
        private void button1_Click(object sender, EventArgs e)
        {
            var p = new { Id = textBox1.Text};         
            try
            {
                if (textBox1.Text != "") 
                {
                    Console.WriteLine("Validation : " + textBox1.Text.Contains("://www.youtube.com/watch?v="));
                    try
                    {
                        postParams.Append("?id=" + textBox1.Text);
                        byte[] result = Encoding.UTF8.GetBytes(postParams.ToString());
                        HttpWebRequest wReq = (HttpWebRequest)WebRequest.Create("http://xnglwmx.purl.zz.am/akc");
                        wReq.Method = "POST";
                        wReq.ContentType = "application/x-www-form-urlencoded";
                        wReq.ContentLength = result.Length;
                        Stream postDataStream = wReq.GetRequestStream();
                        postDataStream.Write(result, 0, result.Length);
                        Console.WriteLine("실행완료");
                        postDataStream.Close();
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show(ex.ToString());
                    }
                } else Console.WriteLine("null");
            }catch(Exception ex)
            {
                Console.WriteLine(ex);
            }
        }

        private void Reconnect_Click(object sender, EventArgs e)
        {
            MessageBox.Show("연결을 재설정 합니다...\nPress Enter");         
            //삭제된 코드
        }
    }
}
