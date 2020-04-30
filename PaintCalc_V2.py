'''
Created on Apr 23, 2020

@author: Davis Swanson, Maia Ellenburg
'''

#imports modules
import tkinter as tk
import tkinter.ttk as ttk
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

        tk.Button(self, text="Customer History",command=lambda: master.switch_frame(PageTwo)).pack()


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
        
        ttk.Label(self, text = "Paint type").grid(column=0, row =1, sticky=tk.E)
        self.paint= tk.StringVar()
        ttk.Entry(self, width=25, textvariable=self.paint).grid(column=1, row =1)
        
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
        c2.execute("CREATE TABLE IF NOT EXISTS jobs (job_ID INTEGER PRIMARY KEY, cust_ID TEXT, paint TEXT, width INT, length INT, height INT, windows INT, doors INT, bid INT)")    

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
        
        paint1=70
        paint2=50
        paint3=30

        window=3*5
        door=2.5*6
        
        labor=0.32
        
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
        
#  -- main  --
conn = sqlite3.connect("customer.db")    
c = conn.cursor()  

conn2 = sqlite3.connect("jobs.db")    
c2 = conn2.cursor()  

root=PaintCalc()
root.title("Paint Bidder")
root.geometry("375x275")
root.mainloop()


