"""
Magnetar QED Physics
Strong-field quantum electrodynamics in magnetar magnetospheres
"""

import numpy as np
from .constants import B_crit, alpha_fine, pi

def magnetar_dipole_field(B_surface, R_ns, r, theta, inclination=0):
    """
    Magnetar dipole magnetic field
    
    B(r,θ) = B_surface (R_ns/r)³ [2 cosθ, sinθ, 0]
    
    From: Stellaris QED Explorer
    """
    B0 = B_surface * (R_ns / (r + 1e-9))**3
    theta_rad = np.radians(theta + inclination)
    
    B_r = 2 * B0 * np.cos(theta_rad)
    B_theta = B0 * np.sin(theta_rad)
    B_mag = np.sqrt(B_r**2 + B_theta**2)
    
    return B_r, B_theta, B_mag


def euler_heisenberg_vacuum(B_over_Bc, polarization='perp'):
    """
    Euler-Heisenberg vacuum refractive index
    n = 1 + α/(45π) (B/B_c)² × (4 for ⟂, 7 for ∥)
    
    From: Stellaris QED Explorer
    """
    x = B_over_Bc**2
    if polarization == 'perp':
        return 1 + 4 * alpha_fine/(45 * np.pi) * x
    elif polarization == 'para':
        return 1 + 7 * alpha_fine/(45 * np.pi) * x
    return 1


def vacuum_birefringence(B_over_Bc):
    """
    Vacuum birefringence Δn = n_⟂ - n_∥
    """
    n_perp = euler_heisenberg_vacuum(B_over_Bc, 'perp')
    n_para = euler_heisenberg_vacuum(B_over_Bc, 'para')
    return n_perp - n_para


def schwinger_pair_production(B_field):
    """
    Schwinger pair production rate
    Γ ∝ exp(-π E_crit / E) with E = B in natural units
    """
    B_norm = B_field / B_crit
    with np.errstate(divide='ignore', invalid='ignore'):
        rate = np.exp(-np.pi / (B_norm + 1e-9))
    return np.clip(rate, 0, 1)


def magnetar_field_energy(B_field, volume):
    """
    Magnetic field energy
    U_B = ∫ (B²/8π) dV
    """
    return np.sum(B_field**2) * volume / (8 * np.pi)


def magnetar_dipole_moment(B_surface, R_ns):
    """
    Magnetic dipole moment
    μ = B_surface R_ns³ / 2
    """
    return B_surface * R_ns**3 / 2
