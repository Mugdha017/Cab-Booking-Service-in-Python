from tkinter import *
from tkinter import ttk
import random
import time
import datetime
from tkinter import messagebox as ms
import sqlite3

# Database setup
with sqlite3.connect('Users.db') as db:
    c = db.cursor()
c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL, password TEXT NOT NULL)')
db.commit()
db.close()

class user:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.widgets()

    def login(self):
        with sqlite3.connect('Users.db') as db:
            c = db.cursor()
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        if result:
            self.logf.pack_forget()
            self.head['text'] = "Welcome " + self.username.get()
            self.head.configure(fg="black")
            self.head.pack(fill=X)
            self.master.geometry("1350x750+0+0")  # Resize for travel app
            application = travel(self.master)
        else:
            ms.showerror('Oops!', 'Username or Password Incorrect.')

    def new_user(self):
        with sqlite3.connect('Users.db') as db:
            c = db.cursor()
        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user, [(self.n_username.get())])
        if c.fetchall():
            ms.showerror('Error!', 'Username Already Taken!')
        else:
            if self.n_username.get() and self.n_password.get():
                insert = 'INSERT INTO user(username, password) VALUES(?,?)'
                c.execute(insert, [(self.n_username.get()), (self.n_password.get())])
                db.commit()
                ms.showinfo('Success!', 'Account Created!')
                self.log()
            else:
                ms.showerror('Error!', 'Please enter a username and password.')

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'Login'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()

    def widgets(self):
        self.head = Label(self.master, text='Login Panel', font=('', 30), pady=10)
        self.head.pack()
        self.logf = Frame(self.master, padx=10, pady=10)
        Label(self.logf, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.logf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.logf, text=' Login ', bd=3, font=('', 15), padx=5, pady=5, command=self.login).grid()
        Button(self.logf, text=' Create Account ', bd=3, font=('', 15), padx=5, pady=5, command=self.cr).grid(row=2, column=1)
        self.logf.pack()

        self.crf = Frame(self.master, padx=10, pady=10)
        Label(self.crf, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.crf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.crf, text='Create Account', bd=3, font=('', 15), padx=5, pady=5, command=self.new_user).grid()
        Button(self.crf, text='Go to Login', bd=3, font=('', 15), padx=5, pady=5, command=self.log).grid(row=2, column=1)

