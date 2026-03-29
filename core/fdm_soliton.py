"""
Fuzzy Dark Matter (FDM) Soliton Physics
Ground state solution of Schrödinger-Poisson equation
ρ(r) = ρ₀ [sin(kr)/(kr)]²
"""

import numpy as np
from scipy.ndimage import gaussian_filter
from .constants import m_fdm_typical

def fdm_soliton_profile(r, fringe, rho0=1.0, m_fdm=None):
    """
    FDM Soliton Core Profile
    ρ(r) = ρ₀ [sin(kr)/(kr)]²
    
    From: QCI AstroEntangle Refiner
    """
    if m_fdm is None:
        m_fdm = m_fdm_typical
    
    # Soliton scale radius depends on FDM mass
    # r_s ∝ 1/m_fdm (de Broglie wavelength)
    r_s = 0.2 * (50.0 / max(fringe, 1))
    k = np.pi / max(r_s, 0.01)
    kr = k * r
    
    with np.errstate(divide='ignore', invalid='ignore'):
        soliton = rho0 * np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)
    
    # Normalize
    soliton = (soliton - soliton.min()) / (soliton.max() - soliton.min() + 1e-9)
    soliton = gaussian_filter(soliton, sigma=2)
    
    return soliton


def fdm_soliton_2d(size, fringe, rho0=1.0):
    """
    Generate 2D FDM soliton core image
    
    Parameters:
        size: (height, width) of output image
        fringe: fringe parameter (controls soliton scale)
        rho0: central density
    
    Returns:
        2D array of soliton density
    """
    h, w = size
    y, x = np.ogrid[:h, :w]
    cx, cy = w//2, h//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / max(h, w, 1)
    
    return fdm_soliton_profile(r, fringe, rho0)


def fdm_soliton_radial_profile(soliton_2d):
    """
    Extract radial profile from 2D soliton image
    """
    h, w = soliton_2d.shape
    cx, cy = w//2, h//2
    y, x = np.ogrid[:h, :w]
    r = np.sqrt((x - cx)**2 + (y - cy)**2)
    
    radii = np.arange(0, min(h, w)//2, 2)
    profile = []
    for rad in radii:
        mask = (r >= rad) & (r < rad + 2)
        if np.any(mask):
            profile.append(np.mean(soliton_2d[mask]))
        else:
            profile.append(0)
    
    return radii, np.array(profile)


def fdm_soliton_quantum_correction(r, m_fdm, rho0=1.0):
    """
    FDM soliton with quantum corrections from self-interactions
    δ_quantum ∝ (m_fdm / m_Planck)²
    """
    from .constants import m_planck
    
    soliton = fdm_soliton_profile(r, m_fdm=m_fdm)
    
    quantum_correction = 1 + (m_fdm / m_planck)**2 * 100
    
    return soliton * rho0 * quantum_correction
