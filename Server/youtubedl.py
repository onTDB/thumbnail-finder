# -*- coding: utf-8 -*-
#134

class ytdl(Exception):
    def __init__(self, storage):
        self.storage = storage
    
    def download(self, url, ip, turl=None):
        import youtube_dl
        self.storage.debuglogger(ip=ip, desc="Import youtube_dl OK", code=200)
        #try:
        #    self.storage.debuglogger(ip=ip, desc="Start to get video info", code=200)
        #    turl = youtube_dl.YoutubeDL({}).extract_info("https://youtu.be/"+yturl, download=False)
        #except youtube_dl.utils.DownloadError:
        #    try:
        #        from time import sleep
        #        sleep(1)
        #        self.storage.debuglogger(ip=ip, desc="Start to get video info Retry", code=200)
        #        turl = youtube_dl.YoutubeDL({}).extract_info("https://youtu.be/"+yturl, download=False)
        #    except:
        #        self.storage.logger(ip=ip, desc="Error to Download Thumbnail", code=503)
        #        raise IndexError
        #except youtube_dl.utils.RegexNotFoundError:
        #    try:
        #        from time import sleep
        #        sleep(1)
        #        self.storage.debuglogger(ip=ip, desc="Start to get video info Retry", code=200)
        #        turl = youtube_dl.YoutubeDL({}).extract_info("https://youtu.be/"+yturl, download=False)
        #    except:
        #        self.storage.logger(ip=ip, desc="Error to Download Thumbnail", code=503)
        #        raise IndexError
        #except:
        #    self.storage.logger(ip=ip, desc="Something Went Wrong!! youtubedl.py::29", code=503)
        #    raise SyntaxError
        if turl == None:
            while True:
                try:
                    turl = youtube_dl.YoutubeDL({}).extract_info(url, download=False)
                    break
                except youtube_dl.utils.ExtractorError:
                    return 0, 0
                except:
                    pass
        self.storage.debuglogger(ip=ip, desc="Get video info OK", code=200)
        fps = self.movie(url, turl, ip)
        self.thumbnail(url, turl, ip)
        return fps, turl
    
    def movie(self, url, turl, ip):
        #from requests import get
        #data = None
        #self.storage.debuglogger(ip=ip, desc="Parse FPS Start", code=200)
        #for i in turl["formats"]:
        #    if i["format_id"] == '134':
        #        data = i
        #        break
        #
        #self.storage.debuglogger(ip=ip, desc="Parse FPS OK", code=200)
        data = turl["formats"][len(turl["formats"])-1]
        if "fps" in data:
            fps = data["fps"]
        else:
            fps = None
        
        
        #if data == None: raise SyntaxError
        #f = open(yturl+".mp4", "wb")
        #f.write(get(data["url"]).content)
        #f.close()
        from os import system
        from os.path import isfile
        self.storage.debuglogger(ip=ip, desc="Start to download video", code=200)
        while True:
            try:
                system("youtube-dl --no-warnings -f {formatid} -o %(id)s.%(ext)s {url}".format(url=url, formatid=data["format_id"]))
            except:
                self.storage.logger(ip=ip, desc="Error to Download Video.", code=503)
                raise ChildProcessError
            
            if isfile(turl["id"]+".mp4"): break
            else: pass

        self.storage.debuglogger(ip=ip, desc="Download video command execute OK", code=200)

        return fps

    
    def thumbnail(self, url, turl, ip):
        from requests import get
        f = open(turl["id"]+".jpg", "wb")
        f.write(get(turl["thumbnails"][int(len(turl["thumbnails"]))-1]["url"]).content)
        f.close()
    
    def checkurl(self, url, ip):
        import youtube_dl
        
        print(url)
        while True:
            try:
                turl = youtube_dl.YoutubeDL({}).extract_info(url, download=False)
                print("OK")
                return turl["id"], turl
            except youtube_dl.utils.DownloadError:
                pass
            except youtube_dl.utils.ExtractorError:
                raise SyntaxError
            except:
                pass
        
        #from parse import parse
        #if "www.youtube.com" in url: 
        #    if "&list" in url: videoid = parse("{}v={id}&list{}", url)["id"]
        #    elif "&feature" in url: videoid = parse("{}v={id}&feature{}", url)["id"]
        #    elif "&t" in url: videoid = parse("{}v={id}&t{}", url)["id"]
        #    else: videoid = parse("{}v={id}", url)["id"]
        #elif "youtu.be" in url:
        #    if "&list" in url: videoid = parse("{}youtu.be/{id}?list{}", url)["id"]
        #    elif "&feature" in url: videoid = parse("{}v={id}&feature{}", url)["id"]
        #    elif "&t" in url: videoid = parse("{}youtu.be/{id}?t{}", url)["id"]
        #    else: videoid = parse("{}youtu.be/{id}", url)["id"]
        #else: 
        #    self.storage.logger(ip=ip, desc="Syntax Error. This is not a youtube url", code=400)
        #    raise SyntaxError

        #return videoid