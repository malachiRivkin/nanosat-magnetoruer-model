#orbit propagator, dynamics, plotting, etc happens here

#dependencies
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt

from satellite import *
from earth import *

#params
n_orbits = 3

#initial conditions
t0 = 0  #ignore for now, will eventually need to incorporate julian time
altitude = 550e3    #m AGL
inclination = 0    #degrees
""" start with circular orbit for now, will consider eccentric orbits in future...
RAAN = 0    #ignore for now
i = 0   #ignore for now
"""
a = altitude
vcircular = np.sqrt(MU/a)
inclination = np.deg2rad(inclination)

#initial state (summary of above)
x0 = R + a  #we'll start at apoapsis, at 0 lat/0 long
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
#test Satellite function
#testOutput = Satellite(0, state0)
#print(testOutput)


propagation = sci.integrate.solve_ivp(Satellite, tspan, state0)#, maxstep=60)
tout = propagation.t
sol_out = propagation.y
print("Simulation Complete")


############Plot Results################3
#(might want to consider moving all of this to a separate function/script/class//etc)
#extract states
xout = sol_out[0]/1000
yout = sol_out[1]/1000
zout = sol_out[2]/1000

#housekeeping
#fig, axes = plt.subplots(1,3)

#plot orbit in 3d
#plt.scatter(xout, yout, zout)
plt.plot(xout,yout)
plt.show()