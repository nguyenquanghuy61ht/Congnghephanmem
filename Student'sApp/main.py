import Frame1, Frame2, threading, firebase
from tkinter import *


def main():
    thr1 = threading.Thread(name="Thread-1", target=firebase.dowloadDtb)
    thr2 = threading.Thread(name="Thread-2", target=firebase.dowloadTrainingData)
    thr1.start()
    thr2.start()
    root = Tk()
    mg = Frame1.Frame1(root)
    root.mainloop()
    firebase.uploadDtb()
    firebase.uploadTrainingData()


##Tạm tắt tải lên xuống file training vì tải vài lần là hết sạch cloud

if __name__ == "__main__":
    main()
