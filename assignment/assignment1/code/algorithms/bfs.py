"""
Breadth-First Search (BFS) Algorithm (uninformed)
"""

def search(agent:'Agent') -> list[str]:
  """
  Perform breadth-first search to find the shortest path from the agent's location to the goal.
  
  Args:
    agent (Agent): The agent object.
    
  Returns:
    dict: A dictionary to store the result of the search with the following keys:
      - 'path' (list[str]): A list of directions (up, left, down, right) to reach the goal. Empty list if no path is found.
      - 'goal' (Cell): The goal cell reached.
      - 'count' (int): The number of cells visited during the search.
  """
  start = agent.cell
  queue = [start]
  visited = {start}
  start.parent = None
  
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell
  
  while queue:
    # Pop the first cell from the queue
    current = queue.pop(0)
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


if __name__ == "__main__":
  import sys, os

  directory = os.path.dirname(os.path.dirname(__file__))
  sys.path.append(directory)

  from environment import *
  from map import *
  
  for filename in os.listdir(os.path.join(directory, "maps")):
    print(filename)
    grid_size, agent_loc, goal_locs, walls = load_map(filename)
    map = Grid(grid_size, walls)
    agent = Agent(map, agent_loc, goal_locs)
    print_map(grid_size, agent_loc, goal_locs, walls)
    result = search(agent)
    print("Result:", result, "\n")