import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="QCAUS v1.0 - Quantum Cosmology & Astrophysics Unified Suite",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .download-button {
        display: inline-block;
        padding: 8px 16px;
        background-color: #ff4b4b;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🔭 QCAUS v1.0</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center">FDM · PDP · Magnetar · QCIS · EM Spectrum</div>', unsafe_allow_html=True)

# Sidebar for parameters
with st.sidebar:
    st.markdown("## ⚛️ Core Physics")
    
    omega_pd = st.slider("Omega_PD Entanglement", 0.05, 0.50, 0.20, 0.01)
    fringe_scale = st.slider("Fringe Scale (pixels)", 10, 80, 45, 1)
    kinetic_mixing = st.slider("Kinetic Mixing eps", 1e-12, 1e-8, 1e-10, format="%.1e")
    fdm_mass = st.slider("FDM Mass x10^-22 eV", 0.10, 10.00, 1.00, 0.01)
    
    st.markdown("---")
    st.markdown("## 🌟 Magnetar")
    
    b0_log10 = st.slider("B0 log10 G", 13.0, 16.0, 15.0, 0.1)
    magnetar_eps = st.slider("Magnetar eps", 0.01, 0.50, 0.10, 0.01)
    
    st.markdown("---")
    st.markdown("## 📈 QCIS")
    
    f_nl = st.slider("f_NL", 0.00, 5.00, 0.00, 0.01)
    n_q = st.slider("n_q", 0.00, 2.00, 0.00, 0.01)
    
    st.markdown("---")
    st.markdown("**Tony Ford | tlcagford@gmail.com | Patent Pending | 2026**")

# Main content
st.markdown("## 🔭 QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite")

# File upload section
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### Preset Real Data — click to run instantly")
    preset_data = st.button("Run with SGR 1806-20", use_container_width=True)
    
with col2:
    st.markdown("### — OR —")
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=['jpg', 'jpeg', 'png'],
        help="Limit 200MB per file"
    )

# Helper functions
def normalize_image(img):
    """Normalize image to [0,1] range"""
    if isinstance(img, np.ndarray):
        if img.dtype == np.float32 or img.dtype == np.float64:
            img = np.nan_to_num(img, nan=0.0, posinf=1.0, neginf=0.0)
            img = np.clip(img, 0, 1)
        elif img.dtype == np.uint8:
            img = img / 255.0
        else:
            img = img.astype(np.float32)
            img_min = img.min()
            img_max = img.max()
            if img_max > img_min:
                img = (img - img_min) / (img_max - img_min)
            else:
                img = np.zeros_like(img)
    return img

def load_image(file):
    """Load image from uploaded file or create default"""
    if file is not None:
        img = Image.open(file)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Resize if too large
        if max(img.size) > 1024:
            img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        return np.array(img)
    else:
        # Create default simulated image
        size = 512
        x = np.linspace(-5, 5, size)
        y = np.linspace(-5, 5, size)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        theta = np.arctan2(Y, X)
        
        img = np.exp(-R**2 / 6) * (1 + 0.4 * np.cos(6*R - 2*theta))
        img += 0.15 * np.exp(-((R-2.5)**2)/0.5) * (1 + np.cos(8*theta))
        img += 0.05 * np.random.randn(size, size) * 0.05
        img = np.clip(img, 0, 1)
        img_rgb = np.stack([img, img*0.8, img*0.6], axis=2)
        return (img_rgb * 255).astype(np.uint8)

# Physics functions
def apply_pdp_entanglement(img, omega_pd):
    """PDP Entanglement: I_ent = I * (1 + Ω_PD * sin(2πI))"""
    img_float = img.astype(np.float32) / 255.0
    if len(img.shape) == 3:
        gray = np.mean(img_float, axis=2, keepdims=True)
        phase_factor = 1 + omega_pd * np.sin(2 * np.pi * gray)
        return np.clip(img_float * phase_factor, 0, 1)
    return np.clip(img_float * (1 + omega_pd * np.sin(2 * np.pi * img_float)), 0, 1)

