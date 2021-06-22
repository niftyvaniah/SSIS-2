import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import sqlite3



class SIS(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Student, Course):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Student)

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

        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()

        #FUNCTIONS
        def connectCourse():
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses (Course_Code TEXT PRIMARY KEY, Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def addCourse():
            if Course_Code.get()=="" or Course_Name.get()=="": 
                tkinter.messagebox.showinfo("SSIS", "Please fill up the Box correctly")
            else:
                conn = sqlite3.connect("StudentDatabase.db")
                c = conn.cursor()         
                #Insert Table
                c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",\
                          (Course_Code.get(),Course_Name.get()))        
                conn.commit()           
                conn.close()
                Course_Code.set('')
                Course_Name.set('') 
                tkinter.messagebox.showinfo("SSIS", "Course Recorded Successfully")
                displayCourse()
                
                
              
        def displayCourse():
            treecourse.delete(*treecourse.get_children())
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                treecourse.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def updateCourse():
            for selected in treecourse.selection():
                conn = sqlite3.connect("StudentDatabase.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", \
                            (Course_Code.get(),Course_Name.get(), treecourse.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("SSIS", "Course Updated Successfully")
                displayCourse()
                conn.close()
                
        def editCourse():
            x = treecourse.focus()
            if x == "":
                tkinter.messagebox.showerror("SSIS", "Please select a record from the table.")
                return
            values = treecourse.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def deleteCourse(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("SSIS", "Do you want to permanently delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudentDatabase.db")
                    cur = con.cursor()
                    x = treecourse.selection()[0]
                    id_no = treecourse.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    treecourse.delete(x)
                    tkinter.messagebox.showinfo("SSIS", "Course Deleted Successfully")
                    displayCourse()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("SSIS", "Students are still enrolled in this course")
                
        def searchCourse():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("StudentDatabase.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
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
            Course_Code.set('')
            Course_Name.set('') 

        #LAY-OUT
        #Label and Entry
        
        self.lblCourseCode = Label(self, font=("Palatino Linotype",13,"bold"),fg="#4A6274", text="COURSE CODE:*", padx=5, pady=5)
        self.lblCourseCode.place(x=100,y=260)
        self.txtCourseCode = Entry(self, font=("Poppins", 13), textvariable=Course_Code, width=35)
        self.txtCourseCode.place(x=250,y=265)
        

        self.lblCourseName = Label(self, font=("Palatino Linotype",13,"bold"),fg="#4A6274", text="COURSE NAME:*", padx=5, pady=5)
        self.lblCourseName.place(x=100,y=300)
        self.txtCourseName = Entry(self, font=("Poppins", 13), textvariable=Course_Name, width=35)
        self.txtCourseName.place(x=250,y=305)
        
        self.Search =  Label(self, font=("Palatino Linotype",12,"bold"),fg="#4A6274", text="Search by Course Code", padx=5, pady=5)
        self.Search.place(x=585, y= 165)
        self.SearchBar = Entry(self, font=("Palatino Linotype",12), textvariable=SearchBar_Var, width=29)
        self.SearchBar.place(x=776,y=170)
        self.SearchBar.insert(0,'Course Code')
        

        ## Treeview
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1225,y=255,height=350)

        treecourse = ttk.Treeview(self,
                                        columns=("Course Code","Course Name"),
                                        height = 16,
                                        yscrollcommand=scrollbar.set)

        treecourse.heading("Course Code", text="Course Code", anchor=W)
        treecourse.heading("Course Name", text="Course Name",anchor=W)
        treecourse['show'] = 'headings'

        treecourse.column("Course Code", width=200, anchor=W, stretch=False)
        treecourse.column("Course Name", width=430, stretch=False)


        treecourse.place(x=585,y=255)
        scrollbar.config(command=treecourse.yview)
            
        ## Buttons

        self.btnAddID = Button(self, text="Add", font=('Palatino Linotype', 10), height=1, width=10,
                                bg="#4A6274", fg="snow", command=addCourse)
        self.btnAddID.place(x=460,y=490)
        
        self.btnUpdate = Button(self, text="Update", font=('Palatino Linotype', 10), height=1, width=10,
                                bg="#4A6274", fg="snow", command=updateCourse) 
        self.btnUpdate.place(x=460,y=530)
        
        self.btnClear = Button(self, text="Clear", font=('Palatino Linotype', 10), height=1, width=10,
                                bg="#4A6274", fg="snow", command=clear)
        self.btnClear.place(x=460,y=570)
        
        self.btnDelete = Button(self, text="Delete", font=('Palatino Linotype', 10), height=1, width=10,
                                bg="#4A6274", fg="snow", command=deleteCourse)
        self.btnDelete.place(x=1120,y=210)
        
        self.btnSelect = Button(self, text="Select", font=('Palatino Linotype', 10), height=1, width=10,
                              bg="#4A6274", fg="snow", command=editCourse)
        self.btnSelect.place(x=1020,y=210)
        
        self.btnSearch = Button(self, text="Search", font=('Palatino Linotype', 10), height=1, width=10,
                                bg="#4A6274", fg="snow", command=searchCourse)
        self.btnSearch.place(x=1020,y=170)
        
        self.btnRefresh = Button(self, text="Show All", font=('Palatino Linotype', 10), height=1, width=10,
                              bg="#4A6274", fg="snow", command=Refresh)
        self.btnRefresh.place(x=1120,y=170)
        
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
        Course_Code = StringVar()
        

        def connect():
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS studentdatabase (StudentID  TEXT PRIMARY KEY, Firstname TEXT,\
                        Midname TEXT, Surname TEXT, Course_Code TEXT,\
                        Yearlevel TEXT, Gender TEXT,\
                        FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def addData():
            if StudentID.get() == "" or Firstname.get() == "" or Surname.get() == "" or Course_Code.get() == "" or Yearlevel.get() == "" or Gender.get() == "": 
                tkinter.messagebox.showinfo("SSIS", "Please fill up the Box correctly")
            else:  
                ID = StudentID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("SSIS", "ID is invalid\nIt should be in YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("SSIS", "ID is invalid\nIt should be in YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("SSIS", "ID is invalid\nIt should be in YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("SSIS", "ID is invalid")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("SSIS", "ID is Invalid")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("StudentDatabase.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO studentdatabase(StudentID,Firstname,Midname,Surname,Course_Code,Yearlevel,Gender) VALUES (?,?,?,?,?,?,?)",\
                                              (StudentID.get(),Firstname.get(),Midname.get(),Surname.get(),Course_Code.get(),Yearlevel.get(),Gender.get()))                                      
                                                                       
                                    tkinter.messagebox.showinfo("SSIS", "Student Recorded")
                                    conn.commit() 
                                    clear()
                                    displayData()
                                    conn.close()
                                except:
                                    tkinter.messagebox.showerror("SSIS", "Course Unavailable")
                    else:
                        tkinter.messagebox.showerror("SSIS", "ID is invalid")
                else:
                    tkinter.messagebox.showerror("SSIS", "ID is Invalid")
                 
        def updateData():
            for selected in tree.selection():
                conn = sqlite3.connect("StudentDatabase.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE studentdatabase SET StudentID=?, Firstname=?, Midname=?,Surname=?,Course_Code=?, Yearlevel=?,Gender=?\
                      WHERE StudentID=?", ((StudentID.get(),Firstname.get(),Midname.get(),Surname.get(),Course_Code.get(),Yearlevel.get(),Gender.get(),\
                          tree.set(selected, '#1'))))
                conn.commit()
                tkinter.messagebox.showinfo("SSIS", "Student Information is Updated")
                displayData()
                conn.close()
        
        def deleteData():   
            try:
                messageDelete = tkinter.messagebox.askyesno("SSIS", "Do you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("StudentDatabase.db")
                    cur = con.cursor()
                    x = tree.selection()[0]
                    id_no = tree.item(x)["values"][0]
                    cur.execute("DELETE FROM studentdatabase WHERE StudentID = ?",(id_no,))                   
                    con.commit()
                    tree.delete(x)
                    tkinter.messagebox.showinfo("SSIS", "Student is successfully deleted")
                    displayData()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def searchData():
            StudentID = Searchbar.get()
            try:  
                con = sqlite3.connect("StudentDatabase.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM studentdatabase WHERE StudentID = ?",(StudentID,))
                con.commit()
                tree.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    tree.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("SSIS", "ID is invalid")
            
                
        def displayData():
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("StudentDatabase.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM studentdatabase")
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
            Course_Code.set(values[4])
            Yearlevel.set(values[5])
            Gender.set(values[6])
            
        def Refresh():
            displayData()
        
        def clear():
            StudentID.set('')
            Firstname.set('')
            Midname.set('')
            Surname.set('')
            Course_Code.set('')
            Yearlevel.set('')
            Gender.set('')
            
        ## Label and Entry
        
        self.StudentID = Label(self, font=("Palatino Linotype",14,"bold"),fg="#4A6274", text="STUDENT ID:", padx=5, pady=5)
        self.StudentID.place(x=85,y=170)
        self.StudentIDEntry = Entry(self, font=("Poppins", 13), textvariable=StudentID, width=33)
        self.StudentIDEntry.place(x=260,y=176)
        self.StudentIDEntry.insert(0,'YYYY-NNNN')
        

        self.Firstname = Label(self, font=("Palatino Linotype",14,"bold"),fg="#4A6274", text="FIRST NAME:", padx=5, pady=5)
        self.Firstname.place(x=80,y=210)
        self.FirstnameEntry = Entry(self, font=("Poppins", 13), textvariable=Firstname, width=33)
        self.FirstnameEntry.place(x=260,y=216)

        self.Midname = Label(self, font=("Palatino Linotype",14,"bold"),fg="#4A6274", text="MIDDLE INITIAL:", padx=5, pady=5)
        self.Midname.place(x=80,y=250)
        self.MidnameEntry = Entry(self, font=("Poppins", 13), textvariable=Midname, width=33)
        self.MidnameEntry.place(x=260,y=256)

        self.Surname = Label(self, font=("Palatino Linotype",14,"bold"), fg="#4A6274",text="SURNAME:", padx=5, pady=5)
        self.Surname.place(x=80,y=290)
        self.SurnameEntry = Entry(self, font=("Poppins", 13), textvariable=Surname, width=33)
        self.SurnameEntry.place(x=260,y=296)

        self.Course = Label(self, font=("Palatino Linotype",14,"bold"), fg="#4A6274",text="COURSE:", padx=5, pady=5)
        self.Course.place(x=80,y=330)
        self.CourseEntry = Entry(self, font=("Poppins", 13), textvariable=Course_Code, width=33)
        self.CourseEntry.place(x=260,y=336)
        

        self.StudentYearLevel = Label(self, font=("Palatino Linotype",14,"bold"),fg="#4A6274", text="YEAR LEVEL:", padx=5, pady=5)
        self.StudentYearLevel.place(x=80,y=370)
        self.StudentYearLevelEntry = ttk.Combobox(self,
                                                value=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
                                                state="readonly", font=("Poppins", 13), textvariable=Yearlevel,
                                                width=31)
        self.StudentYearLevelEntry.place(x=260,y=376)
        

        self.Gender = Label(self, font=("Palatino Linotype",14,"bold"),fg="#4A6274", text="GENDER:", padx=5, pady=5)
        self.Gender.place(x=80,y=410)
        self.GenderEntry = ttk.Combobox(self, value=["Male", "Female"], font=("Poppins", 13),
                                             state="readonly", textvariable=Gender, width=31)
        self.GenderEntry.place(x=260,y=416)

        self.Search =  Label(self, font=("Palatino Linotype",13,"bold"),fg="#4A6274", text="Search by ID Number", padx=5, pady=5)
        self.Search.place(x=585, y= 165)
        self.SearchBar = Entry(self, font=("Palatino Linotype",12), textvariable=Searchbar, width=29)
        self.SearchBar.place(x=776,y=170)
        self.SearchBar.insert(0,'YYYY-NNNN')
       
        

        ## Treeview
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1255,y=255,height=350)

        tree = ttk.Treeview(self,
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

        tree.place(x=585,y=255)
        scrollbar.config(command=tree.yview)
        
        ## Buttons
        
        btnAddID = Button(self, text="Add", font=('Poppins', 11), height=1, width=10,
                             bg="#4A6274", fg="snow", command=addData)
        btnAddID.place(x=460,y=490)
        btnAddID.config(cursor= "hand2")
        
        btnUpdate = Button(self, text="Update", font=('Poppins', 11), height=1, width=10,
                             bg="#4A6274", fg="snow", command=updateData)
        btnUpdate.place(x=460,y=530)
        btnUpdate.config(cursor= "hand2")
        
        btnClear = Button(self, text="Clear", font=('Poppins', 11), height=1, width=10,
                             bg="#4A6274", fg="snow", command=clear)
        btnClear.place(x=460,y=570)
        btnClear.config(cursor= "hand2")
        
        btnDelete = Button(self, text="Delete", font=('Poppins', 10), height=1, width=10,
                             bg="#4A6274", fg="snow", command=deleteData)
        btnDelete.place(x=1120,y=210)
        btnDelete.config(cursor= "hand2")
        
        btnSelect = Button(self, text="Select", font=('Poppins', 10), height=1, width=10,
                             bg="#4A6274", fg="snow", command=editData)
        btnSelect.config(cursor= "hand2")
        btnSelect.place(x=1020,y=210)
        
        btnSearch = Button(self, text="Search", font=('Poppins', 10), height=1, width=10,
                                bg="#4A6274", fg="snow", command=searchData)
        btnSearch.place(x=1020,y=170)
        
        btnDisplay = Button(self, text="Show All", font=('Poppins', 10), height=1, width=10,
                             bg="#4A6274", fg="snow", command=Refresh)
        btnDisplay.place(x=1120,y=170)
        btnDisplay.config(cursor= "hand2")
        connect()
        displayData()

ssis = SIS()
ssis.geometry("1355x650+0+0")
ssis.resizable(False,False)
ssis.mainloop()
