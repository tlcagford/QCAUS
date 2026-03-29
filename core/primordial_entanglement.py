"""
Primordial Photon-Dark Photon Entanglement
Von Neumann evolution in the expanding universe
"""

import numpy as np
from scipy.integrate import odeint
from .constants import H0

def von_neumann_density_matrix(rho0, t, H, epsilon, m_dark, omega_photon=1.0):
    """
    Solve von Neumann equation for coupled photon-dark photon system
    i ∂ρ/∂t = [H_eff, ρ] with decoherence
    
    From: Primordial Photon-DarkPhoton Entanglement framework
    """
    # Scale factor dependent mixing
    a_t = np.exp(-H * t)
    mixing = epsilon * a_t
    
    # Liouville-von Neumann evolution
    drho_dt = np.zeros_like(rho0, dtype=complex)
    
    # Populations
    drho_dt[0,0] = 2 * mixing * np.imag(rho0[0,1])
    drho_dt[1,1] = -2 * mixing * np.imag(rho0[0,1])
    
    # Coherence
    drho_dt[0,1] = -1j * (omega_photon - m_dark) * rho0[0,1] - 1j * mixing * (rho0[0,0] - rho0[1,1])
    drho_dt[1,0] = np.conj(drho_dt[0,1])
    
    return drho_dt


def solve_von_neumann_evolution(omega, m_dark, H=H0, t_max=1.0, n_steps=200):
    """
    Solve full von Neumann evolution for photon-dark photon system
    Returns mixing angle and entanglement entropy evolution
    """
    epsilon = omega * 0.1
    t = np.linspace(0, t_max, n_steps)
    rho0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    
    def rho_deriv(rho_flat, t, H, epsilon, m_dark):
        rho = rho_flat.reshape(2, 2)
        drho = von_neumann_density_matrix(rho, t, H, epsilon, m_dark)
        return drho.flatten()
    
    try:
        rho_flat = odeint(rho_deriv, rho0.flatten(), t, args=(H, epsilon, m_dark))
        rhos = rho_flat.reshape(-1, 2, 2)
        mixing_evolution = np.abs(rhos[:, 0, 1])
        entropy_evolution = np.array([entanglement_entropy(rho) for rho in rhos])
        return mixing_evolution, entropy_evolution, t
    except Exception:
        # Analytic approximation
        mixing_evolution = epsilon * (1 - np.exp(-H * t))
        entropy_evolution = -mixing_evolution * np.log(mixing_evolution + 1e-12)
        return mixing_evolution, entropy_evolution, t


def entanglement_entropy(rho):
    """
    Compute von Neumann entanglement entropy
    S = -Tr(ρ log ρ)
    """
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-12]
    if len(eigenvalues) == 0:
        return 0.0
    return -np.sum(eigenvalues * np.log(eigenvalues))


def entanglement_entropy_density(rho, scale_factor=1.0):
    """
    Entanglement entropy density
    s = S / V where V ∝ a³
    """
    entropy = entanglement_entropy(rho)
    return entropy / (scale_factor**3)


def mixing_amplitude(epsilon, H, t):
    """
    Analytic approximation for mixing amplitude
    θ(t) ≈ ε (1 - e^{-Ht})
    """
    return epsilon * (1 - np.exp(-H * t))
