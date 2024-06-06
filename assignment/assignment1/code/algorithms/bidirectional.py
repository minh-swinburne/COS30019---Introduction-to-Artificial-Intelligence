"""
Bidirectional search algorithm (informed)
"""

def search(agent:'Agent') -> list[str]:
  """
  Perform bidirectional A* search to find the shortest path from the agent's location to the goal.
  
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
  
  open_list_start = [start]
  open_list_goal = [goal]
  closed_set_start = set()
  closed_set_goal = set()
  
  while open_list_start and open_list_goal:
    # Update the current start and goal cells
    current_start = min(open_list_start, key=lambda cell: cell.f)
    current_goal = min(open_list_goal, key=lambda cell: cell.f)
    
    # print(f"Open List Start: {open_list_start} - Open List Goal: {open_list_goal}")    
    # print(f"Current Start: {current_start} <= {current_start.parent} - Current Goal: {current_goal} <= {current_goal.parent}\n")
    
    open_list_start.remove(current_start)
    closed_set_start.add(current_start)
    
    open_list_goal.remove(current_goal)
    closed_set_goal.add(current_goal)
    
    # Explore the neighbors of the current start
    for neighbor in agent.map.get_neighbors(current_start):
      if neighbor.blocked or neighbor in closed_set_start:
        continue
      if neighbor not in open_list_start:
        if neighbor.parent:
          # print("Tracing path from current start:", current_start, "to", neighbor)
          path_start = agent.trace_path(current_start)
          path_goal = agent.trace_path(neighbor, backward=False)
          return {
            'path': path_start + [current_start - neighbor] + path_goal,
            'goal': goal,
            'count': count
          }
        count += 1
        open_list_start.append(neighbor)
        # Update the g and h values for the neighbor cell
        neighbor.g = current_start.g + 1
        neighbor.h = neighbor.manhattan_distance(goal)
        neighbor.parent = current_start
      elif current_start.g + 1 < neighbor.g:
        neighbor.g = current_start.g + 1
        neighbor.parent = current_start
    
    for neighbor in agent.map.get_neighbors(current_goal):
      if neighbor.blocked or neighbor in closed_set_goal:
        continue
      if neighbor not in open_list_goal:
        if neighbor.parent:
          # print("Tracing path from current goal:", current_goal, "to", neighbor)
          path_start = agent.trace_path(neighbor)
          path_goal = agent.trace_path(current_goal, backward=False)
          return {
            'path': path_start + [neighbor - current_goal] + path_goal,
            'goal': goal,
            'count': count
          }
        count += 1
        open_list_goal.append(neighbor)
        # Update the g and h values for the neighbor cell
        neighbor.g = current_goal.g + 1
        neighbor.h = neighbor.manhattan_distance(start)
        neighbor.parent = current_goal
        # current_goal.parent = neighbor
      elif current_goal.g + 1 < neighbor.g:
        neighbor.g = current_goal.g + 1
        neighbor.parent = current_goal
        # current_goal.parent = neighbor
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