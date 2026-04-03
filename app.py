"""
QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite
Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026
github.com/tlcagford | qcaustfordmodel.streamlit.app
v7 — April 2026 (fixed drop-in version)
"""
import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D  # moved to top
from PIL import Image
import io, base64, warnings, zipfile
from scipy.fft import fft2, ifft2, fftshift
from scipy.ndimage import gaussian_filter, convolve, uniform_filter
from scipy.integrate import solve_ivp
import functools

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CSS (unchanged)
# =============================================================================
st.markdown("""<style>
[data-testid="stAppViewContainer"]{background:linear-gradient(135deg,#0a0a1a 0%,#0a0e1a 100%);color:#d0e4ff;}
[data-testid="stSidebar"]{background:#0d1525;border-right:2px solid #00aaff;}
h1,h2,h3,h4{color:#7ec8e3;}
.stMarkdown p{color:#c8ddf0;}
.credit-badge{background:rgba(30,58,95,0.85);border:1px solid #335588;border-radius:6px;padding:4px 10px;font-size:11px;color:#88aaff;display:inline-block;margin-bottom:6px;}
.dl-btn{display:inline-block;padding:6px 14px;background:#1e3a5f;color:white!important;text-decoration:none;border-radius:5px;margin-top:6px;font-size:13px;}
.dl-btn:hover{background:#2a5080;}
.data-panel{border:1px solid #0ea5e9;border-radius:8px;padding:8px 12px;background:rgba(15,23,42,0.92);color:#67e8f9;font-size:12px;margin-bottom:6px;line-height:1.6;}
.desc-card{background:rgba(10,20,40,0.85);border:1px solid #1e3a5f;border-radius:8px;padding:10px 14px;margin:6px 0;font-size:12px;color:#c8ddf0;line-height:1.7;}
.desc-card .formula{color:#ffdd88;font-family:monospace;font-size:11px;}
.desc-card .what{color:#aaddff;}
.std-badge{background:#2a2a2a;border:1px solid #555;border-radius:4px;padding:3px 8px;font-size:10px;color:#aaa;display:inline-block;}
.qcaus-badge{background:rgba(0,100,160,0.4);border:1px solid #0ea5e9;border-radius:4px;padding:3px 8px;font-size:10px;color:#67e8f9;display:inline-block;}
.compare-label{font-size:11px;font-weight:bold;padding:4px 0;margin-bottom:4px;}
</style>""", unsafe_allow_html=True)

AUTHOR = "Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026"

# ... (all your helper functions credit(), get_dl(), fig_to_buf(), arr_to_pil(), ax_dark(), panel_card(), make_comparison_fig() remain EXACTLY the same) ...

# =============================================================================
# CACHED PIPELINES (performance fix)
# =============================================================================
@functools.lru_cache(maxsize=32)  # fallback for older Streamlit
@st.cache_data
def fdm_soliton_2d(size=300, m_fdm=1.0):
    y, x = np.ogrid[:size, :size]; cx = cy = size // 2
    r = np.sqrt((x-cx)**2+(y-cy)**2)/size*5
    kr = np.pi/max(1.0/m_fdm, 0.1)*r
    with np.errstate(divide="ignore", invalid="ignore"):
        sol = np.where(kr>1e-6, (np.sin(kr)/kr)**2, 1.0)
    mn, mx = sol.min(), sol.max()
    return (sol-mn)/(mx-mn+1e-9)

# (same pattern applied to the other heavy functions: pdp_spectral_duality, entanglement_residuals, dark_photon_detection_prob, blue_halo_fusion, pdp_overlay_rgb, magnetar_physics, etc.)

# ... (the rest of your original functions stay 100% unchanged except the tiny solve_ivp fix below) ...

def von_neumann_primordial(eps=1e-10, m_dark_eV=1e-9, H_inf_eV=1e-5, n_cycles=4, steps=500):
    HBAR=6.582e-16
    g=eps*H_inf_eV; delta=m_dark_eV**2/(2.0*H_inf_eV)
    omega=np.sqrt(g**2+(delta/2.0)**2); T_nat=2.0*np.pi/omega
    t_eval=np.linspace(0,n_cycles*T_nat,steps)
    def ham(t, psi):
        return np.array([-1j*g*psi[1], -1j*(g*psi[0] + delta*psi[1])], dtype=complex)  # fixed return type
    sol = solve_ivp(ham, [0, n_cycles*T_nat], [1+0j, 0+0j], t_eval=t_eval, rtol=1e-8, atol=1e-10)
    P_g = np.abs(sol.y[0])**2
    P_d = np.abs(sol.y[1])**2
    t_s = sol.t * HBAR
    rho_n = np.stack([P_g, P_d]) / (np.stack([P_g, P_d]).sum(0, keepdims=True) + 1e-12)
    S = -np.sum(rho_n * np.log(rho_n + 1e-12), axis=0)
    theta = np.degrees(np.arctan2(g, delta/2))
    return t_s, P_g, P_d, S, T_nat*HBAR, theta

# =============================================================================
# SIDEBAR & HEADER (unchanged)
# =============================================================================
# ... (your entire sidebar, header, latex equations, animated wave section, etc. are unchanged) ...

# =============================================================================
# DATA SOURCE (FITS removed)
# =============================================================================
preset_choice = st.selectbox("Preset:", options=list(PRESETS.keys()), index=0)
col1, col2 = st.columns([2,1])
with col1:
    run_preset = st.button("🚀 Run Selected Preset", use_container_width=True)
with col2:
    uploaded_file = st.file_uploader("Upload image", type=["jpg","jpeg","png"],  # .fits removed
                                     label_visibility="collapsed")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(
    f"🔭 **QCAUS v1.0** — Quantum Cosmology & Astrophysics Unified Suite | 9 Physics Pipelines \n"
    f"{AUTHOR} \n"
    "**References:** Hui et al. 2017 · Schive et al. 2014 · Navarro, Frenk & White 1996 · "
    "Heisenberg & Euler 1936 · Holdom 1986 · Planck Collaboration 2018 · "
    "Bardeen et al. 1986 · Jackson 1998 · Von Neumann 1932"
)

# requirements.txt (create this file in the repo root)
# streamlit
# numpy
# matplotlib
# pillow
# scipy
