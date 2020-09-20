import sys
import math
from Map import Map_Obj

task5 = False

#-----------------------------------------------------------------------------------
#                           INITIALIZATION OF THE MAP
#-----------------------------------------------------------------------------------

# If you run windows, uncomment the line which represents the task you want to run
# For Task 5, uncomment both lines under the '# Task 5' comment

# Task 1
map = Map_Obj(1)

# Task 2
#map = Map_Obj(2)

# Task 3
#map = Map_Obj(3)

# Task 4
#map = Map_Obj(4)

# Task 5
#map = Map_Obj(5)
#task5 = True

#-----------------------------------------------------------------------------------
#                   IMPLEMENTATION OF A* AND OTHER FUNCTIONS
#-----------------------------------------------------------------------------------

# Function that returns the heuristic value of the position
def h(pos, goal = map.get_goal_pos()):
    # Returns the euclidian distance from some position to the goal
    return math.sqrt((pos[0]-goal[0])**2 + (pos[1]-goal[1])**2)

# The function implementing A* algorithm
def a_star():
    # Creating frontier, which will house the nodes available to explore
    frontier = []
    # Creating closed, which will house the nodes allready explored
    closed = []

    start_pos = map.get_start_pos()
    # Creating node with this schema:
    # [f value, position, parent position]
    # f value = g() + h()
    current_node = [0 + h(start_pos), start_pos, start_pos]

    # Adding the starting node to the frontier
    frontier.append(current_node)
    
    # Looping intil the current node is the goal node
    while current_node[1] != map.get_goal_pos():
        # If the task is Task 5, then this function ensures that 
        # the goal is moves properly
        if task5: map.tick()

        # Finding the positions of adjacent nodes
        adjacent_pos = [
            [current_node[1][0]-1, current_node[1][1]], # North
            [current_node[1][0]+1, current_node[1][1]], # South
            [current_node[1][0], current_node[1][1]+1], # East
            [current_node[1][0], current_node[1][1]-1]  # West
        ]
        
        # For each adjacent position
        for position in adjacent_pos:
            # If the position is not a wall, and is not in closed
            if map.get_cell_value(position) != -1 and position not in closed:
                # Then create a node with the f value calculated from this point
                # Set the node's parent to be the current node
                frontier.append([current_node[0] + map.get_cell_value(position) + h(position), position, current_node])

        # Append current node to closed
        closed.append(current_node[1])

        # Find the node that has the smallest f value and is not in closed
        shortest_distance = [float("inf"), [-1, -1], [-1, -1]]
        for shortest_f in frontier:
            if shortest_f[0] < shortest_distance[0] and shortest_f[1] not in closed:
                shortest_distance = shortest_f
        
        # Set the current node to the node with the smallest f value from frontier
        current_node = shortest_distance

    # The function returns the goal node with reference to its parent node
    # This allows to backtrack from goal node to start node
    return current_node

# Recursive function that changes the values in the map to indicate the path
def draw_path(node):
    # If the node position is the goal
    if node[1] == map.get_goal_pos():
        # Skip to parent node
        draw_path(node[2])
    # If the node position is the start
    elif node[1] == map.get_start_pos():
        # Done!
        return
    else:
        # Replaces the value of the node position with 9
        # 9 was chosen because it's undefined in the draw function
        # which means it will be filled in with yellow
        map.replace_map_values(node[1], 9, map.get_goal_pos())
        # Move on to the parent
        draw_path(node[2]) 

#-----------------------------------------------------------------------------------
#                               CODE THAT USES A*
#-----------------------------------------------------------------------------------

# a_star() function returns the goal node with references to its parent node.
# It gets passed immediately to the draw_path function which recursively indicates
# which tiles are the path taken from start to goal.
draw_path(a_star())

# The map is then shown
map.show_map()
