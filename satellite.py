### satellite parameters and dynamics here
from earth import *
import numpy as np


#differential eq, which will later be solved with an integrator
def Satellite(t, state):
    # first three elements =position
    # second three elements = 1st time derivative of position

    #mass properties
    m = 6   #kg - satellite mass
    """
    Ix = 1
    Iy = 1
    Iz = 1
    """

    #kinematics
    position = state[0:3]
    velocity = state[3:6]

    #2 body, point mass gravity model
    r = position
    rnorm = np.linalg.norm(r)
    rhat = r/rnorm
    Fg = -(G*M*m/rnorm) * rhat
    

    #translational dynamics
    #Fexternal = 0   #this would become a vector if thrust, solar pressure, etc are assumed to act on body
    F = Fg #+ Fexternal
    acceleration = F/M

    #state derivatives
    dstatedt = [*velocity, *acceleration]
    return dstatedt
