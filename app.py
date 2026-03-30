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
    .stMetric {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.5rem;
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
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        return np.array(img)
    else:
        # Create sample image for demonstration
        size = 512
        x = np.linspace(-5, 5, size)
        y = np.linspace(-5, 5, size)
        X, Y = np.meshgrid(x, y)
        # Create a simulated magnetar image
        R = np.sqrt(X**2 + Y**2)
        # Simulated emission with rings and central peak
        img = np.exp(-R**2 / 8) * (1 + 0.3 * np.cos(8*R))
        # Add some structure
        img += 0.1 * np.sin(5*X) * np.sin(5*Y)
        img = np.clip(img, 0, 1)
        # Convert to RGB by repeating
        img_rgb = np.stack([img, img, img], axis=2)
        return (img_rgb * 255).astype(np.uint8)

# PDP entanglement function
def apply_pdp_entanglement(img, omega_pd):
    """Apply PDP entanglement effect"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        # Apply to each channel
        entangled = img_float * (1 + omega_pd * np.sin(2 * np.pi * img_float.mean(axis=2, keepdims=True)))
    else:
        img_float = img.astype(np.float32) / 255.0
        entangled = img_float * (1 + omega_pd * np.sin(2 * np.pi * img_float))
    return normalize_image(entangled)

# FDM soliton simulation - FIXED VERSION
def simulate_fdm_soliton(img, fdm_mass, scale_kpc=1.0):
    """Simulate Fuzzy Dark Matter soliton"""
    # Convert to float and handle RGB
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        # Create soliton pattern with same dimensions as image
        h, w = img.shape[0], img.shape[1]
    else:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape
    
    # Create coordinate grid matching image dimensions
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X**2 + Y**2)
    
    # Soliton profile: ~ 1/(1 + (r/rc)^2) with core radius scaling with mass
    rc = 0.5 / np.sqrt(max(fdm_mass, 0.1))  # Core radius scales inversely with sqrt(mass)
    soliton = 1.0 / (1 + (r/rc)**2)
    # Normalize soliton to [0, 1]
    soliton = (soliton - soliton.min()) / (soliton.max() - soliton.min())
    
    # Apply soliton modulation
    if len(img.shape) == 3:
        # Expand soliton to 3D for RGB multiplication
        soliton_3d = np.stack([soliton, soliton, soliton], axis=2)
        result = img_float * soliton_3d
    else:
        result = img_float * soliton
    
    return normalize_image(result)

# PDP interference pattern - FIXED VERSION
def pdp_interference(img, fringe_scale):
    """Generate PDP interference pattern"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape[0], img.shape[1]
    else:
        img_float = img.astype(np.float32) / 255.0
        h, w = img.shape
    
    # Create coordinate grid matching image dimensions
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    X, Y = np.meshgrid(x, y)
    
    # Generate interference pattern
    interference = np.sin(2 * np.pi * fringe_scale * X / 20) * np.sin(2 * np.pi * fringe_scale * Y / 20)
    interference = (interference + 1) / 2  # Normalize to [0,1]
    
    # Apply interference
    if len(img.shape) == 3:
        interference_3d = np.stack([interference, interference, interference], axis=2)
        result = img_float * interference_3d
    else:
        result = img_float * interference
    
    return normalize_image(result)

# Dark photon conversion - FIXED VERSION
def dark_photon_conversion(img, kinetic_mixing, magnetar_eps):
    """Simulate dark photon conversion"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
    else:
        img_float = img.astype(np.float32) / 255.0
    
    # Dark photon conversion probability
    conversion_prob = np.exp(-2 * (1 - np.exp(-magnetar_eps**2 / (2 * max(kinetic_mixing, 1e-12)**2))))
    
    # Apply conversion
    result = img_float * conversion_prob
    return normalize_image(result)

# Scientific magnetar plot - FIXED VERSION
def plot_magnetar_dipole_field(B0=1e15, epsilon=0.1, r_max=10):
    """Create scientific magnetar dipole field plot with QED effects"""
    
    # Calculate parameters
    B_crit = 4.414e13
    B_Bcrit = B0 / B_crit
    
    # Create grid
    grid_size = 150
    x = np.linspace(-r_max, r_max, grid_size)
    y = np.linspace(-r_max, r_max, grid_size)
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
    dark_photon_prob = np.exp(-2 * (1 - np.exp(-(B_Bcrit * (R0/R)**3)**2 / (2 * max(epsilon, 1e-6)**2))))
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), dpi=100)
    
    # 1. Magnetic field lines
    ax1 = axes[0, 0]
    magnitude = np.sqrt(Bx**2 + By**2)
    
    # Create streamplot with proper scaling
    skip = 3
    X_sub = X[::skip, ::skip]
    Y_sub = Y[::skip, ::skip]
    Bx_sub = Bx[::skip, ::skip]
    By_sub = By[::skip, ::skip]
    mag_sub = np.log10(np.sqrt(Bx_sub**2 + By_sub**2) + 1e-10)
    
    stream = ax1.streamplot(X_sub, Y_sub, Bx_sub, By_sub, 
                           color=mag_sub,
                           cmap='plasma', linewidth=1.2, density=1.2)
    
    # Add neutron star
    ax1.add_patch(Circle((0, 0), R0, color='white', zorder=5, edgecolor='black', linewidth=2))
    ax1.set_xlim(-r_max, r_max)
    ax1.set_ylim(-r_max, r_max)
    ax1.set_aspect('equal')
    ax1.set_xlabel('x / R_star', fontsize=12)
    ax1.set_ylabel('y / R_star', fontsize=12)
    ax1.set_title(f'Magnetic Field Lines\nB₀ = {B0:.1e} G', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=mag_sub.min(), vmax=mag_sub.max()))
    sm.set_array([])
    cbar1 = plt.colorbar(sm, ax=ax1)
    cbar1.set_label('log₁₀|B| (G)', fontsize=10)
    
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
    dark_radial = np.exp(-2 * (1 - np.exp(-(B_Bcrit * (R0/r)**3)**2 / (2 * max(epsilon, 1e-6)**2))))
    
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

# Create electromagnetic spectrum mapping - FIXED VERSION
def create_em_composite(img):
    """Create EM spectrum composite (R=X-ray, G=Visible, B=IR)"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        # Convert to grayscale for spectral mapping
        img_gray = np.mean(img_float, axis=2)
    else:
        img_gray = img.astype(np.float32) / 255.0
    
    # Simulate different spectral bands
    xray = img_gray ** 1.5  # X-ray: harder contrast
    visible = img_gray ** 0.8  # Visible: natural
    infrared = img_gray ** 0.5  # Infrared: brighter
    
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
        st.image(img_normalized, caption="Original Image", use_container_width=True)
    
    with col2:
        st.markdown(f"### PDP Entangled (Ω={omega_pd:.2f})")
        try:
            entangled = apply_pdp_entanglement(img, omega_pd)
            st.image(entangled, caption="PDP Entangled", use_container_width=True)
        except Exception as e:
            st.error(f"Error in PDP entanglement: {str(e)}")
    
    # Annotated Physics Maps
    st.markdown("## Annotated Physics Maps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### FDM Soliton")
        try:
            fdm_result = simulate_fdm_soliton(img, fdm_mass)
            st.image(fdm_result, caption=f"FDM Soliton (m={fdm_mass:.2f}×10⁻²² eV)", 
                    use_container_width=True)
        except Exception as e:
            st.error(f"Error in FDM soliton: {str(e)}")
    
    with col2:
        st.markdown("### PDP Interference")
        try:
            interference = pdp_interference(img, fringe_scale)
            st.image(interference, caption=f"PDP Interference (scale={fringe_scale} px)", 
                    use_container_width=True)
        except Exception as e:
            st.error(f"Error in PDP interference: {str(e)}")
    
    # Dark photon conversion
    st.markdown("### Dark Photon Conversion")
    try:
        dark_photon = dark_photon_conversion(img, kinetic_mixing, magnetar_eps)
        st.image(dark_photon, caption=f"Dark Photon Conversion (ε={kinetic_mixing:.1e})", 
                use_container_width=True)
    except Exception as e:
        st.error(f"Error in dark photon conversion: {str(e)}")
    
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
    st.markdown("### EM Spectrum Composite (R=IR, G=Visible, B=X-ray)")
    try:
        # Create scientific RGB composite with proper colors
        rgb_composite = create_scientific_rgb_composite(img)
        st.image(rgb_composite, caption="Multi-wavelength Composite", use_container_width=True)
        
        # Add explanation
        st.markdown("""
        **Color Mapping:**
        - 🔴 **Red**: Infrared (thermal emission from dust)
        - 🟢 **Green**: Visible (starlight/optical)
        - 🔵 **Blue**: X-ray (hot gas/ high energy)
        """)
    except Exception as e:
        st.error(f"Error creating EM composite: {str(e)}")

with col2:
    st.markdown("### EM Spectrum Layers")
    
    # Create individual spectrum layers with proper colors
    if len(img.shape) == 3:
        img_gray = np.mean(img.astype(np.float32) / 255.0, axis=2)
    else:
        img_gray = img.astype(np.float32) / 255.0
    
    # Create colored layers
    xray_colored = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    xray_colored[:, :, 2] = img_gray ** 1.2  # Blue channel for X-ray
    
    visible_colored = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    visible_colored[:, :, 0] = img_gray ** 0.8  # Red
    visible_colored[:, :, 1] = img_gray ** 0.8  # Green
    visible_colored[:, :, 2] = img_gray ** 0.9  # Blue
    
    infrared_colored = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    infrared_colored[:, :, 0] = img_gray ** 0.5  # Red channel for IR
    
    # Create tabs for different layers
    tab1, tab2, tab3 = st.tabs(["🔴 Infrared (Cold)", "🟢 Visible", "🔵 X-ray (Hot)"])
    
    with tab1:
        st.image(infrared_colored, caption="Infrared (Cold)\nLong wavelength | Thermal emission | Red color", 
                use_container_width=True)
        st.markdown("*Dust and cool gas emission*")
    
    with tab2:
        st.image(visible_colored, caption="Visible (Human Eye)\nOptical wavelength | Starlight", 
                use_container_width=True)
        st.markdown("*Stars and galaxies*")
    
    with tab3:
        st.image(xray_colored, caption="X-ray (Hot)\nShort wavelength | High energy | Blue color", 
                use_container_width=True)
        st.markdown("*Hot plasma, shocks, and high-energy processes*")

# Add additional scientific explanation
st.markdown("---")
st.markdown("""
### 📡 Scientific Color Interpretation

The colors in astronomical images are often assigned to represent different physical processes:

- **X-ray (Blue)**: Traces hot gas (millions of degrees) from supernova remnants, galaxy clusters, and active galactic nuclei
- **Visible (Green)**: Shows stars, galaxies, and optical light from various sources
- **Infrared (Red)**: Reveals cool dust, star-forming regions, and objects obscured by dust

This multi-wavelength approach allows astronomers to study different physical phenomena simultaneously.
""")
    st.markdown("## 🌈 Electromagnetic Spectrum Mapping")
    st.markdown("*Infrared → Visible → X-ray | Dark Leakage = Equal & Opposite Quantum Signature*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### EM Spectrum Composite (R=X-ray, G=Visible, B=IR)")
        try:
            composite = create_em_composite(img)
            st.image(composite, caption="EM Spectrum Composite", use_container_width=True)
        except Exception as e:
            st.error(f"Error creating EM composite: {str(e)}")
    
    with col2:
        st.markdown("### EM Spectrum Layers")
        
        # Create individual spectrum layers
        if len(img.shape) == 3:
            img_gray = np.mean(img.astype(np.float32) / 255.0, axis=2)
        else:
            img_gray = img.astype(np.float32) / 255.0
        
        infrared_layer = normalize_image(img_gray ** 0.5)
        visible_layer = normalize_image(img_gray ** 0.8)
        xray_layer = normalize_image(img_gray ** 1.5)
        
        # Create tabs for different layers
        tab1, tab2, tab3 = st.tabs(["Infrared (Cold)", "Visible", "X-ray (Hot)"])
        
        with tab1:
            st.image(infrared_layer, caption="Infrared (Cold)\nLong wavelength | Thermal emission", 
                    use_container_width=True)
        with tab2:
            st.image(visible_layer, caption="Visible (Human Eye)", 
                    use_container_width=True)
        with tab3:
            st.image(xray_layer, caption="X-ray (Hot)\nShort wavelength | High energy", 
                    use_container_width=True)
    
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
# Enhanced electromagnetic spectrum mapping with proper colors
def create_em_composite_colored(img):
    """Create EM spectrum composite with proper color mapping"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        # Convert to grayscale for spectral mapping
        img_gray = np.mean(img_float, axis=2)
    else:
        img_gray = img.astype(np.float32) / 255.0
    
    # Apply different colormaps for different spectral bands
    # X-ray: Blue/purple (high energy)
    xray_cmap = plt.cm.plasma(img_gray)
    xray = xray_cmap[:, :, :3]  # Remove alpha channel
    
    # Visible: Natural colors (green/red)
    visible_cmap = plt.cm.viridis(img_gray)
    visible = visible_cmap[:, :, :3]
    
    # Infrared: Red/orange (low energy)
    ir_cmap = plt.cm.inferno(img_gray)
    infrared = ir_cmap[:, :, :3]
    
    return xray, visible, infrared

# Or create a more realistic multi-wavelength composite
def create_multi_wavelength_composite(img):
    """Create realistic multi-wavelength composite with proper colors"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        img_gray = np.mean(img_float, axis=2)
    else:
        img_gray = img.astype(np.float32) / 255.0
    
    # Simulate different physical processes at different wavelengths
    # X-ray: Hot gas (blue/purple) - typically from shock heating
    xray = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    xray[:, :, 0] = img_gray ** 1.5 * 0.3  # Red channel
    xray[:, :, 1] = img_gray ** 1.2 * 0.6  # Green channel  
    xray[:, :, 2] = img_gray ** 1.0 * 1.0  # Blue channel - dominant for X-ray
    
    # Visible: Starlight (yellow/white) - optical emission
    visible = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    visible[:, :, 0] = img_gray ** 0.8 * 0.9  # Red
    visible[:, :, 1] = img_gray ** 0.8 * 0.9  # Green
    visible[:, :, 2] = img_gray ** 0.9 * 0.7  # Blue
    
    # Infrared: Dust emission (red/orange) - thermal emission from dust
    infrared = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    infrared[:, :, 0] = img_gray ** 0.5 * 1.0  # Red - dominant
    infrared[:, :, 1] = img_gray ** 0.6 * 0.5  # Green
    infrared[:, :, 2] = img_gray ** 0.7 * 0.2  # Blue
    
    # Normalize
    xray = np.clip(xray, 0, 1)
    visible = np.clip(visible, 0, 1)
    infrared = np.clip(infrared, 0, 1)
    
    return xray, visible, infrared

# Create a scientific RGB composite (X-ray: Blue, Visible: Green, IR: Red)
def create_scientific_rgb_composite(img):
    """Create scientific RGB composite matching astronomical conventions"""
    if len(img.shape) == 3:
        img_float = img.astype(np.float32) / 255.0
        img_gray = np.mean(img_float, axis=2)
    else:
        img_gray = img.astype(np.float32) / 255.0
    
    # Astronomical color mapping:
    # Red = Infrared (longest wavelength)
    # Green = Visible (optical)
    # Blue = X-ray (shortest wavelength)
    
    rgb_composite = np.zeros((img_gray.shape[0], img_gray.shape[1], 3))
    
    # Red channel (Infrared)
    rgb_composite[:, :, 0] = img_gray ** 0.5  # IR: brighter, smoother
    
    # Green channel (Visible)
    rgb_composite[:, :, 1] = img_gray ** 0.8  # Visible: natural contrast
    
    # Blue channel (X-ray)
    rgb_composite[:, :, 2] = img_gray ** 1.2  # X-ray: sharper contrast
    
    # Apply brightness scaling
    rgb_composite = np.clip(rgb_composite, 0, 1)
    
    # Enhance colors based on intensity
    mask = img_gray > 0.5
    rgb_composite[mask] = rgb_composite[mask] * 1.2
    rgb_composite = np.clip(rgb_composite, 0, 1)
    
    return rgb_composite

