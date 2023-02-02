
#useful functions for spatial transformations, etc go here

import numpy as np
import pyIGRF as igrf
from earth import R


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

def getBinertial(x,y,z):
    """Use IGRF model to get B field in inertial coordinates
    """
    year = 2023.25
    #convert cartesian coords into lat/long/alt (move this to a function...)
    rho = np.linalg.norm([x,y,z])
    phiE = 0
    thetaE = np.arccos(z/rho)
    psiE = np.arctan2(y,x)
    lat = 90 - thetaE*180/np.pi
    long = psiE*180/np.pi
    alt = (rho - R) / 1000 #km
    
    #calculate magnetic field in NED coord sys
    B = igrf.igrf_value(lat, long, alt, year) #nT
    Bned = np.array(B[3:6])

    #convert to inertial cartesian coords
    tib = T_IB(phiE, thetaE + np.pi,psiE)
    #print("tib: ", tib)
    Binertial = np.matmul(tib,Bned.transpose())
    #print("Binertial: ", Binertial)
    #print("Binertial size: ",Binertial.shape)

    return Binertial

def EulerAngles2Quaternions(phi_theta_psi):
    """ matrix multiplication simplification courtesy of Carlos Montalvo 2015
    Input is a Nx3 vector and output is a Nx4 vector
    """

    phi = phi_theta_psi[0]
    theta = phi_theta_psi[1]
    psi = phi_theta_psi[2]

    q0 = np.cos(phi/2) *np.cos(theta/2) *np.cos(psi/2) + np.sin(phi/2) *np.sin(theta/2) *np.sin(psi/2)
    q1 = np.sin(phi/2)*np.cos(theta/2)*np.cos(psi/2) - np.cos(phi/2)*np.sin(theta/2)*np.sin(psi/2)
    q2= np.cos(phi/2)*np.sin(theta/2)*np.cos(psi/2) + np.sin(phi/2)*np.cos(theta/2)*np.sin(psi/2)
    q3 = np.cos(phi/2)*np.cos(theta/2)*np.sin(psi/2) - np.sin(phi/2)*np.sin(theta/2)*np.cos(psi/2)

    return [q0,q1,q2,q3]

def Quaternions2EulerAngles(q0123):
    """input is a Nx4 vector with quaternions.
    output is a Nx3 vector of 3-2-1 euler angles
    matrix multiplication simplification courtesy of Carlos Montalvo 2015
    """
    if(q0123 != (1,3)):
        print("Wrong Dimensions!!")

    q0 = q0123[:,0]
    q1 = q0123[:,1]
    q2 = q0123[:,2]
    q3 = q0123[:,3]

    
    phi = (np.arctan2(2*(q0*q1 + q2*q3),1-2*(q1**2 + q2**2))) #phi
    theta = np.arcsin(2*(q0*q2-q3*q1)) #theta
    psi = np.arctan2(2*(q0*q3 + q1*q2),1-2*(q2**2 + q3**2)) #psi
    ptp = [phi, theta, psi]

    return np.real(ptp)

def T_IBQuaternions(q0123):
    """rotation matrix to to convert from body to inertial frame, via quaternions.. with help from Carlos Montalvo..
    """
    q0 = q0123[0]
    q1 = q0123[1]
    q2 = q0123[2]
    q3 = q0123[3]

    R = [[q0**2+q1**2-q2**2-q3**2, 2*(q1*q2-q0*q3),  2*(q0*q2+q1*q3)], [2*(q1*q2+q0*q3), (q0**2-q1**2+q2**2-q3**2), 2*(q2*q3-q0*q1)], [2*(q1*q3-q0*q2), 2*(q0*q1+q2*q3), (q0**2-q1**2-q2**2+q3**2)]]
    return np.array(R)





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