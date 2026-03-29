"""
Core PDP Physics Library
Shared across all QCAUS modules
"""

import numpy as np
from scipy.constants import c, hbar, e, m_e

B_crit = m_e**2 * c**2 / (e * hbar)  # 4.4e13 G
alpha_fine = 1/137.036


def pdp_mixing_angle(epsilon, B_field, m_dark, omega=1e18):
    """Photon-Dark Photon mixing strength"""
    return epsilon * B_field / (m_dark + 1e-12)


def pdp_conversion_probability(B, L, epsilon, m_dark, omega=1e18):
    """P(γ → A') = (εB/m')² sin²(m'²L/4ω)"""
    if m_dark <= 0:
        return (epsilon * B / 1e15)**2 * np.ones_like(L)
    hbar_ev_s = 6.582e-16
    c_km_s = 3e5
    conv_len = 4 * omega * hbar_ev_s * c_km_s / (m_dark**2)
    return (epsilon * B / 1e15)**2 * np.sin(np.pi * L / conv_len)**2


def fdm_soliton_profile(r, fringe, rho0=1.0):
    """ρ(r) = ρ₀ [sin(kr)/(kr)]²"""
    r_s = 0.2 * (50.0 / max(fringe, 1))
    k = np.pi / max(r_s, 0.01)
    kr = k * r
    with np.errstate(divide='ignore', invalid='ignore'):
        return rho0 * np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)


def von_neumann_evolution(rho0, t, H, epsilon, m_dark, omega=1.0):
    """Solve i∂ρ/∂t = [H_eff, ρ] for photon-dark photon system"""
    mixing = epsilon * np.exp(-H * t)
    drho = np.zeros_like(rho0)
    drho[0,0] = 2 * mixing * np.imag(rho0[0,1])
    drho[1,1] = -2 * mixing * np.imag(rho0[0,1])
    drho[0,1] = -1j * (omega - m_dark) * rho0[0,1] - 1j * mixing * (rho0[0,0] - rho0[1,1])
    drho[1,0] = np.conj(drho[0,1])
    return drho


def entanglement_entropy(rho):
    """S = -Tr(ρ log ρ)"""
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 1e-12]
    return -np.sum(eigvals * np.log(eigvals)) if len(eigvals) > 0 else 0
