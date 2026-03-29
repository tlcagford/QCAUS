import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class PDPTwoFieldTheory:
    """Single source of truth for ALL non-bio physics in QCAUS"""
    
    def __init__(self):
        self.epsilon = 1e-6          # kinetic mixing strength
        self.m_light = 1e-22         # eV (typical FDM mass)
        self.m_dark = 1.1 * self.m_light
        self.G = 6.67430e-11         # m^3 kg^-1 s^-2 (will be rescaled in astro units)
    
    def kinetic_mixing_term(self):
        """ℒ_mix = (ε/2) F_μν F'^μν"""
        return self.epsilon
    
    def two_field_schrodinger_poisson_1d(self, t, y, potential_func):
        """Simplified 1D coupled SP system for live demo"""
        psi_light, psi_dark = y[:len(y)//2], y[len(y)//2:]
        # Placeholder for real solver (expandable later)
        dpsi_dt_light = -1j * (potential_func + self.epsilon * potential_func) * psi_light
        dpsi_dt_dark  = -1j * (potential_func + self.epsilon * potential_func) * psi_dark
        return np.concatenate([dpsi_dt_light, dpsi_dt_dark])
    
    def fdm_soliton_profile(self, r, core_radius=1.0):
        """ρ(r) ∝ [sin(kr)/kr]^2"""
        k = np.pi / core_radius
        return (np.sin(k * r) / (k * r + 1e-8))**2
    
    def entanglement_interference(self, psi1, psi2, delta_phi=0):
        """Total density with quantum interference"""
        return np.abs(psi1)**2 + np.abs(psi2)**2 + 2 * np.real(psi1 * np.conj(psi2) * np.exp(1j * delta_phi))
    
    def demo_plot_soliton(self):
        r = np.linspace(0.01, 10, 500)
        rho = self.fdm_soliton_profile(r)
        fig, ax = plt.subplots()
        ax.plot(r, rho, label='FDM Soliton Core', color='purple')
        ax.set_xlabel('Radius (kpc)')
        ax.set_ylabel('Density')
        ax.set_title('Photon-Dark-Photon FDM Soliton')
        ax.legend()
        return fig
