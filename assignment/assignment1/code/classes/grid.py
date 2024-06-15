from .cell import *


class Grid:
    """
    A 2D grid containing cells.

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