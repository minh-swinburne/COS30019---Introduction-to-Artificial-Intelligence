"""
A* Search Algorithm (informed)

Functions:
  - search(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform A* search to find the shortest path from the agent's location to the seemingly nearest goal (estimated based on Manhattan distance).
  - search_all(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform A* search to find the shortest path from the agent's location to all goals.
  
Main idea:
  The A* search algorithm is an informed search algorithm that uses a heuristic function to estimate the cost of reaching the goal from a given cell. It combines the cost of reaching a cell (g) and the estimated cost of reaching the goal from that cell (h) to determine the priority of exploring the cell. The algorithm uses a priority queue to keep track of the cells to be explored.

  For each cell, the algorithm explores all its neighbors and calculates the g and h values for each neighbor. If the neighbor is not blocked and has not been visited yet, the algorithm adds the neighbor to the priority queue. The algorithm continues until it finds a goal cell or the priority queue is empty.
"""
import heapq

def search(agent:'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform A* search (informed) to find the shortest path from the agent's location to the goal.
  
  Args:
    agent (Agent): The agent object.
    
  Returns:
    If a path is found:
      dict: A dictionary to store the result of the search with the following keys:
        'path' (list[str]): A list of directions (up, left, down, right) to reach the goal.
        'goal' (Cell): The goal cell reached.
        'count' (int): The number of cells visited during the search.
    If no path is found:
      int: The number of cells visited during the search.
  """
  agent.map.reset()
  start = agent.cell
  # If the start cell is a goal, return an empty path immediately
  if start in agent.goals:
    return {
      'path': [],
      'goal': start,
      'count': 1
    }
  # Get the seemingly nearest goal based on Manhattan distance
  goal = agent.get_nearest_goal()
  # Initialize the h value for the start cell
  start.h = start.manhattan_distance(goal)
  # print("Start:", start, "Goal:", goal)
  
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell
  
  # open_list = [start] # Use a list as a priority queue
  open_list = [] # Use a heap as a priority queue
  heapq.heappush(open_list, start)
  closed_set = set()
  
  while open_list:
    # Get the cell with the lowest f value
    # current = min(open_list, key=lambda cell: cell.f)
    # open_list.remove(current)
    current = heapq.heappop(open_list)
    
    closed_set.add(current)
    # print(f"Open List: {open_list} - Current: {current} - Parent: {current.parent}")
    
    if current in agent.goals:
      return {
        'path': agent.trace_path(current),
        'goal': current,
        'count': count
      }
    
    for neighbor in agent.map.get_neighbors(current):
      if neighbor.blocked or neighbor in closed_set:
        continue
      
      tentative_g = current.g + 1
      if neighbor not in open_list:
        # print("Current:", current, "Neighbor:", neighbor)
        # Increment the counter for each visited cell
        count += 1
        # Update the g and h values for the neighbor cell
        neighbor.g = tentative_g
        neighbor.h = neighbor.manhattan_distance(goal)
        # Set the parent of the neighbor cell to the current cell
        neighbor.parent = current
        # Add the neighbor to the open list
        # open_list.append(neighbor)
        heapq.heappush(open_list, neighbor)
      elif tentative_g < neighbor.g: 
        # Update the neighbor's g value
        # print(current, neighbor)
        neighbor.g = tentative_g
        neighbor.parent = current
        # Reheapify the open list after updating the g value
        heapq.heapify(open_list)
  # If no path is found, return the count of visited cells
  return count


def search_all(agent:'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform A* search (informed) to find the shortest path from the agent's location to all goals.
  
  Args:
    agent (Agent): The agent object.
    
  Returns:
    If a path is found:
      dict: A dictionary to store the result of the search with the following keys:
        'path' (list[str]): A list of directions (up, left, down, right) to reach the goal.
        'goal' (Cell): The goal cell reached.
        'count' (int): The number of cells visited during the search.
    If no path is found:
      int: The number of cells visited during the search.
  """
  agent.map.reset()
  start = agent.cell
  goal = agent.get_nearest_goal()
  # print("Start:", start, "Goal:", goal)
  start.h = start.manhattan_distance(goal)
  
  open_list = []
  heapq.heappush(open_list, start)
  closed_set = set()
  
  count = 1
  path = []
  goals = []
  
  while open_list:
    # print("Open List:", open_list)
    current = heapq.heappop(open_list)
    closed_set.add(current)
    
    if current in agent.goals:
      goals.append(current)
      agent.goals.remove(current)
      path.extend(agent.trace_path(current))
      
      # If all goals are reached, return the result
      if not agent.goals:
        return {
          'path': path,
          'goal': goals,
          'count': count
        }
      
      # Reset the search state for the next goal
      open_list = []
      heapq.heappush(open_list, current)
      closed_set = set()
      agent.cell = current
      # Get the next nearest goal (seemingly)
      goal = agent.get_nearest_goal()
      current.g = 0
      current.h = current.manhattan_distance(goal)      
      current.parent = None
      # print("Next goal:", goal)
      continue
    
    for neighbor in agent.map.get_neighbors(current):
      if neighbor.blocked or neighbor in closed_set:
        continue
      
      tentative_g = current.g + 1
      if neighbor not in open_list:
        count += 1
        neighbor.g = tentative_g
        neighbor.h = neighbor.manhattan_distance(goal)
        neighbor.parent = current
        heapq.heappush(open_list, neighbor)
      elif tentative_g < neighbor.g:
        neighbor.g = tentative_g
        neighbor.parent = current
        heapq.heapify(open_list)
  return count  
  
  
if __name__ == "__main__":
  import sys, os

  directory = os.path.dirname(os.path.dirname(__file__))
  sys.path.append(directory)

  from environment import *
  from utils import *
  
  for file in get_available_maps():
    print(file)
    grid_size, agent_loc, goal_locs, walls = load_map(file)
    map = Grid(grid_size, walls)
    agent = Agent(map, agent_loc, goal_locs)
    print_map(grid_size, agent_loc, goal_locs, walls)
    result = search(agent)
    print("Search:", result, "\n")
    result = search_all(agent)
    print("Search All:", result, "\n\n")
    
    
    
    