from sqlite3.dbapi2 import Error
import unittest
import sqlite3
class Test(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.con = sqlite3.connect("database/database.db")
        self.cur = self.con.cursor()
    def test_Conectiondatabase(self):
        self.cur.execute("select * from teacher")
        gv = self.cur.fetchall()
        self.assertTrue(len(gv)>0)
    def test_login(self):
        self.cur.execute("select people.ID, people.PW from people")
        sv = self.cur.fetchall()
        for i in sv:
            self.assertTrue((len(i) == 2) and None not in i)     # mỗi SV có đủ ID và Pass, Không có trường bị trống
        self.assertTrue((100,100) in sv)                         # Các test thực tế xem có Sv đó trong dữ liệu không
        self.assertTrue((101,101) in sv)
        self.assertTrue((102,102) in sv)
        self.assertTrue((103,103) in sv)
        self.assertFalse((100,101) in sv)
        self.assertFalse(("abc",101) in sv)
        self.assertFalse(("","") in sv)
        self.assertFalse(("100","100") in sv)
        self.cur.execute("select people.PW from people where ID = 99") 
        sv = self.cur.fetchall()
        self.assertFalse(len(sv)==1)
        self.assertTrue(len(sv)==0)
        self.cur.execute("select people.PW from people where ID = 101")
        sv = self.cur.fetchall()
        self.assertTrue(len(sv)==1)
        self.assertTrue(sv[0][0]==101)
    def test_showinfo(self):
        self.cur.execute("select people.ID from people")
        sv = self.cur.fetchall()
        list_sv=[]
        for i in range(0, len(sv)):
            self.cur.execute("select people.MSV,people.NAME,people.CLASS,people.GENDER,people.SDT,people.MAJOR,people.FOLK,people.ADDRESS from people where id = %i"%(sv[i]))
            list_sv.append(self.cur.fetchall())
        for i in list_sv:
            self.assertTrue(len(i[0])==8 and None not in i[0]) # mỗi sinh viên phải có đủ 8 thông tin cơ bản để hiện thị ra màn hình.
    def test_updateinfo(self):
        slst=["Luong Nam","Nam","0123456789","Kinh","Hà Nội"]
        self.cur.execute(
                "UPDATE people SET NAME='"+ str(slst[0])+ "', GENDER='"+ str(slst[1])+ "', SDT='"+ str(slst[2])+ "', FOLK='"+ str(slst[3])+ "', ADDRESS='"+ str(slst[4] + "' WHERE ID= %i"%(100)))
        self.con.commit()
        self.cur.execute("select people.NAME,people.GENDER,people.SDT,people.FOLK,people.ADDRESS from people where ID = 100") 
        list = []
        for i in self.cur.fetchone():
            list.append(i)
        self.assertTrue(list == slst)      #Check thông tin sau khi cập nhật
        with self.assertRaises(IndexError):  # Thiếu thông tin
            slst=["Nam","0123456789","Kinh","Hà Nội"]
            self.cur.execute(
                "UPDATE people SET NAME='"+ str(slst[0])+ "', GENDER='"+ str(slst[1])+ "', SDT='"+ str(slst[2])+ "', FOLK='"+ str(slst[3])+ "', ADDRESS='"+ str(slst[4] + "' WHERE ID= %i"%(100)))
            self.con.commit()
  

            
            
if __name__ == '__main__':
    unittest.main(verbosity=2)