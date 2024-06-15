"""
Classes to represent the environment, including Cell, Grid and Agent.

Classes:
    - Direction: An enumeration class to represent the directions.
    - Cell: A cell in the grid with x and y coordinates.
    - Grid: A 2D grid containing cells.
    - Agent: An agent in the grid.
"""
from enum import Enum


class Direction(Enum):
    """
    An enumeration class to represent the directions.

    Attributes:
        - UP: The up direction.
        - LEFT: The left direction.
        - DOWN: The down direction.
        - RIGHT: The right direction.
    """
    UP = "up"
    LEFT = "left"
    DOWN = "down"
    RIGHT = "right"


class Cell:
    """
    A class to represent a cell in the grid.

    Attributes:
        - x (int): The x coordinate of the cell.
        - y (int): The y coordinate of the cell.
        - parent (Cell): The parent cell of the current cell.
        - g (int): The distance from the start node.
        - h (int): The distance from the end node.
        - blocked (bool): The blocked status of the cell.

    Methods:
        - __eq__(self, other) -> bool: Compare the cell with another cell based on their locations.
        - __hash__(self): Return the hash value of the cell.
        - __sub__(self, other) -> str: Get the direction from the current cell to another.
        - __repr__(self): Return the string representation
        - manhattan_distance(self, other) -> int: Calculate the Manhattan distance between current cell and another cell.

    Properties:
        - location -> tuple[int, int]: Return the location of the cell as a tuple (x, y).
        - f -> int: Calculate the total cost of the cell - sum of g and h.
    """
    def __init__(self, x: int, y: int, parent: 'Cell' = None):
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.parent = parent    # Parent cell
        self.g = 0  # Distance from start node
        self.h = 0  # Distance from end node
        # self.f = 0  # Total cost
        self.blocked = False  # Blocked status

    def __eq__(self, other: 'Cell'):
        """
        Compare the cell with another cell based on their locations.
        """
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """
        Return the hash value of the cell.
        """
        return hash((self.x, self.y))

    def __sub__(self, other: 'Cell') -> Direction:
        """
        Subtract the x and y coordinates of the current cell from the x and y coordinates of another cell.

        Returns:
          Direction: The direction from the current cell to the other cell.
        """
        dx, dy = other.x - self.x, other.y - self.y
        if dx == 0:
            return Direction.UP if dy < 0 else Direction.DOWN
        return Direction.LEFT if dx < 0 else Direction.RIGHT

    def __repr__(self) -> str:
        """
        Return the string representation of the cell.
        """
        return f"<Cell ({self.x}, {self.y})>"

    def __lt__(self, other: 'Cell') -> bool:
        """
        Compare the cell with another cell based on their total cost.
        """
        return self.f < other.f

    def __gt__(self, other: 'Cell') -> bool:
        """
        Compare the cell with another cell based on their total cost.
        """
        return self.f > other.f

    def manhattan_distance(self, other:'Cell') -> int:
        """
        Calculate the Manhattan distance between the current cell and another cell.
        
        Args:
            other (Cell): The other cell.
        
        Returns:
            int: The Manhattan distance between the two cells.
        """
        return abs(self.x - other.x) + abs(self.y - other.y)

    def reset(self):
        """
        Reset the cell properties.
        """
        self.g = self.h = 0
        self.parent = None

    @property
    def location(self):
        """
        Return the location of the cell as a tuple (x, y).
        """
        return self.x, self.y

    @property
    def f(self):
        """
        Calculate the total cost of the cell - sum of g and h.
        """
        return self.g + self.h


