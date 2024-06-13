"""
Greedy Best-First Search Algorithm (informed)

Functions:
  - search(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform greedy search to find the shortest path from the agent's location to the (seemingly) nearest goal.
  - search_all(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform greedy search to find the shortest path from the agent's location to all goals.
  
Main idea:
  The greedy best-first search algorithm is an informed search algorithm that explores the search space based on the heuristic value of each cell. It uses a priority queue to keep track of the cells to be explored. The algorithm continues until it finds a goal cell or the priority queue is empty.

  For each cell, the algorithm explores all its neighbors (in the order of up, left, down, right) and adds them to the priority queue if they are not blocked and have not been visited yet. The algorithm continues until it finds a goal cell or the priority queue is empty.
"""
import heapq

def search(agent:'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform greedy search (informed) to find the shortest path from the agent's location to the goal.
  
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
  start.h = start.manhattan_distance(goal)
  
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell
  
  # open_list = [start]
  # Use a heap as a priority queue
  open_list = []
  # Push the start cell with its h value to the heap
  heapq.heappush(open_list, (start.h, start))
  closed_set = set()
  
  while open_list:
    # current = min(open_list, key=lambda cell: cell.h)
    # open_list.remove(current)
    # Pop the cell with the lowest h value (ignoring the h value)
    _, current = heapq.heappop(open_list)
    closed_set.add(current)
    
    if current in agent.goals:
      return {
        'path': agent.trace_path(current),
        'goal': current,
        'count': count
      }
    
    for neighbor in agent.map.get_neighbors(current):
      if neighbor.blocked or neighbor in closed_set:
        continue
      if neighbor not in [cell for _, cell in open_list]:
        # Increment the counter for each visited cell
        count += 1
        neighbor.h = neighbor.manhattan_distance(goal)
        neighbor.parent = current
        # open_list.append(neighbor)
        # Push the neighbor cell with its h value to the heap
        heapq.heappush(open_list, (neighbor.h, neighbor))
  # If no path is found, return the count of visited cells
  return count


def search_all(agent:'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform greedy search (informed) to find the shortest path from the agent's location to all goals.
  
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
  start.h = start.manhattan_distance(goal)
  
  # open_list = [start]
  open_list = []
  heapq.heappush(open_list, (start.h, start))
  closed_set = set()
  
  count = 1
  path = []
  goals = []
  
  while open_list:
    # current = min(open_list, key=lambda cell: cell.h)
    # open_list.remove(current)
    _, current = heapq.heappop(open_list)
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
      heapq.heappush(open_list, (current.h, current))
      closed_set = set()
      # Get the next nearest goal (seemingly)
      goal = agent.get_nearest_goal()
      current.h = current.manhattan_distance(goal)      
      current.parent = None
      # print("Next goal:", goal)
      continue
    
    for neighbor in agent.map.get_neighbors(current):
      if neighbor.blocked or neighbor in closed_set:
        continue
      if neighbor not in [cell for _, cell in open_list]:
        # Increment the counter for each visited cell
        count += 1
        neighbor.h = neighbor.manhattan_distance(goal)
        neighbor.parent = current
        # open_list.append(neighbor)
        heapq.heappush(open_list, (neighbor.h, neighbor))
  # If no path is found, return the count of visited cells
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