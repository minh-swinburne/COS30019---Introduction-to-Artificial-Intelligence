"""
Handles the loading and printing of the map from a text file.

Functions:
  - load_map(file_name: str) -> Tuple[Tuple[int, int], Tuple[int, int], List[Tuple[int, int]], List[Tuple[int, int, int, int]]]
  - print_map(grid_size: Tuple[int, int], agent_loc: Tuple[int, int], goal_locs: List[Tuple[int, int]], walls: List[Tuple[int, int, int, int]]) -> None
"""
import os
# Function to list all modules in a package
from pkgutil import iter_modules

FILENAME = "RobotNav-test.txt"
FREE = '0'
AGENT = 'A'
GOAL = 'G'
WALL = '1'


def get_available_maps():
  """
  Get the list of available map files in the "maps" folder.
  
  Returns:
    list[str]: A list of map file names.
  """
  directory = os.path.dirname(__file__)
  map_dir = os.path.join(directory, "maps")
  return os.listdir(map_dir)


def get_available_algorithms():
  """
  Get the list of available algorithm files in the "algorithms" folder.
  
  Returns:
    list[str]: A list of algorithm file names.
  """
  directory = os.path.dirname(__file__)
  alg_dir = os.path.join(directory, "algorithms")
  modules = [name for _, name, _ in iter_modules([alg_dir])]
  return modules


def load_map(file_name=FILENAME):
  """
  Load the map from a text file.
  
  Args:
    file_name (str): The name of the text file containing the map.
    
  Returns:
    tuple[int, int]: grid size
    tuple[int, int]: agent's initial location
    list[tuple[int, int]]: goal locations
    list[tuple[int, int, int, int]]: wall locations
  """
  dir_path = os.path.dirname(__file__)
  dir_path = os.path.join(dir_path, "maps")
  file_path = os.path.join(dir_path, file_name)
  with open(file_path) as f:
    grid_size = f.readline().strip()    # This is a list of grid dimensions
    grid_size = eval(grid_size)
    
    agent_loc = f.readline().strip()    # This is a tuple of agent's initial location
    agent_loc = eval(agent_loc)
    
    goal_locs = f.readline().strip().split('|')    # This is a list of goal locations
    goal_locs = list(map(eval, goal_locs))
    
    walls = []                      # This is a list of wall locations
    wall = f.readline().strip()
    while wall:                    # Read until the end of the file
      walls.append(eval(wall))
      wall = f.readline().strip()   
    
  return grid_size, agent_loc, goal_locs, walls


def print_map(grid_size, agent_loc, goal_locs, walls, end="\n"):
  """
  Print the map to the console.
  
  Args:
    grid_size (Tuple[int, int]): The dimensions of the grid.
    agent_loc (Tuple[int, int]): The agent's initial location.
    goal_locs (List[Tuple[int, int]]): A list of goal locations.
    walls (List[Tuple[int, int, int, int]]): A list of wall locations.
    
  Returns:
    None
  """
  height, width = grid_size
  for y in range(height):
    for x in range(width):
      if (x, y) == agent_loc:
        print(AGENT, end="")
      elif (x, y) in goal_locs:
        print(GOAL, end="")
      else:
        is_wall = False
        for wall in walls:
          if wall[0] <= x < wall[0] + wall[2] and wall[1] <= y < wall[1] + wall[3]:
            print(WALL, end="")
            is_wall = True
            break
        if not is_wall:
          print(FREE, end="")
    print()
  print(end, end="")
  
  
def suggest_help():
  """
  Suggest the user to use the help option of search.py.
  
  Returns:
    None
  """
  print("\nFor more information, use the help option: 'python search.py help'\n")
  
if __name__ == "__main__":  
  result = grid_size, agent_loc, goal_locs, walls = load_map("no_goal.txt")
  print_map(*result)
  print("Available maps:", get_available_maps())
  print("Available algorithms:", get_available_algorithms())