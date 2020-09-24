class ytdl:
    def down():
        import os
        url = "https://www.youtube.com/watch?v=0WGikTLxZiM&list=RDMM0WGikTLxZiM&start_radio=1"
        path = 'C:\\Users\\Admin\\Desktop\\Github\\thumbnail-finder\\vid'
        if "/watch?v=" in url:
            print("avalible url")
            os.system("youtube-dl -o " + path + url)
        else:
            print("retry")
ytdl.down() 