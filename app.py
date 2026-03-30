import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
import io
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="QCAUS v1.0 - Quantum Cosmology & Astrophysics Unified Suite",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .download-button {
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🔭 QCAUS v1.0</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center">FDM · PDP · Magnetar · QCIS · EM Spectrum</div>', unsafe_allow_html=True)

# Sidebar for parameters
with st.sidebar:
    st.markdown("## ⚛️ Core Physics")
    
    omega_pd = st.slider("Omega_PD Entanglement", 0.05, 0.50, 0.20, 0.01, 
                         help="Phase-dependent polarization entanglement parameter")
    fringe_scale = st.slider("Fringe Scale (pixels)", 10, 80, 45, 1,
                             help="Interference fringe scale in pixels")
    kinetic_mixing = st.slider("Kinetic Mixing eps", 1e-12, 1e-8, 1e-10, format="%.1e",
                               help="Dark photon kinetic mixing parameter")
    fdm_mass = st.slider("FDM Mass x10^-22 eV", 0.10, 10.00, 1.00, 0.01,
                         help="Fuzzy Dark Matter particle mass")
    
    st.markdown("---")
    st.markdown("## 🌟 Magnetar")
    
    b0_log10 = st.slider("B0 log10 G", 13.0, 16.0, 15.0, 0.1,
                         help="Surface magnetic field strength (log10 Gauss)")
    magnetar_eps = st.slider("Magnetar eps", 0.01, 0.50, 0.10, 0.01,
                             help="Magnetar coupling parameter")
    
    st.markdown("---")
    st.markdown("## 📈 QCIS")
    
    f_nl = st.slider("f_NL", 0.00, 5.00, 0.00, 0.01,
                     help="Non-Gaussianity parameter")
    n_q = st.slider("n_q", 0.00, 2.00, 0.00, 0.01,
                    help="Quantum spectral index")
    
    st.markdown("---")
    st.markdown("**Tony Ford | tlcagford@gmail.com | Patent Pending | 2026**")

# Helper function to create download button
def get_image_download_link(img_array, filename, caption):
    """Generate a download link for an image"""
    if img_array.dtype != np.uint8:
        img_array = (img_array * 255).astype(np.uint8)
    
    img = Image.fromarray(img_array)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    
    b64 = base64.b64encode(byte_im).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}" class="download-button">{caption}</a>'
    return href

# Helper function to normalize images
def normalize_image(img):
    """Normalize image to [0, 1] range for display"""
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

# Load and process image
def load_image(file):
    """Load image from uploaded file or preset"""
    if file is not None:
        img = Image.open(file)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        return np.array(img)
    else:
        # Create realistic magnetar nebula simulation
        size = 512
        x = np.linspace(-5, 5, size)
        y = np.linspace(-5, 5, size)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        theta = np.arctan2(Y, X)
        
        # Magnetar wind nebula simulation
        img = np.exp(-R**2 / 6) * (1 + 0.4 * np.cos(6*R - 2*theta))
        img += 0.15 * np.exp(-((R-2.5)**2)/0.5) * (1 + np.cos(8*theta))
        img += 0.1 * np.random.randn(size, size) * 0.05
        img = np.clip(img, 0, 1)
        
        img_rgb = np.stack([img, img*0.8, img*0.6], axis=2)
        return (img_rgb * 255).astype(np.uint8)

# PDP entanglement - REAL FORMULA
def apply_pdp_entanglement(img, omega_pd):
    """
    Phase-Dependent Polarization Entanglement
    Formula: I_entangled = I * (1 + Ω_PD * sin(2πI))
    Where Ω_PD is the entanglement parameter
    """
    img_float = img.astype(np.float32) / 255.0
    
    if len(img.shape) == 3:
        # Convert to grayscale for phase calculation
        gray = np.mean(img_float, axis=2, keepdims=True)
        # Apply entanglement formula
        phase_factor = 1 + omega_pd * np.sin(2 * np.pi * gray)
        entangled = img_float * phase_factor
    else:
        entangled = img_float * (1 + omega_pd * np.sin(2 * np.pi * img_float))
    
    return normalize_image(entangled)

