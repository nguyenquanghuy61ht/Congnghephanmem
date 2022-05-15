import sqlite3, os, Frame1, MyMainException, cv2, time, firebase, threading
from tkinter import Frame, Tk, Button, Label, Entry, ttk, messagebox
from PIL import Image, ImageTk

onlTime = 0
ClassStatus = 0


class Frame2:
    def __init__(self, master):
        self.__master = master
        self.__frame2 = Frame(master)
        threading.Thread(target=self.__getOnlTime).start()
        self.__camOn = 0
        self.__config()

    def __getOnlTime(self):
        global onlTime
        try:
            onlTime = firebase.getTime(Frame1.MyID)
        except:
            onlTime = 0

    def forget(self):
        self.__frame2.forget()

    def __config(self):
        img = ImageTk.PhotoImage(
            file=os.path.join(os.getcwd(), r"resource\bgframe2.png")
        )
        Tlg = ImageTk.PhotoImage(file=os.path.join(os.getcwd(), r"resource\tlogo.png"))
        bg = Label(self.__frame2, image=img)
        bg.image_names = img
        bg.place(x=-2, y=0)
        tlabel = Label(self.__frame2, image=Tlg)
        tlabel.image_names = Tlg
        tlabel.place(x=8, y=8)

        Button(
            self.__frame2,
            text="Đăng xuất",
            fg="red",
            font=("Arial", 15, "bold"),
            width=23,
            borderwidth=4,
            command=self.__SignOut,
        ).place(x=10, y=185)

        imgbt = ImageTk.PhotoImage(file=os.getcwd() + r"\resource\q.png")
        bt1 = Button(
            self.__frame2,
            text="Điểm danh",
            font=("Arial", 20, "bold"),
            width=283,
            height=50,
            image=imgbt,
            compound="center",
            command=self.__Attendance,
        )
        bt1.image_names = imgbt
        bt1.place(x=10, y=243)

        bt2 = Button(
            self.__frame2,
            text="Thông tin chi tiết",
            font=("Arial", 20, "bold"),
            width=283,
            height=50,
            image=imgbt,
            compound="center",
           
        )
        bt2.image_names = imgbt
        bt2.place(x=10, y=315)

        bt3 = Button(
            self.__frame2,
            text="Sửa thông tin",
            font=("Arial", 20, "bold"),
            width=283,
            height=50,
            image=imgbt,
            compound="center",
        )
        bt3.image_names = imgbt
        bt3.place(x=10, y=387)

        bt4 = Button(
            self.__frame2,
            text="Chương trình đào tạo",
            font=("Arial", 20, "bold"),
            width=283,
            height=50,
            image=imgbt,
            compound="center",
        )
        bt4.image_names = imgbt
        bt4.place(x=10, y=459)

        bt5 = Button(
            self.__frame2,
            text="Comming Soon",
            font=("Arial", 20, "bold"),
            width=283,
            height=50,
            image=imgbt,
            compound="center",
            command=self.__CommingSoon,
        )
        bt5.image_names = imgbt
        bt5.place(x=10, y=531)

    def pack(self):
        self.__frame2.pack(fill="both", expand=1)

    def __SignOut(self):
        if self.__camOn == 0:
            self.__master.unbind("<Return>")
            Frame1.MyID = None
            self.__frame2.forget()
            self.__frame1 = Frame1.Frame1(self.__master)
            self.__frame1.pack()
        else:
            messagebox.showwarning("Error", "Bạn chưa rời lớp học")

    

    

    def __Attendance(self):
        threading.Thread(target=self.__getClassStatus).start()
        global onlTime
        self.__master.unbind("<Return>")
        frame4 = Frame(self.__frame2, width=684, height=585)
        frame4.place(x=310, y=10)
        imgl = ImageTk.PhotoImage(file=os.getcwd() + r"\resource\atlg1.jpg")
        lb = Label(frame4, image=imgl)
        lb.image_names = imgl
        lb.place(x=0, y=0)
        Button(
            frame4,
            text="Join",
            font=("Arial", 15, "bold"),
            fg="Green",
            command=self.__joinClass,
        ).place(x=300, y=265)

    def __joinClass(self):
        self.__startime = self.__endtime = onlTime + time.time()
        threading.Thread(target=self.__getClassStatus).start()
        global ClassStatus
        if int(ClassStatus) == 1:
            frame5 = Frame(self.__frame2, width=684, height=585, bg="White")
            frame5.place(x=310, y=10)
            lb = Label(frame5)
            lb.place(x=20, y=0)
            self.__camOn = 1
            Button(
                frame5,
                text="Leave",
                font=("Arial", 20, "bold"),
                fg="Red",
                command=self.__leaveClass,
            ).place(x=290, y=500)

            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            threading.Thread(
                name="Thread-1",
                target=recognizer.read(os.getcwd() + r"\recognizer\trainingData.yml"),
            ).start()
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
            listID = []
            self.__showFrame(lb, cap, face_cascade, recognizer, listID)
        else:
            messagebox.showinfo("Thông báo", "Lớp học chưa bắt đầu")

    def __showFrame(self, lb, cap, face_cascade, recognizer, listID):
        threading.Thread(target=self.__getClassStatus).start()
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray)
        for (x, y, w, h) in face:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y : y + h, x : x + w]
            id, tl = recognizer.predict(roi_gray)
            listID.append(id)
            if len(listID) == 100:
                if listID.count(int(Frame1.MyID)) < 10:
                    messagebox.showwarning(
                        "EDAT",
                        "Bạn đã bị kick khỏi lớp do thông tin nhận dạng không đúng",
                    )
                    self.__leaveClass()
                listID = []
            if tl < 85:
                cv2.putText(
                    frame,
                    str(id),
                    (x + 10, y - 10),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (0, 0, 255),
                    2,
                )
        imgtk = ImageTk.PhotoImage(
            Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        )
        lb.config(image=imgtk)
        lb.image_names = imgtk
        global onlTime
        t = self.__endtime - self.__startime + onlTime
        if (round(t, 1) - 0.5) % 10 == 0 and t != 0:
            threading.Thread(target=firebase.updateTime(Frame1.MyID, t)).start()
        self.__endtime = onlTime + time.time()

        global ClassStatus
        if int(ClassStatus) == 0:
            onlTime = 0
            messagebox.showinfo("Thông báo", "Lớp học đã kết thúc")
            self.__leaveClass()
        elif self.__camOn == 1:
            lb.after(
                10, lambda: self.__showFrame(lb, cap, face_cascade, recognizer, listID)
            )

    def __leaveClass(self):
        global ClassStatus
        if int(ClassStatus) == 1:
            global onlTime
            onlTime = int(self.__endtime - self.__startime + onlTime)
        self.__camOn = 0
        cv2.destroyAllWindows()
        self.__Attendance()

    def __getClassStatus(self):
        global ClassStatus
        ClassStatus = int(firebase.getClassStatus())

    def __CommingSoon(self):
        self.__master.unbind("<Return>")
        self.__config()


"""root = Tk()
t = Frame2(root)
root.mainloop()"""
