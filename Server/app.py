# -*- coding: utf-8 -*-
class Storage(Exception):
    def __init__(self):
        from youtubedl import ytdl
        import logging
        import cv2
        self.logging = logging
        self.logging.basicConfig(filename='debug.log', level=logging.DEBUG)
        self.storage = self
        self.server = server(self)
        self.debug = True
        self.cv2 = cv2
        self.sift = cv2.xfeatures2d.SIFT_create()
        self.ytdl = ytdl(self)
        self.now = []
        self.threads = {}
        pass
    
    def save(self, movid, arg, ip):
        from json import loads, dumps
        from os.path import isfile
        if isfile("data.json"): 
            f = open("data.json", "r")
            try: q = loads(f.read())
            except: 
                self.storage.debuglogger(ip=ip, desc="Cannot get jsondata", code=503)
                return {"status": 503, "line": "Cannot get data file."}
            q.update({movid: arg})
            f.close()
        f = open("data.json", "w")
        f.write(dumps(q))
        f.close()
    
    def search(self, movid, ip):
        from json import loads
        from os.path import isfile
        if isfile("data.json"): 
            f = open("data.json", "r")
            try: q = loads(f.read())
            except: 
                self.storage.debuglogger(ip=ip, desc="Cannot get jsondata", code=503)
                return {"status": 503, "line": "Cannot get data file."}
            f.close()
            if movid in q: return {"status": 200, "data": q[movid]}
            else: return {"status": 404, "line": "movie information is not found."}
        else: 
            self.storage.debuglogger(ip=ip, desc="Cannot find data.json", code=503)
            return {"status": 503, "line": "Cannot find data file."}

    def logger(self, ip, desc, code):
        import time
        #time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time()))
        print("{ip} - - {time} {desc} {code} -".format(ip=ip, desc=desc, time=time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())), code=str(code)))
        if self.debug == True:
            self.logsave(desc="{ip} - - {time} {desc} {code} -".format(ip=ip, desc=desc, time=time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())), code=str(code)), code=code)
        pass

    def debuglogger(self, ip, desc, code, frame=None):
        import time
        if self.debug == True: 
            if frame == None: 
                print("{ip} - - {time} || DEBUG || {desc} {code} -".format(ip=ip, desc=desc, time=time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())), code=str(code)))
                self.logsave(desc="{ip} - - {time} || DEBUG || {desc} {code} -".format(ip=ip, desc=desc, time=time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())), code=str(code)), code=code)
            else: 
                print("{ip} - - {time} || DEBUG || OPENCV || {frame} || {desc} {code} -".format(ip=ip, desc=desc, time=time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())), code=str(code), frame=frame))
                self.logsave(desc="{ip} - - {time} || OPENCV || {frame} || {desc} {code} -".format(ip=ip, desc=desc, time=time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())), code=str(code), frame=frame), code=code, frame=frame)

        pass

    def logsave(self, desc, code, frame=None):
        #from os import system
        #system('echo "{desc}" >> debug.log'.format(desc=desc))
        if frame != None: self.logging.debug(desc)
        elif code == 200: self.logging.info(desc)
        elif code == 400: self.logging.warning(desc)
        elif code == 503: self.logging.error(desc)
        else: self.logging.debug(desc)


