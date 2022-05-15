from tkinter import messagebox


class IDException(Exception):
    def __init__(self, id) -> None:
        self.__id = id

    def warning(self):
        if len(self.__id) == 0:
            messagebox.showwarning("Error", "ID không được để trống")
        elif len(self.__id) > 10:
            messagebox.showwarning("Error", "ID không được dài hơn 10")
        elif not self.__id.isdigit():
            messagebox.showwarning("Error", "ID không được chứa kí tự")

    def __str__(self):
        return str(self.__id)


class PWException(Exception):
    def __init__(self, pw) -> None:
        self.__pw = pw

    def warning(self):
        if len(self.__pw) == 0:
            messagebox.showwarning("Error", "PW không được để trống")
        elif len(self.__pw) > 10:
            messagebox.showwarning("Error", "PW không được dài hơn 10")
        elif not self.__pw.isdigit():
            messagebox.showwarning("Error", "PW không được chứa kí tự")

    def __str__(self):
        return str(self.__pw)


class ReEnterPWException(Exception):
    def __init__(self, pw) -> None:
        self.__pw = pw

    def warning(self):
        if self.__pw.endswith("@notmatch@"):
            messagebox.showwarning("Error", "Nhập lại mật khẩu không khớp")
        else:
            messagebox.showwarning("Error", "Hãy nhập lại mật khẩu")

    def __str__(self):
        return str(self.__pw)





def checkID(id):
    if len(id) > 10 or len(id) == 0 or not id.isdigit():
        raise IDException(id)


def checkPW(pw):
    if len(pw) > 10 or len(pw) == 0 or not pw.isdigit():
        raise PWException(pw)




def checkReEnterPass(p1, p2):
    if p2 == "":
        raise ReEnterPWException(p2)
    elif p1 != p2:
        raise ReEnterPWException(p2 + "@notmatch@")





