uninformed = ["bfs", "dfs", "iddfs"]
informed = ["astar", "greedy", "bidirectional"]

__all__ = uninformed + informed

from . import bfs
from . import dfs
from . import astar
from . import greedy
from . import iddfs
from . import bidirectional