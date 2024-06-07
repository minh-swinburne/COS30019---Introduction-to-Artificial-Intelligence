"""
Iterative Deepening Depth-First Search (IDDFS) Algorithm (uninformed)
"""

def search(agent:'Agent', limit:int=10**5) -> list[str]:
  """
  Perform iterative deepening depth-first search to find the shortest path from the agent's location to the goal.
  
  Args:
    agent (Agent): The agent object.
    
  Returns:
    dict: A dictionary to store the result of the search with the following keys:
      - 'path' (list[str]): A list of directions (up, left, down, right) to reach the goal. Empty list if no path is found.
      - 'goal' (Cell): The goal cell reached.
      - 'count' (int): The number of cells visited during the search.
  """
  # Define a recursive depth-limited search function
  def dls(src:'Cell', current:'Cell', target:'Cell', max_depth:int, map:'Grid', visited:set) -> bool:
    nonlocal count, limit
    
    print("Depth:", max_depth, "- Current:", current.location, "<= ", current.parent, "- Neighbors: ", map.get_neighbors(current))
    
    if current == target:
      # print("Found target:", target.location)
      return True
    # If the maximum depth is reached, stop recursion
    if max_depth <= 0:
      return False
    
    for neighbor in map.get_neighbors(current):
      # If the number of visited cells exceeds the limit, stop recursion and accept failure
      if count >= limit:
        return False
      # Skip blocked cells
      if neighbor.blocked or neighbor in visited:
        continue      
      # print("Source:", src.location, "- Neighbor:", neighbor.location, "- Count:", count)
      # print("Visited:", visited)
      visited.add(neighbor)
      count += 1
      if dls(src, neighbor, target, max_depth - 1, map, visited):
        neighbor.parent = current
        return True
      visited.remove(neighbor)
    return False
  
  start = agent.cell
  goal = agent.get_nearest_goal()
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell
  
  max_depth = agent.map.net_area
  # print("Max Depth:", max_depth)
  for depth in range(max_depth + 1):
    # print("\nDepth:", depth)
     # Initialize a set to store visited cells for each depth
    visited = {start}
    if dls(start, start, goal, depth, agent.map, visited):
      # print("Path found!")
      return {
        'path': agent.trace_path(goal),
        'goal': goal,
        'count': count
      }
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