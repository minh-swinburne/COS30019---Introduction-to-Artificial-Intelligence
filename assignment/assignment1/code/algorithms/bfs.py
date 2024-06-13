"""
Breadth-First Search (BFS) Algorithm (uninformed)

Functions:
  - search(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform breadth-first search to find the shortest path from the agent's location to the nearest goal.
  - search_all(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform breadth-first search to find the shortest path from the agent's location to all goals.

Main idea:
  The breadth-first search algorithm is an uninformed search algorithm that explores all the nodes at the present depth before moving on to the nodes at the next depth level. It uses a queue to keep track of the nodes to be explored.

  For each cell, the algorithm explores all its neighbors (in the order of up, left, down, right) and adds them to the queue if they are not blocked and have not been visited yet. The algorithm continues until it finds a goal cell or the queue is empty.
"""
from collections import deque

def search(agent:'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform breadth-first search to find the shortest path from the agent's location to the goal.
  
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
  queue = deque([start])
  visited = {start}
  
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell
  
  while queue:
    # Pop the first cell from the queue
    current = queue.popleft()
    # If the current cell is a goal, tell the agent to return the path
    if current in agent.goals:
      return {
        'path': agent.trace_path(current),
        'goal': current,
        'count': count
      }
    
    # print("Current:", current.location, end=" - Neighbors: ")
    
    # Explore all valid neighbors of the current cell
    for neighbor in agent.map.get_neighbors(current):
      if not neighbor.blocked and neighbor not in visited:
        # Increment the counter for each visited cell
        count += 1
        # Append the neighbor to the end of the queue (FIFO)
        queue.append(neighbor)
        visited.add(neighbor)
        neighbor.parent = current
        # print(neighbor.location, end=" ")
    # print()
  # If no path is found, return the count of visited cells
  return count


def search_all(agent:'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform breadth-first search to find the shortest path from the agent's location to all goals.
  
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
  queue = deque([start])
  visited = {start}
  
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell

  path = []
  goals = []
  
  while queue:
    # print("Queue:", [cell.location for cell in queue])
    # print("Visited:", [cell.location for cell in visited])
    # Pop the first cell from the queue
    current = queue.popleft()
    # If the current cell is a goal, add it to the list of goals
    if current in agent.goals:
      goals.append(current)
      agent.goals.remove(current)
      path.extend(agent.trace_path(current))
      # print(f"Goal reached: {current.location} - Remaining goals: {len(agent.goals)}\n")
      
      # If all goals are reached, return the result
      if not agent.goals:
        return {
          'path': path,
          'goal': goals,
          'count': count
        }
      
      # Reset the search state for the next goal
      queue = deque([current])
      visited = {current}
      current.parent = None
      continue
    
    # print(f"Current: {current} <= {current.parent} - Neighbors: ", end="")
    
    # Explore all valid neighbors of the current cell
    for neighbor in agent.map.get_neighbors(current):
      if not neighbor.blocked and neighbor not in visited:
        # Increment the counter for each visited cell
        count += 1
        # Append the neighbor to the end of the queue (FIFO)
        queue.append(neighbor)
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