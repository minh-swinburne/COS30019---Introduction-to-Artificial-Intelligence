"""
Greedy Best-First Search Algorithm (informed)
"""

def search(agent:'Agent') -> list[str]:
  """
  Perform greedy search (informed) to find the shortest path from the agent's location to the goal.
  
  Args:
    agent (Agent): The agent object.
    
  Returns:
    dict: A dictionary to store the result of the search with the following keys:
      - 'path' (list[str]): A list of directions (up, left, down, right) to reach the goal. Empty list if no path is found.
      - 'goal' (Cell): The goal cell reached.
      - 'count' (int): The number of cells visited during the search.
  """
  start = agent.cell
  goal = agent.get_nearest_goal()
  
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell
  
  start.h = start.manhattan_distance(goal)
  open_list = [start]
  closed_set = set()
  
  
  while open_list:
    current = min(open_list, key=lambda cell: cell.h)
    open_list.remove(current)
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
      if neighbor not in open_list:
        # Increment the counter for each visited cell
        count += 1
        open_list.append(neighbor)
        neighbor.h = neighbor.manhattan_distance(goal)
        neighbor.parent = current
  # If no path is found, return the count of visited cells
  return count


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
    print("Result:", result, "\n")