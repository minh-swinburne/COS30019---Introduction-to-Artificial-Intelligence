from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from enum import Enum, auto

from environment import *

class State(Enum):
  IDLE = auto()
  AGENT = auto()
  GOAL = auto()
  WALL = auto()
  READY = auto()
  PENDING = auto()
  VISITED = auto()
  PATH = auto()


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
      State.VISITED: "navy",
      State.PATH: "gold"
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
  WINDOW_HEIGHT = 600
  WINDOW_WIDTH = 1000
  CANVAS_WIDTH = 650
  BLOCK_SIZE = 50
  
  def __init__(self):
    self.root = Tk()
    self.root.title("Robot Navigation GUI")
    self.root.geometry("1000x600")
    self.root.configure(bg="dodgerblue")
    
    ico = Image.open("icon.png")
    self.icon = ImageTk.PhotoImage(ico)
    self.root.iconphoto(False, self.icon)
    
    menu = self.create_menu()
    self.root.config(menu=menu)
    
    self.panel = PanedWindow(self.root)
    self.panel.pack(fill=BOTH, expand=1)
    
    self.canvas = Canvas(self.panel, bg="white", width=650)
    self.panel.add(self.canvas)
    
    right = PanedWindow(self.panel, orient=VERTICAL)
    self.panel.add(right)
    
    # self.canvas = Canvas(self.root, bg="navy", width=self.root.winfo_width()*2/3, height=self.root.winfo_height())
    # self.canvas.pack(side=LEFT)
    
    # self.label = Label(self.root, text="Hello World!")
    # self.label.pack()

  def create_menu(self):
    menu = Menu(self.root)
    menu.add_command(label="New", command=self.create_map)
    menu.add_command(label="Open", command=self.open_map)
    menu.add_command(label="Exit", command=self.root.quit)
    return menu

  def run(self):
    self.root.mainloop()
    
  def create_map(self):
    pass
    # self.label.config(text="New file created!")
    
  def open_map(self):
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")], initialdir="maps")
    if filename:
      # content = file.readline()
      self.label.config(text=filename)
    # self.label.config(text="File opened!")
    
  def draw_map(self, size, walls, agent_loc, goal_locs):
    rows, cols = size
    self.blocks = [[Block() for _ in range(cols)] for _ in range(rows)]
    
    
    
        
window = GUI()
window.run()