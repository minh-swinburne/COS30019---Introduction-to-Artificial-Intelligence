"""
Iterative Deepening Depth-First Search (IDDFS) Algorithm (uninformed)
  
Functions:
  - dls(agent:'Agent', current: 'Cell', max_depth: int, visited: set, count: int, limit: int) -> dict[bool, int]: Perform depth-limited search to find the shortest path from the current cell to the target cell.
  - search(agent:'Agent', limit: int=10**5) -> dict[list[str], 'Cell', int] | int: Perform iterative deepening depth-first search to find the shortest path from the agent's location to the goal.
  - search_all(agent:'Agent', limit: int=10**5) -> dict[list[str], 'Cell', int] | int: Perform iterative deepening depth-first search to find the shortest path from the agent's location to all goals.

Main idea:
  The iterative deepening depth-first search algorithm is an uninformed search algorithm that combines the benefits of depth-first search and breadth-first search. It performs depth-limited search with increasing depth limits until the goal is found. The algorithm continues until it finds a goal cell or the maximum depth is reached.
  
  For each cell, the algorithm explores all its neighbors in the order of up, left, down, right and adds them to the stack if they are not blocked and have not been visited yet. The algorithm continues until it finds a goal cell or the maximum depth is reached.
  
  The algorithm also includes a limit parameter to stop the search if the number of visited cells exceeds the limit.
"""


def dls(agent: 'Agent', current: 'Cell', max_depth: int, visited: set, count: int, limit: int) -> dict[bool, 'Cell', int]:
    """
    Perform depth-limited search to find the shortest path from the current cell to the target cell.

    Args:
        agent (Agent): The agent object.
        current (Cell): The current cell.
        max_depth (int): The maximum depth to explore.
        visited (set): A set to store visited cells.
        count (int): The number of cells visited during the search.
        limit (int): The maximum number of cells to visit during the search before stopping.

    Returns:
        dict: A dictionary to store the result of the search with the following keys:
            'success' (bool): True if the target cell is found; False otherwise.
            'count' (int): The number of cells visited during the search.
            'goal' (Cell): The goal cell reached. If the target cell is not found, this key is not included.
            # 'reason' (Reason): The reason for stopping the search. If the target cell is found, this key is not included.
    """
    # print("Depth:", max_depth, "- Current:", current.location, "<= ", current.parent, "- Neighbors: ", map.get_neighbors(current), "- Visited:", visited)

    if current in agent.goals:
        # print("Found goal:", current.location)
        return {
            'success': True,
            'goal': current,
            'count': count
        }
    # If the maximum depth is reached, stop recursion
    if max_depth <= 0:
        return {
            'success': False,
            'count': count
        }

    for neighbor in agent.grid.get_neighbors(current):
        # If the number of visited cells exceeds the limit, stop recursion and accept failure
        if count >= limit:
            return {
                'success': False,
                'count': count
            }
        # Skip blocked cells
        if neighbor.blocked or neighbor in visited:
            continue
        # print("- Neighbor:", neighbor.location, "- Count:", count)
        # print("Visited:", visited)
        visited.add(neighbor)
        count += 1
        result = dls(agent, neighbor, max_depth - 1, visited, count, limit)
        count = result['count']
        if result['success']:
            neighbor.parent = current
            return {
                'success': True,
                'goal': result['goal'],
                'count': count
            }
        visited.remove(neighbor)
    # If the target cell is not found, return the count of visited cells
    return {
        'success': False,
        'count': count
    }


def search(agent: 'Agent', limit: int = 10**5) -> dict[list[str], 'Cell', int] | int:
    """
    Perform iterative deepening depth-first search to find the shortest path from the agent's location to the goal.

    Args:
        agent (Agent): The agent object.
        limit (int): The maximum number of cells to visit during the search before stopping. Default is 100,000.

    Returns:
        If a path is found:
            dict: A dictionary to store the result of the search with the following keys:
            'path' (list[str]): A list of directions (up, left, down, right) to reach the goal.
            'goal' (Cell): The goal cell reached.
            'count' (int): The number of cells visited during the search.
        If no path is found:
            int: The number of cells visited during the search.
    """
    agent.grid.reset()
    start = agent.cell
    max_depth = agent.grid.net_area
    # print("Max Depth:", max_depth)
    # Initialize the counter of the result dictionary
    count = 1  # Start with 1 for the start cell

    for depth in range(max_depth + 1):
        # print("\nDepth:", depth)
       # Initialize a set to store visited cells for each depth
        visited = {start}
        result = dls(agent, start, depth, visited, count, limit)
        count = result['count']
        if result['success']:
            # print("Path found!")
            return {
                'path': agent.trace_path(result['goal']),
                'goal': result['goal'],
                'count': count
            }
    # If no path is found, return the count of visited cells
    return count


def search_all(agent: 'Agent', limit: int = 10**5) -> dict[list[str], 'Cell', int] | int:
    """
    Perform iterative deepening depth-first search to find the shortest path from the agent's location to all goals.

    Args:
        agent (Agent): The agent object.
        limit (int): The maximum number of cells to visit during the search before stopping. Default is 100,000.

    Returns:
      If a path is found:
        dict: A dictionary to store the result of the search with the following keys:
          'path' (list[str]): A list of directions (up, left, down, right) to reach the goal.
          'goal' (Cell): The goal cell reached.
          'count' (int): The number of cells visited during the search.
      If no path is found:
        int: The number of cells visited during the search.
    """
    agent.grid.reset()
    start = agent.cell
    count = 1
    max_depth = agent.grid.net_area

    path = []
    goals = []

    while agent.goals and count < limit:
        found_goal = False
        for depth in range(max_depth + 1):
            # print("\nDepth:", depth)
            # Initialize a set to store visited cells for each depth
            visited = {start}
            result = dls(agent, start, depth, visited, count, limit)
            count = result['count']
            if result['success']:
                goal = result['goal']
                goals.append(goal)
                agent.goals.remove(goal)
                path.extend(agent.trace_path(goal))
                # print("Goal found:", goal.location, "- Depth:", depth, "- Remaining Goals:", agent.goals)

                # If all goals are reached, return the result
                if not agent.goals:
                    return {
                        'path': path,
                        'goal': goals,
                        'count': count
                    }
                # Reset the search state for the next goal
                start = goal
                start.parent = None
                found_goal = True
                break
        # If there is no path to any goals, stop the search
        if not found_goal:
            break
    # If no path is found, return the count of visited cells
    return count


if __name__ == "__main__":
    import sys
    import os

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
