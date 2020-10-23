# coding: utf-8

class ytdl(Exception):
    def __init__(self, url):
        self.url = url
        self.parsedurl = None
        self.vid
    
    def download(self):
        from os import system
        try:
            system("youtube-dl --no-warnings --no-playlist -o '%(id)' {url}")
        except:
            raise ChildProcessError
    
    def checkurl(self):
        from parse import parse
        if "www.youtube.com" in self.url: 
            if "list" in self.url: self.vid = parse(self.url, "{}v={id}&list{}")["id"]
            elif "t" in self.url: self.vid = parse(self.url, "{}v={id}&t{}")["id"]
            else: self.vid = parse(self.url, "{}v={id}")["id"]
        elif "youtu.be" in self.url:
            if "list" in self.url: self.vid = parse(self.url, "youtu.be/{id}?list{}")["id"]
            elif "t" in self.url: self.vid = parse(self.url, "youtu.be/{id}?t{}")["id"]
            else: self.vid = parse(self.url, "youtu.be/{id}")["id"]
        else: 
            raise SyntaxError

        self.parsedurl = "https://youtu.be/"+self.vid
        return self.parsedurl
