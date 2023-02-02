#orbit propagator, dynamics, plotting, etc happens here

#dependencies
import numpy as np
import scipy as sci
import matplotlib.pyplot as plt

from satellite import *
from earth import *
from configuration import *
from spaceMath import *


import time
start = time.time()
#params
n_orbits = 1

#initial conditions
#t0 = 0  #ignore for now, will eventually need to incorporate julian time
altitude = 550e3    #m AGL
inclination = 88   #degrees
""" start with circular orbit for now, will consider eccentric orbits in future...
RAAN = 0    #ignore for now
i = 0   #ignore for now
"""
a = altitude + R
vcircular = np.sqrt(MU/a)
inclination = np.deg2rad(inclination)

#initial state (summary of above)
#translational
x0 = a  #we'll start at apoapsis, at 0 lat/0 long
y0 = 0
z0 = 0
xdot0 = 0
ydot0 = vcircular * np.cos(inclination)
zdot0 = vcircular * np.sin(inclination)
#attitude
phi0 = 0
theta0 = 0
psi0 = 0
ptp0 = [phi0,theta0,psi0]
q0123_0 = EulerAngles2Quaternions(ptp0)
p0 = 0
q0 = 0
r0 = 0

state0 = [x0, y0, z0, xdot0, ydot0, zdot0, q0123_0[0], q0123_0[1], q0123_0[2], q0123_0[3],p0,q0,r0]

#timesteps to integrate over
period = 2*np.pi/np.sqrt(MU)*a**(3/2)
tspan = [0,period*n_orbits] #period over which to integrate ode


#integrate numerically
propagation = sci.integrate.solve_ivp(Satellite, tspan, state0, method='RK45', max_step=30)

tout = propagation.t.T
sol_out = propagation.y.T

#print("tout: ", tout)
#print("yout: ", sol_out)
#print(tout.shape)
#print(sol_out.shape)

#extract results
xout = sol_out[:,0]
yout = sol_out[:,1]
zout = sol_out[:,2]
q0123out = sol_out[:,6:10]
ptpout = Quaternions2EulerAngles(q0123out)
pqrout = sol_out[:,10:13]

#loop through output to extract B field components
Bout = np.array([])
#ByIout = BxIout;
#BzIout = BxIout;

for i,t in enumerate(tout):
    #print("i: ", i)
    B = getBinertial(xout[i], yout[i], zout[i])
    #print("\n)")
    #Bout = np.concatenate((Bout, B), axis=1)
    #Bout = np.vstack((Bout, B)) #works!!! see above instantiation of empty array
    Bout = np.append(Bout, B)

Bout = np.reshape(Bout, (-1,3))

    

print("Simulation Complete")
print("T out max: ", max(tout))

###Save state vectors
header = " "    #possibly store epoch, other data here for futer visualizations
fileName = "simOut.csv"

#print("contents: ", [tout.T.shape, sol_out.shape])
#contents = np.concatenate((tout.T,sol_out), axis=1)
#print(contents.shape)
#np.savetxt(fileName, propagation, delimiter=',')




############Plot Results################3
#(might want to consider moving all of this to a separate function/script/class//etc)
#extract states (convert to km)
xout = sol_out[:,0]/1000
yout = sol_out[:,1]/1000
zout = sol_out[:,2]/1000
#print(xout)
#plt.plot(tout, np.array([xout,yout,zout]).T)

####housekeeping
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
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

#plot arrows
qx = [0,10000,0]
qy = [0,0,0]
qz = [10000,0,-10000]
qu = [0,0,0]
qv = qu
qw = qu
ax.quiver(qu,qv,qw,qx,qy,qz, color='black')

#plot magnetic field
fig2, axes = plt.subplots()
axes.plot(tout, Bout, label=["Bx", "By", "Bz"])
axes.set_xlabel("Time (s)")
axes.set_ylabel("Magnetic Flux Density (nT)")
fig2.legend()

#plot attitude 
fig3, axes = plt.subplots()
axes.plot(tout, np.rad2deg(ptpout.T), label=["phi", "theta", "psi"])
axes.set_xlabel("Time (s)")
axes.set_ylabel("Euler Angles (deg)")
fig3.legend()

#plot attitude rates
fig4, axes = plt.subplots()
axes.plot(tout, pqrout, label=["phi_dot", "theta_dot", "psi_dot"])
axes.set_xlabel("Time (s)")
axes.set_ylabel("Angular Rates (rad/s)")
fig4.legend()
#
# record end time
end = time.time()
 
# print the difference between start
# and end time in milli. secs
print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")


plt.show()





