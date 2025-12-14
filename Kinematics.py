import numpy as np
from config import L1, L2, L3, Z_MIN, Z_MAX

# -------------------------------------------------
# Forward Kinematics
# -------------------------------------------------
def fk(d, t1, t2, t3):
    p0 = np.array([0, 0, 0])
    p1 = np.array([0, 0, d])

    p2 = p1 + np.array([L1*np.cos(t1), L1*np.sin(t1), 0])
    g2 = t1 + t2

    p3 = p2 + np.array([L2*np.cos(g2), L2*np.sin(g2), 0])
    g3 = g2 + t3

    p4 = p3 + np.array([L3*np.cos(g3), L3*np.sin(g3), 0])
    return np.array([p0, p1, p2, p3, p4])

# -------------------------------------------------
# Inverse Kinematics
# -------------------------------------------------
def ik(x, y, z, phi=0.0):
    z = np.clip(z, Z_MIN, Z_MAX)
    d = z

    wx = x - L3*np.cos(phi)
    wy = y - L3*np.sin(phi)

    r = np.sqrt(wx**2 + wy**2)
    if r > (L1 + L2):
        raise ValueError("Target out of reach")

    c2 = (r**2 - L1**2 - L2**2) / (2*L1*L2)
    c2 = np.clip(c2, -1.0, 1.0)

    t2 = np.arccos(c2)
    t1 = np.arctan2(wy, wx) - np.arctan2(
        L2*np.sin(t2), L1 + L2*np.cos(t2)
    )
    t3 = phi - (t1 + t2)

    return np.array([d, t1, t2, t3])
