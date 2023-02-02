""" utility for visuilizing euler angles - perhaps simpler to use quaternions instead, will consider modifying in the future
"""

### Dependencies
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
from matplotlib.animation import FuncAnimation
import mpl_toolkits.mplot3d.axes3d as p3

from spaceMathOLD import *

### Generate some bogus data - will eventually settle on a convenient form for input
#euler angles
t = np.linspace(0,100,100)  # seconds - approximatly 1 period in LEO
alpha = .1 * t
beta =  alpha #t/10
gamma =  beta#t/10

### create csv 
state = np.array([t.T,alpha.T,beta.T,gamma.T])
print(state)
columnNames = ('t', 'phi', 'theta', 'psi')
np.savetxt('state.csv',state.T, delimiter=', ', header=columnNames)



phi = .05
theta=.1
psi=.2
"""
### Construct figure, etc
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
#ax = p3.Axes3D(fig)
##ax.set_aspect('equal')
#lim_sym = (-10,10)
#ax.set_xlim(lim_sym), ax.set_ylim3d(lim_sym), ax.set_zlim3d(lim_sym)
#ax.set_xlabel('X')
#ax.set_ylabel('Y')
#ax.set_zlabel('Z')
#ax.axis('equal')
#ax.set_frame_on(False)
#ax.grid(False)


def plotRotation(phi,theta,psi):
    #dims
    x = 1/2
    y = 2/2
    z = 3/2

    #x = 1/10
    #y = 2/10
    #z = 3/10

    p1 = [-x, -y,-z]
    p2 = [x, -y,-z]
    p3 = [x, y,-z]
    p4 = [-x, y,-z]
    p5 = [-x, -y,z]
    p6 = [x, -y,z]
    p7 = [x, y,z]
    p8 = [-x, y,z]

    points = np.array([p1,p2,p3,p4,p5,p6,p7,p8])

    #rotate points
    #create rotation matrix
    Rot = T_IB(phi, theta, psi)
    newVerts = np.matmul(Rot, points.T)
    newVerts = newVerts.T
    p1 = newVerts[0]
    p2 = newVerts[1]
    p3 = newVerts[2]
    p4 = newVerts[3]
    p5 = newVerts[4]
    p6 = newVerts[5]
    p7 = newVerts[6]
    p8 = newVerts[7]
    verts = [[p1,p2,p3,p4],[p5,p6,p7,p8],[p2,p3,p7,p6],[p1,p4,p8,p5],[p1,p2,p6,p5],[p4,p3,p7,p8]]

    #ax.plot_surface(f1x,f1y,f1z, alpha=0.5)
    #ax.clear()
    ax.add_collection3d(Poly3DCollection(verts, linewidths=1, edgecolors='black', alpha=.50, color='green'))
    #plt.show()
    return


#run plotting
def animate(i):
    ax.clear()
    plotRotation(alpha[i], beta[i], gamma[i])
    lim_sym = (-5,5)
    ax.set_xlim(lim_sym), ax.set_ylim3d(lim_sym), ax.set_zlim3d(lim_sym)
    
    return


ani = FuncAnimation(fig, animate, frames = len(t), interval = 20)
plt.show()

#from matplotlib.animation import PillowWriter
# Save the animation as an animated GIF
#ani.save("simple_animation.gif", dpi=300,writer=PillowWriter(fps=1))




"""

