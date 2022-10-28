from tkinter import *  
import tkinter as tk
from tkinter import ttk
user = Tk()  
uname = Label(user,text = "uname").grid(row =1, column = 1)  
un= Entry(user).grid(row = 0, column = 0)  
passw = Label(user,text = "pass").grid(row = 1, column = 1)  
ps = Entry(user).grid(row = 1, column = 1)  
result = Button(user, text = "submit").grid(row = 3, column = 3)  
comb = tk.Label(user,
                    text = "Please select the option")
comb.grid(column=2, row=1)

example = ttk.Combobox(user, 
                            values=[
                                    "first", 
                                    "second",
                                    "third",
                                    "four"])
print(dict(example))  
example.grid(column=2, row=2)
example.current(3)
user.mainloop()  