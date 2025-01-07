import heapq
from pygame.math import Vector2
from config import *

# Simple implementation of Dijkstras algorithm. Finds shortest path from start to goal in grid.
def dijkstra(start, goal, snake):
    goal = tuple(goal)
    # Init the fringe set with start node
    fringe_set = [(0, tuple(start))]
    heapq.heapify(fringe_set)
    came_from = {}
    
    # Init costs
    cost = {(float(x), float(y)): float('inf') for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
    cost[tuple(start)] = 0
    
    while fringe_set:
        _, current_node = heapq.heappop(fringe_set)
        
        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            
            path.reverse()
            return path

        for move in [UP, DOWN, LEFT, RIGHT]:
            neighbour = (current_node[0] + move[0], current_node[1] + move[1])
            
            if (
                0 <= neighbour[0] < GRID_WIDTH
                and 0 <= neighbour[1] < GRID_HEIGHT
                and (Vector2(neighbour) not in snake) # Avoid snake body
            ):
                tentative_cost = cost[current_node] + 1
                
                if tentative_cost < cost[neighbour]:
                    came_from[neighbour] = current_node
                    cost[neighbour] = tentative_cost
                    heapq.heappush(fringe_set, (cost[neighbour], neighbour))
        
    return [] # No path

# For use when there is no valid path to food. Finds best fitting neighbour cell, based on
# longest valid empty path from snake
def find_best_empty_cell(snake, snake_dir):
    head = snake[0]
    
    longest_path = -1
    best_move = (head[0] + snake_dir[0], head[1] + snake_dir[1]) # Best CURRENTLY KNOWN move
    
    for move in [UP, RIGHT, DOWN, LEFT]:
        neighbour = (head[0] + move[0], head[1] + move[1])
        
        # Check if neighbour is valid
        if (
            0 <= neighbour[0] < GRID_WIDTH
            and 0 <= neighbour[1] < GRID_WIDTH
            and Vector2(neighbour) not in snake
        ):
            path_length = calculate_potential_path_length(snake, neighbour)
            if path_length > longest_path:
                longest_path = path_length
                best_move = neighbour
    
    # Returns best fitting neighbour cell
    return best_move           

# A modified version of the Dijkstra function which returns the length of the
# longest empty path from the snake
def calculate_potential_path_length(snake, start):
    # Init fringe set with start node
    fringe_set = [(0, tuple(start))]
    heapq.heapify(fringe_set)
    
    # Init costs
    cost = {(x, y): float('inf') for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}
    cost[tuple(start)] = 0
    
    potential_path_length = 0
    
    while fringe_set:
        _, current = heapq.heappop(fringe_set)
        
        for move in (UP, RIGHT, DOWN, LEFT):
            neighbour = (current[0] + move[0], current[1] + move[1])
            
            # Check if neighbour is valid
            if (
                0 <= neighbour[0] < GRID_WIDTH
                and 0 <= neighbour[1] < GRID_WIDTH
                and (Vector2(neighbour) not in snake)
            ):
                tentative_cost = cost[current] + 1
                
                if tentative_cost < cost[neighbour]:
                    cost[neighbour] = tentative_cost
                    heapq.heappush(fringe_set, (cost[neighbour], neighbour))
                
        if cost[current] > potential_path_length:
            potential_path_length = cost[current]
    
    return potential_path_length