def simulate_fdm_soliton(img, fdm_mass):
    """FDM Soliton: ρ(r) = ρ₀/(1 + (r/r_c)²)²"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape[0], img.shape[1]
        gray = np.mean(img_float, axis=2)
    else:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape
        gray = img_float
    
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X**2 + Y**2)
    rc = 0.3 / np.sqrt(max(fdm_mass, 0.1))
    soliton = 1.0 / (1 + (r/rc)**2)**2
    soliton = soliton / soliton.max()
    
    if len(img.shape) == 3:
        soliton_3d = np.stack([soliton, soliton, soliton], axis=2)
        return np.clip(img_float * (1 + 0.5 * soliton_3d), 0, 1)
    return np.clip(img_float * (1 + 0.5 * soliton), 0, 1)

def pdp_interference(img, fringe_scale):
    """PDP Interference: I = I₀·sin(2πf x)·sin(2πf y)"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape[0], img.shape[1]
    else:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape
    
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x, y)
    interference = np.sin(2 * np.pi * fringe_scale * X / 20) * np.sin(2 * np.pi * fringe_scale * Y / 20)
    interference = (interference + 1) / 2
    
    if len(img.shape) == 3:
        interference_3d = np.stack([interference, interference, interference], axis=2)
        return np.clip(img_float * interference_3d, 0, 1)
    return np.clip(img_float * interference, 0, 1)

def dark_photon_conversion(img, kinetic_mixing, magnetar_eps):
    """Dark Photon: P_conv = exp(-2(1 - exp(-ε²/(2m_γ'²))))"""
    img_float = img.astype(np.float32) / 255.0
    conversion_prob = np.exp(-2 * (1 - np.exp(-magnetar_eps**2 / (2 * max(kinetic_mixing, 1e-12)**2))))
    return np.clip(img_float * conversion_prob, 0, 1)

