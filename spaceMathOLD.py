
#useful functions for spatial transformations, etc go here

import numpy as np

def T_IB(phi, theta, psi):
    """construct rotation tensor to convert from NED coords to inertial cartesian
    """
    ct = np.cos(theta)
    st = np.sin(theta)
    sp = np.sin(phi)
    cp = np.cos(phi)
    ss = np.sin(psi)
    cs = np.cos(psi)

    tib = np.array([[ct*cs,sp*st*cs-cp*ss,cp*st*cs+sp*ss],[ct*ss,sp*st*ss+cp*cs,cp*st*ss-sp*cs],[-st,sp*ct,cp*ct]])

    return tib





#test igrf model
"""
import pyIGRF as igrf


lat = 0
long = 0
alt = 0
t = 2023.0

mag = igrf.igrf_value(lat, long, alt, t)
Bned = mag[3:6]

print(mag)
print(B)
"""