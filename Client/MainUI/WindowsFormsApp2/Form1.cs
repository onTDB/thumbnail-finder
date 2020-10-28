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
using System.Net.Http;
using System.IO;
using Newtonsoft.Json.Linq;
using System.Diagnostics;
using Microsoft.Win32;

namespace WindowsFormsApp2
{
    public partial class Form1 : MetroFramework.Forms.MetroForm
    {
        public string returnURL = null;
        public string container=null;
        public static Process process = new Process();
        public JObject rtn1 = JObject.Parse(@"{}");
        public StringBuilder postParams = new StringBuilder();

        public Form1()
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.AutoSizeMode = AutoSizeMode.GrowAndShrink;
            this.FormBorderStyle = FormBorderStyle.None;
            this.TopMost = true;
            this.Reconnect.Visible = false;
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
                        container = textBox1.Text;
                        input.Visible = false;
                        postParams.Append("?url=" + container);
                        byte[] result = Encoding.UTF8.GetBytes(postParams.ToString());
                        HttpWebRequest wReq = (HttpWebRequest)WebRequest.Create("http://xnglwmx.purl.zz.am:8080/act?url="+ container);
                        wReq.Method = "POST";
                        wReq.ContentType = "application/x-www-form-urlencoded";
                        wReq.ContentLength = result.Length;
                        Stream postDataStream = wReq.GetRequestStream();
                        postDataStream.Write(result, 0, result.Length);

                        HttpWebResponse wResp = (HttpWebResponse)wReq.GetResponse();
                        Stream respPostStream = wResp.GetResponseStream();
                        StreamReader readerPost = new StreamReader(respPostStream, Encoding.Default);

                        var requestResult = readerPost.ReadToEnd();
                        JObject rtn = JObject.Parse(requestResult);

                    
                        MessageBox.Show(rtn["status"].ToString());
                        if (rtn["status"].ToString() == "200")
                        {
                            while(true)
                            {
                                HttpWebRequest wReq1 = (HttpWebRequest)WebRequest.Create("http://xnglwmx.purl.zz.am:8080/rtn?url=" + container);
                                
                                
                                wReq1.Method = "POST";
                                wReq1.ContentType = "application/x-www-form-urlencoded";
                                Stream postDataStream1 = wReq1.GetRequestStream();

                                HttpWebResponse wResp1 = (HttpWebResponse)wReq1.GetResponse();
                                Stream respPostStream1 = wResp1.GetResponseStream();
                                StreamReader readerPost1 = new StreamReader(respPostStream1, Encoding.Default);

                                var requestResult1 = readerPost1.ReadToEnd();
                                rtn1 = JObject.Parse(requestResult1);

                                if (rtn1["status"].ToString() == "200")
                                {
                                    MessageBox.Show(rtn1["data"]["timestampMinSec"].ToString());
                                    break;
                                }else if(rtn1["status"].ToString() == "503" )
                                {
                                    System.Threading.Thread.Sleep(5000);
                                    Console.WriteLine("503");
                                }else
                                {
                                    MessageBox.Show("서버에 문제 발생" + rtn["line"]);
                                    break;
                                }
                            }
                        } else
                        {
                            MessageBox.Show("서버에 문제 발생" + rtn["line"]);
                        }
                        postDataStream.Close();
                        input.Visible = true;
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show(ex.ToString());
                    }finally
                    {
                        Reconnect.Visible = true;
                        returnURL = "https://youtu.be/" + container.Substring(container.IndexOf("=") + 1) + "?t=" + rtn1["data"]["timestamp"].ToString();
                        process = Process.Start(returnURL);
                        textBox1.Text = null;                        
                    }
                } else Console.WriteLine("textbox1 == null");
            }catch(Exception ex)
            {
                Console.WriteLine(ex);
            }
        }

        private void Reconnect_Click(object sender, EventArgs e)
        {
            process = Process.Start(returnURL);
            MessageBox.Show("연결을 재설정 합니다...\nPress Enter");
        }
    }
}
