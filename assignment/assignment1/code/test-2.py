from tkinter import *
root = Tk()

m = PanedWindow(root)
m.pack(fill=BOTH, expand=1)

text1 = Text(m, height=15, width =15)
m.add(text1) 

text2=Text(m, height=15, width=15)
m.add(text2) 

root.mainloop()