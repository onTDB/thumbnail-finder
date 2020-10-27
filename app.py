class Storage(Exception):
    def __init__(self):
        from youtubedl import ytdl
        import cv2
        self.debug = False
        self.cv2 = cv2
        self.sift = cv2.xfeatures2d.SIFT_create()
        self.ytdl = ytdl(self)
        self.now = []
        pass
    
    def opencvclassmaker(self, thumbnailpath, vidpath):
        from opencv import cvstorage, opencv
        opencv = cvstorage(self, thumbnailpath, vidpath)

class server(Exception):
    def __init__(self):
        pass

    def checkurl(self):
        pass

from flask import Flask, request, render_template
from flask_compress import Compress
import os
import ssl

compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/act', method=["POST"])
def requestedpost():
    if "url" in request.json: param = request.json["url"]
    elif "id" in request.json: param = request.json["id"]
    else: return {"status": 400}


if __name__ == '__main__':
    app.debug = True
    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    #ssl_context.load_cert_chain(certfile='certfile.crt', keyfile='private.key', password='password')
    #app.run(host="0.0.0.0", threaded=True, port=443, ssl_context=ssl_context)
    app.run(host="0.0.0.0", threaded=True, port=80)