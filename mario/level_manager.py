from levels.map_level1 import level_1
from levels.map_level2 import level_2

levels = [level_1, level_2]

def get_level_data(level_index):
    if level_index < len(levels):
        return levels[level_index]
    else:
        return None
