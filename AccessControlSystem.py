#Imported Libries
import tkinter as tk
import os
import RPi.GPIO as GPIO
import time

#Mainframe
class Studio(tk.Tk):

   def __init__(self, *args, **kwargs):
       tk.Tk.__init__(self, *args, **kwargs)

       tk.Tk.wm_title(self, 'AccessControlSystem')

       container = tk.Frame(self)
       container.pack(side='top', fill='both', expand=True)
       container.grid_rowconfigure(0, weight=1)
       container.grid_columnconfigure(0, weight=1)

       self.frames = {}

       for F in (StartPage, AdminLoginPage, Register):
           frame = F(container, self)

           self.frames[F] = frame

           frame.grid(row=0, column=0, sticky='nsew')

       self.show_frame(StartPage)

   def show_frame(self, cont):
       frame = self.frames[cont]
       frame.tkraise()

#Main window for the application
class StartPage(tk.Frame):

   def __init__(self, parent, controller):
       tk.Frame.__init__(self, parent)

       self.empid = tk.StringVar()

       entry = tk.Entry(self, width="50", show='*', font='Helvetica 42', textvariable=self.empid, justify='center')
       entry.place(x=90, y=200, width=500) #Has the entry field that used for login

       nextButton = tk.Button(self, text='Login', width='70', height='15', bg="light grey", command=lambda: self.login())
       nextButton.place(x=90, y=300) #Login Button

       nextButton = tk.Button(self, text='Admin Login', width='70', height='1',command=lambda: controller.show_frame(AdminLoginPage))
       nextButton.place(x=90, y=540) #Button for routing to Admin login

   def clear(self): #Clears out the written Employee ID
       self.empid.set('')


   def login(self): #login system for access
       username1 = self.empid.get()

       list_of_files = os.listdir()
       if username1 in list_of_files:
           file1 = open(username1, 'r')
           verify = file1.read().splitlines()
           print('login success')
           self.clear()

           self.GPIO()
       else:
           print('user_not_found')
           self.clear()

   def GPIO(self):
       channel = 4

       # GPIO setup for opening the relay and therefore the doorlock
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(channel, GPIO.OUT)

       def motor_on(pin):
           GPIO.output(pin, GPIO.HIGH)  # Turn motor on

       def motor_off(pin):
           GPIO.output(pin, GPIO.LOW)  # Turn motor off

       if __name__ == '__main__':
           try:
               motor_on(channel)
               time.sleep(1)
               motor_off(channel)
               time.sleep(1)
               GPIO.cleanup()
           except KeyboardInterrupt:
               GPIO.cleanup()
       pass


class AdminLoginPage(tk.Frame):
       def __init__(self, parent, controller):
           tk.Frame.__init__(self, parent)

           # The Admin login page

           self.empid = tk.StringVar()
           self.password = tk.StringVar()

           label = tk.Label(self, text=' Admin Login Page ')
           label.config(font=('Verdana', 32))
           label.place(x=325, y=100, anchor='center')

           label = tk.Label(self, text='Enter Employee ID ')
           label.place(x=130, y=250)

           entry = tk.Entry(self, textvariable=self.empid)
           entry.place(x=250, y=250, width=200)

           label = tk.Label(self, text='Enter Admin Password ')
           label.place(x=100, y=300)

           entry = tk.Entry(self, show='*', textvariable=self.password)
           entry.place(x=250, y=300, width=200)

           button = tk.Button(self, text='  Admin \n Login   ',
                              command=lambda: self.login(controller), height=2, width=30)
           button.place(x=465, y=250, width=150, height=115)

           button = tk.Button(self, text='  Cancel   ',
                              command=lambda: controller.show_frame(StartPage), height=2, width=30)
           button.place(x=250, y=325, width=200) # The cancel button will redirect to the Main window

       def AdminClear(self): #For clearing out the input from user
           self.empid.set('')
           self.password.set('')

       def login(self,controller): # The login Screen
           username1 = self.empid.get()
           password1 = self.password.get()

           list_of_files = os.listdir()
           if username1 in list_of_files:
               file1 = open(username1, 'r')
               verify = file1.read().splitlines()
               if password1 in verify:
                   self.AdminClear()
                   controller.show_frame(Register)
               else:
                   StartPage.clear(self)
                   # print('password_not_recognised')
           else:
               StartPage.clear(self)
               # print('user_not_found')


class Register(tk.Frame): #Registration of users or Admins
   def __init__(self, parent, controller):
       tk.Frame.__init__(self, parent)

       self.LastName = tk.StringVar()
       self.FirstName = tk.StringVar()
       self.empid = tk.StringVar()


       label = tk.Label(self, text='Admin Registration Panel')
       label.config(font=('Verdana', 15))
       label.place(x=225, y=5)

       label = tk.Label(self, text='Enter Employee ID ')
       label.place(x=70, y=50)

       LastName_entry = tk.Entry(self, textvariable=self.empid, width=60)
       LastName_entry.place(x=175, y=50)

       label = tk.Label(self, text='Your last name ')
       label.place(x=75, y=100)

       LastName_entry = tk.Entry(self, textvariable=self.LastName, width=60)
       LastName_entry.place(x=175, y=100)

       label = tk.Label(self, text='Your first names ')
       label.place(x=65, y=150)

       last_name_entry = tk.Entry(self, textvariable=self.FirstName, width=60)
       last_name_entry.place(x=175, y=150)

       button = tk.Button(self, text=' Open \nDoor', width='12', height='3', command=lambda: StartPage.GPIO(self))
       button.place(x=250, y=525)

       button = tk.Button(self, text='Main Menu', width='12', height='3', command=lambda: controller.show_frame(StartPage))
       button.place(x=350, y=525)

       button = tk.Button(self, text='Register User', width='12', height='3', command=lambda: self.registered_user())
       button.place(x=450, y=525)

       button = tk.Button(self, text='Quit', width='12', height='3', command=self.quit)
       button.place(x=250, y=625)

   def clear_reg(self):
       self.empid.set('')
       self.LastName.set('')
       self.FirstName.set('')


   def registered_user(self):

        empid_info = self.empid.get()
        last_name_info = self.LastName.get()
        first_name_info = self.FirstName.get()
        self.clear_reg()

        file = open(empid_info, 'w')
        file.write(last_name_info)
        file.write('\n')
        file.write(first_name_info)
        file.close()



app = Studio()
app.geometry('700x750')
app.mainloop()
