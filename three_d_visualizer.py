import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os
import sys
import tempfile

def plot_loading_plan(items, container_dims):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Trailer floor
    L, W, H = container_dims
    ax.bar3d(0, 0, 0, L, W, 0.01, color='gray', alpha=0.3)
    
    for itm in items:
        x, y, z = itm['pos']
        dx, dy, dz = itm['dims']
        xx = [x, x, x+dx, x+dx, x, x, x+dx, x+dx]
        yy = [y, y+dy, y+dy, y, y, y+dy, y+dy, y]
        zz = [z, z, z, z, z+dz, z+dz, z+dz, z+dz]
        vertices = [[(xx[i], yy[i], zz[i]) for i in range(8)]]
        
        faces = [
            [vertices[0][0], vertices[0][1], vertices[0][2], vertices[0][3]],
            [vertices[0][4], vertices[0][5], vertices[0][6], vertices[0][7]],
            [vertices[0][0], vertices[0][1], vertices[0][5], vertices[0][4]],
            [vertices[0][2], vertices[0][3], vertices[0][7], vertices[0][6]],
            [vertices[0][1], vertices[0][2], vertices[0][6], vertices[0][5]],
            [vertices[0][4], vertices[0][7], vertices[0][3], vertices[0][0]]
        ]
        ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='b', alpha=0.6))
    
    ax.set_xlim(0, L)
    ax.set_ylim(0, W)
    ax.set_zlim(0, H)
    ax.set_xlabel('Length (m)')
    ax.set_ylabel('Width (m)')
    ax.set_zlabel('Height (m)')
    plt.title("Genset Trailer Loading Plan")
    plt.show()
