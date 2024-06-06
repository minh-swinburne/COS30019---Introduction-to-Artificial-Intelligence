uninformed = ["bfs", "dfs", "iddfs"]
informed = ["astar", "greedy", "beam", "bidirectional"]

__all__ = uninformed + informed

from . import bfs
from . import dfs
from . import iddfs
from . import astar
from . import greedy
from . import beam
from . import bidirectional