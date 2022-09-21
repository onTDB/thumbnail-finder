# -*- coding: utf-8 -*-
class cvstorage():
    def __init__(self, sto, thumbnailpath, vidpath, fps, ip, turl):
        self.ytdldata = turl
        self.ip = ip
        self.fps = fps
        self.count = []
        self.mainstorage = sto
        self.thumbnailpath = thumbnailpath
        self.vidpath = vidpath
        self.thumbnail = None
        self.opencv = opencv(self)
        self.debug = self.mainstorage.debug
        self.logger = self.mainstorage.logger
        self.debuglogger = self.mainstorage.debuglogger

class tempstr():
    def __init__(self):
        import cv2
        self.cv2 = cv2
        self.sift = cv2.SIFT_create()

class storage():
    def __init__(self, thumbnailpath, vidpath):
        self.id = "DEBUG"
        self.count = []
        self.mainstorage = tempstr()
        self.thumbnailpath = thumbnailpath
        self.vidpath = vidpath
        self.thumbnail = None
        self.opencv = opencv(self)
        self.debug = False
    
    def logger(self, ip, desc, code):
        import time
        #time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time()))
        print("{ip} - - {time} {desc} {code} -".format(ip=ip, desc=desc, time=time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())), code=str(code)))
        pass

    def debuglogger(self, ip, desc, code):
        import time
        if self.debug == True: print("{ip} - - {time} || DEBUG || {desc} {code} -".format(ip=ip, desc=desc, time=time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time())), code=str(code)))
        pass


