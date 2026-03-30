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
    .parameter-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
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
        type=['fits', 'fit', 'fz', 'jpg', 'jpeg', 'png'],
        help="Limit 200MB per file"
    )

# Helper function to normalize images
def normalize_image(img):
    """Normalize image to [0, 1] range for display"""
    if isinstance(img, np.ndarray):
        if img.dtype == np.float32 or img.dtype == np.float64:
            # Handle NaN and inf values
            img = np.nan_to_num(img, nan=0.0, posinf=1.0, neginf=0.0)
            # Clip to [0, 1] range
            img = np.clip(img, 0, 1)
        elif img.dtype == np.uint8:
            img = img / 255.0
        else:
            # For other integer types, normalize
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
        return np.array(img)
    else:
        # Create sample image for demonstration
        x = np.linspace(-5, 5, 512)
        y = np.linspace(-5, 5, 512)
        X, Y = np.meshgrid(x, y)
        # Create a simulated magnetar image
        R = np.sqrt(X**2 + Y**2)
        img = np.exp(-R**2 / 2) * np.cos(5*R) + 0.5 * np.exp(-(R-2)**2/0.5)
        img = np.clip(img, 0, 1)
        return (img * 255).astype(np.uint8)

# PDP entanglement function
def apply_pdp_entanglement(img, omega_pd):
    """Apply PDP entanglement effect"""
    img_float = img.astype(np.float32) / 255.0
    # Simulate quantum entanglement effect
    entangled = img_float * (1 + omega_pd * np.sin(2 * np.pi * img_float))
    return normalize_image(entangled)

# FDM soliton simulation
def simulate_fdm_soliton(img, fdm_mass, scale_kpc=1.0):
    """Simulate Fuzzy Dark Matter soliton"""
    img_float = img.astype(np.float32) / 255.0
    # Soliton profile: ~ 1/(1 + (r/rc)^2)
    x = np.linspace(-1, 1, img.shape[0])
    y = np.linspace(-1, 1, img.shape[1])
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X**2 + Y**2)
    rc = 1.0 / np.sqrt(fdm_mass)  # Core radius scales with mass
    soliton = 1.0 / (1 + (r/rc)**2)
    # Normalize
    soliton = soliton / soliton.max()
    # Apply to image
    result = img_float * soliton
    return normalize_image(result)

# PDP interference pattern
def pdp_interference(img, fringe_scale):
    """Generate PDP interference pattern"""
    img_float = img.astype(np.float32) / 255.0
    x = np.linspace(-1, 1, img.shape[0])
    y = np.linspace(-1, 1, img.shape[1])
    X, Y = np.meshgrid(x, y)
    interference = np.sin(2 * np.pi * fringe_scale * X) * np.sin(2 * np.pi * fringe_scale * Y)
    interference = (interference + 1) / 2  # Normalize to [0,1]
    result = img_float * interference
    return normalize_image(result)

# Dark photon conversion
def dark_photon_conversion(img, kinetic_mixing, magnetar_eps):
    """Simulate dark photon conversion"""
    img_float = img.astype(np.float32) / 255.0
    # Dark photon conversion probability
    conversion_prob = np.exp(-2 * (1 - np.exp(-magnetar_eps**2 / (2 * kinetic_mixing**2))))
    result = img_float * conversion_prob
    return normalize_image(result)