class travel:
    def __init__(self, root):
        self.root = root
        self.root.title("JatriGo Cab Booking System")
        self.root.configure(background='gray20')

        # Variables
        self.DateofOrder = StringVar()
        self.DateofOrder.set(time.strftime("%d/%m/%Y"))
        self.Receipt_Ref = StringVar()
        self.PaidTax = StringVar()
        self.SubTotal = StringVar()
        self.TotalCost = StringVar()

        self.var1 = IntVar()  # Base Charge
        self.var2 = IntVar()  # Distance
        self.journeyType = IntVar()
        self.carType = IntVar()

        self.varl1 = StringVar()  # Pickup
        self.varl2 = StringVar()  # Drop
        self.varl3 = StringVar()  # Payment Method
        self.varl4 = StringVar()  # Booking Date
        self.varl5 = StringVar()  # Booking Time

        self.Firstname = StringVar()
        self.Surname = StringVar()
        self.Address = StringVar()
        self.Postcode = StringVar()
        self.Mobile = StringVar()
        self.Telephone = StringVar()
        self.Email = StringVar()

        self.CabTax = StringVar()
        self.Km = StringVar()
        self.CNG = StringVar()
        self.Sedan = StringVar()
        self.SUV = StringVar()

        self.CabTax.set("0")
        self.Km.set("0")
        self.CNG.set("0")
        self.Sedan.set("0")
        self.SUV.set("0")
        self.varl3.set("")
        self.varl4.set("")
        self.varl5.set("")

        self.reset_counter = 0

        # Date and time options
        today = datetime.date.today()
        date_options = [today + datetime.timedelta(days=i) for i in range(7)]
        date_options = [d.strftime("%d/%m/%Y") for d in date_options]
        date_options.insert(0, "")

        time_options = [f"{hour:02d}:00 {period}" for period in ["AM", "PM"] for hour in range(8, 12) if not (period == "PM" and hour == 12)] + \
                       [f"{hour:02d}:00 PM" for hour in range(1, 12)]
        time_options.insert(0, "")

        # Distance matrix
        self.locations = [
            'Hazrat Shahjalal International Airport (HSIA)', 'Gabtoli Bus Terminal', 'Sayedabad Bus Terminal',
            'Mohakhali Bus Terminal', 'Kamalapur Railway Station', 'Airport Railway Station',
            'Gulshan Avenue', 'Dhanmondi Road', 'Banani Road', 'Mirpur Road', 'Motijheel',
            'Uttara', 'Mohammadpur', 'Shahbagh', 'Bashundhara', 'Paltan', 'Farmgate'
        ]
        self.distance_matrix = {
            'Hazrat Shahjalal International Airport (HSIA)': {
                'Hazrat Shahjalal International Airport (HSIA)': 0, 'Gabtoli Bus Terminal': 14, 'Sayedabad Bus Terminal': 20,
                'Mohakhali Bus Terminal': 6, 'Kamalapur Railway Station': 20, 'Airport Railway Station': 5,
                'Gulshan Avenue': 8, 'Dhanmondi Road': 18, 'Banani Road': 7, 'Mirpur Road': 14, 'Motijheel': 20,
                'Uttara': 5, 'Mohammadpur': 16, 'Shahbagh': 19, 'Bashundhara': 6, 'Paltan': 20, 'Farmgate': 14
            },
            'Gabtoli Bus Terminal': {
                'Hazrat Shahjalal International Airport (HSIA)': 14, 'Gabtoli Bus Terminal': 0, 'Sayedabad Bus Terminal': 12,
                'Mohakhali Bus Terminal': 13, 'Kamalapur Railway Station': 12, 'Airport Railway Station': 10,
                'Gulshan Avenue': 14, 'Dhanmondi Road': 10, 'Banani Road': 13, 'Mirpur Road': 5, 'Motijheel': 12,
                'Uttara': 10, 'Mohammadpur': 6, 'Shahbagh': 10, 'Bashundhara': 15, 'Paltan': 11, 'Farmgate': 7
            },
            'Sayedabad Bus Terminal': {
                'Hazrat Shahjalal International Airport (HSIA)': 20, 'Gabtoli Bus Terminal': 12, 'Sayedabad Bus Terminal': 0,
                'Mohakhali Bus Terminal': 14, 'Kamalapur Railway Station': 5, 'Airport Railway Station': 18,
                'Gulshan Avenue': 15, 'Dhanmondi Road': 10, 'Banani Road': 14, 'Mirpur Road': 12, 'Motijheel': 5,
                'Uttara': 18, 'Mohammadpur': 11, 'Shahbagh': 8, 'Bashundhara': 16, 'Paltan': 6, 'Farmgate': 10
            },
            'Mohakhali Bus Terminal': {
                'Hazrat Shahjalal International Airport (HSIA)': 6, 'Gabtoli Bus Terminal': 13, 'Sayedabad Bus Terminal': 14,
                'Mohakhali Bus Terminal': 0, 'Kamalapur Railway Station': 12, 'Airport Railway Station': 6,
                'Gulshan Avenue': 5, 'Dhanmondi Road': 10, 'Banani Road': 3, 'Mirpur Road': 8, 'Motijheel': 12,
                'Uttara': 6, 'Mohammadpur': 9, 'Shahbagh': 10, 'Bashundhara': 7, 'Paltan': 11, 'Farmgate': 7
            },
            'Kamalapur Railway Station': {
                'Hazrat Shahjalal International Airport (HSIA)': 20, 'Gabtoli Bus Terminal': 12, 'Sayedabad Bus Terminal': 5,
                'Mohakhali Bus Terminal': 12, 'Kamalapur Railway Station': 0, 'Airport Railway Station': 15,
                'Gulshan Avenue': 12, 'Dhanmondi Road': 8, 'Banani Road': 11, 'Mirpur Road': 10, 'Motijheel': 3,
                'Uttara': 15, 'Mohammadpur': 9, 'Shahbagh': 6, 'Bashundhara': 12, 'Paltan': 5, 'Farmgate': 8
            },
            'Airport Railway Station': {
                'Hazrat Shahjalal International Airport (HSIA)': 5, 'Gabtoli Bus Terminal': 10, 'Sayedabad Bus Terminal': 18,
                'Mohakhali Bus Terminal': 6, 'Kamalapur Railway Station': 15, 'Airport Railway Station': 0,
                'Gulshan Avenue': 7, 'Dhanmondi Road': 17, 'Banani Road': 6, 'Mirpur Road': 12, 'Motijheel': 19,
                'Uttara': 4, 'Mohammadpur': 16, 'Shahbagh': 17, 'Bashundhara': 5, 'Paltan': 18, 'Farmgate': 12
            },
            'Gulshan Avenue': {
                'Hazrat Shahjalal International Airport (HSIA)': 8, 'Gabtoli Bus Terminal': 14, 'Sayedabad Bus Terminal': 15,
                'Mohakhali Bus Terminal': 5, 'Kamalapur Railway Station': 12, 'Airport Railway Station': 7,
                'Gulshan Avenue': 0, 'Dhanmondi Road': 10, 'Banani Road': 3, 'Mirpur Road': 8, 'Motijheel': 12,
                'Uttara': 7, 'Mohammadpur': 10, 'Shahbagh': 10, 'Bashundhara': 6, 'Paltan': 11, 'Farmgate': 8
            },
            'Dhanmondi Road': {
                'Hazrat Shahjalal International Airport (HSIA)': 18, 'Gabtoli Bus Terminal': 10, 'Sayedabad Bus Terminal': 10,
                'Mohakhali Bus Terminal': 10, 'Kamalapur Railway Station': 8, 'Airport Railway Station': 17,
                'Gulshan Avenue': 10, 'Dhanmondi Road': 0, 'Banani Road': 9, 'Mirpur Road': 6, 'Motijheel': 8,
                'Uttara': 12, 'Mohammadpur': 4, 'Shahbagh': 6, 'Bashundhara': 12, 'Paltan': 7, 'Farmgate': 5
            },
            'Banani Road': {
                'Hazrat Shahjalal International Airport (HSIA)': 7, 'Gabtoli Bus Terminal': 13, 'Sayedabad Bus Terminal': 14,
                'Mohakhali Bus Terminal': 3, 'Kamalapur Railway Station': 11, 'Airport Railway Station': 6,
                'Gulshan Avenue': 3, 'Dhanmondi Road': 9, 'Banani Road': 0, 'Mirpur Road': 7, 'Motijheel': 11,
                'Uttara': 6, 'Mohammadpur': 9, 'Shahbagh': 9, 'Bashundhara': 5, 'Paltan': 10, 'Farmgate': 7
            },
            'Mirpur Road': {
                'Hazrat Shahjalal International Airport (HSIA)': 14, 'Gabtoli Bus Terminal': 5, 'Sayedabad Bus Terminal': 12,
                'Mohakhali Bus Terminal': 8, 'Kamalapur Railway Station': 10, 'Airport Railway Station': 12,
                'Gulshan Avenue': 8, 'Dhanmondi Road': 6, 'Banani Road': 7, 'Mirpur Road': 0, 'Motijheel': 10,
                'Uttara': 10, 'Mohammadpur': 5, 'Shahbagh': 8, 'Bashundhara': 10, 'Paltan': 9, 'Farmgate': 5
            },
            'Motijheel': {
                'Hazrat Shahjalal International Airport (HSIA)': 20, 'Gabtoli Bus Terminal': 12, 'Sayedabad Bus Terminal': 5,
                'Mohakhali Bus Terminal': 12, 'Kamalapur Railway Station': 3, 'Airport Railway Station': 19,
                'Gulshan Avenue': 12, 'Dhanmondi Road': 8, 'Banani Road': 11, 'Mirpur Road': 10, 'Motijheel': 0,
                'Uttara': 15, 'Mohammadpur': 9, 'Shahbagh': 6, 'Bashundhara': 12, 'Paltan': 5, 'Farmgate': 8
            },
            'Uttara': {
                'Hazrat Shahjalal International Airport (HSIA)': 5, 'Gabtoli Bus Terminal': 10, 'Sayedabad Bus Terminal': 18,
                'Mohakhali Bus Terminal': 6, 'Kamalapur Railway Station': 15, 'Airport Railway Station': 4,
                'Gulshan Avenue': 7, 'Dhanmondi Road': 12, 'Banani Road': 6, 'Mirpur Road': 10, 'Motijheel': 15,
                'Uttara': 0, 'Mohammadpur': 12, 'Shahbagh': 14, 'Bashundhara': 8, 'Paltan': 15, 'Farmgate': 10
            },
            'Mohammadpur': {
                'Hazrat Shahjalal International Airport (HSIA)': 16, 'Gabtoli Bus Terminal': 6, 'Sayedabad Bus Terminal': 11,
                'Mohakhali Bus Terminal': 9, 'Kamalapur Railway Station': 9, 'Airport Railway Station': 16,
                'Gulshan Avenue': 10, 'Dhanmondi Road': 4, 'Banani Road': 9, 'Mirpur Road': 5, 'Motijheel': 9,
                'Uttara': 12, 'Mohammadpur': 0, 'Shahbagh': 7, 'Bashundhara': 12, 'Paltan': 8, 'Farmgate': 5
            },
            'Shahbagh': {
                'Hazrat Shahjalal International Airport (HSIA)': 19, 'Gabtoli Bus Terminal': 10, 'Sayedabad Bus Terminal': 8,
                'Mohakhali Bus Terminal': 10, 'Kamalapur Railway Station': 6, 'Airport Railway Station': 17,
                'Gulshan Avenue': 10, 'Dhanmondi Road': 6, 'Banani Road': 9, 'Mirpur Road': 8, 'Motijheel': 6,
                'Uttara': 14, 'Mohammadpur': 7, 'Shahbagh': 0, 'Bashundhara': 12, 'Paltan': 6, 'Farmgate': 6
            },
            'Bashundhara': {
                'Hazrat Shahjalal International Airport (HSIA)': 6, 'Gabtoli Bus Terminal': 15, 'Sayedabad Bus Terminal': 16,
                'Mohakhali Bus Terminal': 7, 'Kamalapur Railway Station': 12, 'Airport Railway Station': 5,
                'Gulshan Avenue': 6, 'Dhanmondi Road': 12, 'Banani Road': 5, 'Mirpur Road': 10, 'Motijheel': 12,
                'Uttara': 8, 'Mohammadpur': 12, 'Shahbagh': 12, 'Bashundhara': 0, 'Paltan': 12, 'Farmgate': 9
            },
            'Paltan': {
                'Hazrat Shahjalal International Airport (HSIA)': 20, 'Gabtoli Bus Terminal': 11, 'Sayedabad Bus Terminal': 6,
                'Mohakhali Bus Terminal': 11, 'Kamalapur Railway Station': 5, 'Airport Railway Station': 18,
                'Gulshan Avenue': 11, 'Dhanmondi Road': 7, 'Banani Road': 10, 'Mirpur Road': 9, 'Motijheel': 5,
                'Uttara': 15, 'Mohammadpur': 8, 'Shahbagh': 6, 'Bashundhara': 12, 'Paltan': 0, 'Farmgate': 7
            },
            'Farmgate': {
                'Hazrat Shahjalal International Airport (HSIA)': 14, 'Gabtoli Bus Terminal': 7, 'Sayedabad Bus Terminal': 10,
                'Mohakhali Bus Terminal': 7, 'Kamalapur Railway Station': 8, 'Airport Railway Station': 12,
                'Gulshan Avenue': 8, 'Dhanmondi Road': 5, 'Banani Road': 7, 'Mirpur Road': 5, 'Motijheel': 8,
                'Uttara': 10, 'Mohammadpur': 5, 'Shahbagh': 6, 'Bashundhara': 9, 'Paltan': 7, 'Farmgate': 0
            }
        }

        # Functions
        def iExit():
            result = ms.askyesno("Prompt!", "Do you want to exit?")
            if result:
                root.destroy()

        def Reset():
            self.CabTax.set("0")
            self.Km.set("0")
            self.CNG.set("0")
            self.Sedan.set("0")
            self.SUV.set("0")

            self.Firstname.set("")
            self.Surname.set("")
            self.Address.set("")
            self.Postcode.set("")
            self.Mobile.set("")
            self.Telephone.set("")
            self.Email.set("")

            self.PaidTax.set("")
            self.SubTotal.set("")
            self.TotalCost.set("")
            self.txtReceipt1.delete("1.0", END)
            self.txtReceipt2.delete("1.0", END)

            self.var1.set(0)
            self.var2.set(0)
            self.journeyType.set(0)
            self.carType.set(0)
            self.varl1.set("")
            self.varl2.set("")
            self.varl3.set("")
            self.varl4.set("")
            self.varl5.set("")

            self.cboPickup.current(0)
            self.cboDrop.current(0)
            self.cboPayment.current(0)
            self.cboDate.current(0)
            self.cboTime.current(0)

            self.txtCabTax.configure(state=DISABLED)
            self.txtKm.configure(state=DISABLED)
            self.txtCNG.configure(state=DISABLED)
            self.txtSedan.configure(state=DISABLED)
            self.txtSUV.configure(state=DISABLED)
            self.reset_counter = 1

        def Receiptt():
            if (self.reset_counter == 0 and self.Firstname.get() and self.Surname.get() and
                self.Address.get() and self.Postcode.get() and self.Mobile.get() and
                self.Telephone.get() and self.Email.get() and self.varl3.get() and
                self.varl4.get() and self.varl5.get()):
                self.txtReceipt1.delete("1.0", END)
                self.txtReceipt2.delete("1.0", END)
                x = random.randint(10853, 500831)
                randomRef = str(x)
                self.Receipt_Ref.set(randomRef)

                self.txtReceipt1.insert(END, "Receipt Ref:\n")
                self.txtReceipt2.insert(END, self.Receipt_Ref.get() + "\n")
                self.txtReceipt1.insert(END, 'Date:\n')
                self.txtReceipt2.insert(END, self.DateofOrder.get() + "\n")
                self.txtReceipt1.insert(END, 'Cab No:\n')
                self.txtReceipt2.insert(END, 'TR ' + self.Receipt_Ref.get() + " BW\n")
                self.txtReceipt1.insert(END, 'Firstname:\n')
                self.txtReceipt2.insert(END, self.Firstname.get() + "\n")
                self.txtReceipt1.insert(END, 'Surname:\n')
                self.txtReceipt2.insert(END, self.Surname.get() + "\n")
                self.txtReceipt1.insert(END, 'Address:\n')
                self.txtReceipt2.insert(END, self.Address.get() + "\n")
                self.txtReceipt1.insert(END, 'Postal Code:\n')
                self.txtReceipt2.insert(END, self.Postcode.get() + "\n")
                self.txtReceipt1.insert(END, 'Telephone:\n')
                self.txtReceipt2.insert(END, self.Telephone.get() + "\n")
                self.txtReceipt1.insert(END, 'Mobile:\n')
                self.txtReceipt2.insert(END, self.Mobile.get() + "\n")
                self.txtReceipt1.insert(END, 'Email:\n')
                self.txtReceipt2.insert(END, self.Email.get() + "\n")
                self.txtReceipt1.insert(END, 'From:\n')
                self.txtReceipt2.insert(END, self.varl1.get() + "\n")
                self.txtReceipt1.insert(END, 'To:\n')
                self.txtReceipt2.insert(END, self.varl2.get() + "\n")
                self.txtReceipt1.insert(END, 'Payment Method:\n')
                self.txtReceipt2.insert(END, self.varl3.get() + "\n")
                self.txtReceipt1.insert(END, 'Booking Date:\n')
                self.txtReceipt2.insert(END, self.varl4.get() + "\n")
                self.txtReceipt1.insert(END, 'Booking Time:\n')
                self.txtReceipt2.insert(END, self.varl5.get() + "\n")
                self.txtReceipt1.insert(END, 'CNG Auto-Rickshaw:\n')
                self.txtReceipt2.insert(END, self.CNG.get() + "\n")
                self.txtReceipt1.insert(END, 'Sedan Taxi:\n')
                self.txtReceipt2.insert(END, self.Sedan.get() + "\n")
                self.txtReceipt1.insert(END, 'Premium SUV:\n')
                self.txtReceipt2.insert(END, self.SUV.get() + "\n")
                self.txtReceipt1.insert(END, 'Paid Tax:\n')
                self.txtReceipt2.insert(END, self.PaidTax.get() + "\n")
                self.txtReceipt1.insert(END, 'SubTotal:\n')
                self.txtReceipt2.insert(END, str(self.SubTotal.get()) + "\n")
                self.txtReceipt1.insert(END, 'Total Cost:\n')
                self.txtReceipt2.insert(END, str(self.TotalCost.get()))
            else:
                self.txtReceipt1.delete("1.0", END)
                self.txtReceipt2.delete("1.0", END)
                self.txtReceipt1.insert(END, "\nPlease fill all required fields")

        def Cab_Tax():
            if self.var1.get() == 1:
                self.txtCabTax.configure(state=NORMAL)
                Item1 = float(80)  # Base charge BDT 80
                self.CabTax.set("BDT " + str(Item1))
                self.Item1 = Item1
            else:
                self.txtCabTax.configure(state=DISABLED)
                self.CabTax.set("0")
                self.Item1 = 0

        def Kilo():
            if self.var2.get() == 0:
                self.txtKm.configure(state=DISABLED)
                self.Km.set("0")
            elif self.var2.get() == 1 and self.varl1.get() and self.varl2.get():
                if self.varl1.get() == self.varl2.get():
                    ms.showwarning("Error", "Pickup and Drop locations cannot be the same!")
                    self.Km.set("0")
                    self.txtKm.configure(state=DISABLED)
                else:
                    try:
                        distance = self.distance_matrix[self.varl1.get()][self.varl2.get()]
                        self.txtKm.configure(state=NORMAL)
                        self.Km.set(str(distance))
                    except KeyError:
                        ms.showerror("Error", "Invalid pickup or drop-off location!")
                        self.Km.set("0")
                        self.txtKm.configure(state=DISABLED)
            else:
                ms.showwarning("Error", "Please select both pickup and drop-off locations!")
                self.Km.set("0")
                self.txtKm.configure(state=DISABLED)

        def selectCar():
            if self.carType.get() == 1:  # CNG Auto-Rickshaw
                self.txtSedan.configure(state=DISABLED)
                self.Sedan.set("0")
                self.txtSUV.configure(state=DISABLED)
                self.SUV.set("0")
                self.txtCNG.configure(state=NORMAL)
                self.Item5 = float(20)  # BDT 20/km
                self.CNG.set("BDT " + str(self.Item5))
            elif self.carType.get() == 2:  # Sedan Taxi
                self.txtCNG.configure(state=DISABLED)
                self.CNG.set("0")
                self.txtSUV.configure(state=DISABLED)
                self.SUV.set("0")
                self.txtSedan.configure(state=NORMAL)
                self.Item5 = float(40)  # BDT 40/km
                self.Sedan.set("BDT " + str(self.Item5))
            elif self.carType.get() == 3:  # Premium SUV
                self.txtCNG.configure(state=DISABLED)
                self.CNG.set("0")
                self.txtSedan.configure(state=DISABLED)
                self.Sedan.set("0")
                self.txtSUV.configure(state=NORMAL)
                self.Item5 = float(65)  # BDT 65/km
                self.SUV.set("BDT " + str(self.Item5))
            else:
                self.txtCNG.configure(state=DISABLED)
                self.txtSedan.configure(state=DISABLED)
                self.txtSUV.configure(state=DISABLED)
                self.CNG.set("0")
                self.Sedan.set("0")
                self.SUV.set("0")
                self.Item5 = 0

        def Total_Paid():
            required_fields = [
                self.var1.get() == 1, self.var2.get() == 1, self.carType.get() != 0,
                self.journeyType.get() != 0, self.varl1.get(), self.varl2.get(),
                self.varl3.get(), self.varl4.get(), self.varl5.get(),
                self.Firstname.get(), self.Surname.get(), self.Address.get(),
                self.Postcode.get(), self.Mobile.get(), self.Telephone.get(), self.Email.get()
            ]
            if all(required_fields):
                try:
                    Item2 = float(self.Km.get())
                    if self.journeyType.get() == 1:  # Single
                        Cost_of_fare = (self.Item1 + (Item2 - 2) * self.Item5) if Item2 > 2 else self.Item1
                    elif self.journeyType.get() == 2:  # Return
                        Cost_of_fare = (self.Item1 + (Item2 - 2) * self.Item5 * 1.5) if Item2 > 2 else self.Item1 * 1.5
                    else:  # Special Needs
                        Cost_of_fare = (self.Item1 + (Item2 - 2) * self.Item5 * 2) if Item2 > 2 else self.Item1 * 2

                    Tax = "BDT " + str('%.2f' % (Cost_of_fare * 0.07))
                    ST = "BDT " + str('%.2f' % Cost_of_fare)
                    TT = "BDT " + str('%.2f' % (Cost_of_fare + (Cost_of_fare * 0.07)))

                    self.PaidTax.set(Tax)
                    self.SubTotal.set(ST)
                    self.TotalCost.set(TT)
                except ValueError:
                    ms.showerror("Error", "Invalid distance value!")
            else:
                ms.showwarning("Error", "Please fill all required fields, including customer details, booking date, and time!")

        # Main Frame
        MainFrame = Frame(self.root, bg='gray20')
        MainFrame.pack(fill=BOTH, expand=True)

        Tops = Frame(MainFrame, bd=10, width=1350, relief=RIDGE, bg='gray20')
        Tops.pack(side=TOP, fill=BOTH)

        self.lblTitle = Label(Tops, font=('arial', 40, 'bold'), text="\tJatriGo Cab Booking Agency", bg='gray20', fg='gold')
        self.lblTitle.grid()

        # Customer Details Frame
        CustomerDetailsFrame = LabelFrame(MainFrame, width=1350, height=500, bd=20, pady=5, relief=RIDGE, bg='gray20')
        CustomerDetailsFrame.pack(side=BOTTOM, fill=BOTH, expand=True)

        FrameDetails = Frame(CustomerDetailsFrame, width=880, height=400, bd=10, relief=RIDGE, bg='gray20')
        FrameDetails.pack(side=LEFT, fill=BOTH, expand=True)

        CustomerName = LabelFrame(FrameDetails, width=150, height=250, bd=10, font=('arial', 12, 'bold'), text="Customer Info", relief=RIDGE, bg='gray20', fg='gold')
        CustomerName.grid(row=0, column=0)

        TravelFrame = LabelFrame(FrameDetails, bd=10, width=300, height=250, font=('arial', 12, 'bold'), text="Booking Detail", relief=RIDGE, bg='gray20', fg='gold')
        TravelFrame.grid(row=0, column=1)

        Book_Frame = LabelFrame(FrameDetails, width=300, height=150, relief=FLAT, bg='gray20')
        Book_Frame.grid(row=1, column=0)

        CostFrame = LabelFrame(FrameDetails, width=150, height=150, bd=5, relief=FLAT, bg='gray20')
        CostFrame.grid(row=1, column=1)

        # Receipt Frame
        Receipt_BottonFrame = LabelFrame(CustomerDetailsFrame, bd=10, width=450, height=400, relief=RIDGE, bg='gray20')
        Receipt_BottonFrame.pack(side=RIGHT, fill=BOTH, expand=True)

        ReceiptFrame = LabelFrame(Receipt_BottonFrame, width=350, height=300, font=('arial', 12, 'bold'), text="Receipt", relief=RIDGE, bg='gray20', fg='gold')
        ReceiptFrame.grid(row=0, column=0)

        ButtonFrame = LabelFrame(Receipt_BottonFrame, width=350, height=100, relief=RIDGE, bg='gray20')
        ButtonFrame.grid(row=1, column=0)

        # Customer Info Widgets
        self.lblFirstname = Label(CustomerName, font=('arial', 14, 'bold'), text="Firstname", bd=7, bg='gray20', fg='white')
        self.lblFirstname.grid(row=0, column=0, sticky=W)
        self.txtFirstname = Entry(CustomerName, font=('arial', 14, 'bold'), textvariable=self.Firstname, bd=7, insertwidth=2, justify=RIGHT, bg='white', fg='black', relief=SUNKEN)
        self.txtFirstname.grid(row=0, column=1)

        self.lblSurname = Label(CustomerName, font=('arial', 14, 'bold'), text="Surname", bd=7, bg='gray20', fg='white')
        self.lblSurname.grid(row=1, column=0, sticky=W)
        self.txtSurname = Entry(CustomerName, font=('arial', 14, 'bold'), textvariable=self.Surname, bd=7, insertwidth=2, justify=RIGHT, bg='white', fg='black', relief=SUNKEN)
        self.txtSurname.grid(row=1, column=1)

        self.lblAddress = Label(CustomerName, font=('arial', 14, 'bold'), text="Address", bd=7, bg='gray20', fg='white')
        self.lblAddress.grid(row=2, column=0, sticky=W)
        self.txtAddress = Entry(CustomerName, font=('arial', 14, 'bold'), textvariable=self.Address, bd=7, insertwidth=2, justify=RIGHT, bg='white', fg='black', relief=SUNKEN)
        self.txtAddress.grid(row=2, column=1)

        self.lblPostcode = Label(CustomerName, font=('arial', 14, 'bold'), text="Postcode", bd=7, bg='gray20', fg='white')
        self.lblPostcode.grid(row=3, column=0, sticky=W)
        self.txtPostcode = Entry(CustomerName, font=('arial', 14, 'bold'), textvariable=self.Postcode, bd=7, insertwidth=2, justify=RIGHT, bg='white', fg='black', relief=SUNKEN)
        self.txtPostcode.grid(row=3, column=1)

        self.lblTelephone = Label(CustomerName, font=('arial', 14, 'bold'), text="Telephone", bd=7, bg='gray20', fg='white')
        self.lblTelephone.grid(row=4, column=0, sticky=W)
        self.txtTelephone = Entry(CustomerName, font=('arial', 14, 'bold'), textvariable=self.Telephone, bd=7, insertwidth=2, justify=RIGHT, bg='white', fg='black', relief=SUNKEN)
        self.txtTelephone.grid(row=4, column=1)

        self.lblMobile = Label(CustomerName, font=('arial', 14, 'bold'), text="Mobile", bd=7, bg='gray20', fg='white')
        self.lblMobile.grid(row=5, column=0, sticky=W)
        self.txtMobile = Entry(CustomerName, font=('arial', 14, 'bold'), textvariable=self.Mobile, bd=7, insertwidth=2, justify=RIGHT, bg='white', fg='black', relief=SUNKEN)
        self.txtMobile.grid(row=5, column=1)

        self.lblEmail = Label(CustomerName, font=('arial', 14, 'bold'), text="Email", bd=7, bg='gray20', fg='white')
        self.lblEmail.grid(row=6, column=0, sticky=W)
        self.txtEmail = Entry(CustomerName, font=('arial', 14, 'bold'), textvariable=self.Email, bd=7, insertwidth=2, justify=RIGHT, bg='white', fg='black', relief=SUNKEN)
        self.txtEmail.grid(row=6, column=1)

        # Booking Details Widgets
        self.lblPickup = Label(TravelFrame, font=('arial', 14, 'bold'), text="Pickup", bd=7, bg='gray20', fg='white')
        self.lblPickup.grid(row=0, column=0, sticky=W)
        self.cboPickup = ttk.Combobox(TravelFrame, textvariable=self.varl1, state='readonly', font=('arial', 16, 'bold'), width=14, foreground='black')
        self.cboPickup['values'] = ('', 'Hazrat Shahjalal International Airport (HSIA)', 'Gabtoli Bus Terminal', 'Sayedabad Bus Terminal', 'Mohakhali Bus Terminal', 'Kamalapur Railway Station', 'Airport Railway Station')
        self.cboPickup.current(0)
        self.cboPickup.grid(row=0, column=1)

        self.lblDrop = Label(TravelFrame, font=('arial', 14, 'bold'), text="Drop", bd=7, bg='gray20', fg='white')
        self.lblDrop.grid(row=1, column=0, sticky=W)
        self.cboDrop = ttk.Combobox(TravelFrame, textvariable=self.varl2, state='readonly', font=('arial', 16, 'bold'), width=14, foreground='black')
        self.cboDrop['values'] = ('', 'Gulshan Avenue', 'Dhanmondi Road', 'Banani Road', 'Mirpur Road', 'Motijheel', 'Uttara', 'Mohammadpur', 'Shahbagh', 'Bashundhara', 'Paltan', 'Farmgate')
        self.cboDrop.current(0)
        self.cboDrop.grid(row=1, column=1)

        self.chkCabTax = Checkbutton(TravelFrame, text="Base Charge *", variable=self.var1, onvalue=1, offvalue=0, font=('arial', 16, 'bold'), command=Cab_Tax, bg='gray20', fg='white')
        self.chkCabTax.grid(row=2, column=0, sticky=W)
        self.txtCabTax = Label(TravelFrame, font=('arial', 14, 'bold'), textvariable=self.CabTax, bd=6, width=18, bg="white", fg='black', state=DISABLED, justify=RIGHT, relief=SUNKEN)
        self.txtCabTax.grid(row=2, column=1)

        self.chkKm = Checkbutton(TravelFrame, text="Distance(KMs) *", variable=self.var2, onvalue=1, offvalue=0, font=('arial', 16, 'bold'), command=Kilo, bg='gray20', fg='white')
        self.chkKm.grid(row=3, column=0, sticky=W)
        self.txtKm = Label(TravelFrame, font=('arial', 14, 'bold'), textvariable=self.Km, bd=6, width=18, bg="white", fg='black', state=DISABLED, justify=RIGHT, relief=SUNKEN)
        self.txtKm.grid(row=3, column=1)

        self.lblPayment = Label(TravelFrame, font=('arial', 14, 'bold'), text="Payment Method", bd=7, bg='gray20', fg='white')
        self.lblPayment.grid(row=4, column=0, sticky=W)
        self.cboPayment = ttk.Combobox(TravelFrame, textvariable=self.varl3, state='readonly', font=('arial', 16, 'bold'), width=14, foreground='black')
        self.cboPayment['values'] = ('', 'Cash', 'Cards', 'Digital Wallets')
        self.cboPayment.current(0)
        self.cboPayment.grid(row=4, column=1)

        self.lblDate = Label(TravelFrame, font=('arial', 14, 'bold'), text="Booking Date", bd=7, bg='gray20', fg='white')
        self.lblDate.grid(row=5, column=0, sticky=W)
        self.cboDate = ttk.Combobox(TravelFrame, textvariable=self.varl4, state='readonly', font=('arial', 16, 'bold'), width=14, foreground='black')
        self.cboDate['values'] = date_options
        self.cboDate.current(0)
        self.cboDate.grid(row=5, column=1)

        self.lblTime = Label(TravelFrame, font=('arial', 14, 'bold'), text="Booking Time", bd=7, bg='gray20', fg='white')
        self.lblTime.grid(row=6, column=0, sticky=W)
        self.cboTime = ttk.Combobox(TravelFrame, textvariable=self.varl5, state='readonly', font=('arial', 16, 'bold'), width=14, foreground='black')
        self.cboTime['values'] = time_options
        self.cboTime.current(0)
        self.cboTime.grid(row=6, column=1)

        # Payment Information
        self.lblPaidTax = Label(CostFrame, font=('arial', 14, 'bold'), text="Paid Tax", bd=7, bg='gray20', fg='white')
        self.lblPaidTax.grid(row=0, column=2, sticky=W)
        self.txtPaidTax = Label(CostFrame, font=('arial', 14, 'bold'), textvariable=self.PaidTax, bd=7, width=10, justify=RIGHT, bg="white", fg='black', relief=SUNKEN)
        self.txtPaidTax.grid(row=0, column=3)

        self.lblSubTotal = Label(CostFrame, font=('arial', 14, 'bold'), text="Sub Total", bd=7, bg='gray20', fg='white')
        self.lblSubTotal.grid(row=1, column=2, sticky=W)
        self.txtSubTotal = Label(CostFrame, font=('arial', 14, 'bold'), textvariable=self.SubTotal, bd=7, width=10, justify=RIGHT, bg="white", fg='black', relief=SUNKEN)
        self.txtSubTotal.grid(row=1, column=3)

        self.lblTotalCost = Label(CostFrame, font=('arial', 14, 'bold'), text="Total Cost", bd=7, bg='gray20', fg='white')
        self.lblTotalCost.grid(row=2, column=2, sticky=W)
        self.txtTotalCost = Label(CostFrame, font=('arial', 14, 'bold'), textvariable=self.TotalCost, bd=7, width=10, justify=RIGHT, bg="white", fg='black', relief=SUNKEN)
        self.txtTotalCost.grid(row=2, column=3)

        # Cab Selection
        self.chkCNG = Radiobutton(Book_Frame, text="CNG Auto-Rickshaw", value=1, variable=self.carType, font=('arial', 14, 'bold'), command=selectCar, bg='gray20', fg='white')
        self.chkCNG.grid(row=0, column=0, sticky=W)
        self.txtCNG = Label(Book_Frame, font=('arial', 14, 'bold'), width=7, textvariable=self.CNG, bd=5, state=DISABLED, justify=RIGHT, bg="white", fg='black', relief=SUNKEN)
        self.txtCNG.grid(row=0, column=1)

        self.chkSedan = Radiobutton(Book_Frame, text="Sedan Taxi", value=2, variable=self.carType, font=('arial', 14, 'bold'), command=selectCar, bg='gray20', fg='white')
        self.chkSedan.grid(row=1, column=0, sticky=W)
        self.txtSedan = Label(Book_Frame, font=('arial', 14, 'bold'), width=7, textvariable=self.Sedan, bd=5, state=DISABLED, justify=RIGHT, bg="white", fg='black', relief=SUNKEN)
        self.txtSedan.grid(row=1, column=1)

        self.chkSUV = Radiobutton(Book_Frame, text="Premium SUV", value=3, variable=self.carType, font=('arial', 14, 'bold'), command=selectCar, bg='gray20', fg='white')
        self.chkSUV.grid(row=2, column=0, sticky=W)
        self.txtSUV = Label(Book_Frame, font=('arial', 14, 'bold'), width=7, textvariable=self.SUV, bd=5, state=DISABLED, justify=RIGHT, bg="white", fg='black', relief=SUNKEN)
        self.txtSUV.grid(row=2, column=1)

        self.chkSingle = Radiobutton(Book_Frame, text="Single", value=1, variable=self.journeyType, font=('arial', 14, 'bold'), bg='gray20', fg='white')
        self.chkSingle.grid(row=0, column=2, sticky=W)
        self.chkReturn = Radiobutton(Book_Frame, text="Return", value=2, variable=self.journeyType, font=('arial', 14, 'bold'), bg='gray20', fg='white')
        self.chkReturn.grid(row=1, column=2, sticky=W)
        self.chkSpecialsNeeds = Radiobutton(Book_Frame, text="Special Needs", value=3, variable=self.journeyType, font=('arial', 14, 'bold'), bg='gray20', fg='white')
        self.chkSpecialsNeeds.grid(row=2, column=2, sticky=W)

        # Receipt Display
        self.txtReceipt1 = Text(ReceiptFrame, width=22, height=21, font=('arial', 10, 'bold'), borderwidth=0, bg='white', fg='black')
        self.txtReceipt1.grid(row=0, column=0, columnspan=2)
        self.txtReceipt2 = Text(ReceiptFrame, width=22, height=21, font=('arial', 10, 'bold'), borderwidth=0, bg='white', fg='black')
        self.txtReceipt2.grid(row=0, column=2, columnspan=2)

        # Buttons
        self.btnTotal = Button(ButtonFrame, padx=18, bd=7, font=('arial', 11, 'bold'), width=2, text='Total', command=Total_Paid, bg='gray20', fg='white')
        self.btnTotal.grid(row=0, column=0)
        self.btnReceipt = Button(ButtonFrame, padx=18, bd=7, font=('arial', 11, 'bold'), width=2, text='Receipt', command=Receiptt, bg='gray20', fg='white')
        self.btnReceipt.grid(row=0, column=1)
        self.btnReset = Button(ButtonFrame, padx=18, bd=7, font=('arial', 11, 'bold'), width=2, text='Reset', command=Reset, bg='gray20', fg='white')
        self.btnReset.grid(row=0, column=2)
        self.btnExit = Button(ButtonFrame, padx=18, bd=7, font=('arial', 11, 'bold'), width=2, text='Exit', command=iExit, bg='gray20', fg='white')
        self.btnExit.grid(row=0, column=3)


if __name__ == '__main__':
    root = Tk()
    root.geometry("500x300+320+200")
    root.title('Login Form')
    application = user(root)
    root.mainloop()