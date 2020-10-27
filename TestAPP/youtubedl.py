# coding: utf-8

class ytdl(Exception):
    def __init__(self, storage):
        self.storage = storage
    
    def download(self, yturl):
        self.movie(yturl)
        self.thumbnail(yturl)
    
    def movie(self, yturl):
        from os import system
        try:
            system("youtube-dl --no-warnings -f 160 -o %(id)s.%(ext)s {url}".format(url="https://youtu.be/"+yturl))
        except:
            raise ChildProcessError
    
    def thumbnail(self, yturl):
        from os import system
        from youtube_dl import YoutubeDL
        try:
            turl = YoutubeDL({}).extract_info("https://youtu.be/"+yturl)
        except:
            raise SyntaxError

        from requests import get
        f = open(yturl+".jpg", "wb")
        f.write(get(turl).content)
        f.close()
    
    def checkurl(self, url):
        from parse import parse
        if "www.youtube.com" in url: 
            if "list" in url: videoid = parse(url, "{}v={id}&list{}")["id"]
            elif "t" in url: videoid = parse(url, "{}v={id}&t{}")["id"]
            else: videoid = parse(url, "{}v={id}")["id"]
        elif "youtu.be" in url:
            if "list" in url: videoid = parse(url, "youtu.be/{id}?list{}")["id"]
            elif "t" in url: videoid = parse(url, "youtu.be/{id}?t{}")["id"]
            else: videoid = parse(url, "youtu.be/{id}")["id"]
        else: 
            raise SyntaxError

        return videoid
