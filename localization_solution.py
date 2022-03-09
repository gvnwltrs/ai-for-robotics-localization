import numpy as np

def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    
    # >>> Insert your code here <<<
    for i in range(len(measurements)):
        p = move(p, motions[i], p_move, colors)
        p = sense(p, measurements[i], sensor_right, colors)
    return p

def sense(p, Z, pHit, colors):
    pMiss = 1. - pHit
    q = [[0 for row in range(len(colors[0]))] for col in range(len(colors))]
    for x in range(len(p[0])):
        for y in range(len(p)):
            hit = (Z == colors[y][x]) 
            q[y][x] = (p[y][x] * (hit * pHit + (1-hit) * pMiss))
    print('before normalization: ', q)
    s = sum(map(sum,q))
    for x in range(len(q[0])):
        for y in range(len(q)):
            q[y][x] = q[y][x] / s
    return q

def move(p, U, p_move, colors):
    p_stay = 1. - p_move
    q = [[0 for row in range(len(colors[0]))] for col in range(len(colors))]
    for x in range(len(q[0])):
        for y in range(len(q)):
            s = p_move * p[(y-U[0]) % len(p)][(x-U[1]) % len(p[0])]
            s += p_stay * p[y][x]
            q[y][x] = s
    return q

colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 1.0
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
print(np.matrix(p))