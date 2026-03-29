"""
Physics Constants
All fundamental constants used across QCAUS
"""

import numpy as np
from scipy.constants import c, hbar, e, m_e, alpha, pi

# ============================================
# QUANTUM ELECTRODYNAMICS
# ============================================

# Schwinger critical field (4.4e13 G)
B_crit = m_e**2 * c**2 / (e * hbar)

# Schwinger critical field in Tesla
B_crit_T = B_crit * 1e-4

# Critical electric field (1.3e18 V/m)
E_crit = m_e**2 * c**3 / (e * hbar)

# Fine structure constant
alpha_fine = alpha

# Compton wavelength (3.86e-13 m)
lambda_compton = hbar / (m_e * c)

# Electron rest energy (511 keV)
m_eV = m_e * c**2 / 1.602e-19

# ============================================
# COSMOLOGICAL CONSTANTS
# ============================================

# Hubble constant (km/s/Mpc)
H0 = 70.0

# Critical density (g/cm³)
rho_crit = 9.2e-30

# Planck mass (eV)
m_planck = 1.22e28

# ============================================
# ASTROPHYSICAL CONSTANTS
# ============================================

# Solar mass (kg)
M_sun = 1.989e30

# Solar radius (km)
R_sun = 6.96e5

# Parsec to km
pc_to_km = 3.086e13

# Kiloparsec to km
kpc_to_km = 3.086e16

# ============================================
# DARK MATTER PARAMETERS
# ============================================

# Typical FDM mass (eV)
m_fdm_typical = 1e-22

# FDM de Broglie wavelength (kpc)
lambda_dB = lambda m: 2 * np.pi * hbar * c / (m * 1.602e-19) / kpc_to_km

# ============================================
# HELPER FUNCTIONS
# ============================================

def normalize(arr, clip_percentiles=(0.5, 99.5)):
    """Normalize array to [0,1] with percentile clipping"""
    arr = np.nan_to_num(arr, nan=0.0, posinf=1.0, neginf=0.0)
    vmin, vmax = np.percentile(arr, clip_percentiles[0]), np.percentile(arr, clip_percentiles[1])
    if vmax - vmin < 1e-9:
        return np.zeros_like(arr)
    return np.clip((arr - vmin) / (vmax - vmin + 1e-9), 0, 1)