# FDM soliton - REAL FORMULA
def simulate_fdm_soliton(img, fdm_mass):
    """
    Fuzzy Dark Matter Soliton Profile
    Formula: ρ(r) = ρ0 / (1 + (r/rc)^2)^2
    Core radius: rc ∝ 1/√(m_FDM)
    """
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape[0], img.shape[1]
        # Convert to grayscale
        gray = np.mean(img_float, axis=2)
    else:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape
        gray = img_float
    
    # Create coordinate grid
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X**2 + Y**2)
    
    # Soliton profile: ρ(r) = ρ0 / (1 + (r/rc)^2)^2
    rc = 0.3 / np.sqrt(max(fdm_mass, 0.1))  # Core radius in normalized units
    soliton = 1.0 / (1 + (r/rc)**2)**2
    
    # Normalize soliton profile
    soliton = soliton / soliton.max()
    
    # Apply soliton modulation (gravitational lensing effect)
    if len(img.shape) == 3:
        soliton_3d = np.stack([soliton, soliton, soliton], axis=2)
        result = img_float * (1 + 0.5 * soliton_3d)
    else:
        result = img_float * (1 + 0.5 * soliton)
    
    return normalize_image(result)

# PDP Interference - REAL FORMULA
def pdp_interference(img, fringe_scale):
    """
    Phase-Dependent Polarization Interference Pattern
    Formula: I_interference = I * sin(2πfringe_scale * x/20) * sin(2πfringe_scale * y/20)
    """
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape[0], img.shape[1]
    else:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape
    
    # Create coordinate grid
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x, y)
    
    # Generate interference pattern
    interference = np.sin(2 * np.pi * fringe_scale * X / 20) * \
                   np.sin(2 * np.pi * fringe_scale * Y / 20)
    interference = (interference + 1) / 2  # Normalize to [0,1]
    
    # Apply interference modulation
    if len(img.shape) == 3:
        interference_3d = np.stack([interference, interference, interference], axis=2)
        result = img_float * interference_3d
    else:
        result = img_float * interference
    
    return normalize_image(result)

# Dark Photon Conversion - REAL FORMULA
def dark_photon_conversion(img, kinetic_mixing, magnetar_eps):
    """
    Dark Photon Conversion Probability
    Formula: P_conv = exp(-2 * (1 - exp(-ε^2 / (2 * m_γ'^2))))
    Where ε is kinetic mixing, m_γ' is dark photon mass
    """
    img_float = img.astype(np.float32) / 255.0
    
    # Conversion probability from dark photon to photon
    # P_conv = exp(-2 * (1 - exp(-ε^2 / (2 * μ^2))))
    # where μ = m_γ'/m_pl
    conversion_prob = np.exp(-2 * (1 - np.exp(-magnetar_eps**2 / (2 * max(kinetic_mixing, 1e-12)**2))))
    
    result = img_float * conversion_prob
    return normalize_image(result)

