"""
QCIS Framework - Quantum-Corrected Cosmological Perturbations
Power spectra with quantum corrections from vacuum fluctuations
"""

import numpy as np
from .constants import H0, rho_crit

def quantum_corrected_power_spectrum(k, A_s=2.1e-9, n_s=0.965, f_nl=1.0, r=0.01):
    """
    Quantum-corrected power spectrum
    P(k) = P_ΛCDM(k) × (1 + f_NL (k/k₀)^{n_q})
    
    From: QCIS Framework
    """
    k0 = 0.05  # Mpc⁻¹ pivot scale
    P_lcdm = A_s * (k / k0)**(n_s - 1)
    quantum_correction = 1 + f_nl * (k / k0)**0.8
    P_quantum = P_lcdm * quantum_correction
    tensor_spectrum = r * P_lcdm
    
    return P_lcdm, P_quantum, tensor_spectrum, quantum_correction


def matter_transfer_function(k, omega_m=0.3, omega_b=0.05, h=0.7):
    """
    Matter transfer function with quantum corrections
    T(k) = T_EH(k) × (1 + ω_q (k/k_eq)^{n_q})
    """
    # Eisenstein-Hu transfer function
    q = k / (omega_m * h**2)
    T_EH = np.log(1 + 2.34*q) / (2.34*q) * (1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**(-0.25)
    
    # Quantum correction term
    k_eq = 0.01  # Equality scale in h/Mpc
    n_q = 0.8
    omega_q = 0.1
    quantum_factor = 1 + omega_q * (k / k_eq)**n_q
    
    return T_EH * quantum_factor, quantum_factor


def non_gaussianity_correction(k, f_nl, k0=0.05):
    """
    Local non-Gaussianity correction to power spectrum
    P(k) → P(k) × (1 + f_nl (k/k₀)^{n_q})
    """
    n_q = 0.8
    return 1 + f_nl * (k / k0)**n_q


def quantum_stress_energy_tensor(mode_amplitude, k):
    """
    Quantum stress-energy tensor from vacuum fluctuations
    ⟨T_μν⟩_quantum ∝ ∫ dk k² |δφ_k|²
    """
    # Simplified calculation
    return mode_amplitude**2 * k**2


def tensor_to_scalar_ratio(r, quantum_correction=True):
    """
    Tensor-to-scalar ratio with quantum corrections
    r = P_t / P_s
    """
    if quantum_correction:
        return r * 0.95  # Slight suppression from quantum effects
    return r
