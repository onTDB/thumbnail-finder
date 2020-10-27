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
        self.threads = {}
        pass
    
    def save(self, movid, arg):
        from json import loads, dumps
        f = open("data.json", "r")
        q = loads(f.read())
        q.update({movid: arg})
        f.close()
        f = open("data.json", "w")
        f.write(dumps(q))
        f.close()
    
    def search(self, movid):
        from json import loads
        f = open("data.json", "r")
        q = loads(f.read())
        f.close()
        if movid in q: return {"status": 200, "data": q[movid]}
        else: return {"status": 404, "line": "movie information is not found."}


class server(Exception):
    def __init__(self, storage):
        self.storage = storage
        pass

    def opencvclassmaker(self, movid, fps):
        from threading import Thread
        t = Thread(target=self.opencvclassstarter, args=(self.storage, movid, fps))
        t.start()
        self.storage.threads.update({movid: t})
    
    def opencvclassstarter(self, storage, movid, fps):
        from opencv import cvstorage
        print ("OPENCV Is now working...")
        rtn = cvstorage(storage, thumbnailpath="./{movid}.jpg".format(movid=movid), vidpath="./{movid}.mp4".format(movid=movid), fps=fps).opencv.imgparse()
        storage.save(movid, rtn)
        storage.threads[movid] = None
        storage.now.remove(movid)

    def processstarter(self, param):
        try:
            movid = self.storage.ytdl.checkurl(param)
        except SyntaxError:
            return {"status": 400, "line": "Syntax Error. This is not a youtube url"}
        
        # Check
        rtn = self.storage.search(movid)
        if rtn["status"] == 200: return {"status": 200}
        if movid in self.storage.now: return {"status": 200}

        try:
            fps = self.storage.ytdl.download(movid)
        except:
            return {"status": 503, "line": "Cannot download Video. Retry again"}
        
        from os.path import isfile
        if isfile(movid+".mp4"): pass
        else: return {"status": 503, "line": "Cannot download Video. Retry again."}
        if isfile(movid+".jpg"): pass
        else: return {"status": 503, "line": "Cannot download thumbnail. Retry again."}
        
        # Start
        
        self.storage.now.append(movid)
        self.opencvclassmaker(movid, fps)
        return {"status": 200}

    def movtimestampsearch(self, param):
        try:
            movid = self.storage.ytdl.checkurl(param)
        except SyntaxError:
            return {"status": 400, "line": "Syntax Error. This is not a youtube url"}
        
        if movid in self.storage.now:
            return {"status": 503, "line": "Service Unavailable. This movie is now analyzing. Please try again."}
            
        return self.storage.search(movid)


from flask import Flask, request, render_template
from flask_compress import Compress
import os
import ssl

storage = Storage()

compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def main():
    return "It Works!"

@app.route('/act', methods=["POST"])
def requestedpost():
    if "url" in request.json: param = request.json["url"]
    elif "id" in request.json: param = request.json["id"]
    else: return {"status": 400, "line": "Cannot find parameter."}
    return storage.server.processstarter(param)
    

@app.route('/rtn', methods=["POST"])
def requestedstatuspost():
    if "url" in request.json: param = request.json["url"]
    elif "id" in request.json: param = request.json["id"]
    else: return {"status": 400, "line": "Cannot find parameter."}
    return storage.server.movtimestampsearch(param)

@app.route('/act', methods=["GET"])
def requestedget():
    if "url" in request.args: param = request.args["url"]
    elif "id" in request.args: param = request.args["id"]
    else: return {"status": 400, "line": "Cannot find parameter."}
    return storage.server.processstarter(param)

@app.route('/rtn', methods=["GET"])
def requestedstatusget():
    if "url" in request.args: param = request.args["url"]
    elif "id" in request.args: param = request.args["id"]
    else: return {"status": 400, "line": "Cannot find parameter."}
    return storage.server.movtimestampsearch(param)

@app.route('/reset')
def reset():
    try:
        storage.now = []
        storage.threads = {}
    except:
        return {"status": 500, "line": "Internal Server Error. Cannot find error"}
    return {"status": 200}
    
    


if __name__ == '__main__':
    app.debug = True
    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    #ssl_context.load_cert_chain(certfile='certfile.crt', keyfile='private.key', password='password')
    #app.run(host="0.0.0.0", threaded=True, port=443, ssl_context=ssl_context)
    app.run(host="0.0.0.0", threaded=True, port=8080)