class server(Exception):
    def __init__(self, storage):
        self.storage = storage
        pass

    def opencvclassmaker(self, movid, fps, ip, turl):
        from threading import Thread
        t = Thread(target=self.opencvclassstarter, args=(self.storage, movid, fps, ip, turl))
        self.storage.debuglogger(ip=ip, desc="OPENCV Threading Start", code=200)
        t.start()
        self.storage.debuglogger(ip=ip, desc="threading list append OK", code=200)
        self.storage.threads.update({movid: t})
    
    def opencvclassstarter(self, storage, movid, fps, ip, turl):
        from opencv import cvstorage
        self.storage.debuglogger(ip=ip, desc="opencv class import OK", code=200)
        rtn = cvstorage(storage, thumbnailpath="./{movid}.jpg".format(movid=movid), vidpath="./{movid}.mp4".format(movid=movid), fps=fps, ip=ip, turl=turl).opencv.vidparse()
        storage.save(movid, rtn, ip)
        storage.threads[movid] = None
        storage.now.remove(movid)

    def processstarter(self, param, ip):
        try: movid = self.storage.ytdl.checkurl(param, ip)
        except SyntaxError: return {"status": 400, "line": "Syntax Error. This is not a youtube url"}
        self.storage.debuglogger(ip=ip, desc="Youtube URL Checker OK", code=200)
        
        # Check
        rtn = self.storage.search(movid, ip)
        if rtn["status"] == 200: 
            self.storage.logger(ip=ip, desc="Already analyzed.", code=200)
            return {"status": 200}

        if movid in self.storage.now: 
            self.storage.logger(ip=ip, desc="Already Now analyzing...", code=200)
            return {"status": 200}

        # Download Start

        self.storage.debuglogger(ip=ip, desc="Download Start", code=200)
        try: fps, turl = self.storage.ytdl.download(movid, ip)

        except: return {"status": 503, "line": "Cannot download Video. Retry again."}
        
        from os.path import isfile
        if isfile(movid+".mp4"): pass
        else: 
            self.storage.logger(ip=ip, desc="Error to Download Video", code=503)
            return {"status": 503, "line": "Cannot download Video. Retry again."}
        if isfile(movid+".jpg"): pass
        else: return {"status": 503, "line": "Cannot download thumbnail. Retry again."}
        
        self.storage.debuglogger(ip=ip, desc="Download OK", code=200)

        # Start
        self.storage.now.append(movid)
        self.storage.debuglogger(ip=ip, desc="Now analyze append OK", code=200)
        self.storage.debuglogger(ip=ip, desc="!!OPENCV THREAD START!!", code=200)
        self.opencvclassmaker(movid, fps, ip, turl)
        return {"status": 200}

    def movtimestampsearch(self, param, ip):
        try:
            movid = self.storage.ytdl.checkurl(param, ip)
        except SyntaxError:
            self.storage.debuglogger(ip=ip, desc="Syntax Error. This is not a youtube url", code=400)
            return {"status": 400, "line": "Syntax Error. This is not a youtube url"}
        
        if movid in self.storage.now:
            self.storage.debuglogger(ip=ip, desc="Service Unavailable. This movie is now analyzing. Please try again.", code=500)
            return {"status": 503, "line": "Service Unavailable. This movie is now analyzing. Please try again."}
        
        return self.storage.search(movid, ip)


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
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #if "url" in request.json: param = request.json["url"]
    #elif "id" in request.json: param = request.json["id"]
    if "url" in request.args: param = request.args["url"]
    elif "id" in request.args: param = request.args["id"]
    else: return {"status": 400, "line": "Cannot find parameter."}
    return storage.server.processstarter(param, ip)
    

@app.route('/rtn', methods=["POST"])
def requestedstatuspost():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #if "url" in request.json: param = request.json["url"]
    #elif "id" in request.json: param = request.json["id"]
    if "url" in request.args: param = request.args["url"]
    elif "id" in request.args: param = request.args["id"]
    else: return {"status": 400, "line": "Cannot find parameter."}
    return storage.server.movtimestampsearch(param, ip)

@app.route('/act', methods=["GET"])
def requestedget():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if "url" in request.args: param = request.args["url"]
    elif "id" in request.args: param = request.args["id"]
    else: return {"status": 400, "line": "Cannot find parameter."}
    return storage.server.processstarter(param, ip)

@app.route('/rtn', methods=["GET"])
def requestedstatusget():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if "url" in request.args: param = request.args["url"]
    elif "id" in request.args: param = request.args["id"]
    else: return {"status": 400, "line": "Cannot find parameter."}
    return storage.server.movtimestampsearch(param, ip)

@app.route('/reset')
def reset():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    try:
        storage.now = []
        storage.threads = {}
        storage.logger(ip=ip, desc="Success to purge data", code=200)
    except:
        storage.logger(ip=ip, desc="Internal Server Error. Cannot find error", code=500)
        return {"status": 500, "line": "Internal Server Error. Cannot find error"}
    return {"status": 200}
    
    


if __name__ == '__main__':
    app.debug = True
    #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    #ssl_context.load_cert_chain(certfile='certfile.crt', keyfile='private.key', password='password')
    #app.run(host="0.0.0.0", threaded=True, port=443, ssl_context=ssl_context)
    app.run(host="0.0.0.0", threaded=True, port=8080)