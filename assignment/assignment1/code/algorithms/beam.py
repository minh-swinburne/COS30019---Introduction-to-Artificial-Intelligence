"""
Beam search algorithm (informed)

Modified from the A* search algorithm to use a beam width to limit the number of cells to explore.
"""


def search(agent: 'Agent', beam_width: int = 2) -> dict[list[str], 'Cell', int] | int:
    """
    Perform beam search to find the shortest path from the agent's location to the goal.

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
    open_list = [start]
    closed_set = set()

    # Initialize the counter of the result dictionary
    count = 1  # Start with 1 for the start cell

    while open_list:
        # print("Open List:", open_list)
        current = min(open_list, key=lambda cell: cell.f)
        open_list.remove(current)
        closed_set.add(current)

        if current in agent.goals:
            return {
                'path': agent.trace_path(current),
                'goal': current,
                'count': count
            }

        for neighbor in agent.grid.get_neighbors(current):
            if neighbor.blocked or neighbor in closed_set:
                continue
            if neighbor not in open_list:
                # Increment the counter for each visited cell
                count += 1
                open_list.append(neighbor)
                neighbor.h = neighbor.manhattan_distance(goal)
                neighbor.parent = current
            elif current.g + 1 < neighbor.g:
                neighbor.g = current.g + 1
                neighbor.parent = current
        # Sort the open list by f value and keep only the top beam_width cells
        open_list = sorted(open_list, key=lambda cell: cell.f)[:beam_width]
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
        print("Result:", result, "\n")
