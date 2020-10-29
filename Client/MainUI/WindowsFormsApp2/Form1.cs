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
using Newtonsoft.Json.Linq;
using System.Diagnostics;
using Microsoft.Win32;

namespace WindowsFormsApp2
{
    //public partial class Form1 : MetroFramework.Forms.MetroForm//디자인 오류나는 것은public partial class Form1 : Form으로 고치면 가능하긴 한데 멋이 떨어짐
    public partial class Form1 : Form
    {
        public string returnURL = null;
        public string container = null;
        public static Process process = new Process();
        public JObject rtn1 = JObject.Parse(@"{}");
        public StringBuilder postParams = new StringBuilder();

        public Form1()
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.AutoSizeMode = AutoSizeMode.GrowAndShrink;
            //this.FormBorderStyle = FormBorderStyle.None;
            this.TopMost = true;
            this.Reconnect.Visible = false;
            string dir = Directory.GetCurrentDirectory() + @"\url.txt";
            string dir2 = Directory.GetCurrentDirectory() + @"\n.txt";
            Console.WriteLine(dir2);

            //string n=File.ReadAllText(dir2);
            //JObject SaveUrl = new JObject(new JProperty(("url"+n).ToString(), "sonhung"));
            
            JObject SaveUrl = new JObject(new JProperty(("url").ToString(), "sonhung"));
            
            string content = File.ReadAllText(dir);
            File.WriteAllText(dir, content+"\n"+SaveUrl.ToString()); 
            Console.WriteLine(content);

        }
        public string GetRtn()
        {
            byte[] result = Encoding.UTF8.GetBytes(postParams.ToString());
            HttpWebRequest wReq = (HttpWebRequest)WebRequest.Create("http://xnglwmx.purl.zz.am:8080/act?url=" + container);
            wReq.Method = "POST";
            wReq.ContentType = "application/x-www-form-urlencoded";
            wReq.ContentLength = result.Length;
            Console.WriteLine("2단계 wReq 검사 완료.");

            postDataStream = wReq.GetRequestStream();
            postDataStream.Write(result, 0, result.Length);
            Console.WriteLine("3단계 Write 검사 완료."); //실패됨 아마 서버오류

            HttpWebResponse wResp = (HttpWebResponse)wReq.GetResponse();
            Stream respPostStream = wResp.GetResponseStream();
            StreamReader readerPost = new StreamReader(respPostStream, Encoding.Default);

            var requestResult = readerPost.ReadToEnd();

            return requestResult;
        }
        public string GetRtn1()
        {
            HttpWebRequest wReq1 = (HttpWebRequest)WebRequest.Create("http://xnglwmx.purl.zz.am:8080/rtn?url=" + container);

            wReq1.Method = "POST";
            wReq1.ContentType = "application/x-www-form-urlencoded";
            postDataStream1 = wReq1.GetRequestStream();

            HttpWebResponse wResp1 = (HttpWebResponse)wReq1.GetResponse();
            Stream respPostStream1 = wResp1.GetResponseStream();
            StreamReader readerPost1 = new StreamReader(respPostStream1, Encoding.Default);

            var requestResult1 = readerPost1.ReadToEnd();

            return requestResult1;
        }
        private void button1_Click(object sender, EventArgs e)
        {
            var p = new { Id = textBox1.Text};         
            try
            {            
                if (textBox1.Text != "") 
                {
                    if (textBox1.Text.Contains("youtu.be/"))
                    {

                        if (textBox1.Text.Contains("?t="))
                        {
                            textBox1.Text = textBox1.Text.Substring(0, textBox1.Text.IndexOf("?"));
                        }
                        container = textBox1.Text;
                        input.Visible = false;
                        try
                        {
                            postParams.Append("?url=" + container);
                            JObject rtn = JObject.Parse(GetRtn());

                            MessageBox.Show(rtn["status"].ToString());
                            if (rtn["status"].ToString() == "200")
                            {
                                try
                                {
                                    while (true)
                                    {
                                        rtn1 = JObject.Parse(GetRtn1());

                                        if (rtn1["status"].ToString() == "200")
                                        {
                                            MessageBox.Show("status : " + rtn1["data"]["timestampMinSec"].ToString() + "\n분석 완료");
                                            break;
                                        }
                                        else if (rtn1["status"].ToString() == "503")
                                        {
                                            System.Threading.Thread.Sleep(5000);
                                            Console.WriteLine("503");
                                        }
                                        else
                                        {
                                            MessageBox.Show("서버에 문제 발생" + rtn["line"]);
                                            Console.WriteLine(rtn["line"]);
                                            break;
                                        }
                                    }
                                }
                                catch (Exception ex)
                                {
                                    MessageBox.Show(ex.ToString());
                                }
                            }
                            else
                            {
                                MessageBox.Show("서버에 문제 발생" + rtn["line"]);
                            }
                            postDataStream.Close();
                            input.Visible = true;
                        }
                        catch(Exception ex)
                        {
                            MessageBox.Show(ex.ToString());
                        }
                        finally
                        {
                            Reconnect.Visible = true;
                            returnURL = container + "?t=" + rtn1["data"]["timestamp"].ToString();
                            JObject SaveUrl = new JObject(new JProperty("url", returnURL));
                            File.WriteAllText(Directory.GetCurrentDirectory(),SaveUrl.ToString());
                            process = Process.Start(returnURL);
                            textBox1.Text = null;
                        }
                    }
                    else if (textBox1.Text.Contains("youtube.com"))
                    {
                        container = textBox1.Text;
                        input.Visible = false;
                        Console.WriteLine("1단계 clickevent 발생 후 if 검사 완료.");
                        try
                        {                      
                            postParams.Append("?url=" + container);
                            JObject rtn = JObject.Parse(GetRtn());
                            MessageBox.Show("status : " + rtn["status"].ToString());
                            if (rtn["status"].ToString() == "200")
                            {
                                try
                                {
                                    while (true)
                                    {                                       
                                        rtn1 = JObject.Parse(GetRtn1());

                                        if (rtn1["status"].ToString() == "200")
                                        {
                                            MessageBox.Show("status : " + rtn1["data"]["timestampMinSec"].ToString() + "\n분석 진행중");
                                            break;
                                        }
                                        else if (rtn1["status"].ToString() == "503")
                                        {
                                            System.Threading.Thread.Sleep(5000);
                                            Console.WriteLine("503");
                                        }
                                        else
                                        {
                                            MessageBox.Show("서버에 문제 발생" + rtn["line"]);
                                            break;
                                        }
                                    }

                                }
                                catch (Exception ex)
                                {
                                    MessageBox.Show(ex.ToString());
                                }
                            }
                            else
                            {
                                MessageBox.Show("서버에 문제 발생" + rtn["line"]);
                            }
                            postDataStream.Close();
                            input.Visible = true;
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show(ex.ToString());
                        }
                        finally
                        {
                            Reconnect.Visible = true;
                            returnURL = "https://youtu.be/" + container.Substring(container.IndexOf("=") + 1) + "?t=" + rtn1["data"]["timestamp"].ToString();
                            process = Process.Start(returnURL);
                            textBox1.Text = null;
                        }

                    }
                }
                else Console.WriteLine("textbox1 == null");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
            }
        }

        private void Reconnect_Click(object sender, EventArgs e)
        {
            MessageBox.Show("연결을 재설정 합니다...\nPress Enter");
            process = Process.Start(returnURL);

        }
        public Stream postDataStream;
        public Stream postDataStream1;
        
    }
}
