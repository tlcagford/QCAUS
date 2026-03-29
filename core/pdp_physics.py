"""
Photon-Dark Photon (PDP) Physics
Kinetic mixing, oscillation, and conversion probability
"""

import numpy as np
from .constants import alpha_fine, B_crit, hbar, c

def pdp_mixing_angle(epsilon, B_field, m_dark, omega=1e18):
    """
    Photon-Dark Photon mixing angle
    
    Parameters:
        epsilon: Kinetic mixing parameter
        B_field: Magnetic field strength (G)
        m_dark: Dark photon mass (eV)
        omega: Photon angular frequency (Hz)
    
    Returns:
        mixing_angle: θ = εB/m'
    """
    return epsilon * B_field / (m_dark + 1e-12)


def pdp_conversion_probability(B, L, epsilon, m_dark, omega=1e18):
    """
    Photon ↔ Dark Photon conversion probability
    P(γ → A') = (εB/m')² sin²(m'²L/4ω)
    
    From: Primordial Photon-DarkPhoton Entanglement framework
    """
    if m_dark <= 0:
        return (epsilon * B / 1e15)**2 * np.ones_like(L)
    
    # Conversion length (km)
    hbar_ev_s = 6.582e-16  # eV·s
    c_km_s = 3e5  # km/s
    conversion_length = 4 * omega * hbar_ev_s * c_km_s / (m_dark**2)
    
    P = (epsilon * B / 1e15)**2 * np.sin(np.pi * L / conversion_length)**2
    return np.clip(P, 0, 1)


def pdp_conversion_matrix(B_field, epsilon, m_dark, energy_range, L_range):
    """
    Compute full conversion matrix for photon-dark photon system
    Returns 2D array of conversion probabilities
    """
    hbar_ev_s = 6.582e-16
    c_km_s = 3e5
    omega_range = energy_range / hbar_ev_s
    
    P_matrix = np.zeros((len(omega_range), len(L_range)))
    for i, omega in enumerate(omega_range):
        for j, length in enumerate(L_range):
            if m_dark > 0:
                conv_len = 4 * omega * hbar_ev_s * c_km_s / (m_dark**2)
                P = (epsilon * B_field / 1e15)**2 * np.sin(np.pi * length / conv_len)**2
            else:
                P = (epsilon * B_field / 1e15)**2
            P_matrix[i, j] = np.clip(P, 0, 1)
    
    return P_matrix


def pdp_dark_photon_spectrum(B_field, epsilon, m_dark, energy_range, L_opt=None):
    """
    Dark photon spectrum produced from conversion
    """
    if L_opt is None:
        hbar_ev_s = 6.582e-16
        c_km_s = 3e5
        if m_dark > 0:
            L_opt = 4 * 1e18 * hbar_ev_s * c_km_s / (m_dark**2) / 2
        else:
            L_opt = 10
    
    omega = energy_range / 6.582e-16
    P = np.zeros_like(energy_range)
    
    for i, omega_val in enumerate(omega):
        if m_dark > 0:
            conv_len = 4 * omega_val * 6.582e-16 * 3e5 / (m_dark**2)
            P[i] = (epsilon * B_field / 1e15)**2 * np.sin(np.pi * L_opt / conv_len)**2
        else:
            P[i] = (epsilon * B_field / 1e15)**2
        P[i] = np.clip(P[i], 0, 1)
    
    # Dark photon flux (arbitrary normalization)
    dark_photon_flux = P * (energy_range)**(-2)
    
    return dark_photon_flux, P
