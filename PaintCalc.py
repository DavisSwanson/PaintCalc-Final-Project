'''
Created on Apr 23, 2020

@author: Davis Swanson, Maia Ellenburg
'''
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3  

#from builtins import True
class SampleApp(tk.Tk):
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

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="PaintCalc", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Create Customer",
                  command=lambda: master.switch_frame(CustomerFrame)).pack()
        tk.Button(self, text="Add Job",
                  command=lambda: master.switch_frame(PageTwo)).pack()
        tk.Button(self, text="View Customer History",
                  command=lambda: master.switch_frame(PageTwo)).pack()



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
        
        #Create ExitButton
        ttk.Button(self, text="Back", command=lambda: parent.switch_frame(StartPage)).grid(column=1, row = 5) 
        
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
        c.execute("CREATE TABLE IF NOT EXISTS customers (name TEXT, cust_ID TEXT, job_ID INT, address TEXT, phone INT)")    

    def data_entry(self):          
        #Get customer info
        name=self.name.get()
        address=self.address.get()
        phone=self.phone.get()
        
        cust_ID=str(name[:5]+phone[6:])
        
        #Add customer info to database
        sql = '''INSERT INTO customers (name, address, phone, cust_ID)
                 VALUES (?,?,?,?)'''
        c.execute(sql, (name,address,phone,cust_ID))
        conn.commit()
        
        ttk.Label(self, text="Saved!").grid(column=0, row=4, sticky=tk.E)  
        

#  -- main  --
conn = sqlite3.connect("customer.db")    
c = conn.cursor()  
root=SampleApp()
root.title("PaintCalc")
root.geometry("300x200")
root.mainloop()



