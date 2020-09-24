class storage():
    def __init__(self, thumbnailpath, vidpath):
        self.thumbnailpath = thumbnailpath
        self.vidpath = vidpath
        self.thumbnail = None
        self.opencv = opencv(self)
        self.debug = False

class opencv():
    def __init__(self, storage):
        import cv2
        self.cv2 = cv2
        self.storage = storage

        storage.thumbnail = self.cv2.imread(storage.thumbnailpath,0)
        self.sift = self.cv2.xfeatures2d.SIFT_create()
        self.kp1, self.des1 = self.sift.detectAndCompute(self.storage.thumbnail,None)
        self.vids = {}
        self.vidsf = {}

        #SETUP
        pass

    def core(self, vidimg, frame):
        #img = self.cv2.imread(vidimg,0)

        kp2, des2 = self.sift.detectAndCompute(vidimg,None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   
        flann = self.cv2.FlannBasedMatcher(index_params,search_params)
        if self.storage.debug == True:
            from matplotlib import pyplot as plt
            plt.imshow(vidimg,),plt.show()
        try:
            matches = flann.knnMatch(self.des1,des2,k=2)
        
            matchesMask = [[0,0] for i in range(len(matches))]

            rtn = 0
            for i,(m,n) in enumerate(matches):
                if m.distance < 0.3*n.distance:
                    matchesMask[i]=[1,0]
                    rtn += 1
            
            if self.storage.debug == True:
                draw_params = dict(matchColor = (0,255,0),
                                singlePointColor = (255,0,0),
                                matchesMask = matchesMask,
                                flags = 0)
                img3 = self.cv2.drawMatchesKnn(self.storage.thumbnail,self.kp1,vidimg,kp2,matches,None,**draw_params)
                from matplotlib import pyplot as plt
                plt.imshow(img3,),plt.show()


                self.vids.update({str(frame): rtn})
                if str(rtn) in self.vidsf: self.vidsf[str(rtn)].append(frame)
                else: self.vidsf.update({str(rtn): [frame]})
        except:
            self.vids.update({str(frame): rtn})
            if "0" in self.vidsf: self.vidsf["0"].append(frame)
            else: self.vidsf.update({"0": [frame]})

    def imgparse(self):
        from threading import Thread
        vc = self.cv2.VideoCapture(self.storage.vidpath)
        
        threads = []

        forfps = int(vc.get(self.cv2.CAP_PROP_FPS)) # video의 fps 가져옴
        if self.storage.debug == True:
            print("forfps: "+str(forfps))
            print("isOpened: "+str(vc.isOpened()))
            print("Nowfps: "+str(vc.get(1)))
            print("\n\n")

        while True:
            print("Nowfps: "+str(vc.get(1)))
            ret, img = vc.read()
            
            #if int(vc.get(1)) == 4232: 
            #    from matplotlib import pyplot as plt
            #    plt.imshow(img,),plt.show()
            #    exit()


            if self.storage.debug == True:
                print("forfps: "+str(forfps))
                print("isOpened: "+str(vc.isOpened()))
                print("Nowfps: "+str(vc.get(1)))
                print("\n\n")
            if (int(vc.get(1)) % forfps == 0): 
                print("Nowfps: "+str(vc.get(1)))
                t = Thread(target=self.core, args=(img,int(vc.get(1))))
                t.start()
                threads.append(t)

            if int(vc.get(1)) == int(vc.get(self.cv2.CAP_PROP_FRAME_COUNT)): break
        
        i = 0
        while True:
            if i == len(threads): break
            threads[i].join()
            i += 1
        
        print(self.vids)
        print("\n\n")
        print(self.vidsf)


if __name__ == "__main__":
    tpath = "./testmov/thumbnail_32si5cfrCNc.jpg"
    vpath = "./testmov/32si5cfrCNc.mp4"
    storage = storage(thumbnailpath=tpath, vidpath=vpath)
    storage.opencv.imgparse()


    pass