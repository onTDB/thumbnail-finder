class ytdl:
    def __init__(self, storage):
        import os
        import youtube_dl

        self.storage = storage
        self.ytdl = youtube_dl.YoutubeDL({})

        if "" in url:
            print("avail")
        else:
            print("retry")