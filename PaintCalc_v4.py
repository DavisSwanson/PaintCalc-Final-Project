'''
Created on Apr 23, 2020

@author: Davis Swanson, Maia Ellenburg
'''

#imports modules
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Combobox
import sqlite3  

#Defines Frame for Program and creates function for switching frames
class PaintCalc(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

#Defines start page
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Paint Bidder", font=('Helvetica', 18, "bold")).pack(side="top", fill='x', pady=5)
        
        tk.Button(self, text="Create Customer",command=lambda: master.switch_frame(CustomerFrame)).pack()
        
        tk.Button(self, text="Add Job",command=lambda: master.switch_frame(AddJob)).pack()

        tk.Button(self, text="Customers",command=lambda: master.switch_frame(CustomerHistory)).pack()
        
        tk.Button(self, text="Settings",command=lambda: master.switch_frame(Settings)).pack()


#Creates frame for creating new customers
class CustomerFrame(ttk.Frame):
    def __init__(self, parent):
          
        conn = sqlite3.connect("customer.db")    
        c = conn.cursor()  
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.pack(fill=tk.BOTH, expand=True)   
        self.create_table()     
                  
       
        #Define text entry fields and labels
        ttk.Label(self, text="Name").grid(column=0, row=0, sticky=tk.E)
        self.name = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.name).grid(column=1, row=0)
        
        ttk.Label(self, text="Address").grid(column=0, row=1, sticky=tk.E)
        self.address = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.address).grid(column=1, row=1)
        
        ttk.Label(self, text="Phone #").grid(column=0, row=2, sticky=tk.E)
        self.phone = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.phone).grid(column=1, row=2)

        #Create Clearbutton
        ttk.Button(self, text="Clear", command=self.clear).grid(column=1, row = 4)

        #Create Savebutton    
        ttk.Button(self, text="Save", command=self.data_entry).grid(column=1, row = 3) 
        
        #Create Button to go to bid
        ttk.Button(self, text="Go to create Job", command=lambda: parent.switch_frame(AddJob)).grid(column=1, row = 5)
        
        #Create ExitButton
        ttk.Button(self, text="Back", command=lambda: parent.switch_frame(StartPage)).grid(column=1, row = 6) 
        
        c.close()    
        conn.close()  
                    
        #Add padding to all child components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
                        
    def clear(self):
        #Define the event listener for the Clear button
        print("Name", self.name.get())
        self.name.set("")
        
        print("Address", self.address.get())
        self.address.set("")
        
        print("Phone", self.phone.get())
        self.phone.set("") 
  
    def create_table(self):    
        c.execute("CREATE TABLE IF NOT EXISTS customers (name TEXT, cust_ID INT, address TEXT, phone INT)")    

    def data_entry(self):          
        #Get customer info
        name=self.name.get()
        address=self.address.get()
        phone=self.phone.get()
        
        #Creates cust id based off name and phone number
        cust_ID=str(name[:5]+phone[6:])
        
        #Add customer info to database
        sql = '''INSERT INTO customers (name, address, phone, cust_ID)
                 VALUES (?,?,?,?)'''
        c.execute(sql, (name,address,phone,cust_ID))
        conn.commit()
        
        #Lets user know its been saved
        ttk.Label(self, text="Saved!").grid(column=0, row=4, sticky=tk.E)  
        
