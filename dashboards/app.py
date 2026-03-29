import streamlit as st
import sys
from pathlib import Path

# ====================== PATH FIX FOR STREAMLIT CLOUD ======================
# This solves ModuleNotFoundError when importing from subfolders like 'core/'
current_file = Path(__file__).resolve()
repo_root = current_file.parent.parent  # Goes up from dashboards/ to QCAUS root
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
# ========================================================================

import numpy as np
import matplotlib.pyplot as plt

# Now import from core (this should now work)
from core.theory import PDPTwoFieldTheory

# ====================== APP CONFIG ======================
st.set_page_config(
    page_title="QCAUS",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌌 QCAUS — Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("""
**Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework**  
One consistent set of equations powering cosmology, astrophysics, scalar defense, stealth radar, and more.
""")

# Sidebar
st.sidebar.title("QCAUS v1.0")
st.sidebar.caption("Unified Framework by Tony E. Ford • Greeley, Colorado")
st.sidebar.success("✅ Core physics consolidated\nBio projects untouched")

# ====================== TABS ======================
tab_home, tab_cosmo, tab_astro, tab_defense, tab_radar, tab_bio, tab_theory = st.tabs([
    "🏠 Home", "🌌 Cosmology", "⭐ Astrophysics", 
    "🛡️ Scalar Defense", "📡 Stealth PDP Radar", 
    "🧬 Bio Digital Twin", "📜 Unified Theory"
])

with tab_home:
    st.header("Welcome to the Unified QCAUS Platform")
    st.markdown("""
    This single dashboard consolidates your previous projects under one Photon-Dark-Photon Two-Field FDM core.
    
    - Cosmology & primordial entanglement  
    - Astrophysical simulations & image refinement  
    - Scalar defense concepts  
    - Stealth radar demos  
    - **Bio projects (PDPBioGen) kept completely separate** in `biogen/original/`
    """)
    st.info("Use the tabs above to explore each domain. All non-bio modules import from `core/theory.py`.")

with tab_cosmo:
    st.header("Cosmology Simulator")
    theory = PDPTwoFieldTheory()
    st.pyplot(theory.demo_plot_soliton())
    st.caption("FDM Soliton Core Profile — generated from consolidated two-field equations")

with tab_astro:
    st.header("Astrophysics Overlays")
    st.info("Magnetar QED effects, galaxy clusters, and JWST/HST image refiner will go here. All using the shared core theory.")
    # Demo placeholder
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 10, 200)
    ax.plot(x, np.sin(x) * np.exp(-0.2 * x), label="Sample Magnetar Pulse Profile")
    ax.set_xlabel("Time / Phase")
    ax.set_ylabel("Intensity")
    ax.legend()
    st.pyplot(fig)

with tab_defense:
    st.header("Scalar Defense Simulator")
    st.write("Demonstrates gravitational potential engineering via dark-photon interference")
    phi = st.slider("Interference Phase Shift (radians)", 0.0, 4.0, 1.0, 0.1)
    theory = PDPTwoFieldTheory()
    r = np.linspace(0, 10, 300)
    psi1 = np.exp(-r**2)
    psi2 = np.exp(-(r - 2)**2)
    interference = theory.entanglement_interference(psi1, psi2, delta_phi=phi)
    st.line_chart(interference, use_container_width=True)
    st.caption("Total density with quantum interference term")

with tab_radar:
    st.header("Stealth PDP Radar")
    st.write("Dark-photon leakage / entanglement signature detection demo")
    st.info("Your original StealthPDPRadar code can be integrated here. It now re-uses the core theory module.")

with tab_bio:
    st.header("🧬 Bio Digital Twin (PDPBioGen)")
    st.warning("Bio projects are **kept exactly as-is** in the `biogen/original/` folder as requested.")
    st.markdown("""
    No neural network or multiprocessing changes were applied.  
    To run your original PDPBioGen apps:
    - Navigate to `biogen/original/` locally  
    - Run `streamlit run your_bio_app.py` (or your main script)
    """)
    st.success("You can add a `biogen/neural_parallel/` folder later if you want performance upgrades.")

with tab_theory:
    st.header("Unified Theory — Single Source of Truth")
    st.markdown("""
    All non-bio modules now share these core equations:
    
    - Kinetic mixing: ℒ_mix = (ε/2) F_μν F'^μν  
    - Two-field coupled Schrödinger-Poisson system  
    - Von Neumann density matrix evolution  
    - FDM soliton profiles ρ(r) ∝ [sin(kr)/(kr)]²  
    - Entanglement interference term
    """)
    st.caption("Everything imports cleanly from `core/theory.py` — no duplicated math across domains.")

# Footer
st.markdown("---")
st.caption("QCAUS • Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework • Consolidated from multiple previous repos")
