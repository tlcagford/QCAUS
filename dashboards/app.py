import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from core.theory import PDPTwoFieldTheory

st.set_page_config(page_title="QCAUS", page_icon="🌌", layout="wide")

st.title("🌌 QCAUS — Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("**Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework** — One math, every scale (cosmology → stars → defense → imaging)")

# Sidebar branding
st.sidebar.image("https://via.placeholder.com/150x150.png?text=QCAUS", width=150)  # replace with your logo later
st.sidebar.title("QCAUS v1.0")
st.sidebar.caption("Unified by Tony E. Ford • Greeley, CO")
st.sidebar.markdown("**Core Theory** imported from `core/theory.py`")

# Tabs
tab_home, tab_cosmo, tab_astro, tab_defense, tab_radar, tab_bio, tab_theory = st.tabs([
    "🏠 Home", 
    "🌌 Cosmology", 
    "⭐ Astrophysics", 
    "🛡️ Scalar Defense", 
    "📡 Stealth PDP Radar", 
    "🧬 Bio Digital Twin", 
    "📜 Unified Theory"
])

with tab_home:
    st.header("Welcome to QCAUS")
    st.markdown("""
    One framework. One set of equations.  
    From primordial entanglement → magnetars → asteroid deflection → high-res imaging.  
    **Bio projects kept fully separate** in `biogen/original/` as requested.
    """)
    st.success("✅ Core physics consolidated • Bio untouched • Ready for expansion")

with tab_cosmo:
    st.header("Cosmology Simulator")
    theory = PDPTwoFieldTheory()
    st.pyplot(theory.demo_plot_soliton())
    st.caption("FDM soliton core from the consolidated two-field equations")

with tab_astro:
    st.header("Astrophysics Overlays")
    st.info("Magnetar QED, galaxy clusters, JWST/HST image refiner coming next — all using the same core theory")
    # Placeholder for real overlays (you can drop in your old code here)
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0,10,100), np.sin(np.linspace(0,10,100)), label="Sample magnetar pulse (demo)")
    ax.legend()
    st.pyplot(fig)

with tab_defense:
    st.header("Scalar Defense Simulator")
    st.write("Coupled Schrödinger-Poisson asteroid deflection demo (using core interference term)")
    # Simple interactive demo
    phi = st.slider("Gravitational potential strength", 0.0, 2.0, 1.0)
    theory = PDPTwoFieldTheory()
    r = np.linspace(0,10,200)
    interference = theory.entanglement_interference(
        np.exp(-r**2), np.exp(- (r-2)**2), delta_phi=phi*np.pi
    )
    st.line_chart(interference)

with tab_radar:
    st.header("Stealth PDP Radar")
    st.write("Live dark-photon leakage detection using entanglement signatures")
    st.info("Your original StealthPDPRadar Streamlit logic can be pasted here — it now imports from core.theory")

with tab_bio:
    st.header("🧬 Bio Digital Twin (PDPBioGen)")
    st.warning("Bio projects are kept **exactly as-is** in `biogen/original/`")
    st.markdown("No neural or parallel changes were made. To run your original PDPBioGen:")
    st.code("cd biogen/original\nstreamlit run your_original_app.py  # or python your_script.py")
    st.success("You can later add a neural_parallel/ subfolder if you want speed-ups")

with tab_theory:
    st.header("Unified Theory — Single Source of Truth")
    st.markdown("""
    **Key Consolidated Equations** (from all previous repos):
    - Kinetic mixing: ℒ_mix = (ε/2) F_μν F'^μν
    - Two-field Schrödinger-Poisson system
    - Von Neumann evolution i∂_t ρ = [H_eff, ρ]
    - FDM soliton ρ(r) ∝ [sin(kr)/kr]²
    - Interference density with dark-photon phase
    """)
    st.caption("Everything else imports from `core/theory.py` — no more duplicated math!")

# Footer
st.markdown("---")
st.caption("QCAUS • Photon-Dark-Photon Two-Field FDM Framework • All previous repos now consolidated")