# Scientific magnetar plot
def plot_magnetar_dipole_field(B0=1e15, epsilon=0.1, r_max=10):
    """Create scientific magnetar dipole field plot with QED effects"""
    
    # Calculate parameters
    B_crit = 4.414e13
    B_Bcrit = B0 / B_crit
    
    # Create grid
    x = np.linspace(-r_max, r_max, 200)
    y = np.linspace(-r_max, r_max, 200)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    
    # Avoid division by zero
    R = np.maximum(R, 0.2)
    R0 = 1.0  # neutron star radius
    
    # Dipole field components
    B_r = B0 * (R0/R)**3 * 2 * np.cos(theta)
    B_theta = B0 * (R0/R)**3 * np.sin(theta)
    
    # Convert to Cartesian components
    Bx = B_r * np.cos(theta) - B_theta * np.sin(theta)
    By = B_r * np.sin(theta) + B_theta * np.cos(theta)
    
    # QED vacuum polarization effect
    QED_factor = np.exp(-2 * (B_Bcrit * (R0/R)**3)**2)
    
    # Dark photon conversion probability
    dark_photon_prob = np.exp(-2 * (1 - np.exp(-(B_Bcrit * (R0/R)**3)**2 / (2 * epsilon**2))))
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), dpi=100)
    
    # 1. Magnetic field lines
    ax1 = axes[0, 0]
    magnitude = np.sqrt(Bx**2 + By**2)
    # Avoid log of zero
    log_magnitude = np.log10(np.maximum(magnitude, 1e-10))
    
    # Create streamplot with proper scaling
    skip = 3
    X_sub = X[::skip, ::skip]
    Y_sub = Y[::skip, ::skip]
    Bx_sub = Bx[::skip, ::skip]
    By_sub = By[::skip, ::skip]
    
    stream = ax1.streamplot(X_sub, Y_sub, Bx_sub, By_sub, 
                           color=np.log10(np.sqrt(Bx_sub**2 + By_sub**2) + 1e-10),
                           cmap='plasma', linewidth=1, density=1.2)
    
    # Add neutron star
    ax1.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=2))
    ax1.set_xlim(-r_max, r_max)
    ax1.set_ylim(-r_max, r_max)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x / R_star', fontsize=12)
    ax1.set_ylabel('y / R_star', fontsize=12)
    ax1.set_title(f'Magnetic Field Lines\nB₀ = {B0:.1e} G', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 2. QED Polarization effect
    ax2 = axes[0, 1]
    im2 = ax2.imshow(QED_factor, extent=[-r_max, r_max, -r_max, r_max], 
                     origin='lower', cmap='viridis', aspect='auto')
    ax2.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=2))
    ax2.set_xlabel('x / R_star', fontsize=12)
    ax2.set_ylabel('y / R_star', fontsize=12)
    ax2.set_title('QED Vacuum Polarization\nP = exp[-2(B/B_crit)²]', fontsize=14, fontweight='bold')
    cbar2 = plt.colorbar(im2, ax=ax2)
    cbar2.set_label('Polarization Factor', fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # 3. Dark photon conversion probability
    ax3 = axes[1, 0]
    im3 = ax3.imshow(dark_photon_prob, extent=[-r_max, r_max, -r_max, r_max],
                     origin='lower', cmap='inferno', aspect='auto')
    ax3.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=2))
    ax3.set_xlabel('x / R_star', fontsize=12)
    ax3.set_ylabel('y / R_star', fontsize=12)
    ax3.set_title(f'Dark Photon Conversion\nε = {epsilon:.3f}', fontsize=14, fontweight='bold')
    cbar3 = plt.colorbar(im3, ax=ax3)
    cbar3.set_label('Conversion Probability', fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # 4. Radial profiles
    ax4 = axes[1, 1]
    r = np.linspace(1.1, r_max, 100)
    B_radial = B0 * (R0/r)**3
    QED_radial = np.exp(-2 * (B_Bcrit * (R0/r)**3)**2)
    dark_radial = np.exp(-2 * (1 - np.exp(-(B_Bcrit * (R0/r)**3)**2 / (2 * epsilon**2))))
    
    # Avoid numerical issues
    B_radial = np.maximum(B_radial, 1e-20)
    
    ax4.semilogy(r, B_radial, 'b-', linewidth=2.5, label='Magnetic Field')
    ax4.set_xlabel('r / R_star', fontsize=12)
    ax4.set_ylabel('|B| (G)', fontsize=12, color='b')
    ax4.tick_params(axis='y', labelcolor='b')
    ax4.set_xlim([1, r_max])
    ax4.grid(True, alpha=0.3)
    
    ax4_twin = ax4.twinx()
    ax4_twin.plot(r, QED_radial, 'r--', linewidth=2, label='QED Factor')
    ax4_twin.plot(r, dark_radial, 'g-.', linewidth=2, label='Dark Photon')
    ax4_twin.set_ylabel('Probability', fontsize=12, color='r')
    ax4_twin.tick_params(axis='y', labelcolor='r')
    ax4_twin.set_ylim([0, 1.05])
    
    ax4.set_title('Radial Profiles', fontsize=14, fontweight='bold')
    
    # Add legend
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc='best', fontsize=10)
    
    plt.tight_layout()
    return fig

# Create electromagnetic spectrum mapping
def create_em_composite(img):
    """Create EM spectrum composite (R=X-ray, G=Visible, B=IR)"""
    img_float = img.astype(np.float32) / 255.0
    
    # Simulate different spectral bands
    xray = img_float ** 1.5  # X-ray: harder contrast
    visible = img_float ** 0.8  # Visible: natural
    infrared = img_float ** 0.5  # Infrared: brighter
    
    # Create RGB composite
    composite = np.stack([xray, visible, infrared], axis=2)
    return normalize_image(composite)