# Scientific magnetar plot with REAL QED formulas
def plot_magnetar_dipole_field(B0=1e15, epsilon=0.1, r_max=10):
    """
    Magnetar Dipole Field with QED Effects
    Formulas:
    - Dipole field: B(r) = B0 * (R_star/r)^3
    - QED polarization: P_QED = exp(-2(B/B_crit)^2)
    - Dark photon conversion: P_DM = exp(-2(1 - exp(-(B/B_crit)^2/(2ε^2))))
    """
    B_crit = 4.414e13  # QED critical field
    B_Bcrit = B0 / B_crit
    
    # Create grid
    grid_size = 150
    x = np.linspace(-r_max, r_max, grid_size)
    y = np.linspace(-r_max, r_max, grid_size)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    
    R = np.maximum(R, 0.2)
    R0 = 1.0
    
    # Dipole field: B = B0 * (R0/R)^3 * (2cosθ r̂ + sinθ θ̂)
    B_r = B0 * (R0/R)**3 * 2 * np.cos(theta)
    B_theta = B0 * (R0/R)**3 * np.sin(theta)
    
    Bx = B_r * np.cos(theta) - B_theta * np.sin(theta)
    By = B_r * np.sin(theta) + B_theta * np.cos(theta)
    
    # QED Vacuum Polarization: P = exp(-2(B/B_crit)^2)
    QED_factor = np.exp(-2 * (B_Bcrit * (R0/R)**3)**2)
    
    # Dark Photon Conversion: P = exp(-2(1 - exp(-(B/B_crit)^2/(2ε^2))))
    dark_photon_prob = np.exp(-2 * (1 - np.exp(-(B_Bcrit * (R0/R)**3)**2 / (2 * max(epsilon, 1e-6)**2))))
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), dpi=100)
    
    # 1. Magnetic field lines
    ax1 = axes[0, 0]
    skip = 3
    X_sub = X[::skip, ::skip]
    Y_sub = Y[::skip, ::skip]
    Bx_sub = Bx[::skip, ::skip]
    By_sub = By[::skip, ::skip]
    mag_sub = np.log10(np.sqrt(Bx_sub**2 + By_sub**2) + 1e-10)
    
    ax1.streamplot(X_sub, Y_sub, Bx_sub, By_sub, 
                   color=mag_sub, cmap='plasma', linewidth=1.2, density=1.2)
    ax1.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=2))
    ax1.set_xlim(-r_max, r_max)
    ax1.set_ylim(-r_max, r_max)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x / R_star', fontsize=12)
    ax1.set_ylabel('y / R_star', fontsize=12)
    ax1.set_title(f'Magnetic Dipole Field\nB₀ = {B0:.1e} G', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=mag_sub.min(), vmax=mag_sub.max()))
    sm.set_array([])
    plt.colorbar(sm, ax=ax1, label='log₁₀|B| (G)')
    
    # 2. QED Polarization
    ax2 = axes[0, 1]
    im2 = ax2.imshow(QED_factor, extent=[-r_max, r_max, -r_max, r_max], 
                     origin='lower', cmap='viridis', aspect='auto')
    ax2.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=2))
    ax2.set_xlabel('x / R_star', fontsize=12)
    ax2.set_ylabel('y / R_star', fontsize=12)
    ax2.set_title('QED Vacuum Polarization\nP = exp[-2(B/B_crit)²]', fontsize=14, fontweight='bold')
    plt.colorbar(im2, ax=ax2, label='Polarization Factor')
    ax2.grid(True, alpha=0.3)
    
    # 3. Dark Photon Conversion
    ax3 = axes[1, 0]
    im3 = ax3.imshow(dark_photon_prob, extent=[-r_max, r_max, -r_max, r_max],
                     origin='lower', cmap='inferno', aspect='auto')
    ax3.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=2))
    ax3.set_xlabel('x / R_star', fontsize=12)
    ax3.set_ylabel('y / R_star', fontsize=12)
    ax3.set_title(f'Dark Photon Conversion\nP = exp[-2(1 - exp(-(B/B_crit)²/(2ε²)))]\nε = {epsilon:.3f}', 
                  fontsize=14, fontweight='bold')
    plt.colorbar(im3, ax=ax3, label='Conversion Probability')
    ax3.grid(True, alpha=0.3)
    
    # 4. Radial Profiles
    ax4 = axes[1, 1]
    r = np.linspace(1.1, r_max, 100)
    B_radial = B0 * (R0/r)**3
    QED_radial = np.exp(-2 * (B_Bcrit * (R0/r)**3)**2)
    dark_radial = np.exp(-2 * (1 - np.exp(-(B_Bcrit * (R0/r)**3)**2 / (2 * epsilon**2))))
    
    B_radial = np.maximum(B_radial, 1e-20)
    
    ax4.semilogy(r, B_radial, 'b-', linewidth=2.5, label='|B| = B₀(R_star/r)³')
    ax4.set_xlabel('r / R_star', fontsize=12)
    ax4.set_ylabel('|B| (G)', fontsize=12, color='b')
    ax4.tick_params(axis='y', labelcolor='b')
    ax4.set_xlim([1, r_max])
    ax4.grid(True, alpha=0.3)
    
    ax4_twin = ax4.twinx()
    ax4_twin.plot(r, QED_radial, 'r--', linewidth=2, label='P_QED = exp[-2(B/B_crit)²]')
    ax4_twin.plot(r, dark_radial, 'g-.', linewidth=2, label='P_DM = exp[-2(1 - exp(-(B/B_crit)²/(2ε²)))]')
    ax4_twin.set_ylabel('Probability', fontsize=12, color='r')
    ax4_twin.tick_params(axis='y', labelcolor='r')
    ax4_twin.set_ylim([0, 1.05])
    
    ax4.set_title('Radial Profiles', fontsize=14, fontweight='bold')
    ax4.legend(loc='upper right', fontsize=9)
    ax4_twin.legend(loc='lower left', fontsize=9)
    
    plt.tight_layout()
    return fig

