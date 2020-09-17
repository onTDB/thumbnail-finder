class opencv():
    def __init__(self, storage, thumbnail):
        import cv2
        import numpy
        self.cv2 = cv2
        self.storage = storage
        self.thumbnail = self.cv2.imread(vidimg,0)
        
        pass

    def core(self, vidimg):
        #img = self.cv2.imread(vidimg,0)
        sift = self.cv2.xfeatures2d.SIFT_create()

        kp1, des1 = sift.detectAndCompute(self.thumbnail,None)
        kp2, des2 = sift.detectAndCompute(img2,None)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   
        flann = self.cv2.FlannBasedMatcher(index_params,search_params)
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
            img3 = self.cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
            from matplotlib import pyplot as plt
            plt.imshow(img3,),plt.show()

        return rtn

    def imgparse(self, video):
        vc = self.cv2.VideoCapture(video)
        while (vc.isOpened()):
            ret, img = vc.read()
            if (int(vidcap.get(1) % 10 == 0):
                self.core(img)