#Frame for creating new job
class AddJob(ttk.Frame):
    def __init__(self, parent):
        
        #Connect to our databases
        conn3 = sqlite3.connect("settings.db")    
        c3 = conn3.cursor()
        
        conn2 = sqlite3.connect("jobs.db")    
        c2 = conn2.cursor()  
        
        conn = sqlite3.connect("customer.db")    
        c = conn.cursor()  
        
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.pack(fill=tk.BOTH, expand=True)   
        self.create_table() 
        
        #Define text entry fields and labels    
        ttk.Label(self, text="Customer Name").grid(column=0, row=0, sticky=tk.E)
        self.name = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.name).grid(column=1, row=0)
        
        self.paint=tk.StringVar()
        ttk.Label(self, text = "Paint type").grid(column=0, row =1, sticky=tk.E)
        ttk.Combobox(self, textvariable=self.paint, values=['1','2','3']).grid(column=1, row =1)
       
    
        ttk.Label(self, text = "# of Windows").grid(column=0, row=2, sticky=tk.E)
        self.windows = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.windows).grid(column=1, row=2)
        
        ttk.Label(self, text = "# of Doors").grid(column=0, row=3, sticky=tk.E)
        self.doors = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.doors).grid(column=1, row=3)
        
        ttk.Label(self, text = "Room Length (ft)").grid(column=0, row=4, sticky=tk.E)
        self.length = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.length).grid(column=1, row=4)
        
        ttk.Label(self, text = "Room Width (ft)").grid(column=0, row=5, sticky=tk.E)
        self.width = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.width).grid(column=1, row=5)
        
        ttk.Label(self, text = "Wall height (ft)").grid(column=0, row=6, sticky=tk.E)
        self.height = tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.height).grid(column=1, row=6)
        
        ttk.Label(self, text="Bid Value: $").grid(column=0, row=7, sticky=tk.E)
        self.bid = tk.StringVar()
        ttk.Entry(self, width=30, textvariable=self.bid,state="readonly").grid(
            column=1, row=7)
        
        #Adds job entry to database
        ttk.Button(self, text="Create Job", command=self.create_job).grid(column=1, row = 9) 
        
        #Returns to home screen
        ttk.Button(self, text="Back", command=lambda: parent.switch_frame(StartPage)).grid(column=1, row = 10) 
        
        #Clears entry fields
        ttk.Button(self, text="Clear", command=self.clear).grid(column=1, row = 11) 
        
        ttk.Button(self, text="Create New Customer", command=lambda: parent.switch_frame(CustomerFrame)).grid(column=0, row = 11)
        
        
    
    #Creates table
    def create_table(self):    
        c2.execute("CREATE TABLE IF NOT EXISTS jobs (job_ID INTEGER PRIMARY KEY, cust_ID TEXT, paint INT, width INT, length INT, height INT, windows INT, doors INT, bid FLOAT)")    

    def create_job(self):      
   
        #Gets data
        name=self.name.get()
        paint=self.paint.get()
        windows=self.windows.get()
        doors=self.doors.get()
        height=self.height.get()
        length=self.length.get()
        width=self.width.get()
        
        #Finds customer ID related to name given
        query = '''SELECT cust_ID FROM customers WHERE name = ?'''
        
        c.execute(query, (name,))
        result = c.fetchone()
        
        #Checks to see if the customer is in the database. If not it will prompt you to go to create new customer
        if result==None:
            ttk.Label(self, text="No Customer with that name").grid(column=0, row=9, sticky=tk.E)
            ttk.Label(self, text="Must create new customer first").grid(column=0, row=10, sticky=tk.E)

            
            self.clear()
        else:
            self.calculate()
            bid=self.bid.get()
            id=result[0]
            sql = '''INSERT INTO jobs (job_ID, cust_id, paint, width, length, height, windows, doors, bid)
                 VALUES (NULL,?,?,?,?,?,?,?,?)'''
            c2.execute(sql, (id,paint, width, length, height, windows, doors, bid))
            conn2.commit()
            
            ttk.Label(self, text="Job Created!").grid(column=0, row=9, sticky=tk.E)
    
    #Calculate bid
    def calculate(self):
        windows=float(self.windows.get())
        doors=float(self.doors.get())
        height=float(self.height.get())
        length=float(self.length.get())
        width=float(self.width.get())
        paint=float(self.paint.get())
        
        settings='''SELECT * FROM settings'''
        c3.execute(settings)
        values=c3.fetchone()
        
        print(values)
        
        paint1=70
        paint2=50
        paint3=30

        window=values[1]
        door=values[2]
        
        labor=values[3]
        
        sq_ft=2*(((2*width+2*length)*height)-((window*windows)-(door*doors)))
        labor_cost=labor*sq_ft
        gallons=sq_ft/300
        
        if paint==1:
            bid=(gallons*paint1)+labor_cost
        elif paint==2:
            bid=(gallons*paint2)+labor_cost
        elif paint==3:
            bid=(gallons*paint3)+labor_cost
        
        
        self.bid.set(round(bid,2))
        
    def clear(self):
        #Define the event listener for the Clear button
        self.name.set("")
        self.paint.set("")
        self.windows.set("") 
        self.doors.set("") 
        self.height.set("") 
        self.length.set("") 
        self.width.set("") 
        self.bid.set("") 
        