class opencv():
    def __init__(self, storage):
        self.storage = storage
        self.cv2 = self.storage.mainstorage.cv2

        self.sift = self.storage.mainstorage.sift
        self.kp1, self.des1 = self.sift.detectAndCompute(self.cv2.imread(storage.thumbnailpath,0),None)

        #SETUP
        pass

    def core(self, storage, vidimg, frame):
        self.storage.debuglogger(ip=self.storage.ip, desc="Entry Of OpenCV Core::"+str(int(frame)), code=200, frame=frame)
        #img = self.cv2.imread(vidimg,0)
        sift = self.sift

        kp1 = self.kp1
        des1 = self.des1
        kp2, des2 = sift.detectAndCompute(vidimg,None)

        self.storage.debuglogger(ip=self.storage.ip, desc="Load all images", code=200, frame=frame)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   
        flann = self.cv2.FlannBasedMatcher(index_params,search_params)
        self.storage.debuglogger(ip=self.storage.ip, desc="FlannBasedMatcher OK", code=200, frame=frame)
        #if self.storage.debug == True:
        #    from matplotlib import pyplot as plt
        #    plt.imshow(vidimg,),plt.show()
        try:
            matches = flann.knnMatch(des1,des2,k=2) 
            self.storage.debuglogger(ip=self.storage.ip, desc="Match Check OK", code=200, frame=frame)
        
            matchesMask = [[0,0] for i in range(len(matches))]
            self.storage.debuglogger(ip=self.storage.ip, desc="MatchTask OK", code=200, frame=frame)

            rtn = 0
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.3*n.distance:
                    self.storage.debuglogger(ip=self.storage.ip, desc="Matching "+str(rtn+1), code=200, frame=frame)
                    matchesMask[i]=[1,0]
                    rtn += 1
            
            #if self.storage.debug == True:
            #    draw_params = dict(matchColor = (0,255,0), singlePointColor = (255,0,0), matchesMask = matchesMask, flags = 0)
            #    img3 = self.cv2.drawMatchesKnn(self.storage.thumbnail,kp1,vidimg,kp2,matches,None,**draw_params)
            #    from matplotlib import pyplot as plt
            #    plt.imshow(img3,),plt.show()

            storage.vids.update({str(frame): rtn})
            if str(rtn) in storage.vidsf: storage.vidsf[str(rtn)].append(frame)
            else: storage.vidsf.update({str(rtn): [frame]})
            if rtn in storage.count: pass
            else: storage.count.append(rtn)
            self.storage.debuglogger(ip=self.storage.ip, desc="Append match: "+str(rtn), code=200, frame=frame)
        except:
            self.storage.debuglogger(ip=self.storage.ip, desc="Append match: 0", code=200, frame=frame)
            storage.vids.update({str(frame): 0})
            if str(0) in storage.vidsf: storage.vidsf[str(0)].append(frame)
            else: storage.vidsf.update({str(0): [frame]})
            if 0 in storage.count: pass
            else: storage.count.append(0)

    def vidparse(self):
        from time import time
        starttime = time()
        self.storage.debuglogger(ip=self.storage.ip, desc="LOADED Img Parser", code=200)
        from threading import Thread
        vc = self.cv2.VideoCapture(self.storage.vidpath)
        self.storage.vids = {}
        self.storage.vidsf = {}
        threads = []


        self.storage.debuglogger(ip=self.storage.ip, desc="Clear methods OK", code=200)


        self.storage.debuglogger(ip=self.storage.ip, desc="===== VIDEO INFO =====", code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="VideoID: "+self.storage.vidpath, code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="VideoFPS: "+str(self.storage.fps), code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="Is Opened: "+str(vc.isOpened()), code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="NowFps: "+str(int(vc.get(1))), code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="======================", code=200)
        
        #forfps = int(vc.get(self.cv2.CAP_PROP_FPS)) # Get Video's FPS / Not using
        #if self.storage.debug == True:
        #    print("forfps: "+str(self.storage.fps))
        #    print("isOpened: "+str(vc.isOpened()))
        #    print("Nowfps: "+str(vc.get(1)))
        #    print("\n\n")
        
        

        while True:
            #print("Nowfps: "+str(vc.get(1)))
            ret, img = vc.read()
            
            #if int(vc.get(1)) == 4232: 
            #    from matplotlib import pyplot as plt
            #    plt.imshow(img,),plt.show()
            #    exit()

            #self.storage.debuglogger(ip=self.storage.ip, desc="===== FPS INFO =====", code=200)
            #self.storage.debuglogger(ip=self.storage.ip, desc="VideoFPS: "+str(self.storage.fps), code=200)
            #self.storage.debuglogger(ip=self.storage.ip, desc="NowFps: "+str(int(vc.get(1))), code=200)


            if (int(vc.get(1)) % self.storage.fps == 0): 
                #self.storage.debuglogger(ip=self.storage.ip, desc="===== FPS INFO =====", code=200)
                #self.storage.debuglogger(ip=self.storage.ip, desc="VideoFPS: "+str(self.storage.fps), code=200)
                #elf.storage.debuglogger(ip=self.storage.ip, desc="NowFps: "+str(int(vc.get(1))), code=200)
                #print("Nowfps: "+str(vc.get(1)))
                #if vc.get(1) == 930:
                    #save image
                    #self.cv2.imwrite("test.jpg", img)
                tmp = Thread(target=self.core, args=(self.storage, img, vc.get(1),))
                tmp.daemon = True
                tmp.start()
                threads.append(tmp)
                #self.core(self.storage, img, vc.get(1))
                #self.storage.debuglogger(ip=self.storage.ip, desc="Stauts: True", code=200)
            #else:
                #self.storage.debuglogger(ip=self.storage.ip, desc="Stauts: False", code=200)
            #self.storage.debuglogger(ip=self.storage.ip, desc="====================", code=200)

            if int(vc.get(1)) == int(vc.get(self.cv2.CAP_PROP_FRAME_COUNT)): break

        i = 0
        while True:
            #print(i)
            if i == len(threads): break
            threads[i].join()
            i += 1
        endtime = time()

        self.storage.debuglogger(ip=self.storage.ip, desc="==OpenCV Result==", code=200)
        self.storage.count.sort(reverse=True)
        self.storage.debuglogger(ip=self.storage.ip, desc="ID: {movid}".format(movid=self.storage.ytdldata["id"]), code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="Take Time: {time}".format(time=str(int(endtime-starttime))), code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="\n", code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc=str(self.storage.vids), code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="\n", code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc=str(self.storage.vidsf), code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="\n", code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="{frame} is the best. maches: {maches}".format(frame=self.storage.vidsf[str(self.storage.count[0])][0], maches=self.storage.count[0]), code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc="\n", code=200)
        self.storage.debuglogger(ip=self.storage.ip, desc=str(str(int(self.storage.vidsf[str(self.storage.count[0])][0]/self.storage.fps/60))+":"+str(int(int(self.storage.vidsf[str(self.storage.count[0])][0]/self.storage.fps)-int(self.storage.vidsf[str(self.storage.count[0])][0]/self.storage.fps/60)*60))), code=200)        
        self.storage.debuglogger(ip=self.storage.ip, desc="\n\n", code=200)

        f = open(self.storage.ytdldata["id"]+".jpg", "rb")
        a = f.read()
        f.close()
        return {"frame": self.storage.vidsf[str(self.storage.count[0])][0], "maches": self.storage.count[0], "timestamp": int(self.storage.vidsf[str(self.storage.count[0])][0]/self.storage.fps), "timestampMinSec": str(str(int(self.storage.vidsf[str(self.storage.count[0])][0]/self.storage.fps/60))+":"+str(int(int(self.storage.vidsf[str(self.storage.count[0])][0]/self.storage.fps)-int(self.storage.vidsf[str(self.storage.count[0])][0]/self.storage.fps/60)*60)))}



if __name__ == "__main__":
    import time
    a = time.time()

    tpath = "./testmov/thumbnail_32si5cfrCNc.jpg"
    vpath = "./testmov/32si5cfrCNc.mp4"
    storage = storage(thumbnailpath=tpath, vidpath=vpath)
    storage.opencv.vidparse()

    print(time.time()-a)
    pass