class Grid:
    """"
    A class to represent a grid.

    Attributes:
        - height (int): The height of the grid.
        - width (int): The width of the grid.
        - grid (list[list[Cell]]): A 2D list of cells representing the grid.

    Methods:
        - get_cell(self, location: tuple[int, int]) -> Cell: Get the cell at the given coordinates.
        - is_valid(self, x:int, y:int) -> bool: Check if the cell at the given coordinates is valid.
        - get_neighbors(self, cell: Cell) -> list[Cell]: Get the neighbors of the cell at the given coordinates.

    Properties:
        - size -> tuple[int, int]: Return the size of the grid as a tuple (height, width).
        - net_area -> int: Calculate the net area of the grid (total area - blocked area).
    """
    def __init__(self, size: tuple[int, int], walls: list[tuple[int, int, int, int]]):
        self.height, self.width = size
        # Create a 2D list of cells
        self.grid = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        # Set the blocked status of the cells based on the walls
        for wall in walls:
            start_x, start_y, width, height = wall
            for row in range(start_y, start_y + height):
                for col in range(start_x, start_x + width):
                    self.grid[row][col].blocked = True

    def get_cell(self, location:tuple[int, int]) -> Cell:
        """
        Get the cell at the given coordinates.
        
        Args:
            location (tuple[int, int]): The coordinates of the cell.
            
        Returns:
            Cell: The cell at the given coordinates.
        """
        x, y = location
        return self.grid[y][x]

    def is_valid(self, x:int, y:int) -> bool:
        """
        Check if the cell at the given coordinates is valid.
        
        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.
        
        Returns:
            bool: True if the cell is valid, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_neighbor(self, cell:Cell, direction:Direction, distance:int=1) -> Cell | None:
        """
        Get the neighbor of the cell at the given direction and distance.

        Args:
            cell (Cell): the cell to get the neighbor from.
            direction (Direction): the direction of the neighbor.
            distance (int, optional): the distance from the original cell. Defaults to 1.

        Returns:
            Cell: the neighbor cell if it is valid, None otherwise.
        """
        x = y = -1
        if direction == Direction.UP:
            x, y = cell.x, cell.y - distance
        elif direction == Direction.LEFT:
            x, y = cell.x - distance, cell.y
        elif direction == Direction.DOWN:
            x, y = cell.x, cell.y + distance
        else: # direction == Direction.RIGHT
            x, y = cell.x + distance, cell.y
        if self.is_valid(x, y):
            return self.grid[y][x]
        return None

    def get_neighbors(self, cell:Cell, can_jump=False) -> list[Cell]:
        """
        Get all neighbors of the given cell.
        
        Args:
            cell (Cell): The cell to get the neighbors from.
            can_jump (bool, optional): Whether to allow movement with distance greater than 1. Defaults to False.
        
        Returns:
            list[Cell]: A list of neighbor cells. Empty list if no neighbors are found.
        """
            
        neighbors = []
        # Add neighbors IN ORDER (up, left, down, right) around the cell
        for direction in list(Direction):
            distance = 1
            neighbor = self.get_neighbor(cell, direction, distance)
            while neighbor is not None:
                neighbors.append(neighbor)
                if not can_jump:
                    break
                distance += 1
                neighbor = self.get_neighbor(cell, direction, distance)
        # neighbors = [self.get_neighbor(cell, direction) for direction in list(Direction)]
        
        # for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        #     if self.is_valid(cell.x + dx, cell.y + dy):
        #         neighbors.append(self.grid[cell.y + dy][cell.x + dx])

        # for x in range(-1, 2):  # Loop through the 3x3 grid around the cell
        #   for y in range(-1, 2):
        #     if x == 0 and y == 0:
        #       continue
        #     if self.is_valid(cell.x + x, cell.y + y):
        #       neighbors.append(self.grid[cell.y + y][cell.x + x])

        return neighbors

    def reset(self):
        """
        Reset all cells in the grid.
        """
        for row in self.grid:
            for cell in row:
                cell.reset()

    @property
    def size(self):
        """
        Return the size of the grid as a tuple (height, width).
        """
        return self.height, self.width

    @property
    def net_area(self):
        """
        Calculate the net area of the grid (total area - blocked area).
        """
        return self.height * self.width - sum(cell.blocked for row in self.grid for cell in row)


class Agent:
    """
    A class to represent an agent in the grid.

    Attributes:
        - grid (Grid): The grid object.
        - cell (Cell): The cell object representing the agent's location.
        - goals (list[Cell]): A list of cell objects representing the goal locations.
        - can_jump (bool): Whether the agent can jump over obstacles.

    Methods:
        - trace_path(self, cell:Cell, backward=True) -> list[str]: Given the goal cell, return the path from the start cell to the goal cell as a list of directions (up, down, left, right).
        - get_nearest_goal(self) -> tuple[int, int]: Get the nearest goal to the agent's current location (Manhattan distance).
    """
    def __init__(self, grid:Grid, location:tuple[int, int], goals:list[tuple[int, int]], can_jump=False):
        self.grid = grid
        self.cell = grid.get_cell(location)
        self.goals = []
        for goal in goals:
            cell = self.grid.get_cell(goal)
            self.goals.append(cell)
        self.can_jump = can_jump

    def trace_path(self, cell:Cell, backward=True) -> list[str]:
        """
        Given the goal cell, return the path from the start cell to the goal cell as a list of directions (up, down, left, right).

        Args:
            - cell (Cell): The goal cell.
            - backward (bool, optional): The direction of the path. True for backward, False for forward. Defaults to True.

        Returns:
            - list[str]: A list of directions (up, down, left, right) to reach the goal cell.
        """
        path = []
        while cell.parent:
            # print(f"Cell: {cell.location} - Parent: {cell.parent.location}")
            distance = cell.manhattan_distance(cell.parent)
            distance_str = f"_{distance}" if self.can_jump else ""
            if backward:
                path.insert(0, (cell.parent - cell).value + distance_str)
            else: # Forward
                path.append((cell - cell.parent).value + distance_str)
            cell = cell.parent
        return path

    def get_nearest_goal(self) -> Cell:
        """
        Get the nearest goal to the agent's current location (Manhattan distance).
        """
        return min(self.goals, key=self.cell.manhattan_distance)


if __name__ == "__main__":
    from utils import load_map, print_map
    
    grid_size, agent_loc, goal_locs, wall_blocks = load_map()
    map_grid = Grid(grid_size, wall_blocks)
    agent = Agent(map_grid, agent_loc, goal_locs, True)
    print_map(grid_size, agent_loc, goal_locs, wall_blocks)
    print(list(Direction), Direction.UP, Direction.UP.value)
    print(agent.grid.get_neighbors(agent.cell, True))
    
    locations = [(0, 1), (1, 1), (1, 3), (5, 3)]
    for idx, location in enumerate(locations):
        cell = map_grid.get_cell(location)
        if idx > 0:
            cell.parent = map_grid.get_cell(locations[idx - 1])
    print(agent.trace_path(map_grid.get_cell(locations[-1])))
    # path = agent.bfs()
    # print(path)
