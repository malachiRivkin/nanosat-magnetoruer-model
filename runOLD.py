#orbit propagator, dynamics, plotting, etc happens here

#dependencies
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt

from satelliteOLD import *
from earth import *

#params
n_orbits = 1

#initial conditions
#t0 = 0  #ignore for now, will eventually need to incorporate julian time
altitude = 550e3    #m AGL
inclination = 98    #degrees
""" start with circular orbit for now, will consider eccentric orbits in future...
RAAN = 0    #ignore for now
i = 0   #ignore for now
"""
a = altitude + R
vcircular = np.sqrt(MU/a)
inclination = np.deg2rad(inclination)

#initial state (summary of above)
x0 = a  #we'll start at apoapsis, at 0 lat/0 long
y0 = 0
z0 = 0
xdot0 = 0
ydot0 = vcircular * np.cos(inclination)
zdot0 = -vcircular * np.sin(inclination)

state0 = [x0, y0, z0, xdot0, ydot0, zdot0]

#timesteps to integrate over
period = 2*np.pi/np.sqrt(MU)*a**(3/2)
tspan = [0,period*n_orbits] #period over which to integrate ode


#integrate numerically
propagation = sci.integrate.solve_ivp(Satellite, tspan, state0, method='RK45', max_step=100)
tout = propagation.t
sol_out = propagation.y
#print(foo)

#loop through output to extract B field components
BIout = []#np.zeros(length(tout)); #create an empty array
#ByIout = BxIout;
#BzIout = BxIout;
for i,t in enumerate(tout):
    out = Satellite(t,sol_out[:,i])
    #BIout = BIout.append(foo)
    #print(foo)
    

print("Simulation Complete")
print("T out max: ", max(tout))



"""
############Plot Results################3
#(might want to consider moving all of this to a separate function/script/class//etc)
#extract states
xout = sol_out[0,:]/1000
yout = sol_out[1,:]/1000
zout = sol_out[2,:]/1000

#housekeeping
#fig, axes = plt.subplots(1,3)

#plot orbit in 3d
#plt earth
u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
x = R*np.cos(u) * np.sin(v)
y = R*np.sin(u) * np.sin(v)
z = R*np.cos(v)

#plot orbit
ax = plt.axes(projection='3d')
ax.plot_surface(x/1000, y/1000, z/1000, cmap=plt.cm.YlGnBu_r, alpha=.5)
ax.scatter3D(xout, yout, zout)

#plot arrows
qx = [0,10000,0]
qy = [0,0,0]
qz = [10000,0,-10000]
qu = [0,0,0]
qv = qu
qw = qu
ax.quiver(qu,qv,qw,qx,qy,qz, color='black')

plt.show()
"""