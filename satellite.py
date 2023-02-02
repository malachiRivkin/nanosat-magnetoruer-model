### satellite parameters and dynamics here
from earth import *
from spaceMath import *
from configuration import *

import numpy as np
import pyIGRF as igrf


#differential eq, which will later be solved with an integrator
def Satellite(t, state):
    # first three elements =position
    # second three elements = 1st time derivative of position
    
    #date
    #year = 2023.25

    #mass properties
    m = 6.5   #kg - satellite mass
    I = [[0.119,0,0], [0,0.143,0], [0,0,0.111]]
    Iinv = np.linalg.inv(I)
    dipoleMoment = np.array([0,0,.5]).T  #dipole moment of passive magnets

    #kinematics
    #translational
    position = state[0:3]
    velocity = state[3:6]
    x = state[0]
    y = state[1]
    z = state[2]
    #rotational
    #q0123 = state[6]
    q0 = state[6]
    q1 = state[7]
    q2 = state[8]
    q3 = state[9]
    #print(q0123)
    p = state[10]
    q = state[11]
    r = state[12]
    pqr = state[10:13]
    q0123 = state[6:10]
    PQRMAT = [[0, -p, -q, -r],[p, 0, r, -q],[q, -r, 0, p],[r, q, -p, 0]]
    q0123dot = 0.5*np.matmul(PQRMAT,q0123)
    

    #2 body, point mass gravity model
    r = position
    rho = np.linalg.norm(r)
    rhohat = r/rho
    Fg = -(G*M*m/rho**2) * rhohat
    
    
    #get magnetic field in inertial coordinates
    B = getBinertial(x,y,z)

    #get magnetic field in spacecraft body coordinates
    Bbody = np.matmul(T_IBQuaternions(q0123).T, B)   #transpose of rot matrix is same as inverse...
    Bbody = Bbody * 1e-9    #convert to Tesla
    
    #translational dynamics
    #Fexternal = 0   #this would become a vector if thrust, solar pressure, etc are assumed to act on body
    F = Fg #+ Fexternal
    acceleration = F/m

    #rotational dynamics
    T_mag = np.cross(dipoleMoment,Bbody)
    H = np.matmul(I,pqr)
    pqrdot = np.matmul(Iinv,(T_mag - np.cross(pqr,H)))
    #print("pqr experiment: ", pqrdot)
    #pqrdot = np.array([0,0,0])

    #state derivatives
    dstatedt = [*velocity, *acceleration, *q0123dot, *pqrdot]
    return dstatedt
