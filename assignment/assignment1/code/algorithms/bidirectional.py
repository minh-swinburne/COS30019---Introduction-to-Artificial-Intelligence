"""
Bidirectional search algorithm (informed)

Functions:
  - search(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform bidirectional A* search to find the shortest path from the agent's location to the (seemingly) nearest goal.
  - search_all(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform bidirectional A* search to find the shortest path from the agent's location to all goals.
  
Main idea:
  The bidirectional A* search algorithm is an informed search algorithm that explores the search space from both the start and goal cells simultaneously. It uses two open lists to keep track of the cells to be explored from the start and goal cells. The algorithm continues until it finds a common cell in both open lists or one of the open lists is empty.

  For each cell, the algorithm explores all its neighbors (in the order of up, left, down, right) and adds them to the open list if they are not blocked and have not been visited yet. The algorithm continues until it finds a common cell in both open lists or one of the open lists is empty.
"""
import heapq

def search(agent:'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform bidirectional A* search to find the shortest path from the agent's location to the goal.
  
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
  
  # Initialize the counter of the result dictionary
  count = 1 # Start with 1 for the start cell
  
  # Use a list as a priority 
  # open_list_start = [start]queue
  # open_list_goal = [goal]
  
  # Use a heap as a priority queue
  open_list_start = [] 
  heapq.heappush(open_list_start, start)
  open_list_goal = []
  heapq.heappush(open_list_goal, goal)
  
  closed_set_start = set()
  closed_set_goal = set()
  
  while open_list_start and open_list_goal:
    # Update the current start and goal cells
    # current_start = min(open_list_start, key=lambda cell: cell.f)
    # open_list_start.remove(current_start)
    # current_goal = min(open_list_goal, key=lambda cell: cell.f)
    # open_list_goal.remove(current_goal)
    current_start = heapq.heappop(open_list_start)
    current_goal = heapq.heappop(open_list_goal)
    
    closed_set_start.add(current_start)    
    closed_set_goal.add(current_goal)
     
    # print(f"Open List Start: {open_list_start} - Open List Goal: {open_list_goal}")    
    # print(f"Current Start: {current_start} <= {current_start.parent} - Current Goal: {current_goal} <= {current_goal.parent}\n")
    
    # Explore the neighbors of the current start
    for neighbor in agent.map.get_neighbors(current_start):
      if neighbor.blocked or neighbor in closed_set_start:
        continue
      
      tentative_g = current_start.g + 1
      if neighbor not in open_list_start:
        if neighbor.parent: # If the neighbor has a parent, a path is found
          # print("Tracing path from current start:", current_start, "to", neighbor)
          path_start = agent.trace_path(current_start)
          path_goal = agent.trace_path(neighbor, backward=False)
          return {
            'path': path_start + [current_start - neighbor] + path_goal,
            'goal': goal,
            'count': count
          }
        count += 1
        # Update the g and h values, and parent for the neighbor cell
        neighbor.g = tentative_g
        neighbor.h = neighbor.manhattan_distance(goal)
        neighbor.parent = current_start
        # Add the neighbor to the open list
        # open_list_start.append(neighbor)
        heapq.heappush(open_list_start, neighbor)
      elif tentative_g < neighbor.g:
        neighbor.g = tentative_g
        neighbor.parent = current_start
        # Reheapify the open list after updating the g value
        heapq.heapify(open_list_start)
    
    for neighbor in agent.map.get_neighbors(current_goal):
      if neighbor.blocked or neighbor in closed_set_goal:
        continue
      
      tentative_g = current_goal.g + 1
      if neighbor not in open_list_goal:
        count += 1
        if neighbor.parent:
          # print("Tracing path from current goal:", current_goal, "to", neighbor)
          path_start = agent.trace_path(neighbor)
          path_goal = agent.trace_path(current_goal, backward=False)
          return {
            'path': path_start + [neighbor - current_goal] + path_goal,
            'goal': goal,
            'count': count
          }
        neighbor.g = tentative_g
        neighbor.h = neighbor.manhattan_distance(start)
        neighbor.parent = current_goal
        # open_list_goal.append(neighbor)
        heapq.heappush(open_list_goal, neighbor)
      elif tentative_g < neighbor.g:
        neighbor.g = tentative_g
        neighbor.parent = current_goal
        heapq.heapify(open_list_goal)
  # If no path is found, return the count of visited cells
  return count


def search_all(agent:'Agent') -> dict[list[str], 'Cell', int] | int:
  """
  Perform bidirectional A* search to find the shortest path from the agent's location to all goals.
  
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
  
  open_list_start = []
  heapq.heappush(open_list_start, start)
  open_list_goal = []
  heapq.heappush(open_list_goal, goal)
  
  closed_set_start = set()
  closed_set_goal = set()
  
  count = 1
  path = []
  goals = []
  
  while open_list_start and open_list_goal:
    current_start = heapq.heappop(open_list_start)
    current_goal = heapq.heappop(open_list_goal)
    
    closed_set_start.add(current_start)
    closed_set_goal.add(current_goal)
    
    found_goal = False
    
    for neighbor in agent.map.get_neighbors(current_start):
      if neighbor.blocked or neighbor in closed_set_start:
        continue      
      tentative_g = current_start.g + 1
      if neighbor not in open_list_start:
        count += 1
        if neighbor.parent:
          found_goal = True
          goals.append(goal)
          agent.goals.remove(goal)
          # Extend the path
          path_start = agent.trace_path(current_start)
          path_goal = agent.trace_path(neighbor, backward=False)
          path.extend(path_start + [current_start - neighbor] + path_goal)
          break        
        neighbor.g = tentative_g
        neighbor.h = neighbor.manhattan_distance(goal)
        neighbor.parent = current_start
        heapq.heappush(open_list_start, neighbor)
      elif tentative_g < neighbor.g:
        neighbor.g = tentative_g
        neighbor.parent = current_start
        heapq.heapify(open_list_start)
    
    for neighbor in agent.map.get_neighbors(current_goal):
      if neighbor.blocked or neighbor in closed_set_goal:
        continue      
      tentative_g = current_goal.g + 1
      if neighbor not in open_list_goal:
        count += 1
        if neighbor.parent and not found_goal:
          found_goal = True
          goals.append(goal)
          agent.goals.remove(goal)
          # Extend the path
          path_start = agent.trace_path(neighbor)
          path_goal = agent.trace_path(current_goal, backward=False)
          path.extend(path_start + [neighbor - current_goal] + path_goal)
          break
        
        neighbor.g = tentative_g
        neighbor.h = neighbor.manhattan_distance(start)
        neighbor.parent = current_goal
        heapq.heappush(open_list_goal, neighbor)
      elif tentative_g < neighbor.g:
        neighbor.g = tentative_g
        neighbor.parent = current_goal
        heapq.heapify(open_list_goal)
    
    # If a goal is found, reset the search state for the next goal
    if found_goal:
      if not agent.goals:
        return {
          'path': path,
          'goal': goals,
          'count': count
        }
      agent.map.reset()
      agent.cell = goal
      start = agent.cell
      goal = agent.get_nearest_goal()
      start.h = start.manhattan_distance(goal)
      
      open_list_start = []
      heapq.heappush(open_list_start, start)
      closed_set_start = set()
      
      open_list_goal = []
      heapq.heappush(open_list_goal, goal)
      closed_set_goal = set()
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
    print("Search:", result, "\n")
    result = search_all(agent)
    print("Search All:", result, "\n\n")