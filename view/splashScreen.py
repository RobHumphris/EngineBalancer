from tkinter import *
from fullScreen import *

root = Tk()

sp = FullScreen(root)
sp.config(bg="#3366ff")

m = Label(sp, text="This is a test of the splash screen\n\n\nThis is only a test.\nwww.sunjay-varma.com")
m.pack(side=TOP, expand=YES)
m.config(bg="#3366ff", justify=CENTER, font=("calibri", 29))

Button(sp, text="Press this button to kill the program", bg='red', command=root.destroy).pack(side=BOTTOM, fill=X)
root.mainloop()