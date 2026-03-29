import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class PDPTwoFieldTheory:
    """Real consolidated Photon-Dark-Photon Two-Field FDM core — now with expanded Magnetar QED"""
    
    def __init__(self):
        self.epsilon = 1e-6
        self.m_light = 1e-22
        self.m_dark = 1.1 * self.m_light
        self.hbar = 1.0545718e-34
        self.G = 6.67430e-11
        self.alpha = 1/137.036   # fine-structure constant
    
    def kinetic_mixing(self):
        return self.epsilon
    
    def von_neumann_evolution(self, rho0, t_span, H_eff):
        def rhs(t, rho_flat):
            rho = rho_flat.reshape(2, 2)
            commutator = 1j * (H_eff @ rho - rho @ H_eff)
            return commutator.flatten()
        sol = solve_ivp(rhs, t_span, rho0.flatten(), method='RK45')
        return sol.y.reshape(2, 2, -1)
    
    def two_field_schrodinger_poisson_1d(self, t, y, V_ext):
        N = len(y) // 2
        psi_l, psi_d = y[:N], y[N:]
        laplacian = np.gradient(np.gradient(psi_l))
        dpsi_l = 1j * (laplacian / (2 * self.m_light) - (V_ext + self.epsilon * V_ext) * psi_l)
        dpsi_d = 1j * (laplacian / (2 * self.m_dark)  - (V_ext + self.epsilon * V_ext) * psi_d)
        return np.concatenate([dpsi_l, dpsi_d])
    
    def fdm_soliton_profile(self, r, core_radius=1.0):
        k = np.pi / core_radius
        return (np.sin(k * r) / (k * r + 1e-8))**2
    
    def entanglement_interference(self, psi1, psi2, delta_phi=0.0):
        return np.abs(psi1)**2 + np.abs(psi2)**2 + 2 * np.real(psi1 * np.conj(psi2) * np.exp(1j * delta_phi))
    
    # ====================== EXPANDED MAGNETAR QED ======================
    def magnetar_qed_correction(self, B_field=1e14):
        B_crit = 4.414e13  # Schwinger critical field in Gauss
        return 1 + (self.alpha / (45 * np.pi)) * (B_field / B_crit)**2
    
    def vacuum_birefringence(self, B_field=1e14):
        B_crit = 4.414e13
        return (self.alpha / (45 * np.pi)) * (B_field / B_crit)**2 * 2.0   # Δn parallel - perpendicular
    
    def photon_splitting_probability(self, energy_kev, B_field=1e14):
        # Simplified scaling from literature (scales ~ B³ E³)
        return 1e-4 * (energy_kev / 100)**3 * (B_field / 1e14)**3
    
    def pair_production_rate(self, energy_kev, B_field=1e14):
        # Exponential suppression below threshold, rapid above
        threshold = 1.022 * (1e14 / B_field)  # MeV scaled
        if energy_kev < threshold:
            return 0.0
        return 0.05 * np.exp(-(threshold / energy_kev))
    
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
    
    def radar_leakage_detector(self, signal, noise_level=0.01):
        interference = self.entanglement_interference(signal, signal * 0.1, delta_phi=np.pi/4)
        leakage = np.max(interference) * (1 + noise_level * np.random.randn())
        return leakage > 0.15
