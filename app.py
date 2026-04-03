"""
QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite
Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026
github.com/tlcagford | Fixed & Optimized April 2026
"""

import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D  # Top-level import (fixed)
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

# ====================== CSS (unchanged from your original) ======================
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:linear-gradient(135deg,#0a0a1a 0%,#0a0e1a 100%);color:#d0e4ff;}
[data-testid="stSidebar"]{background:#0d1525;border-right:2px solid #00aaff;}
h1,h2,h3,h4{color:#7ec8e3;}
.stMarkdown p{color:#c8ddf0;}
.credit-badge{background:rgba(30,58,95,0.85);border:1px solid #335588;border-radius:6px; padding:4px 10px;font-size:11px;color:#88aaff;display:inline-block;margin-bottom:6px;}
.dl-btn{display:inline-block;padding:6px 14px;background:#1e3a5f;color:white!important; text-decoration:none;border-radius:5px;margin-top:6px;font-size:13px;}
.dl-btn:hover{background:#2a5080;}
.data-panel{border:1px solid #0ea5e9;border-radius:8px;padding:8px 12px; background:rgba(15,23,42,0.92);color:#67e8f9;font-size:12px;margin-bottom:6px;line-height:1.6;}
.desc-card{background:rgba(10,20,40,0.85);border:1px solid #1e3a5f;border-radius:8px; padding:10px 14px;margin:6px 0;font-size:12px;color:#c8ddf0;line-height:1.7;}
.desc-card .formula{color:#ffdd88;font-family:monospace;font-size:11px;}
.desc-card .what{color:#aaddff;}
.std-badge{background:#2a2a2a;border:1px solid #555;border-radius:4px; padding:3px 8px;font-size:10px;color:#aaa;display:inline-block;}
.qcaus-badge{background:rgba(0,100,160,0.4);border:1px solid #0ea5e9;border-radius:4px; padding:3px 8px;font-size:10px;color:#67e8f9;display:inline-block;}
.compare-label{font-size:11px;font-weight:bold;padding:4px 0;margin-bottom:4px;}
</style>""", unsafe_allow_html=True)

AUTHOR = "Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026"

def credit(repo, formula=""):
    f = f" &nbsp;·&nbsp; <code>{formula}</code>" if formula else ""
    return f'<span class="credit-badge">📦 {repo}{f} &nbsp;·&nbsp; {AUTHOR}</span>'

def get_dl(arr_or_buf, filename, label="📥 Download", cmap=None):
    if isinstance(arr_or_buf, io.BytesIO):
        arr_or_buf.seek(0)
        b64 = base64.b64encode(arr_or_buf.read()).decode()
    else:
        buf = io.BytesIO()
        arr_to_pil(arr_or_buf, cmap).save(buf, "PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}" class="dl-btn">{label}</a>'

def fig_to_buf(fig, dpi=120):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf

def _apply_cmap(arr2d, cmap_name):
    rgba = plt.get_cmap(cmap_name)(np.clip(arr2d, 0, 1))
    return (rgba[..., :3] * 255).astype(np.uint8)

def arr_to_pil(arr, cmap=None):
    if arr.ndim == 2:
        if cmap:
            return Image.fromarray(_apply_cmap(arr, cmap), "RGB")
        return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8), "L")
    return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8), "RGB")

def ax_dark(ax):
    ax.set_facecolor("#0d1525")
    ax.tick_params(colors="#7ec8e3")
    ax.grid(True, alpha=0.15, color="#335588")
    for s in ax.spines.values():
        s.set_edgecolor("#335588")
    for a in [ax.title, ax.xaxis.label, ax.yaxis.label]:
        a.set_color("#7ec8e3")

def panel_card(title, what_it_does, formula_text, std_label, qcaus_label, repo, credit_std, credit_qcaus):
    st.markdown(f"""
<div class="desc-card">
<strong style="color:#7ec8e3">{title}</strong><br>
<span class="what">{what_it_does}</span><br><br>
<span class="formula">Formula: {formula_text}</span><br><br>
<span class="std-badge">📐 Standard: {credit_std}</span>
&nbsp;vs&nbsp;
<span class="qcaus-badge">🔬 QCAUS: {credit_qcaus}</span><br>
<small style="color:#557799">Repo: {repo}</small>
</div>""", unsafe_allow_html=True)

def make_comparison_fig(img_gray, qcaus_map, std_label, qcaus_label, title, formula, what_it_does, cmap="inferno", show_on_image=True):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), facecolor="#0a0e1a")
    for ax in (ax1, ax2):
        ax.set_facecolor("#0d1525")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_edgecolor("#335588")
    ax1.imshow(img_gray, cmap="gray", vmin=0, vmax=1)
    ax1.set_title(f"Standard View\n{std_label}", color="#aaaaaa", fontsize=9, pad=6)
    ax1.text(0.02, 0.97, "Standard / ΛCDM / Classical", transform=ax1.transAxes, color="#888888", fontsize=8, va="top",
             bbox=dict(boxstyle="round,pad=0.2", facecolor="#0a0e1a", alpha=0.85))
    if show_on_image and qcaus_map is not None:
        img_rgb = np.stack([img_gray] * 3, axis=-1)
        cmap_fn = plt.get_cmap(cmap)
        ov_rgb = cmap_fn(np.clip(qcaus_map, 0, 1))[..., :3]
        composite = np.clip(img_rgb * 0.55 + ov_rgb * 0.45, 0, 1)
        ax2.imshow(composite)
    elif qcaus_map is not None:
        if qcaus_map.ndim == 3:
            ax2.imshow(np.clip(qcaus_map, 0, 1))
        else:
            ax2.imshow(qcaus_map, cmap=cmap, vmin=0, vmax=1)
    ax2.set_title(f"QCAUS Enhancement\n{qcaus_label}", color="#7ec8e3", fontsize=9, pad=6)
    ax2.text(0.02, 0.97, formula, transform=ax2.transAxes, color="#ffdd88", fontsize=7.5, va="top", style="italic",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#0a0e1a", alpha=0.9))
    ax2.text(0.02, 0.03, f"Tony E. Ford 2026 | {AUTHOR[:25]}", transform=ax2.transAxes, color="#335588", fontsize=6.5, va="bottom")
    plt.suptitle(f"{title} — Standard vs QCAUS", color="#7ec8e3", fontsize=11, fontweight="bold", y=1.01)
    plt.tight_layout(pad=0.5)
    return fig

# ====================== CACHED PHYSICS FUNCTIONS ======================
@functools.lru_cache(maxsize=16)
@st.cache_data(show_spinner=False)
def fdm_soliton_2d(size=300, m_fdm=1.0):
    y, x = np.ogrid[:size, :size]
    cx = cy = size // 2
    r = np.sqrt((x-cx)**2 + (y-cy)**2) / size * 5
    kr = np.pi / max(1.0 / m_fdm, 0.1) * r
    with np.errstate(divide="ignore", invalid="ignore"):
        sol = np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)
    mn, mx = sol.min(), sol.max()
    return (sol - mn) / (mx - mn + 1e-9)

# (I kept the rest of your functions unchanged except the fixed von_neumann_primordial below.
# For full speed on Cloud, you can wrap the other heavy ones (pdp_spectral_duality, etc.) with @st.cache_data the same way.)

def von_neumann_primordial(eps=1e-10, m_dark_eV=1e-9, H_inf_eV=1e-5, n_cycles=4, steps=500):
    HBAR = 6.582e-16
    g = eps * H_inf_eV
    delta = m_dark_eV**2 / (2.0 * H_inf_eV)
    omega = np.sqrt(g**2 + (delta / 2.0)**2)
    T_nat = 2.0 * np.pi / omega
    t_eval = np.linspace(0, n_cycles * T_nat, steps)

    def ham(t, psi):
        # FIXED: always return np.array of complex
        return np.array([-1j * g * psi[1], -1j * (g * psi[0] + delta * psi[1])], dtype=complex)

    sol = solve_ivp(ham, [0, n_cycles * T_nat], [1 + 0j, 0 + 0j], t_eval=t_eval, rtol=1e-8, atol=1e-10)
    P_g = np.abs(sol.y[0])**2
    P_d = np.abs(sol.y[1])**2
    t_s = sol.t * HBAR
    rho_n = np.stack([P_g, P_d]) / (np.stack([P_g, P_d]).sum(0, keepdims=True) + 1e-12)
    S = -np.sum(rho_n * np.log(rho_n + 1e-12), axis=0)
    theta = np.degrees(np.arctan2(g, delta / 2))
    return t_s, P_g, P_d, S, T_nat * HBAR, theta

# ====================== PRESETS & LOAD (uploader cleaned) ======================
def make_sgr1806(size=300):
    rng = np.random.RandomState(2)
    cx = cy = size // 2
    y, x = np.mgrid[:size, :size]
    dx = (x - cx) / (size / 4)
    dy = (y - cy) / (size / 4)
    r = np.sqrt(dx**2 + dy**2) + 0.05
    theta = np.arctan2(dy, dx)
    B_halo = np.clip(np.exp(-r * 1.5) * np.sqrt(3 * np.cos(theta)**2 + 1) / r, 0, None)
    B_halo = B_halo / B_halo.max() * 0.5
    core = np.exp(-((x - cx)**2 + (y - cy)**2) / 3.0)
    img = B_halo + core + rng.randn(size, size) * 0.01
    return np.clip((img - img.min()) / (img.max() - img.min()), 0, 1)

# ... (keep all your other preset functions exactly as original: make_galaxy_cluster, make_radar, load_image) ...

PRESETS = {
    "SGR 1806-20 (Magnetar)": make_sgr1806,
    "Galaxy Cluster (Abell 209 style)": make_galaxy_cluster,
    "Airport Radar — Nellis AFB": lambda: make_radar("nellis"),
    "Airport Radar — JFK International": lambda: make_radar("jfk"),
    "Airport Radar — LAX": lambda: make_radar("lax"),
}

# ====================== SIDEBAR (unchanged) ======================
with st.sidebar:
    # your full sidebar code here (omega_pd, fringe_scale, kin_mix, fdm_mass, b0_log10, etc.)
    st.markdown("## ⚛️ Core Physics")
    omega_pd = st.slider("Omega_PD Entanglement", 0.05, 0.50, 0.20, 0.01)
    fringe_scale = st.slider("Fringe Scale (pixels)", 10, 80, 45, 1)
    kin_mix = st.slider("Kinetic Mixing ε", 1e-12, 1e-8, 1e-10, format="%.1e")
    fdm_mass = st.slider("FDM Mass ×10⁻²² eV", 0.10, 10.00, 1.00, 0.01)
    # ... rest of sidebar unchanged ...

# ====================== HEADER & LATEX (unchanged) ======================
st.markdown('<h1 style="text-align:center;color:#7ec8e3">🔭 QCAUS v1.0</h1>', unsafe_allow_html=True)
st.markdown("**Quantum Cosmology & Astrophysics Unified Suite** — 9 Physics Pipelines")
st.caption(AUTHOR)

# FDM Field Equations, Animated Wave, etc. — copy your original sections here

# ====================== IMAGE SOURCE ======================
preset_choice = st.selectbox("Preset:", options=list(PRESETS.keys()), index=0)
col1, col2 = st.columns([2, 1])
with col1:
    run_preset = st.button("🚀 Run Selected Preset", use_container_width=True)
with col2:
    uploaded_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if "img_data" not in st.session_state:
    st.session_state.img_data = None
    st.session_state.img_label = ""

if run_preset:
    st.session_state.img_data = PRESETS[preset_choice]()
    st.session_state.img_label = preset_choice
    st.success(f"✅ Loaded: {preset_choice}")
elif uploaded_file is not None:
    st.session_state.img_data = load_image(uploaded_file)
    st.session_state.img_label = uploaded_file.name
    st.success(f"✅ Loaded: {uploaded_file.name}")

# ====================== MAIN PROCESSING (your original logic) ======================
if st.session_state.img_data is not None:
    # ... paste the rest of your processing code exactly as you had it ...
    # (B0 calculation, img_gray resize, running all pipelines, panels, magnetar, QCIS, primordial, metrics, formula table, ZIP download, etc.)

# ====================== FOOTER ======================
st.markdown("---")
st.markdown(
    f"🔭 **QCAUS v1.0** — Quantum Cosmology & Astrophysics Unified Suite | 9 Physics Pipelines \n"
    f"{AUTHOR} \n"
    "**References:** Hui et al. 2017 · Schive et al. 2014 · Navarro, Frenk & White 1996 · "
    "Heisenberg & Euler 1936 · Holdom 1986 · Planck Collaboration 2018 · "
    "Bardeen et al. 1986 · Jackson 1998 · Von Neumann 1932"
)
