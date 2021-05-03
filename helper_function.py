import math
import numpy as np
import random


# get a random point within a circile
def get_random_point(circle_x,circle_y,circle_r):
    # random angle
    alpha = 2 * math.pi * random.random()
    # random radius
    r = circle_r * math.sqrt(random.random())
    # calculating coordinates
    x = r * math.cos(alpha) + circle_x
    y = r * math.sin(alpha) + circle_y
    return x,y

# generate list of random points
def generate_position(num_points,circle_x,circle_y,circle_r):
    points_x=[]
    points_y=[]
    for i in range(num_points):
        x,y=get_random_point(circle_x,circle_y,circle_r)
        points_x.append(x)
        points_y.append(y)
    return np.c_[points_x,points_y]

# return the 9 nozzles position, use margin to control the distance between nozzles and edge of the circle
def get_nozzles_position(circle_x,circle_y, radius,margin=0.2):
    # random angle
    cluster_density=2 * math.pi/36
    cluster_alpha=[]
    for num in range(3):
        cluster_alpha.append(2 * math.pi*num/3-cluster_density)
        cluster_alpha.append(2 * math.pi*num/3)
        cluster_alpha.append(2 * math.pi*num/3+cluster_density)
    positions=[]
    for alpha in cluster_alpha:
        # random radius
        r = radius + margin
        # calculating coordinates
        x = r * math.sin(alpha) + circle_x
        y = r * math.cos(alpha) + circle_y
        rotation= math.degrees(alpha)
        positions.append((x,y,-rotation))
    return positions

# Get the nozzles_status
def get_nozzles_status(active_nozzles):
    active_num=int(9*active_nozzles/100)
    active_order=[0,3,6,1,4,7,2,5,8]
    active_nozzles_array=[False for i in range(9)]
    for i in range(active_num):
        active_nozzles_array[active_order[i]]=True
    return active_nozzles_array

def update_nozzles_status(nozzles,status):
    for index, status in enumerate(status):
        if status:
            nozzles[index].set_text("+")
        else:
            nozzles[index].set_text("-")
