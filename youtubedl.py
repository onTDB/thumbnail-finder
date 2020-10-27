# coding: utf-8
#134

class ytdl(Exception):
    def __init__(self, storage):
        self.storage = storage
    
    def download(self, yturl):
        import youtube_dl
        try:
            turl = youtube_dl.YoutubeDL({}).extract_info("https://youtu.be/"+yturl, download=False)
        except youtube_dl.utils.DownloadError:
            turl = youtube_dl.YoutubeDL({}).extract_info("https://youtu.be/"+yturl, download=False)
        except youtube_dl.utils.RegexNotFoundError:
            turl = youtube_dl.YoutubeDL({}).extract_info("https://youtu.be/"+yturl, download=False)
        except:
            raise SyntaxError
        self.movie(yturl, turl)
        self.thumbnail(yturl, turl)
    
    def movie(self, yturl, turl):
        from requests import get
        data = None
        for i in turl["formats"]:
            if i["format_id"] == 134:
                data = i
                break

        if data == None:  raise SyntaxError

        f = open(yturl+".mp4", "wb")
        f.write(get(data["url"]).content)
        f.close()
    
    def thumbnail(self, yturl, turl):
        from requests import get
        f = open(yturl+".jpg", "wb")
        f.write(get(turl["thumbnails"][int(len(turl["thumbnails"]))-1]["url"]).content)
        f.close()
    
    def checkurl(self, url):
        from parse import parse
        if "www.youtube.com" in url: 
            if "&list" in url: 
                videoid = parse("{}v={id}&list{}", url)["id"]
            elif "&t" in url: 
                videoid = parse("{}v={id}&t{}", url)["id"]
            else: videoid = parse("{}v={id}", url)["id"]
        elif "youtu.be" in url:
            if "&list" in url: 
                videoid = parse("youtu.be/{id}?list{}", url)["id"]
            elif "&t" in url: 
                videoid = parse("youtu.be/{id}?t{}", url)["id"]
            else: 
                videoid = parse("youtu.be/{id}", url)["id"]
        else: 
            raise SyntaxError

        return videoid
