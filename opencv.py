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

        self.sift = self.cv2.xfeatures2d.SIFT_create()
        self.kp1, self.des1 = self.sift.detectAndCompute(self.cv2.imread(storage.thumbnailpath,0),None)

        #SETUP
        pass

    def core(self, storage, vidimg, frame):
        #img = self.cv2.imread(vidimg,0)
        sift = self.sift

        kp1 = self.kp1
        des1 = self.des1
        kp2, des2 = sift.detectAndCompute(vidimg,None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   
        flann = self.cv2.FlannBasedMatcher(index_params,search_params)
        if self.storage.debug == True:
            from matplotlib import pyplot as plt
            plt.imshow(vidimg,),plt.show()
        try:
            matches = flann.knnMatch(des1,des2,k=2)
        
            matchesMask = [[0,0] for i in range(len(matches))]

            a = []
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
                img3 = self.cv2.drawMatchesKnn(self.storage.thumbnail,kp1,vidimg,kp2,matches,None,**draw_params)
                from matplotlib import pyplot as plt
                plt.imshow(img3,),plt.show()

            storage.vids.update({str(frame): rtn})
            if str(rtn) in storage.vids: storage.vidsf[str(rtn)].append(frame)
            else: storage.vidsf.update({str(rtn): [frame]})
        except:
            storage.vids.update({str(frame): 0})
            if str(0) in storage.vidsf: storage.vidsf[str(0)].append(frame)
            else: storage.vidsf.update({str(0): [frame]})

    def imgparse(self):
        from threading import Thread
        vc = self.cv2.VideoCapture(self.storage.vidpath)
        self.storage.vids = {}
        self.storage.vidsf = {}
        threads = []

        forfps = int(vc.get(self.cv2.CAP_PROP_FPS)) # video의 fps 가져옴
        if self.storage.debug == True:
            print("forfps: "+str(forfps))
            print("isOpened: "+str(vc.isOpened()))
            print("Nowfps: "+str(vc.get(1)))
            print("\n\n")
        
        

        while True:
            #print("Nowfps: "+str(vc.get(1)))
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
                #print("Nowfps: "+str(vc.get(1)))
                tmp = Thread(target=self.core, args=(self.storage, img, vc.get(1),))
                tmp.start()
                threads.append(tmp)
                #self.core(self.storage, img, vc.get(1))

            if int(vc.get(1)) == int(vc.get(self.cv2.CAP_PROP_FRAME_COUNT)): break

        i = 0
        while True:
            #print(i)
            if i == len(threads): break
            threads[i].join()
            i += 1
        
        print(self.storage.vids)
        print("\n\n")
        print(self.storage.vidsf)



if __name__ == "__main__":
    import time
    a = time.time()

    tpath = "./testmov/thumbnail_32si5cfrCNc.jpg"
    vpath = "./testmov/32si5cfrCNc.mp4"
    storage = storage(thumbnailpath=tpath, vidpath=vpath)
    storage.opencv.imgparse()

    print(time.time()-a)
    pass