'''
Programmer : Joelle Kabaka Kuyula
Student number : KXLC9ZWQ1
This program helps to capture and process faults reported on the database .
'''


from tkinter import *
from tkinter import messagebox
import sqlite3

class Main():
    def __init__(self,master):
        self.master = master
        master.geometry("644x377")
        master.title("Fault management")

        # Radiobutton variable
        self.var = IntVar()

        def selection():
            choice = self.var.get()
            m = ""
            if choice == 1:
                m = 'Male'
            elif choice == 2:
                m = 'Female'
            return m

        def display_faults():
            faults = Faults()
            faults.display(master)

        def submit_fault():
            first_name = self.f_name.get()
            last_name = self.l_name.get()
            contact = self.c_number.get()
            apartment = self.apartment.get()
            report_date = self.r_date.get()
            unit = self.unit.get()
            gender = selection()
            fault = self.fault.get()

            # Clear all text boxes
            self.f_name.delete(0, END)
            self.l_name.delete(0, END)
            self.c_number.delete(0, END)
            self.apartment.delete(0, END)
            self.r_date.delete(0, END)
            self.unit.delete(0, END)
            self.fault.delete(0, END)

            try:
                if(first_name =="" or last_name =="" or contact =="" or apartment =="" or report_date =="" or unit =="" or gender =="" or fault ==""):
                    raise Exception()
                else:
                    insert = DBConn()
                    insert.submit(first_name, last_name, contact, apartment, report_date, unit, gender, fault)
            except:
                msg = 'Error: Please enter all the required values'
                messagebox.showinfo('Error', msg,icon="warning")



        # Create labels and text boxes
        self.f_name = Label(root, text="First Name:")
        self.f_name.grid(column=0, row=1)
        self.f_name = Entry(root, bd=3)
        self.f_name.grid(column=1, row=1, padx=10, pady=5, ipadx=100)

        self.l_name= Label(root, text="Last Name:")
        self.l_name.grid(column=0, row=2)
        self.l_name = Entry(root, bd=3)
        self.l_name.grid(column=1, row=2, padx=10, pady=5, ipadx=100)

        self.c_number = Label(root, text="Contact Number:")
        self.c_number.grid(column=0, row=3)
        self.c_number= Entry(root, bd=3)
        self.c_number.grid(column=1, row=3, padx=10, pady=5, ipadx=100)

        self.apartment = Label(root, text="Apartment:")
        self.apartment.grid(column=0, row=4)
        self.apartment = Entry(root, bd=3)
        self.apartment.grid(column=1, row=4, padx=10, pady=5, ipadx=100)

        self.r_date = Label(root, text="Report_Date:")
        self.r_date.grid(column=0, row=5)
        self.r_date = Entry(root, bd=3)
        self.r_date.grid(column=1, row=5, padx=10, pady=5, ipadx=100)

        self.unit = Label(root, text="Unit:", )
        self.unit.grid(column=0, row=6)
        self.unit = Entry(root, bd=3)
        self.unit.grid(column=1, row=6, padx=10, pady=5, ipadx=100)

        self.gender = Label(root, text="Gender:", justify="left")
        self.gender.grid(column=0, row=7)
        self.male = Radiobutton(root, text="Male",bg='white', variable= self.var, value=1,command=selection)
        self.female = Radiobutton(root, text="Female",bg='white', variable=self.var, value=2,command=selection)
        self.male.place(x=150, y=200)
        self.female.place(x=300, y=200)

        self.fault = Label(root, text="Fault:")
        self.fault.grid(column=0, row=8)
        self.fault = Entry(root, bd=3)
        self.fault.grid(column=1, row=8, padx=10, pady=10, ipadx=100, ipady=40)

        # Create a display button
        self.B1 = Button(root, text="List Faults",bg="white",command=display_faults)
        self.B1.grid(column=0, row=16)

        #Create a submit button
        self.B2 = Button(root, text="Submit",bg="white",command=submit_fault)
        self.B2.grid( row=16,column=2)

class DBConn():

    # Create submit function
    def submit(self, first_name, last_name, contact, apartment, report_date, unit, gender, fault):

        self.f_name = first_name
        self.l_name = last_name
        self.c_number = contact
        self.apartment = apartment
        self.r_date = report_date
        self.unit = unit
        self.gender = gender
        self.fault = fault

        try:
            # Connect to the database
            con = sqlite3.connect('my_database.db')
            # Create a cursor
            cur = con.cursor()
            # Insert values into table
            cur.execute("""CREATE TABLE IF NOT EXISTS list (
                                        first_name text,
                                        last_name text,
                                        contact text,
                                        apartment text,
                                        report_date text,
                                        gender text,
                                        unit integer,
                                        fault text
                                        )""")
            cur.execute("INSERT INTO list VALUES (:first_name, :last_name, :contact ,:apartment, :report_date,:unit, :gender, :fault)",
                                { 'first_name': self.f_name,
                                  'last_name': self.l_name,
                                  'contact': self.c_number,
                                  'apartment': self.apartment,
                                  'report_date': self.r_date,
                                  'unit': self.unit,
                                  'gender': self.gender,
                                  'fault': self.fault
                                })
            # Commit changes
            con.commit()

            # Close connection
            con.close()

            msg = 'Your log error has been received!'
            messagebox.showinfo('Add fault', msg)

        except:
            messagebox.showerror('error', 'Unable to add fault')


    #Retrieving Faults
    def get_faults(self):
        con = sqlite3.connect('my_database.db')
        cur = con.cursor()
        result = cur.execute("SELECT oid, first_name ,last_name ,contact,apartment,report_date,gender,unit,fault FROM list")
        return result
        con.close()


class Faults():
    # Create Display function
    def display(self, master):
        newWindow = Toplevel(master)
        newWindow.title("List of Faults")
        newWindow.geometry("1000x500")

        # Connect to the database
        dbConn = DBConn()
        cur = dbConn.get_faults()

        e = Label(newWindow, width=15, text='ID', borderwidth=2, relief='ridge', anchor="w", bg='grey')
        e.grid(row=0, column=0)
        e = Label(newWindow, width=15, text='First name', borderwidth=2, relief='ridge', anchor="w", bg='grey')
        e.grid(row=0, column=1)
        e = Label(newWindow, width=15, text='Last name', borderwidth=2, relief='ridge', anchor="w", bg='grey')
        e.grid(row=0, column=2)
        e = Label(newWindow, width=15, text='Contact', borderwidth=2, relief='ridge', anchor="w", bg='grey')
        e.grid(row=0, column=3)
        e = Label(newWindow, width=15, text='Apartment', borderwidth=2, relief='ridge', anchor="w", bg='grey')
        e.grid(row=0, column=4)
        e = Label(newWindow, width=15, text='Report date', borderwidth=2, relief='ridge', anchor="w", bg='grey')
        e.grid(row=0, column=5)
        e = Label(newWindow, width=15, text='Unit', borderwidth=2, relief='ridge', anchor="w", bg='grey')
        e.grid(row=0, column=6)
        e = Label(newWindow, width=15, text='Gender', borderwidth=2, relief='ridge', anchor="w", bg='grey')
        e.grid(row=0, column=7)
        e = Label(newWindow, width=15, text='Fault', borderwidth=2, relief='ridge', anchor="w", bg='grey')
        e.grid(row=0, column=8)

        i = 1
        for list in cur:
            for j in range(len(list)):
                e = Label(newWindow, width=15, text=list[j], borderwidth=2, relief='ridge', anchor="w")
                e.grid(row=i, column=j)
            i = i + 1


root = Tk()
my_gui = Main(root)
root.mainloop()



