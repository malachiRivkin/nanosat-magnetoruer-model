### satellite parameters and dynamics here
from earth import *
from spaceMathOLD import *

import numpy as np
import pyIGRF as igrf

global foo
#differential eq, which will later be solved with an integrator
def Satellite(t, state):
    # first three elements =position
    # second three elements = 1st time derivative of position
    
    #date
    year = 2023.25

    #mass properties
    m = 2   #kg - satellite mass
    """
    Ix = 1
    Iy = 1
    Iz = 1
    """

    #kinematics
    position = state[0:3]
    velocity = state[3:6]
    x = state[0]
    y = state[1]
    z = state[2]

    #2 body, point mass gravity model
    r = position
    rho = np.linalg.norm(r)
    rhohat = r/rho
    Fg = -(G*M*m/rho**2) * rhohat
    
    
    #convert cartesian coords into lat/long/alt (move this to a function...)
    phiE = 0
    thetaE = np.arccos(z/rho)
    psiE = np.arctan2(y,x)
    lat = 90 - thetaE*180/np.pi
    long = psiE*180/np.pi
    alt = rho - R
    
    #calculate magnetic field in NED coord sys
    B = igrf.igrf_value(lat, long, alt, year)
    Bned = B[3:6]
    #convert to inertial cartesian coords
    #play with some fire here...
    
    foo = T_IB(phiE, thetaE + np.pi,psiE) * Bned
    print(foo)
    """
    global Bxi, Byi, Bzi
    Bxi = Bi[0]
    Byi = Bi[1]
    Bzi = Bi[2]"""

    #translational dynamics
    #Fexternal = 0   #this would become a vector if thrust, solar pressure, etc are assumed to act on body
    F = Fg #+ Fexternal
    acceleration = F/m

    #state derivatives
    dstatedt = [*velocity, *acceleration]
    return dstatedt
