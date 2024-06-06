import tkinter as tk
from tkinter import *

class UI:
  def __init__(self):
    self.root = Tk()
    self.root.title("Hello World")
    self.root.geometry("400x300")
    self.label = Label(self.root, text="Hello World!")
    self.label.pack()
    self.root.mainloop()