# Main processing
if uploaded_file is not None or preset_data:
    if uploaded_file is not None:
        img = load_image(uploaded_file)
        st.info(f"Source: {uploaded_file.name} | Instrument: IMAGE")
    else:
        img = load_image(None)
        st.info("Source: SGR 1806-20 (simulated) | Instrument: IMAGE")
    
    # Calculate B/B_crit
    B0 = 10**b0_log10
    B_crit = 4.414e13
    B_Bcrit = B0 / B_crit
    
    # Display magnetar parameters
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Surface B-field", f"{B0:.1e} G", f"{B0:.1e} G")
    with col2:
        st.metric("Critical field", f"{B_crit:.2e} G")
    with col3:
        st.metric("B/B_crit", f"{B_Bcrit:.2e}")
    
    # Process images with error handling
    st.markdown("## Before vs After")
    
    # Create two columns for before/after
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Original")
        img_normalized = normalize_image(img.astype(np.float32) / 255.0)
        st.image(img_normalized, caption="Original Image", use_container_width=True, clamp=True)
    
    with col2:
        st.markdown(f"### PDP Entangled (Ω={omega_pd:.2f})")
        entangled = apply_pdp_entanglement(img, omega_pd)
        st.image(entangled, caption=f"PDP Entangled", use_container_width=True, clamp=True)
    
    # Annotated Physics Maps
    st.markdown("## Annotated Physics Maps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### FDM Soliton")
        fdm_result = simulate_fdm_soliton(img, fdm_mass)
        st.image(fdm_result, caption=f"FDM Soliton (m={fdm_mass:.2f}×10⁻²² eV)", 
                use_container_width=True, clamp=True)
    
    with col2:
        st.markdown("### PDP Interference")
        interference = pdp_interference(img, fringe_scale)
        st.image(interference, caption=f"PDP Interference (scale={fringe_scale} px)", 
                use_container_width=True, clamp=True)
    
    # Dark photon conversion
    st.markdown("### Dark Photon Conversion")
    dark_photon = dark_photon_conversion(img, kinetic_mixing, magnetar_eps)
    st.image(dark_photon, caption=f"Dark Photon Conversion (ε={kinetic_mixing:.1e})", 
            use_container_width=True, clamp=True)
    
    # Magnetar QED Plot
    st.markdown("## ⚡ Magnetar QED — Dipole Field, QED Polarization, Dark Photon Conversion")
    
    try:
        fig = plot_magnetar_dipole_field(B0=B0, epsilon=magnetar_eps)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        st.error(f"Magnetar plot error: {str(e)}")
        st.info("Please check parameter ranges and try again")
    
    # Magnetar parameters card
    st.markdown("### Magnetar Parameters")
    param_col1, param_col2, param_col3, param_col4 = st.columns(4)
    with param_col1:
        st.metric("Surface B-field", f"{B0:.1e} G", f"({B0:.1e} G)")
    with param_col2:
        st.metric("Critical field", f"{B_crit:.2e} G")
    with param_col3:
        st.metric("B/B_crit", f"{B_Bcrit:.2e}")
    with param_col4:
        st.metric("Kinetic mixing ε", f"{magnetar_eps:.3f}")
    
    # EM Spectrum Mapping
    st.markdown("## 🌈 Electromagnetic Spectrum Mapping")
    st.markdown("*Infrared → Visible → X-ray | Dark Leakage = Equal & Opposite Quantum Signature*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### EM Spectrum Composite (R=X-ray, G=Visible, B=IR)")
        composite = create_em_composite(img)
        st.image(composite, caption="EM Spectrum Composite", use_container_width=True, clamp=True)
    
    with col2:
        st.markdown("### EM Spectrum Layers")
        
        # Create individual spectrum layers
        img_float = img.astype(np.float32) / 255.0
        infrared_layer = normalize_image(img_float ** 0.5)
        visible_layer = normalize_image(img_float ** 0.8)
        xray_layer = normalize_image(img_float ** 1.5)
        
        # Create tabs for different layers
        tab1, tab2, tab3 = st.tabs(["Infrared (Cold)", "Visible", "X-ray (Hot)"])
        
        with tab1:
            st.image(infrared_layer, caption="Infrared (Cold)\nLong wavelength | Thermal emission", 
                    use_container_width=True, clamp=True)
        with tab2:
            st.image(visible_layer, caption="Visible (Human Eye)", 
                    use_container_width=True, clamp=True)
        with tab3:
            st.image(xray_layer, caption="X-ray (Hot)\nShort wavelength | High energy", 
                    use_container_width=True, clamp=True)
    
else:
    st.info("👈 Please upload an image or click 'Run with SGR 1806-20' to begin")
    st.markdown("""
    ### Features:
    - **FDM (Fuzzy Dark Matter)**: Soliton core simulations
    - **PDP (Phase-Dependent Polarization)**: Quantum entanglement effects
    - **Magnetar QED**: Dipole field, QED polarization, dark photon conversion
    - **QCIS**: Quantum cosmological initial conditions
    - **EM Spectrum**: Multi-wavelength mapping
    """)

# Footer
st.markdown("---")
st.markdown("🔭 QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite")
