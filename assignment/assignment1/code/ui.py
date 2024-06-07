# import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

from environment import *

class State:
  IDLE = 0
  AGENT = 1
  GOAL = 2
  WALL = 3
  READY = 4
  PENDING = 5
  VISITED = 6


class Block:
  def __init__(self):
    self.state = State.IDLE
    self.palette = {
      State.IDLE: "white",
      State.AGENT: "red",
      State.GOAL: "limegreen",
      State.WALL: "gray",
      State.READY: "cyan",
      State.PENDING: "dodgerblue",
      State.VISITED: "navy"
    }
    
  @property
  def color(self):
    return self.palette[self.state]
    
  # def set_state(self, state):
  #   self.state = state
    
  # def reset_state(self):
  #   self.state = State.IDLE
    

class Map:
  pass
  
class GUI:
  def __init__(self):
    self.root = Tk()
    self.root.title("Robot Navigation GUI")
    self.root.geometry("900x600")
    self.root.configure(bg="dodgerblue")
    
    ico = Image.open("icon.png")
    self.icon = ImageTk.PhotoImage(ico)
    self.root.iconphoto(False, self.icon)
    
    menu = self.get_menu()
    self.root.config(menu=menu)
    
    self.canvas = Canvas(self.root, bg="navy", width=self.root.winfo_width()/2, height=600)
    self.canvas.pack(side=LEFT)
    
    self.label = Label(self.root, text="Hello World!")
    self.label.pack()

  def get_menu(self):
    menu = Menu(self.root)
    menu.add_command(label="New", command=self.create_map)
    menu.add_command(label="Open", command=self.open_map)
    menu.add_command(label="Exit", command=self.root.quit)
    return menu

  def run(self):
    self.root.mainloop()
    
  def create_map(self):
    self.label.config(text="New file created!")
    
  def open_map(self):
    filename = askopenfilename(filetypes=[("Text files", "*.txt")], initialdir="maps")
    if filename:
      # content = file.readline()
      self.label.config(text=filename)
    # self.label.config(text="File opened!")
    
        
window = GUI()
window.run()