#!/usr/bin/env python

import numpy as np

"""
[Purpose]


[World]
World in this case is a crude form of what the robot sees compared to how Google's self driving car views the world. IRL, Google's self driving car extracts features (2D surface models) from its environment instead of using 'red' and 'green'. 
"""

# 3 x 3 world (commment/uncomment)
# world = [['green', 'green', 'green'],
#          ['green', 'red', 'red'],
#          ['green', 'green', 'green']]

# measurements = ['red', 'red']
# motions = [[0, 0], [0, 1]]

# 4 x 5 world (comment/uncomment)
world = [['red', 'green', 'green', 'red', 'red'],
         ['red', 'red', 'green', 'red', 'red'],
         ['red', 'red', 'green', 'green', 'red'],
         ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green', 'green', 'green']
motions = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1]]

p_hit = 0.7
p_miss = 1.0 - p_hit 

p_move = 0.8
p_stay = 1.0 - p_move

def create_empty_2d_grid(rows, cols):
    grid = [[0 for col in range(cols)] for row in range(rows)]
    return grid

def initialize_belief(world_size):
    aux = create_empty_2d_grid(rows=len(world_size), cols=len(world_size[0]))
    grid_space = len(world_size) * len(world_size[0])
    print('grid space = ', grid_space)
    
    for i in range(len(world_size)): #rows
        for j in range(len(world_size[0])): #cols
            aux[i][j] = 1.0 / grid_space
    print('initialize_belief: ') 
    print(np.matrix(aux))
    print('rows: ', len(aux))
    print('columns: ', len(aux[0]))

    return aux
p = initialize_belief(world)

def measurement_update(p, z, world):
    print('measurement update - posterior:')
    print(np.matrix(p))
    aux = create_empty_2d_grid(len(world), len(world[0]))

    for i in range(len(p)): #rows
        for j in range(len(p[0])): #cols
            if z == world[i][j]:
                print('hit!')
                aux[i][j] = p[i][j]*p_hit
            else:
                print('miss')
                aux[i][j] = p[i][j]*p_miss
    print('before normalization:')
    print(np.matrix(aux))
    aux = normalizer(aux)

    print('measurement update result: ')
    print(np.matrix(aux))
    return aux

def motion_update(p, U):
    print('motion update - posterior: ')
    print(np.matrix(p))
    aux = create_empty_2d_grid(rows=len(p),cols=len(p[0]))

    for i in range(len(p)): #rows
        for j in range(len(p[0])): #cols
            aux[i][j] = p[(i-U[0])%len(p)][(j-U[1])%len(p)]*p_move
            aux[i][j] = aux[i][j] + (p[i][j]*p_stay)
    print('motion update result: ')
    print(np.matrix(aux))
    return aux

def normalizer(p):
    Sum = 0

    for i in range(len(p)): #rows
        for j in range(len(p[0])): #cols
            Sum = Sum + p[i][j]
    print('sum is ', Sum)
    
    for i in range(len(p)): #rows
        for j in range(len(p[0])): #cols
            p[i][j] = p[i][j] / Sum
    
    return p

def localize(p, z, u, m):
    for i in range(len(z)):
        p = motion_update(p, u[i])
        p = measurement_update(p, z[i], world)

    return p

#############
# Run
#############
p = localize(p, measurements, motions, world)