# EM Spectrum with REAL physics
def create_em_composite(img, f_nl, n_q):
    """
    Electromagnetic Spectrum Composite with Quantum Signatures
    Different spectral bands reveal different physical processes
    """
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        img_gray = np.mean(img_float, axis=2)
    else:
        img_gray = img.astype(np.float32) / 255.0
    
    # Apply quantum corrections
    quantum_corr = 1 + f_nl * img_gray * (1 - img_gray) * n_q
    
    # X-ray: Hot plasma (high energy)
    xray = img_gray ** 1.5 * quantum_corr
    
    # Visible: Stellar emission
    visible = img_gray ** 0.8 * quantum_corr
    
    # Infrared: Dust emission (low energy)
    infrared = img_gray ** 0.5 * quantum_corr
    
    # RGB composite (R=IR, G=Visible, B=X-ray)
    rgb = np.stack([infrared, visible, xray], axis=2)
    
    return normalize_image(rgb)

# Main processing
if uploaded_file is not None or preset_data:
    # Load image
    if uploaded_file is not None:
        img = load_image(uploaded_file)
        st.info(f"📁 Source: {uploaded_file.name} | Instrument: IMAGE")
    else:
        img = load_image(None)
        st.info("📁 Source: SGR 1806-20 (simulated magnetar nebula) | Instrument: IMAGE")
    
    # Calculate magnetar parameters
    B0 = 10**b0_log10
    B_crit = 4.414e13
    B_Bcrit = B0 / B_crit
    
    # Display magnetar parameters
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌡️ Surface B-field", f"{B0:.1e} G")
    with col2:
        st.metric("⚡ Critical field", f"{B_crit:.2e} G")
    with col3:
        st.metric("📊 B/B_crit", f"{B_Bcrit:.2e}")
    
    # BEFORE vs AFTER - Side by side with download buttons
    st.markdown("## Before vs After")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📷 Original Image")
        img_normalized = normalize_image(img.astype(np.float32) / 255.0)
        st.image(img_normalized, use_container_width=True)
        
        # Download button for original
        img_uint8 = (img_normalized * 255).astype(np.uint8)
        st.markdown(get_image_download_link(img_uint8, "original_image.png", "📥 Download Original"), 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### 🔮 PDP Entangled (Ω={omega_pd:.2f})")
        entangled = apply_pdp_entanglement(img, omega_pd)
        st.image(entangled, use_container_width=True)
        
        # Download button for entangled
        entangled_uint8 = (entangled * 255).astype(np.uint8)
        st.markdown(get_image_download_link(entangled_uint8, "pdp_entangled.png", "📥 Download PDP Entangled"), 
                   unsafe_allow_html=True)
    
    # Annotated Physics Maps - Side by side with download buttons
    st.markdown("## 📊 Annotated Physics Maps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚛️ FDM Soliton")
        st.markdown("*ρ(r) = ρ₀/(1 + (r/r_c)²)²*")
        fdm_result = simulate_fdm_soliton(img, fdm_mass)
        st.image(fdm_result, use_container_width=True)
        
        fdm_uint8 = (fdm_result * 255).astype(np.uint8)
        st.markdown(get_image_download_link(fdm_uint8, "fdm_soliton.png", "📥 Download FDM Soliton"), 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🌊 PDP Interference")
        st.markdown("*I = I₀·sin(2πf x)·sin(2πf y)*")
        interference = pdp_interference(img, fringe_scale)
        st.image(interference, use_container_width=True)
        
        interference_uint8 = (interference * 255).astype(np.uint8)
        st.markdown(get_image_download_link(interference_uint8, "pdp_interference.png", "📥 Download PDP Interference"), 
                   unsafe_allow_html=True)
    
    # Dark Photon Conversion
    st.markdown("### 🕳️ Dark Photon Conversion")
    st.markdown("*P_conv = exp[-2(1 - exp(-ε²/(2m_γ'²)))]*")
    dark_photon = dark_photon_conversion(img, kinetic_mixing, magnetar_eps)
    st.image(dark_photon, use_container_width=True)
    
    dark_photon_uint8 = (dark_photon * 255).astype(np.uint8)
    st.markdown(get_image_download_link(dark_photon_uint8, "dark_photon_conversion.png", "📥 Download Dark Photon Map"), 
               unsafe_allow_html=True)
    
    # Magnetar QED Plot
    st.markdown("## ⚡ Magnetar QED — Dipole Field, QED Polarization, Dark Photon Conversion")
    
    try:
        fig = plot_magnetar_dipole_field(B0=B0, epsilon=magnetar_eps)
        st.pyplot(fig)
        
        # Save and download magnetar plot
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode()
        st.markdown(f'<a href="data:image/png;base64,{b64}" download="magnetar_qed_plot.png">📥 Download Magnetar QED Plot</a>', 
                   unsafe_allow_html=True)
        plt.close(fig)
    except Exception as e:
        st.error(f"Magnetar plot error: {str(e)}")
    
    # Magnetar parameters
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
    
    # EM Spectrum Mapping
    st.markdown("## 🌈 Electromagnetic Spectrum Mapping")
    st.markdown("*Infrared → Visible → X-ray | Dark Leakage = Equal & Opposite Quantum Signature*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 EM Spectrum Composite")
        st.markdown("*R = Infrared, G = Visible, B = X-ray*")
        em_composite = create_em_composite(img, f_nl, n_q)
        st.image(em_composite, use_container_width=True)
        
        em_uint8 = (em_composite * 255).astype(np.uint8)
        st.markdown(get_image_download_link(em_uint8, "em_composite.png", "📥 Download EM Composite"), 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 EM Spectrum Layers")
        
        if len(img.shape) == 3:
            img_gray = np.mean(img.astype(np.float32) / 255.0, axis=2)
        else:
            img_gray = img.astype(np.float32) / 255.0
        
        # Apply quantum corrections from QCIS
        quantum_corr = 1 + f_nl * img_gray * (1 - img_gray) * n_q
        
        # Create colored layers with physics-based scaling
        infrared = plt.cm.hot(img_gray ** 0.5 * quantum_corr)[:, :, :3]
        visible = plt.cm.viridis(img_gray ** 0.8 * quantum_corr)[:, :, :3]
        xray = plt.cm.plasma(img_gray ** 1.2 * quantum_corr)[:, :, :3]
        
        tab1, tab2, tab3 = st.tabs(["🔴 Infrared (Cold)", "🟢 Visible", "🔵 X-ray (Hot)"])
        
        with tab1:
            st.image(infrared, use_container_width=True)
            st.markdown("*λ ~ 10-1000 μm | Thermal dust emission*")
            ir_uint8 = (infrared * 255).astype(np.uint8)
            st.markdown(get_image_download_link(ir_uint8, "infrared_layer.png", "📥 Download IR Layer"), 
                       unsafe_allow_html=True)
        
        with tab2:
            st.image(visible, use_container_width=True)
            st.markdown("*λ ~ 400-700 nm | Stellar emission*")
            vis_uint8 = (visible * 255).astype(np.uint8)
            st.markdown(get_image_download_link(vis_uint8, "visible_layer.png", "📥 Download Visible Layer"), 
                       unsafe_allow_html=True)
        
        with tab3:
            st.image(xray, use_container_width=True)
            st.markdown("*λ ~ 0.01-10 nm | Hot plasma emission*")
            xray_uint8 = (xray * 255).astype(np.uint8)
            st.markdown(get_image_download_link(xray_uint8, "xray_layer.png", "📥 Download X-ray Layer"), 
                       unsafe_allow_html=True)
    
    # Scientific explanation
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
    
else:
    st.info("👈 Please upload an image or click 'Run with SGR 1806-20' to begin")
    st.markdown("""
    ### 🔭 QCAUS v1.0 Features
    
    - **FDM (Fuzzy Dark Matter)**: Soliton core simulations with ρ(r) = ρ₀/(1 + (r/r_c)²)²
    - **PDP (Phase-Dependent Polarization)**: Quantum entanglement effects with Ω_PD parameter
    - **Magnetar QED**: Dipole fields, QED vacuum polarization, dark photon conversion
    - **QCIS**: Quantum cosmological initial conditions (f_NL, n_q)
    - **EM Spectrum**: Multi-wavelength mapping with quantum signatures
    """)

# Footer
st.markdown("---")
st.markdown("🔭 QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite")
