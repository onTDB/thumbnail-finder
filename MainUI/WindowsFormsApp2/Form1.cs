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

namespace WindowsFormsApp2
{
    public partial class Form1 : MetroFramework.Forms.MetroForm
    {
        public Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        public IPEndPoint IPep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 9999);

        public Form1()
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.AutoSizeMode = AutoSizeMode.GrowAndShrink;
            this.FormBorderStyle = FormBorderStyle.None;
            this.TopMost = true;
            try
            {
                socket.Connect(IPep);
            }catch(Exception ex)
            {
                MessageBox.Show(ex.ToString());

            }
        }
        
        private void button1_Click(object sender, EventArgs e)
        {
            
            try
            {
                if (textBox1.Text != "") 
                {
                    Console.WriteLine(textBox1.Text + "\n" + textBox1.Text.Contains("://www.youtube.com/watch?v="));
                    try
                    {
                        byte[] buff = Encoding.UTF8.GetBytes(textBox1.Text);
                        Console.WriteLine(buff);
                        socket.Send(buff, SocketFlags.None);
                        socket.Close();
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
            try
            {
                socket.Connect(IPep);
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.ToString());
            }            
        }
    }
}
