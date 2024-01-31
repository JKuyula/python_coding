'''
Programmer : Joelle Kabaka Kuyula
Student number : KXLC9ZWQ1
In this program, we have created a contact management system that allows us to add, view, update and delete contact entries .
'''


from tkinter import *
import sqlite3
import re
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox




class Contacts:

    def __init__(self,master):
        self.master = master
        master.geometry("700x400")
        master.title("Contact list")

        self.firstname = StringVar()
        self.lastname = StringVar()
        self.gender = StringVar()
        self.age = StringVar()
        self.address = StringVar()
        self.contact = StringVar()

        def Database():
            conn = sqlite3.connect("my_contact.db")
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS `Contact` (contact_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, gender TEXT, age TEXT, address TEXT, contact TEXT)")
            fetch = cursor.fetchall()
            for data in fetch:
                self.tree.insert('', 'end', values=data)
            cursor.close()
            conn.close()


        def Reset():
            # clear current data from table
            self.tree.delete(*self.tree.get_children())
            # refresh table data
            DisplayData()
            # clear search text
            self.firstname.set("")
            self.lastname.set("")
            self.gender.set("")
            self.age.set("")
            self.address.set("")
            self.contact.set("")




        def isvalid(contact1): # Validate the contact number
            pattern = re.compile("^[0-9]{10}$")
            return pattern.match(contact1)


        def SubmitData2():
            # getting form data
            fname1 = self.firstname.get()
            lname1 = self.lastname.get()
            gender1 = self.gender.get()
            address1 = self.address.get()
            contact1 = self.contact.get()


            # applying empty validation
            if fname1 == '' or lname1 == '' or gender1 == '' or address1 == '' or  contact1 == '':
                tkMessageBox.showinfo("Warning", "fill the empty field!!!")
            else:
                if isvalid(contact1) :
                     curItem = self.tree.focus()
                     contents = (self.tree.item(curItem))
                     selecteditem = contents['values']
                     # update query
                     conn = sqlite3.connect("my_contact.db")
                     cursor = conn.cursor()
                     cursor.execute(
                         'UPDATE Contact SET firstname=?,lastname=?,gender=?,address=?,contact=? WHERE oid = ?',
                         (fname1, lname1, gender1, address1, contact1, selecteditem[0]))
                     conn.commit()
                     tkMessageBox.showinfo("Message", "Contact updated successfully")
                     # reset form
                     Reset()
                     # refresh table data
                     DisplayData()
                     conn.close()
                else:
                    tkMessageBox.showinfo("Error", "The contact number should have 10 digits and start with 0")
                    Reset()

        #def UpdateData():
            #Update()
        def UpdateData():
            global NewWindow
            self.firstname.set("")
            self.lastname.set("")
            self.gender.set("")
            self.age.set("")
            self.address.set("")
            self.contact.set("")
            NewWindow = Toplevel(master)
            NewWindow.title("Contact List")
            NewWindow.geometry("500x300")

            FormTitle = Frame(NewWindow)
            FormTitle.pack(side=TOP)
            ContactForm = Frame(NewWindow)
            ContactForm.pack(side=TOP, pady=10)
            RadioGroup = Frame(ContactForm)
            Radiobutton(RadioGroup, text="Male", variable=self.gender, value="Male", font=('arial', 14)).pack(
                side=LEFT)
            Radiobutton(RadioGroup, text="Female", variable=self.gender, value="Female",
                                 font=('arial', 14)).pack(
                side=LEFT)

            # Labels
            lbl_title = Label(FormTitle, text="Updating Contacts", font=('arial', 16), bg="cyan", width=300)
            lbl_title.pack(fill=X)
            lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
            lbl_firstname.grid(row=0, sticky=W)
            lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
            lbl_lastname.grid(row=1, sticky=W)
            lbl_gender = Label(ContactForm, text="Gender", font=('arial', 14), bd=5)
            lbl_gender.grid(row=2, sticky=W)
            lbl_age = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
            lbl_age.grid(row=3, sticky=W)
            lbl_address = Label(ContactForm, text="Address", font=('arial', 14), bd=5)
            lbl_address.grid(row=4, sticky=W)
            lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
            lbl_contact.grid(row=5, sticky=W)

            # Entries
            firstname = Entry(ContactForm, textvariable=self.firstname, font=('arial', 14))
            firstname.grid(row=0, column=1)
            lastname = Entry(ContactForm, textvariable=self.lastname, font=('arial', 14))
            lastname.grid(row=1, column=1)
            RadioGroup.grid(row=2, column=1)
            age = Entry(ContactForm, textvariable=self.age, font=('arial', 14))
            age.grid(row=3, column=1)
            address = Entry(ContactForm, textvariable=self.address, font=('arial', 14))
            address.grid(row=4, column=1)
            contact = Entry(ContactForm, textvariable=self.contact, font=('arial', 14))
            contact.grid(row=5, column=1)

            # Creating a button to update a record
            btn_addcon = Button(ContactForm, text="Save", width=50, command=SubmitData2)
            btn_addcon.grid(row=6, columnspan=2, pady=10)

    
        def DeleteRecord():
            if not self.tree.selection():
                tkMessageBox.showwarning("Warning", "Select data to delete")
            else:
                result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                                  icon="warning")
                if result == 'yes':
                    curItem = self.tree.focus()
                    contents = (self.tree.item(curItem))
                    selecteditem = contents['values']
                    self.tree.delete(curItem)
                    conn = sqlite3.connect("my_contact.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Contact WHERE oid = %d" % selecteditem[0])
                    conn.commit()
                    cursor.close()
                    conn.close()

        def DisplayData():
            # clear current data
            self.tree.delete(*self.tree.get_children())
            conn = sqlite3.connect("my_contact.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Contact")
            # fetch all data from database
            fetch = cursor.fetchall()
            # loop for displaying all data in GUI
            for data in fetch:
                self.tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()

        def validation(contact):# Validate the contact number
            p= re.compile("^[0-9]{10}$")
            return p.match(contact)

        def SubmitData1(): #save data into the database
            fname = self.firstname.get()
            lname = self.lastname.get()
            gender = self.gender.get()
            age =  self.age.get()
            address = self.address.get()
            contact = self.contact.get()

            if fname == "" or lname == "" or gender == "" or age == "" or address == "" or contact == "":
                tkMessageBox.showwarning('Error', 'Please complete the required field', icon="warning")
            else:
                if validation(contact):

                    self.tree.delete(*self.tree.get_children())
                    # insert query
                    conn = sqlite3.connect("my_contact.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO `Contact` (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)",
                        (
                            str(fname), str(lname), str(gender),
                            int(age),
                            str(address),
                            str(contact)))
                    conn.commit()
                    tkMessageBox.showinfo("Message", "Contact recorded successfully")
                    cursor.execute("SELECT * FROM `Contact`")
                    fetch = cursor.fetchall()
                    for data in fetch:
                        self.tree.insert('', 'end', values=data)
                    cursor.close()
                    conn.close()
                    self.firstname.set("")
                    self.lastname.set("")
                    self.gender.set("")
                    self.age.set("")
                    self.address.set("")
                    self.contact.set("")
                else:
                    tkMessageBox.showinfo("Error", "The contact number should have 10 digits and start with 0")
                    Reset()

        def AddNew():
            global NewWindow
            self.firstname.set("")
            self.lastname.set("")
            self.gender.set("")
            self.age.set("")
            self.address.set("")
            self.contact.set("")
            NewWindow = Toplevel(master)
            NewWindow.title("Contact List")
            NewWindow.geometry("500x300")

            # Create a new frame
            FormTitle = Frame(NewWindow)
            FormTitle.pack(side=TOP)
            ContactForm = Frame(NewWindow)
            ContactForm.pack(side=TOP, pady=10)
            RadioGroup = Frame(ContactForm)
            Radiobutton(RadioGroup, text="Male", variable=self.gender, value="Male", font=('arial', 14)).pack(
                side=LEFT)
            Radiobutton(RadioGroup, text="Female", variable=self.gender, value="Female", font=('arial', 14)).pack(
                side=LEFT)

            # Labels
            lbl_title = Label(FormTitle, text="Adding New Contacts", font=('arial', 16), bg="cyan", width=300)
            lbl_title.pack(fill=X)
            lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
            lbl_firstname.grid(row=0, sticky=W)
            lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
            lbl_lastname.grid(row=1, sticky=W)
            lbl_gender = Label(ContactForm, text="Gender", font=('arial', 14), bd=5)
            lbl_gender.grid(row=2, sticky=W)
            lbl_age = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
            lbl_age.grid(row=3, sticky=W)
            lbl_address = Label(ContactForm, text="Address", font=('arial', 14), bd=5)
            lbl_address.grid(row=4, sticky=W)
            lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
            lbl_contact.grid(row=5, sticky=W)

            # Entries
            firstname = Entry(ContactForm, textvariable=self.firstname, font=('arial', 14))
            firstname.grid(row=0, column=1)
            lastname = Entry(ContactForm, textvariable=self.lastname, font=('arial', 14))
            lastname.grid(row=1, column=1)
            RadioGroup.grid(row=2, column=1)
            age = Entry(ContactForm, textvariable=self.age, font=('arial', 14))
            age.grid(row=3, column=1)
            address = Entry(ContactForm, textvariable=self.address, font=('arial', 14))
            address.grid(row=4, column=1)
            contact = Entry(ContactForm, textvariable=self.contact, font=('arial', 14))
            contact.grid(row=5, column=1)

            # Create a button to submit values
            btn_save = Button(ContactForm, text="Save", width=50, command=SubmitData1)
            btn_save.grid(row=6, columnspan=2, pady=10)


        self.Form = Frame(root, width=600, bd=1, relief=SOLID)
        self.Form.pack(side=TOP, fill=X)
        self.Mid = Frame(root, width=700)
        self.Mid.pack(side=TOP)
        self.MidLeft = Frame(self.Mid, width=100)
        self.MidLeft.pack(side=LEFT, pady=10)
        self.MidLeftPadding = Frame(self.Mid, width=400)
        self.MidLeftPadding.pack(side=LEFT)
        self.MidRight = Frame(self.Mid, width=100)
        self.MidRight.pack(side=RIGHT, pady=10)
        self.TableMargin = Frame(root, width=500)
        self.TableMargin.pack(side=TOP)

        # label for heading
        self.lbl_text = Label(self.Form, text="Contact Management System", font=('Arial', 18), width=600, bg="cyan")
        self.lbl_text.pack(fill=X)

        # Create CRUD buttons
        self.btn_add = Button(self.MidLeft, text="+ ADD NEW", command=AddNew, bg="lightblue")
        self.btn_add.grid(row=0, column=0)
        self.btn_view = Button(self.MidLeft, text="VIEW",command= DisplayData, bg="lightblue")
        self.btn_view.grid(row=0, column=1)
        self.btn_change = Button(self.MidRight, text="UPDATE", command=UpdateData,bg="lightblue")
        self.btn_change.grid(row=0, column=2)
        self.btn_delete = Button(self.MidRight, text="DELETE",command=DeleteRecord, bg="lightblue")
        self.btn_delete.grid(row=0, column=3)

        # Setting scrollbar
        self.scrollbarx = Scrollbar(self.TableMargin, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(self.TableMargin, orient=VERTICAL)
        self.tree = ttk.Treeview(self.TableMargin,
                                 columns=("ID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"),
                                 selectmode="extended", height=100, yscrollcommand=self.scrollbary.set,
                                 xscrollcommand= self.scrollbarx.set)
        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side=RIGHT, fill=Y)
        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side=BOTTOM, fill=X)

        # Setting headings for the columns for the main window
        self.tree.heading('ID', text="ID", anchor=W)
        self.tree.heading('Firstname', text="Firstname", anchor=W)
        self.tree.heading('Lastname', text="Lastname", anchor=W)
        self.tree.heading('Gender', text="Gender", anchor=W)
        self.tree.heading('Age', text="Age", anchor=W)
        self.tree.heading('Address', text="Address", anchor=W)
        self.tree.heading('Contact', text="Contact", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=0)
        self.tree.column('#2', stretch=NO, minwidth=0, width=80)
        self.tree.column('#3', stretch=NO, minwidth=0, width=120)
        self.tree.column('#4', stretch=NO, minwidth=0, width=90)
        self.tree.column('#5', stretch=NO, minwidth=0, width=80)
        self.tree.column('#6', stretch=NO, minwidth=0, width=180)
        self.tree.column('#7', stretch=NO, minwidth=0, width=120)
        self.tree.pack()
        DisplayData()



root = Tk()
my_gui = Contacts(root)
root.mainloop()

