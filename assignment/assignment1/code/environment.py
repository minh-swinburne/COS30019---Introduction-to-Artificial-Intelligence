"""
Classes to represent the environment, including Cell, Grid and Agent.

Classes:
  Cell: A class to represent a cell in the grid.
  Grid: A class to represent a grid.
  Agent: A class to represent an agent in the grid.
"""

class Cell:
  """
  A class to represent a cell in the grid.
  
  Attributes:
    x (int): The x coordinate of the cell.
    y (int): The y coordinate of the cell.
    parent (Cell): The parent cell of the current cell.
    g (int): The distance from the start node.
    h (int): The distance from the end node.
    blocked (bool): The blocked status of the cell.
    
  Methods:
    __eq__(self, other) -> bool: Compare the cell with another cell based on their locations.
    __hash__(self): Return the hash value of the cell.
    __sub__(self, other) -> str: Get the direction from the current cell to another.
    __repr__(self): Return the string representation
    manhattan_distance(self, other) -> int: Calculate the Manhattan distance between the current cell and another cell.
  
  Properties:
    location -> tuple[int, int]: Return the location of the cell as a tuple (x, y).
    f -> int: Calculate the total cost of the cell - sum of g and h.
  """
  def __init__(self, x: int, y: int, parent: 'Cell' = None):
    self.x = x  # x coordinate
    self.y = y  # y coordinate
    self.parent = parent    # Parent cell
    self.g = 0  # Distance from start node
    self.h = 0  # Distance from end node
    # self.f = 0  # Total cost
    self.blocked = False  # Blocked status
    
  def __eq__(self, other: 'Cell'):
    """
    Compare the cell with another cell based on their locations.
    """
    return self.x == other.x and self.y == other.y
  
  def __hash__(self) -> int:
    """
    Return the hash value of the cell.
    """
    return hash((self.x, self.y))
  
  def __sub__(self, other: 'Cell') -> str:
    """
    Subtract the x and y coordinates of the current cell from the x and y coordinates of another cell.
    @return: The direction from the current cell to the other cell.
    """
    dx, dy = other.x - self.x, other.y - self.y
    if dx == 0:
      return "up" if dy < 0 else "down"
    return "left" if dx < 0 else "right"
  
  def __repr__(self) -> str:
    """
    Return the string representation of the cell.
    """
    return f"<Cell ({self.x}, {self.y})>"
  
  def manhattan_distance(self, other: 'Cell') -> int:
    """
    Calculate the Manhattan distance between the current cell and another cell.
    """
    return abs(self.x - other.x) + abs(self.y - other.y)
  
  @property
  def location(self):
    """
    Return the location of the cell as a tuple (x, y).
    """
    return self.x, self.y
  
  @property
  def f(self):
    """
    Calculate the total cost of the cell - sum of g and h.
    """
    return self.g + self.h
  
  
class Grid:
  """"
  A class to represent a grid.
  
  Attributes:
    height (int): The height of the grid.
    width (int): The width of the grid.
    grid (list[list[Cell]]): A 2D list of cells representing the grid.
    
  Methods:
    get_cell(self, location: tuple[int, int]) -> Cell: Get the cell at the given coordinates.
    is_valid(self, x: int, y: int) -> bool: Check if the cell at the given coordinates is valid.
    get_neighbors(self, cell: Cell) -> list[Cell]: Get the neighbors of the cell at the given coordinates.
    
  Properties:
    size -> tuple[int, int]: Return the size of the grid as a tuple (height, width).
    net_area -> int: Calculate the net area of the grid (total area - blocked area).
  """
  def __init__(self, size: tuple[int, int], walls: list[tuple[int, int, int, int]]):
    self.height, self.width = size
    # Create a 2D list of cells
    self.grid = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
    # Set the blocked status of the cells based on the walls
    for wall in walls:
      start_x, start_y, width, height = wall
      for row in range(start_y, start_y + height):
        for col in range(start_x, start_x + width):
          self.grid[row][col].blocked = True
  
  def get_cell(self, location: tuple[int, int]) -> Cell:
    """
    Get the cell at the given coordinates.
    """
    x, y = location
    return self.grid[y][x]
  
  def is_valid(self, x: int, y: int) -> bool:
    """
    Check if the cell at the given coordinates is valid.
    """
    return 0 <= x < self.width and 0 <= y < self.height    
  
  def get_neighbors(self, cell: Cell) -> list[Cell]:
    """
    Get the neighbors of the cell at the given coordinates."""
    neighbors = []
    # Add 4 neighbors IN ORDER (up, left, down, right) around the cell
    for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
      if self.is_valid(cell.x + dx, cell.y + dy):
        neighbors.append(self.grid[cell.y + dy][cell.x + dx])
        
    # for x in range(-1, 2):  # Loop through the 3x3 grid around the cell
    #   for y in range(-1, 2): 
    #     if x == 0 and y == 0:
    #       continue
    #     if self.is_valid(cell.x + x, cell.y + y):
    #       neighbors.append(self.grid[cell.y + y][cell.x + x])
          
    return neighbors
  
  @property
  def size(self):
    """
    Return the size of the grid as a tuple (height, width).
    """
    return self.height, self.width
  
  @property
  def net_area(self):
    """
    Calculate the net area of the grid (total area - blocked area).
    """
    return self.height * self.width - sum(cell.blocked for row in self.grid for cell in row)
    
    
class Agent:
  """
  A class to represent an agent in the grid.
  
  Attributes:
    map (Grid): The grid object.
    cell (Cell): The cell object representing the agent's location.
    goals (list[Cell]): A list of cell objects representing the goal locations.
    
  Methods:
    trace_path(self, cell: Cell, backward=True) -> list[str]: Given the goal cell, return the path from the start cell to the goal cell as a list of directions (up, down, left, right).
    get_nearest_goal(self) -> tuple[int, int]: Get the nearest goal to the agent's current location (Manhattan distance).
  """
  def __init__(self, map: Grid, location: tuple[int, int], goals: list[tuple[int, int]]):
    self.map = map
    self.cell = map.get_cell(location)
    self.goals = []
    for goal in goals:
      cell = self.map.get_cell(goal)
      self.goals.append(cell)

  def trace_path(self, cell: Cell, backward=True) -> list[str]:
    """
    Given the goal cell, return the path from the start cell to the goal cell as a list of directions (up, down, left, right).
    
    Args:
      cell (Cell): The goal cell.
      backward (bool): The direction of the path.
      
    Returns:
      list[str]: A list of directions (up, down, left, right) to reach the goal cell.
    """
    path = []
    while cell.parent:
      # print(f"Cell: {cell.location} - Parent: {cell.parent.location}")
      if backward:
        path.insert(0, cell.parent - cell)
      else:
        path.append(cell - cell.parent)
      cell = cell.parent
    return path
  
  def get_nearest_goal(self) -> tuple[int, int]:
    """
    Get the nearest goal to the agent's current location (Manhattan distance).
    """
    agent = self.cell
    return min(self.goals, key=lambda goal: agent.manhattan_distance(goal))


if __name__ == "__main__":
  from map import *
  grid_size, agent_loc, goal_locs, walls = load_map()
  map = Grid(grid_size, walls)
  agent = Agent(map, agent_loc, goal_locs)
  print_map(grid_size, agent_loc, goal_locs, walls)
  # path = agent.bfs()
  # print(path)