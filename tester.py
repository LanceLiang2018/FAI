from tkinter import *
import random

root = Tk()

var = StringVar()
var.set('234578')

Button(root, textvariable=var, command=lambda: var.set(str(random.randint(0, 255)))).pack()


root.mainloop()