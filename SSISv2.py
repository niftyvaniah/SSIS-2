import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import sqlite3



class SSIS(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Course, Student):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Course)

    def show_frame(self, page_number):

        frame = self.frames[page_number]
        frame.tkraise()
    


       


class Course(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Student Information System")
        centercolor = tk.Label(self,height = 7,width=600, bg="#4A6274")
        centercolor.place(x=0,y=5)

    
        titleheading = tk.Label(self, text="S T U D E N T   I N F O R M A T I O N   S Y S T E M", font=("Palatino Linotype",35,"bold"),bd=0,
                            bg="#4A6274",
                            fg="snow",)
        titleheading.place(x=120,y=10)

        
        #BUTTONS
        Coursebutton = tk.Button(self, text="Course",font=("Palatino Linotype",13,"bold"),bd=0,
                            width = 10,
                            bg="#4A6274",
                            fg="#E2725A",
                            command=lambda: controller.show_frame(Course))
        Coursebutton.place(x=10,y=75)
        Coursebutton.config(cursor= "hand2")
        
        Studbutton= tk.Button(self, text="Student",font=("Palatino Linotype",13,"bold"),bd=0,
                            width = 10,
                            bg="#4A6274",
                            fg="snow",
                            command=lambda: controller.show_frame(Student))
        Studbutton.place(x=100,y=75)
        Studbutton.config(cursor= "hand2")

        CourseCode = StringVar()
        CourseName = StringVar()
        SearchBarVar = StringVar()

        #FUNCTIONS
        def connectCourse():
            conn = sqlite3.connect("Student.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (CourseCode TEXT PRIMARY KEY, CourseName TEXT)") 
            conn.commit() 
            conn.close()
            
        def addCourse():
            if CourseCode.get()=="" or CourseName.get()=="": 
                tkinter.messagebox.showinfo("Student Information System", "Please fill up the Box correctly")
            else:
                conn = sqlite3.connect("Student.db")
                c = conn.cursor()         
                #Insert Table
                c.execute("INSERT INTO courses(CourseCode,CourseName) VALUES (?,?)",\
                          (CourseCode.get(),CourseName.get()))        
                conn.commit()           
                conn.close()
                CourseCode.set('')
                CourseName.set('') 
                tkinter.messagebox.showinfo("Student Information System", "Course Recorded Successfully")
                displayCourse()
                
                
              
        def displayCourse():
            treecourse.delete(*treecourse.get_children())
            conn = sqlite3.connect("Student.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                treecourse.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def updateCourse():
            for selected in treecourse.selection():
                conn = sqlite3.connect("Student.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET CourseCode=?, CourseName=? WHERE CourseCode=?", \
                            (CourseCode.get(),CourseName.get(), treecourse.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("Student Information System", "Course Updated Successfully")
                displayCourse()
                conn.close()
                
        def editCourse():
            x = treecourse.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a record from the table.")
                return
            values = treecourse.item(x, "values")
            CourseCode.set(values[0])
            CourseName.set(values[1])
                    
        def deleteCourse(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("Student Information System", "Do you want to permanently delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("Student.db")
                    cur = con.cursor()
                    x = treecourse.selection()[0]
                    id_no = treecourse.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE CourseCode = ?",(id_no,))                   
                    con.commit()

                    treecourse.delete(x)
                    tkinter.messagebox.showinfo("Student Information System", "Course Deleted Successfully")
                    displayCourse()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("Student Information System", "Students are still enrolled in this course")
                
        def searchCourse():
            CourseCode = SearchBarVar.get()                
            con = sqlite3.connect("Student.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE CourseCode = ?",(CourseCode,))
            con.commit()
            treecourse.delete(*treecourse.get_children())
            rows = cur.fetchall()
            for row in rows:
                treecourse.insert("", tk.END, text=row[0], values=row[0:])
            con.close()
 
        def Refresh():
            pass
            displayCourse()
        
        def clear():
            CourseCode.set('')
            CourseName.set('') 

        #Frames

        ManageFrame=Frame(self, relief =RIDGE, bg="#4A6274")
        ManageFrame.place(x=30, y=130,width=530, height=500)
        
        DisplayFrame=Frame(self, relief =RIDGE, bg="#4A6274")
        DisplayFrame.place(x=580, y=130,width=730, height=500)

        
        #Label and Entry
        
        self.lblCourseCode = Label(ManageFrame, font=("Palatino Linotype",15,"bold"),fg="snow", bg="#4A6274", text="COURSE CODE:", padx=5, pady=5)
        self.lblCourseCode.place(x=10,y=126)
        self.txtCourseCode = Entry(ManageFrame, font=("Poppins", 13), textvariable=CourseCode, width=37)
        self.txtCourseCode.place(x=180,y=132)
        

        self.lblCourseName = Label(ManageFrame, font=("Palatino Linotype",15,"bold"),fg="snow", bg="#4A6274", text="COURSE NAME:", padx=5, pady=5)
        self.lblCourseName.place(x=10,y=160)
        self.txtCourseName = Entry(ManageFrame, font=("Poppins", 13), textvariable=CourseName, width=37)
        self.txtCourseName.place(x=180,y=166)
        
        self.Search =  Label(DisplayFrame, font=("Palatino Linotype",13,"bold"),fg="snow", bg="#4A6274", text="Search by Course Code", padx=5, pady=5)
        self.Search.place(x=15, y= 40)
        self.SearchBar = Entry(DisplayFrame, font=("Poppins",12), textvariable=SearchBarVar, width=25)
        self.SearchBar.place(x=220,y=45)
        self.SearchBar.insert(0,'Course Code')
        

        ## Treeview
        
        scrollbar = Scrollbar(DisplayFrame, orient=VERTICAL)
        scrollbar.place(x=670,y=120,height=350)

        treecourse = ttk.Treeview(DisplayFrame,
                                        columns=("Course Code","Course Name"),
                                        height = 16,
                                        yscrollcommand=scrollbar.set)

        treecourse.heading("Course Code", text="Course Code", anchor=W)
        treecourse.heading("Course Name", text="Course Name",anchor=W)
        treecourse['show'] = 'headings'

        treecourse.column("Course Code", width=200, anchor=W, stretch=False)
        treecourse.column("Course Name", width=430, stretch=False)


        treecourse.place(x=30,y=120)
        scrollbar.config(command=treecourse.yview)
            
        ## Buttons

        self.btnAddID = Button(ManageFrame, text="Add", font=('Poppins', 10, "bold"), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=addCourse)
        self.btnAddID.place(x=400,y=280)
        
        self.btnUpdate = Button(ManageFrame, text="Update", font=('Poppins', 10, "bold"), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=updateCourse) 
        self.btnUpdate.place(x=400,y=320)
        
        self.btnClear = Button(ManageFrame, text="Clear", font=('Poppins', 10,"bold"), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=clear)
        self.btnClear.place(x=400,y=360)
        
        self.btnDelete = Button(DisplayFrame, text="Delete", font=('Poppins', 10, "bold"), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=deleteCourse)
        self.btnDelete.place(x=600,y=80)
        
        self.btnSelect = Button(DisplayFrame, text="Select", font=('Poppins', 10, "bold"), height=1, width=10,
                              bg="#DFE6E9", fg="#4A6274", command=editCourse)
        self.btnSelect.place(x=500,y=80)
        
        self.btnSearch = Button(DisplayFrame, text="Search", font=('Poppins', 10, "bold"), height=1, width=10,
                               bg="#DFE6E9", fg="#4A6274", command=searchCourse)
        self.btnSearch.place(x=500,y=40)
        
        self.btnRefresh = Button(DisplayFrame, text="Show All", font=('Poppins', 10, "bold"), height=1, width=10,
                              bg="#DFE6E9", fg="#4A6274", command=Refresh)
        self.btnRefresh.place(x=600,y=40)
        
        connectCourse()
        displayCourse()
        
        
        
        
        
        

class Student(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("Student Information System")
        centercolor = tk.Label(self,height = 7,width=600, bg="#4A6274")
        centercolor.place(x=0,y=5)
        apptitle = tk.Label(self, text="S T U D E N T   I N F O R M A T I O N   S Y S T E M", font=("Palatino Linotype",35,"bold"),bd=0,
                            bg="#4A6274",
                            fg="snow",)
        apptitle.place(x=120,y=10)

        #buttons
        Coursebutton = tk.Button(self, text="Course",font=("Palatino Linotype",13,"bold"),bd=0,
                                width = 10,
                                bg="#4A6274",
                                fg="snow",
                                command=lambda: controller.show_frame(Course))
        Coursebutton.place(x=10,y=75)
        Coursebutton.config(cursor= "hand2")
            
        Studbutton= tk.Button(self, text="Student",font=("Palatino Linotype",13,"bold"),bd=0,
                                width = 10,
                                bg="#4A6274",
                                fg="#E2725A",
                                command=lambda: controller.show_frame(Student))
        Studbutton.place(x=100,y=75)
        Studbutton.config(cursor= "hand2")

         ## Functions
        StudentID= StringVar()
        Firstname = StringVar()
        Midname = StringVar()
        Surname = StringVar()
        Yearlevel = StringVar()
        Gender = StringVar()
        Searchbar=StringVar()
        CourseCode = StringVar()
        

        def connect():
            conn = sqlite3.connect("Student.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS student (StudentID  TEXT PRIMARY KEY, Firstname TEXT,\
                        Midname TEXT, Surname TEXT, CourseCode TEXT,\
                        Yearlevel TEXT, Gender TEXT,\
                        FOREIGN KEY(CourseCode) REFERENCES courses(CourseCode) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def addData():
            if StudentID.get() == "" or Firstname.get() == "" or Surname.get() == "" or CourseCode.get() == "" or Yearlevel.get() == "" or Gender.get() == "": 
                tkinter.messagebox.showinfo("Student Information System", "Please fill up the Box correctly")
            else:  
                ID = StudentID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("Student Information System", "ID is invalid\nIt should be in YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("Student Information System", "ID is invalid\nIt should be in YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("Student Information System", "ID is invalid\nIt should be in YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "ID is invalid")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "ID is Invalid")
                                except:
                                    pass
                            else:
                                #try:
                                conn = sqlite3.connect("Student.db")
                                c = conn.cursor() 
                                c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                c.execute("INSERT INTO student(StudentID,Firstname,Midname,Surname,CourseCode,Yearlevel,Gender) VALUES (?,?,?,?,?,?,?)",\
                                              (StudentID.get(),Firstname.get(),Midname.get(),Surname.get(),CourseCode.get(),Yearlevel.get(),Gender.get()))                                      
                                                                       
                                tkinter.messagebox.showinfo("Student Information System", "Student Recorded")
                                conn.commit() 
                                clear()
                                displayData()
                                conn.close()
                                #except:
                                    #
                                    #tkinter.messagebox.showerror("Student Information System", "ID is Invalid")
                    else:
                        tkinter.messagebox.showerror("Student Information System", "ID is invalid")
                else:
                    tkinter.messagebox.showerror("Student Information System", "ID is Invalid")
                 
        def updateData():
            for selected in tree.selection():
                conn = sqlite3.connect("Student.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE student SET StudentID=?, Firstname=?, Midname=?,Surname=?,CourseCode=?, Yearlevel=?,Gender=?\
                      WHERE StudentID=?", ((StudentID.get(),Firstname.get(),Midname.get(),Surname.get(),CourseCode.get(),Yearlevel.get(),Gender.get(),\
                          tree.set(selected, '#1'))))
                conn.commit()
                tkinter.messagebox.showinfo("Student Information System", "Student Information is Updated")
                displayData()
                conn.close()
        
        def deleteData():   
            try:
                messageDelete = tkinter.messagebox.askyesno("Student Information System", "Do you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("Student.db")
                    cur = con.cursor()
                    x = tree.selection()[0]
                    id_no = tree.item(x)["values"][0]
                    cur.execute("DELETE FROM student WHERE StudentID = ?",(id_no,))                   
                    con.commit()
                    tree.delete(x)
                    tkinter.messagebox.showinfo("Student Information System", "Student is successfully deleted")
                    displayData()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def searchData():
            StudentID = Searchbar.get()
            try:  
                con = sqlite3.connect("Student.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM student WHERE StudentID = ?",(StudentID,))
                con.commit()
                tree.delete(*tree.get_children())
                rows = cur.fetchall()
                for row in rows:
                    tree.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("Student Information System", "ID is invalid")
            
                
        def displayData():
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("Student.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            for row in rows:
                tree.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
                            
        def editData():
            x = tree.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a record from the table.")
                return
            values = tree.item(x, "values")
            StudentID.set(values[0])
            Firstname.set(values[1])
            Midname.set(values[2])
            Surname.set(values[3])
            CourseCode.set(values[4])
            Yearlevel.set(values[5])
            Gender.set(values[6])
            
        def Refresh():
            displayData()
        
        def clear():
            StudentID.set('')
            Firstname.set('')
            Midname.set('')
            Surname.set('')
            CourseCode.set('')
            Yearlevel.set('')
            Gender.set('')

        con = sqlite3.connect("Student.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM courses")
        books = cur.fetchall()
        bookid = []
        for book in books:
             bookid.append(book[0])

        ManageFrame=Frame(self, relief =RIDGE, bg="#4A6274")
        ManageFrame.place(x=30, y=130,width=530, height=500)
        
        DisplayFrame=Frame(self, relief =RIDGE, bg="#4A6274")
        DisplayFrame.place(x=580, y=130,width=750, height=500)
            
        ## Label and Entry
        
        self.StudentID = Label(ManageFrame, font=("Palatino Linotype",14,"bold"),fg="snow", bg="#4A6274", text="STUDENT ID:", padx=5, pady=5)
        self.StudentID.place(x=20,y=30)
        self.StudentIDEntry = Entry(ManageFrame, font=("Poppins", 13), textvariable=StudentID, width=35)
        self.StudentIDEntry.place(x=200,y=36)
        self.StudentIDEntry.insert(0,'YYYY-NNNN')
        

        self.Firstname = Label(ManageFrame, font=("Palatino Linotype",14,"bold"),fg="snow", bg="#4A6274", text="FIRST NAME:", padx=5, pady=5)
        self.Firstname.place(x=20,y=70)
        self.FirstnameEntry = Entry(ManageFrame, font=("Poppins", 13), textvariable=Firstname, width=35)
        self.FirstnameEntry.place(x=200,y=76)

        self.Midname = Label(ManageFrame, font=("Palatino Linotype",14,"bold"),fg="snow", bg="#4A6274", text="MIDDLE INITIAL:", padx=5, pady=5)
        self.Midname.place(x=20,y=110)
        self.MidnameEntry = Entry(ManageFrame, font=("Poppins", 13), textvariable=Midname, width=35)
        self.MidnameEntry.place(x=200,y=116)

        self.Surname = Label(ManageFrame, font=("Palatino Linotype",14,"bold"),fg="snow", bg="#4A6274",text="SURNAME:", padx=5, pady=5)
        self.Surname.place(x=20,y=150)
        self.SurnameEntry = Entry(ManageFrame, font=("Poppins", 13), textvariable=Surname, width=35)
        self.SurnameEntry.place(x=200,y=156)

        self.Course = Label(ManageFrame, font=("Palatino Linotype",14,"bold"), fg="snow", bg="#4A6274",text="COURSE:", padx=5, pady=5)
        self.Course.place(x=20,y=190)
        self.CourseEntry =ttk.Combobox(ManageFrame,
                                                value=bookid,
                                                state="readonly", font=("Poppins", 13), textvariable=CourseCode, width=33)
        self.CourseEntry.place(x=200,y=196)
        

        self.StudentYearLevel = Label(ManageFrame, font=("Palatino Linotype",14,"bold"),fg="snow", bg="#4A6274", text="YEAR LEVEL:", padx=5, pady=5)
        self.StudentYearLevel.place(x=20,y=230)
        self.StudentYearLevelEntry = ttk.Combobox(ManageFrame,
                                                value=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
                                                state="readonly", font=("Poppins", 13), textvariable=Yearlevel,
                                                width=33)
        self.StudentYearLevelEntry.place(x=200,y=236)
        

        self.Gender = Label(ManageFrame, font=("Palatino Linotype",14,"bold"),fg="snow", bg="#4A6274", text="GENDER:", padx=5, pady=5)
        self.Gender.place(x=20,y=270)
        self.GenderEntry = ttk.Combobox(ManageFrame, value=["Male", "Female"], font=("Poppins", 13),
                                             state="readonly", textvariable=Gender, width=33)
        self.GenderEntry.place(x=200,y=276)

        self.Search =  Label(DisplayFrame, font=("Palatino Linotype",13,"bold"),fg="snow", bg="#4A6274", text="Search by ID Number", padx=5, pady=5)
        self.Search.place(x=15, y= 40)
        self.SearchBar = Entry(DisplayFrame, font=("Palatino Linotype",12), textvariable=Searchbar, width=29)
        self.SearchBar.place(x=220,y=45)
        self.SearchBar.insert(0,'YYYY-NNNN')
       
        

        ## Treeview
        
        scrollbar = Scrollbar(DisplayFrame, orient=VERTICAL)
        scrollbar.place(x=700,y=120,height=350)

        tree = ttk.Treeview(DisplayFrame,
                            columns=("ID Number", "First Name","Mid Initial","Surname", "Course", "Year Level", "Gender"),
                            height = 16,
                            yscrollcommand=scrollbar.set)

        tree.heading("ID Number", text="ID Number", anchor="center")
        tree.heading("First Name", text="First Name",anchor="center")
        tree.heading("Mid Initial", text="M.I.",anchor="center")
        tree.heading("Surname", text="Surname",anchor="center")
        tree.heading("Course", text="Course",anchor="center")
        tree.heading("Year Level", text="Year Level",anchor="center")
        tree.heading("Gender", text="Gender",anchor="center")
        tree['show'] = 'headings'

        tree.column("ID Number", width=100, anchor=W, stretch=False)
        tree.column("First Name", width=100, stretch=False)
        tree.column("Mid Initial", width=50, stretch=False)
        tree.column("Surname", width=80, stretch=False)
        tree.column("Course", width=130, anchor=W, stretch=False)
        tree.column("Year Level", width=100, anchor=W, stretch=False)
        tree.column("Gender", width=100, anchor=W, stretch=False)

        tree.place(x=30,y=120)
        scrollbar.config(command=tree.yview)
        
        ## Buttons
        
        btnAddID = Button(ManageFrame, text="Add", font=('Poppins', 11, "bold"), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=addData)
        btnAddID.place(x=400,y=320)
        btnAddID.config(cursor= "hand2")
        
        btnUpdate = Button(ManageFrame, text="Update", font=('Poppins', 11, "bold"), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=updateData)
        btnUpdate.place(x=400,y=360)
        btnUpdate.config(cursor= "hand2")
        
        btnClear = Button(ManageFrame, text="Clear", font=('Poppins', 11, "bold"), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=clear)
        btnClear.place(x=400,y=400)
        btnClear.config(cursor= "hand2")
        
        btnDelete = Button(DisplayFrame, text="Delete", font=('Poppins', 10, "bold"), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=deleteData)
        btnDelete.place(x=600,y=80)
        btnDelete.config(cursor= "hand2")
        
        btnSelect = Button(DisplayFrame, text="Select", font=('Poppins', 10,"bold"), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=editData)
        btnSelect.config(cursor= "hand2")
        btnSelect.place(x=500,y=80)
        
        btnSearch = Button(DisplayFrame, text="Search", font=('Poppins', 10,"bold"), height=1, width=10,
                                bg="#DFE6E9", fg="#4A6274", command=searchData)
        btnSearch.place(x=500,y=40)
        
        btnDisplay = Button(DisplayFrame, text="Show All", font=('Poppins', 10,"bold"), height=1, width=10,
                             bg="#DFE6E9", fg="#4A6274", command=Refresh)
        btnDisplay.place(x=600,y=40)
        btnDisplay.config(cursor= "hand2")
        connect()
        displayData()

ssis = SSIS()
ssis.geometry("1355x650+0+0")
ssis.resizable(False,False)
ssis.mainloop()
