ALGORITHM = "bfs"

print(f"Timing {ALGORITHM.upper()} algorithm\n")

import sys, os, timeit, tracemalloc, psutil
from classes import *
from utils import *
from importlib import import_module

# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

# decorator function
def profile(func):
    def wrapper(*args, **kwargs):

        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("{}:consumed memory: {:,}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))

        return result
    return wrapper

# instantiation of decorator function
@profile
def time(number=1000):
    setup = f"""
import sys, os

directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(directory)

from classes import Cell, Grid, Agent
from utils import load_map
from importlib import import_module

algorithm = import_module(name="algorithms.{ALGORITHM}")
    """
    
    setup_3 = f"""
agent.can_jump = True
    """
    # directory = os.path.dirname(os.path.dirname(__file__))
    # sys.path.append(directory)

    # algorithm = import_module(name=f"algorithms.{ALGORITHM}")

    for file in get_available_maps():
        print(file)
        # grid_size, agent_loc, goal_locs, walls = load_map(file)
        # map = Grid(grid_size, walls)
        # agent = Agent(map, agent_loc, goal_locs)
        # print_map(grid_size, agent_loc, goal_locs, walls)
        
        setup_2 = f"""
grid_size, agent_loc, goal_locs, walls = load_map('{file}')
grid_map = Grid(grid_size, walls)
agent = Agent(grid_map, agent_loc, goal_locs)
        """
        
        # result = algorithm.search(agent)
        # print("Search:", result)
        print(f"Search (one goal, cannot jump):")
        tracemalloc.start()
        print(f"\t- Time: {timeit.timeit("algorithm.search(agent)", setup=setup+setup_2, number=number)*1000/number} milliseconds (average of {number} runs)")
        print(f"\t- Memory used: {tracemalloc.get_traced_memory()[1]/number} (average of {number} runs)\n")
        tracemalloc.stop()
        
        # result = algorithm.search(agent, all=True)
        # print("Search All:", result)
        print(f"Search (all goals, cannot jump):")
        tracemalloc.start()
        print(f"\t- Time: {timeit.timeit("algorithm.search(agent, all=True)", setup=setup+setup_2, number=number)*1000/number} milliseconds (average of {number} runs)")
        print(f"\t- Memory used: {tracemalloc.get_traced_memory()[1]/number} (average of {number} runs)\n")
        tracemalloc.stop()
        
        print("Enabled Jumping\n")
        # agent.can_jump = True
        # result = algorithm.search(agent)
        # print("Search:", result)
        print(f"Search (one goal, can jump):")
        tracemalloc.start()
        print(f"\t- Time: {timeit.timeit("algorithm.search(agent)", setup=setup+setup_2+setup_3, number=number)*1000/number} milliseconds (average of {number} runs)")
        print(f"\t- Memory used: {tracemalloc.get_traced_memory()[1]/number} (average of {number} runs)\n")
        tracemalloc.stop()
        
        # result = algorithm.search(agent, all=True)
        # print("Search All:", result)
        print(f"Search (all goals, can jump):")
        tracemalloc.start()
        print(f"\t- Time: {timeit.timeit("algorithm.search(agent, all=True)", setup=setup+setup_2+setup_3, number=number)*1000/number} milliseconds (average of {number} runs)")
        print(f"\t- Memory used: {tracemalloc.get_traced_memory()[1]/number} (average of {number} runs)\n")
        tracemalloc.stop()
        # break
        
time(100)