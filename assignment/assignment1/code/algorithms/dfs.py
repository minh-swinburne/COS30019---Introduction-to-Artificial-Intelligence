"""
Depth-First Search (DFS) Algorithm (uninformed)

Functions:
  - search(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform depth-first search to find the shortest path from the agent's location to a goal.
  - search_all(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform depth-first search to find the shortest path from the agent's location to all goals.

Main idea:
  The depth-first search algorithm is an uninformed search algorithm that explores the deepest nodes in the search tree first. It uses a stack to keep track of the nodes to be explored.

  For each cell, the algorithm explores all its neighbors in reverse order (right, down, left, up) and adds them to the stack if they are not blocked and have not been visited yet. The algorithm continues until it finds a goal cell or the stack is empty.
"""
from collections import deque

def search(agent:'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform depth-first search to find the shortest path from the agent's location to the goal.
  
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
  stack = deque([start])
  visited = {start}
  
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell
  
  while stack:
    # Pop the last cell from the stack
    current = stack.pop()
    # If the current cell is a goal, tell the agent to return the path
    if current in agent.goals:
      return {
        'path': agent.trace_path(current),
        'goal': current,
        'count': count
      }
    
    # print("Current:", current.location, "- Stack:", [cell.location for cell in stack], "- Neighbors: ", end="")
    
    # Explore all valid neighbors of the current cell (in reverse order to maintain the same direction priority order as BFS)
    for neighbor in agent.map.get_neighbors(current)[::-1]:
      if not neighbor.blocked and neighbor not in visited:
        # Increment the counter for each visited cell
        count += 1
        # Insert the neighbor at the beginning of the stack (LIFO)
        stack.append(neighbor)
        visited.add(neighbor)
        neighbor.parent = current
        # print(neighbor.location, end=" ")
    # print()
  # If no path is found, return the count of visited cells
  return count


def search_all(agent: 'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform depth-first search to find the shortest path from the agent's location to all goals.
  
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
  stack = deque([start])
  visited = {start}
  
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell
  
  path = []
  goals = []
  
  while stack:
    # Pop the last cell from the stack
    current = stack.pop()
    # If the current cell is a goal, add it to the list of goals
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
      stack = deque([current])
      visited = {current}
      current.parent = None
      continue
    
    # print("Current:", current.location, "- Stack:", [cell.location for cell in stack], "- Neighbors: ", end="")
    
    # Explore all valid neighbors of the current cell (in reverse order to maintain the same direction priority order as BFS)
    for neighbor in agent.map.get_neighbors(current)[::-1]:
      if not neighbor.blocked and neighbor not in visited:
        # Increment the counter for each visited cell
        count += 1
        # Insert the neighbor at the beginning of the stack (LIFO)
        stack.append(neighbor)
        visited.add(neighbor)
        neighbor.parent = current
        # print(neighbor.location, end=" ")
    # print()
  # If no path is found, return the count of visited cells
  return count
  

# Test the algorithm
if __name__ == "__main__":
  import sys, os

  directory = os.path.dirname(os.path.dirname(__file__))
  sys.path.append(directory)

  from environment import *
  from map import *
  
  for file in os.listdir(os.path.join(directory, "maps")):
    print(file)
    grid_size, agent_loc, goal_locs, walls = load_map(file)
    map = Grid(grid_size, walls)
    agent = Agent(map, agent_loc, goal_locs)
    print_map(grid_size, agent_loc, goal_locs, walls)
    result = search(agent)
    print("Search:", result, "\n")
    result = search_all(agent)
    print("Search All:", result, "\n")