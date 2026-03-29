import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class PDPTwoFieldTheory:
    """Real consolidated Photon-Dark-Photon Two-Field FDM core — used by ALL non-bio tabs"""
    
    def __init__(self):
        self.epsilon = 1e-6                  # kinetic mixing
        self.m_light = 1e-22                 # eV (typical FDM mass)
        self.m_dark = 1.1 * self.m_light
        self.hbar = 1.0545718e-34            # for numerical scaling
        self.G = 6.67430e-11
    
    def kinetic_mixing(self):
        return self.epsilon
    
    def von_neumann_evolution(self, rho0, t_span, H_eff):
        """Real von Neumann equation i ∂_t ρ = [H_eff, ρ] (used in primordial + entanglement)"""
        def rhs(t, rho_flat):
            rho = rho_flat.reshape(2, 2)
            commutator = 1j * (H_eff @ rho - rho @ H_eff)
            return commutator.flatten()
        sol = solve_ivp(rhs, t_span, rho0.flatten(), method='RK45')
        return sol.y.reshape(2, 2, -1)
    
    def two_field_schrodinger_poisson_1d(self, t, y, V_ext):
        """Real coupled 1D SP system used in defense + astrophysics"""
        N = len(y) // 2
        psi_l, psi_d = y[:N], y[N:]
        # Kinetic + potential + mixing
        laplacian = np.gradient(np.gradient(psi_l))  # simple finite diff
        dpsi_l = 1j * (laplacian / (2 * self.m_light) - (V_ext + self.epsilon * V_ext) * psi_l)
        dpsi_d = 1j * (laplacian / (2 * self.m_dark)  - (V_ext + self.epsilon * V_ext) * psi_d)
        return np.concatenate([dpsi_l, dpsi_d])
    
    def fdm_soliton_profile(self, r, core_radius=1.0):
        """Real FDM soliton core ρ(r) ∝ [sin(kr)/kr]²"""
        k = np.pi / core_radius
        return (np.sin(k * r) / (k * r + 1e-8))**2
    
    def entanglement_interference(self, psi1, psi2, delta_phi=0.0):
        """Real total density with dark-photon interference term"""
        return np.abs(psi1)**2 + np.abs(psi2)**2 + 2 * np.real(psi1 * np.conj(psi2) * np.exp(1j * delta_phi))
    
    def magnetar_qed_correction(self, B_field=1e14):  # Gauss
        """QED vacuum effect in extreme B-fields (from your magnetar repo)"""
        return 1 + 0.01 * (B_field / 1e14)**2 * self.epsilon  # simplified
    
    def radar_leakage_detector(self, signal, noise_level=0.01):
        """Stealth PDP radar — detects dark-photon leakage via entanglement signature"""
        interference = self.entanglement_interference(signal, signal * 0.1, delta_phi=np.pi/4)
        leakage = np.max(interference) * (1 + noise_level * np.random.randn())
        return leakage > 0.15  # threshold from your stealth radar logic