class Settings(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.pack(fill=tk.BOTH, expand=True)   
        self.create_table() 
        
        conn3 = sqlite3.connect("settings.db")    
        c3 = conn3.cursor()   
        
        self.window = tk.StringVar()
        self.door = tk.StringVar()
        self.labor = tk.StringVar()
        
        ttk.Label(self, text="Window ft^2:").grid(
            column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=30, textvariable=self.window).grid(
            column=1, row=0)
        
        ttk.Label(self, text="Door ft^2:").grid(
            column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=30, textvariable=self.door).grid(
            column=1, row=1)
        
        ttk.Label(self, text="Labor %:").grid(
            column=0, row=2, sticky=tk.E)
        ttk.Entry(self, width=30, textvariable=self.labor).grid(
            column=1, row=2)
        
        ttk.Button(self, text="Update",command=self.update).grid(
            column=1, row=3)
        
        ttk.Button(self, text="Back", command=lambda: parent.switch_frame(StartPage)).grid(column=1, row = 4) 
    
    def create_table(self):    
        c3.execute("CREATE TABLE IF NOT EXISTS settings (setting_id INTEGER PRIMARY KEY, window INT, door INT, labor FLOAT)") 
        
    def update(self):
        window=self.window.get()
        door=self.door.get()
        labor=self.labor.get()
        
        query='''INSERT OR REPLACE INTO settings VALUES(?,?,?,?)'''
        
        c3.execute(query, (1, window, door, labor))
        conn3.commit()
        
        ttk.Label(self, text="Data Updated").grid(
            column=0, row=4, sticky=tk.E)
        

class CustomerHistory(ttk.Frame):
    def __init__(self, parent):
        
        #Connect to databases
        conn2 = sqlite3.connect("jobs.db")    
        c2 = conn2.cursor()  
        
        conn = sqlite3.connect("customer.db")    
        c = conn.cursor()  
        
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.pack(fill=tk.BOTH, expand=True)   
    
        #Define Labels and Fields
        
        ttk.Label(self, text = "Customer Name: ").grid(column=0, row=0, sticky=tk.E)
        self.name = tk.StringVar()
        ttk.Entry(self, width=30, textvariable=self.name).grid(column=1, row=0)
        
        #Gets jobs from database
        ttk.Button(self, text="Customer History", command=self.generate).grid(column=2, row =0 ) 
        
        #Clear button
        ttk.Button(self, text="Clear", command=self.clear).grid(column=1, row =2) 
        
        #Delete button
        ttk.Button(self, text="Delete", command=self.delete).grid(column=1, row =1) 
    
        #Back button
        ttk.Button(self, text= "Back",command=lambda: parent.switch_frame(StartPage)).grid(column =1, row=3)
      
        #Field for displaying retrieved data
        ttk.Label(self, text="Job History ").grid(column=0, row=5, sticky=tk.E)
     
        self.string=tk.StringVar("")
        ttk.Label(self, textvariable=self.string).grid(column=1, row=6, sticky=tk.E)
        
    def delete(self):
        name = self.name.get()
        query1 = '''SELECT cust_id FROM customers WHERE name =?'''
        c.execute(query1, (name,))
        cust_id =c.fetchall()
        
        id = cust_id[0]
        
        query2 = '''DELETE FROM customers WHERE cust_id = ?'''
        c.execute(query2, (id))
        results = c.fetchall()
        
        ttk.Label(self,text="Customer Deleted!" ).grid(column = 0, row = 9, sticky=tk.E)
 
 
 
 #Clears text box
    def clear(self):
        self.name.set(" ")
        
    def generate(self):
        #Gets data
         name = self.name.get()
         query = '''SELECT cust_id FROM customers WHERE name = ?'''
         
         c.execute(query, (name,))
         result = c.fetchone()
#        
         if result==None:
           ttk.Label(self, text="No Customer with that name").grid(column=1, row=9, sticky=tk.E)
           ttk.Label(self, text="Must create new customer first").grid(column=1, row=10, sticky=tk.E)
        
         else:
            self.getjobs()
            
    
    def getjobs(self):
        name = self.name.get()
        query1 = '''SELECT cust_id FROM customers WHERE name = ?'''
         
        c.execute(query1, (name,))
        cust_id = c.fetchone()
        
        id=cust_id[0]
        
        query2 = '''SELECT cust_ID, paint, width, length, height, bid FROM jobs WHERE cust_ID = ?'''
        c2.execute(query2, (id,))
        results = c2.fetchall()
        
        line_format = "{:4s} {:4s} {:4s} {:4s} {:4s} {:4s}"
        history="cust_ID    Paint   Width   Length   Height   Bid \n"
        
        for x in results:
            history+='\n'
            for y in x:
                history+=str(y)+"        "
        
        self.string.set(history)
        
#  -- main  --
conn = sqlite3.connect("customer.db")    
c = conn.cursor()  

conn2 = sqlite3.connect("jobs.db")    
c2 = conn2.cursor()  

conn3 = sqlite3.connect("settings.db")    
c3 = conn3.cursor()     

root=PaintCalc()
root.title("Paint Bidder")
root.geometry("500x275")
root.mainloop()

