class Storage(Exception):
    def __init__(self):
        from youtubedl import ytdl
        import cv2
        self.server = server(self)
        self.debug = False
        self.cv2 = cv2
        self.sift = cv2.xfeatures2d.SIFT_create()
        self.ytdl = ytdl(self)
        self.now = []
        pass
    
    def save(self, movid, arg):
        from json import load, dumps
        f = open("data.json", "r")
        q = load(f.read())
        q.update({movid: {"frame": arg["frame"], "timestamp": arg["timestamp"], "maches": arg["maches"]}})
        f.close()
        f = open("data.json", "w")
        f.write(dumps(q))
        f.close()
    
    def search(self, movid):
        from json import load
        f = open("data.json", "r")
        q = load(f.read())
        f.close()
        if movid in q: return {"status": 200, "data": q[movid]}
        else: return {"status": 404}

class server(Exception):
    def __init__(self, storage):
        self.storage = storage
        pass

    def opencvclassmaker(self, movid):
        from opencv import cvstorage, opencv
        return cvstorage(self.storage, thumbnailpath="./{movid}.jpg".format(movid=movid), vidpath="./{movid}.mp4".format(movid=movid))

    def processstarter(self, param):
        try:
            movid = self.storage.ytdl.checkurl(param)
        except SyntaxError:
            return {"status": 503}
        
        # Check
        rtn = self.storage.search(movid)
        if rtn["status"] == 200: return {"status": 200}

        try:
            self.storage.ytdl.download(movid)
        except:
            return {"status": 503}
        
        # Start

        self.storage.now.append(movid)
        self.opencvclassmaker(movid)
        self.storage.now.remove(movid)

    def 


from flask import Flask, request, render_template
from flask_compress import Compress
import os
import ssl

compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def main():
    return "It Works!"

@app.route('/act', method=["POST"])
def requestedpost():
    if "url" in request.json: param = request.json["url"]
    elif "id" in request.json: param = request.json["id"]
    else: return {"status": 400}

@app.route('/rtn', method=["POST"])
def requestedstatuspost():
    if "url" in request.json: param = request.json["url"]
    elif "id" in request.json: param = request.json["id"]
    else: return {"status": 400}

@app.route('/act', method=["GET"])
def requestedpost():
    if "url" in request.args: param = request.args["url"]
    elif "id" in request.args: param = request.args["id"]
    else: return {"status": 400}

@app.route('/rtn', method=["GET"])
def requestedstatuspost():
    if "url" in request.args: param = request.args["url"]
    elif "id" in request.args: param = request.args["id"]
    else: return {"status": 400}


if __name__ == '__main__':
    app.debug = True
    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    #ssl_context.load_cert_chain(certfile='certfile.crt', keyfile='private.key', password='password')
    #app.run(host="0.0.0.0", threaded=True, port=443, ssl_context=ssl_context)
    app.run(host="0.0.0.0", threaded=True, port=80)