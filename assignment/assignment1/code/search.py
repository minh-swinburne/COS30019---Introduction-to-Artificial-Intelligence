import sys
# Function to import needed search algorithm
from importlib import import_module
# Functions to handle map files
from map import *
# Classes of the environment
from environment import *

# Get system arguments
args = sys.argv

# Process the system arguments
try:
  # Get the map file name and search algorithm
  filename = args[1]
  method = args[2].lower()
  
  # Load the map and create the agent
  size, agent_loc, goal_locs, walls = load_map(filename)
  map = Grid(size, walls)
  agent = Agent(map, agent_loc, goal_locs)
  
  # Import the desired search algorithm from the algorithms package
  algorithm = import_module(name="algorithms." + method)
  
  limit = 0
  if algorithm.__name__ == 'algorithms.iddfs':
    limit_str = args[3] if len(args) > 3 else input("Enter the limit of number of visited cells (Default 100,000): ").strip()
    if limit_str != "" and type(eval(limit_str)) == int:
      limit = int(limit_str)
      
  if limit != 0:
    result = algorithm.search(agent, limit)
  else:
    result = algorithm.search(agent)
  
  # Print the result of the search
  print(filename, method)
  if type(result) == dict: # A goal is found
    print(result['goal'], result['count'])
    print(result['path'])
  else: # No goal is found
    print("No goal is reachable;", result)
    
# In case of missing arguments
except IndexError:
  print("Please provide the name of the map file and search algorithm with this format: 'python search.py <filename> <method>'")
  print("Example: 'python search.py RobotNav-test.txt dfs')")
  
# In case of inexistent map file
except FileNotFoundError: 
  import os
  directory = os.path.dirname(__file__)
  map_dir = os.path.join(directory, 'maps')
  print("Map file not found. Available maps are:", os.listdir(map_dir))
  
# In case of invalid search algorithm
except ModuleNotFoundError: 
  # Function to list all modules in a package
  from pkgutil import iter_modules  
  modules = [name for _, name, _ in iter_modules(['algorithms'])]
  print("Search algorithm not found. Allowed algorithms are:", modules)