def create_em_composite(img, f_nl, n_q):
    """EM Spectrum Composite with quantum corrections"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        img_gray = np.mean(img_float, axis=2)
    else:
        img_gray = img.astype(np.float32) / 255.0
    
    quantum_corr = 1 + f_nl * img_gray * (1 - img_gray) * n_q
    xray = img_gray ** 1.5 * quantum_corr
    visible = img_gray ** 0.8 * quantum_corr
    infrared = img_gray ** 0.5 * quantum_corr
    rgb = np.stack([infrared, visible, xray], axis=2)
    return np.clip(rgb, 0, 1)

def plot_magnetar_dipole_field(B0=1e15, epsilon=0.1):
    """Magnetar QED Plot"""
    B_crit = 4.414e13
    B_Bcrit = B0 / B_crit
    r_max = 10
    
    grid_size = 100
    x = np.linspace(-r_max, r_max, grid_size)
    y = np.linspace(-r_max, r_max, grid_size)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    R = np.maximum(R, 0.2)
    R0 = 1.0
    
    B_r = B0 * (R0/R)**3 * 2 * np.cos(theta)
    B_theta = B0 * (R0/R)**3 * np.sin(theta)
    Bx = B_r * np.cos(theta) - B_theta * np.sin(theta)
    By = B_r * np.sin(theta) + B_theta * np.cos(theta)
    
    QED_factor = np.exp(-2 * (B_Bcrit * (R0/R)**3)**2)
    dark_photon_prob = np.exp(-2 * (1 - np.exp(-(B_Bcrit * (R0/R)**3)**2 / (2 * max(epsilon, 1e-6)**2))))
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Field lines
    ax1 = axes[0, 0]
    skip = 2
    X_sub = X[::skip, ::skip]
    Y_sub = Y[::skip, ::skip]
    Bx_sub = Bx[::skip, ::skip]
    By_sub = By[::skip, ::skip]
    mag_sub = np.log10(np.sqrt(Bx_sub**2 + By_sub**2) + 1e-10)
    
    ax1.streamplot(X_sub, Y_sub, Bx_sub, By_sub, color=mag_sub, cmap='plasma', linewidth=1)
    ax1.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=1))
    ax1.set_xlim(-r_max, r_max)
    ax1.set_ylim(-r_max, r_max)
    ax1.set_aspect('equal')
    ax1.set_title(f'Magnetic Field Lines\nB₀ = {B0:.1e} G')
    ax1.grid(True, alpha=0.3)
    
    # QED Polarization
    ax2 = axes[0, 1]
    ax2.imshow(QED_factor, extent=[-r_max, r_max, -r_max, r_max], origin='lower', cmap='viridis')
    ax2.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=1))
    ax2.set_title('QED Vacuum Polarization\nP = exp[-2(B/B_crit)²]')
    ax2.grid(True, alpha=0.3)
    
    # Dark Photon
    ax3 = axes[1, 0]
    ax3.imshow(dark_photon_prob, extent=[-r_max, r_max, -r_max, r_max], origin='lower', cmap='inferno')
    ax3.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=1))
    ax3.set_title(f'Dark Photon Conversion\nε = {epsilon:.3f}')
    ax3.grid(True, alpha=0.3)
    
    # Radial Profiles
    ax4 = axes[1, 1]
    r = np.linspace(1.1, r_max, 100)
    B_radial = B0 * (R0/r)**3
    QED_radial = np.exp(-2 * (B_Bcrit * (R0/r)**3)**2)
    dark_radial = np.exp(-2 * (1 - np.exp(-(B_Bcrit * (R0/r)**3)**2 / (2 * epsilon**2))))
    
    ax4.semilogy(r, B_radial, 'b-', linewidth=2, label='|B|')
    ax4.set_xlabel('r / R_star')
    ax4.set_ylabel('|B| (G)', color='b')
    ax4.tick_params(axis='y', labelcolor='b')
    ax4.grid(True, alpha=0.3)
    
    ax4_twin = ax4.twinx()
    ax4_twin.plot(r, QED_radial, 'r--', linewidth=2, label='P_QED')
    ax4_twin.plot(r, dark_radial, 'g-.', linewidth=2, label='P_DM')
    ax4_twin.set_ylabel('Probability', color='r')
    ax4_twin.set_ylim([0, 1])
    
    ax4.set_title('Radial Profiles')
    ax4.legend(loc='upper right')
    
    plt.tight_layout()
    return fig

def get_download_link(img_array, filename, text):
    """Create download link"""
    if img_array.dtype != np.uint8:
        img_array = (img_array * 255).astype(np.uint8)
    img = Image.fromarray(img_array)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}" class="download-button">{text}</a>'

# ============ MAIN DISPLAY LOGIC ============
# Determine which image to use
if uploaded_file is not None:
    img = load_image(uploaded_file)
    st.success(f"✅ Loaded: {uploaded_file.name}")
elif preset_data:
    img = load_image(None)
    st.info("📁 Running with SGR 1806-20 simulation data")
else:
    # Default - show placeholder and wait for input
    img = None
    st.info("👈 Please upload an image or click 'Run with SGR 1806-20' to begin")
    st.markdown("""
    ### 🔭 QCAUS v1.0 Features
    
    - **FDM (Fuzzy Dark Matter)**: Soliton core simulations with ρ(r) = ρ₀/(1 + (r/r_c)²)²
    - **PDP (Phase-Dependent Polarization)**: Quantum entanglement effects with Ω_PD parameter
    - **Magnetar QED**: Dipole fields, QED vacuum polarization, dark photon conversion
    - **QCIS**: Quantum cosmological initial conditions (f_NL, n_q)
    - **EM Spectrum**: Multi-wavelength mapping with quantum signatures
    """)

# Only process if we have an image
if img is not None:
    # Calculate magnetar parameters
    B0 = 10**b0_log10
    B_crit = 4.414e13
    B_Bcrit = B0 / B_crit
    
    # Display magnetar summary
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡️ Surface B-field", f"{B0:.1e} G")
    with col2:
        st.metric("⚡ Critical field", f"{B_crit:.2e} G")
    with col3:
        st.metric("📊 B/B_crit", f"{B_Bcrit:.2e}")
    
    # Process all images
    img_norm = normalize_image(img.astype(np.float32) / 255.0)
    entangled = apply_pdp_entanglement(img, omega_pd)
    fdm_result = simulate_fdm_soliton(img, fdm_mass)
    interference = pdp_interference(img, fringe_scale)
    dark_photon = dark_photon_conversion(img, kinetic_mixing, magnetar_eps)
    em_composite = create_em_composite(img, f_nl, n_q)
    
    # BEFORE vs AFTER
    st.markdown("## Before vs After")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📷 Original Image")
        st.image(img_norm, use_container_width=True)
        st.markdown(get_download_link(img_norm, "original.png", "📥 Download"), unsafe_allow_html=True)
    with col2:
        st.markdown(f"### 🔮 PDP Entangled (Ω={omega_pd:.2f})")
        st.image(entangled, use_container_width=True)
        st.markdown(get_download_link(entangled, "entangled.png", "📥 Download"), unsafe_allow_html=True)
    
    # Annotated Physics Maps
    st.markdown("## 📊 Annotated Physics Maps")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚛️ FDM Soliton")
        st.markdown("*ρ(r) = ρ₀/(1 + (r/r_c)²)²*")
        st.image(fdm_result, use_container_width=True)
        st.markdown(get_download_link(fdm_result, "fdm.png", "📥 Download"), unsafe_allow_html=True)
    with col2:
        st.markdown("### 🌊 PDP Interference")
        st.markdown("*I = I₀·sin(2πf x)·sin(2πf y)*")
        st.image(interference, use_container_width=True)
        st.markdown(get_download_link(interference, "interference.png", "📥 Download"), unsafe_allow_html=True)
    
    # Dark Photon
    st.markdown("### 🕳️ Dark Photon Conversion")
    st.markdown("*P_conv = exp[-2(1 - exp(-ε²/(2m_γ'²)))]*")
    st.image(dark_photon, use_container_width=True)
    st.markdown(get_download_link(dark_photon, "dark_photon.png", "📥 Download"), unsafe_allow_html=True)
    
    # Magnetar QED Plot
    st.markdown("## ⚡ Magnetar QED — Dipole Field, QED Polarization, Dark Photon Conversion")
    try:
        fig = plot_magnetar_dipole_field(B0, magnetar_eps)
        st.pyplot(fig, use_container_width=True)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        b64 = base64.b64encode(buf.getvalue()).decode()
        st.markdown(f'<a href="data:image/png;base64,{b64}" download="magnetar_plot.png" class="download-button">📥 Download Plot</a>', unsafe_allow_html=True)
        plt.close(fig)
    except Exception as e:
        st.error(f"Plot error: {e}")
    
    # Magnetar Parameters
    st.markdown("### 📋 Magnetar Parameters")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Surface B-field", f"{B0:.1e} G")
    with col2:
        st.metric("Critical field", f"{B_crit:.2e} G")
    with col3:
        st.metric("B/B_crit", f"{B_Bcrit:.2e}")
    with col4:
        st.metric("Kinetic mixing ε", f"{magnetar_eps:.3f}")
    
    # EM Spectrum
    st.markdown("## 🌈 Electromagnetic Spectrum Mapping")
    st.markdown("*Infrared → Visible → X-ray | Dark Leakage = Equal & Opposite Quantum Signature*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎨 EM Spectrum Composite")
        st.markdown("*R = Infrared, G = Visible, B = X-ray*")
        st.image(em_composite, use_container_width=True)
        st.markdown(get_download_link(em_composite, "em_composite.png", "📥 Download"), unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 EM Spectrum Layers")
        img_gray = np.mean(img.astype(np.float32) / 255.0, axis=2) if len(img.shape) == 3 else img.astype(np.float32) / 255.0
        quantum_corr = 1 + f_nl * img_gray * (1 - img_gray) * n_q
        
        infrared = plt.cm.hot(img_gray ** 0.5 * quantum_corr)[:, :, :3]
        visible = plt.cm.viridis(img_gray ** 0.8 * quantum_corr)[:, :, :3]
        xray = plt.cm.plasma(img_gray ** 1.2 * quantum_corr)[:, :, :3]
        
        tab1, tab2, tab3 = st.tabs(["🔴 Infrared (Cold)", "🟢 Visible", "🔵 X-ray (Hot)"])
        with tab1:
            st.image(infrared, use_container_width=True)
            st.markdown("*λ ~ 10-1000 μm | Thermal dust emission*")
            st.markdown(get_download_link(infrared, "infrared.png", "📥 Download"), unsafe_allow_html=True)
        with tab2:
            st.image(visible, use_container_width=True)
            st.markdown("*λ ~ 400-700 nm | Stellar emission*")
            st.markdown(get_download_link(visible, "visible.png", "📥 Download"), unsafe_allow_html=True)
        with tab3:
            st.image(xray, use_container_width=True)
            st.markdown("*λ ~ 0.01-10 nm | Hot plasma emission*")
            st.markdown(get_download_link(xray, "xray.png", "📥 Download"), unsafe_allow_html=True)
    
    # Scientific Formulas
    st.markdown("---")
    st.markdown("""
    ### 📡 Scientific Formulas Implemented
    
    | Physics | Formula | Description |
    |---------|---------|-------------|
    | **PDP Entanglement** | $I_{ent} = I(1 + \\Omega_{PD}\\sin(2\\pi I))$ | Phase-dependent polarization entanglement |
    | **FDM Soliton** | $\\rho(r) = \\frac{\\rho_0}{(1 + (r/r_c)^2)^2}$ | Fuzzy Dark Matter soliton profile |
    | **QED Polarization** | $P_{QED} = e^{-2(B/B_{crit})^2}$ | Vacuum polarization in strong B-fields |
    | **Dark Photon** | $P_{conv} = e^{-2(1 - e^{-(B/B_{crit})^2/(2\\epsilon^2)})}$ | Dark photon to photon conversion |
    | **Magnetic Dipole** | $B(r) = B_0(R_{star}/r)^3$ | Dipole field scaling |
    """)

# Footer
st.markdown("---")
st.markdown("🔭 QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite")
