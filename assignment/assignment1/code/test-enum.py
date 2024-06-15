# import enum and auto 
from enum import Enum, auto 
  
# Using enum.auto() method 
class language(Enum): 
    Java = auto() 
    Python = auto() 
    HTML = auto() 

HEIGHT, WIDTH = 5, 11

def get_neighbors(location):
    def check_condition(direction, distance):
        if direction == "up":
            return 0 <= y - distance
        if direction == "left":
            return 0 <= x - distance
        if direction == "down":
            return y + distance < HEIGHT
        if direction == "right":
            return x + distance < WIDTH
    x, y = location
    neighbors = []
    for direction in ["up", "left", "down", "right"]:
        distance = 1
        while check_condition(direction, distance):
            neighbors.append((x, y))
            distance += 1
    return neighbors


location = (0, 1)
neighbors = get_neighbors(location)
print(neighbors)

print([language.Java, language.Python, language.HTML])
# print(list(language))
# print("Hmm\n\
# Hey there\
# Hello")
