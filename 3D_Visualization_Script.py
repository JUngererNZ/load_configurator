import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def plot_loading_plan(items, container_dims):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_view(30, -45, 10, 10) # Set perspective
    ax = fig.add_subplot(111, projection='3d')
    
    # Trailer dimensions
    L, W, H = container_dims
    
    for itm in items:
        # Define 8 vertices of the box
        x, y, z = itm['pos']
        dx, dy, dz = itm['dims']
        
        xx = [x, x, x+dx, x+dx, x, x, x+dx, x+dx]
        yy = [y, y+dy, y+dy, y, y, y+dy, y+dy, y]
        zz = [z, z, z, z, z+dz, z+dz, z+dz, z+dz]
        
        vertices = [[(xx[i], yy[i], zz[i]) for i in range(8)]]
        # Faces of the genset
        faces = [[vertices[0][0], vertices[0][1], vertices[0][2], vertices[0][3]],
                 [vertices[0][4], vertices[0][5], vertices[0][6], vertices[0][7]], 
                 [vertices[0][0], vertices[0][1], vertices[0][5], vertices[0][4]],
                 [vertices[0][2], vertices[0][3], vertices[0][7], vertices[0][6]],
                 [vertices[0][1], vertices[0][2], vertices[0][6], vertices[0][5]],
                 [vertices[0][4], vertices[0][7], vertices[0][3], vertices[0][0]]]

        ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='b', alpha=0.6))

    # Set plot limits
    ax.set_xlim(0, L)
    ax.set_ylim(0, W)
    ax.set_zlim(0, H)
    ax.set_xlabel('Length (m)')
    ax.set_ylabel('Width (m)')
    ax.set_zlabel('Height (m)')
    plt.title("Genset Vehicle Configuration")
    plt.show()

# Sample packed data: [{'pos': (x,y,z), 'dims': (l,w,h)}]
packed_gensets = [
    {'pos': (0.5, 0.2, 0), 'dims': (4.0, 2.0, 2.2)},
    {'pos': (5.0, 0.2, 0), 'dims': (3.5, 2.0, 2.0)}
]
plot_loading_plan(packed_gensets, (13.6, 2.4, 2.6))