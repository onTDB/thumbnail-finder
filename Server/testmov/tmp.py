class Storage():
    def __init__(self):
        self.tmpapp = []

        from threading import Thread
        p = Thread(target=testsub, args=(self,))
        p.start()
        p.join()

        print (self.tmpapp)

    def asd(self):
        self.tmpapp.append("asdasd")
        print("aa", self.tmpapp)

class testsub():
    def __init__(self, storage):
        storage.tmpapp.append("asdasd")
        print("aa", storage.tmpapp)

if __name__ == "__main__":
    s = Storage()
    pass