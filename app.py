import numpy as np
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64
import warnings
from datetime import datetime
from scipy.signal import find_peaks
from scipy.fft import fft2, ifft2, fftshift
from scipy.ndimage import gaussian_filter

warnings.filterwarnings("ignore")

# ============================================================================
# ORIGINAL FUNCTIONS FROM YOUR CODEBASE
# ============================================================================

def ensure_square(img: np.ndarray) -> np.ndarray:
    """Ensure image is square by cropping center."""
    if img is None:
        return None
    
    if len(img.shape) == 2:
        h, w = img.shape
        if h == w:
            return img
        min_dim = min(h, w)
        top = (h - min_dim) // 2
        left = (w - min_dim) // 2
        return img[top:top+min_dim, left:left+min_dim]
    else:
        h, w, c = img.shape
        if h == w:
            return img
        min_dim = min(h, w)
        top = (h - min_dim) // 2
        left = (w - min_dim) // 2
        return img[top:top+min_dim, left:left+min_dim, :]

def create_interference_pattern(shape, omega, kinetic_mixing=0):
    """Create interference pattern matching the given shape."""
    if len(shape) == 2:
        h, w = shape
    else:
        h, w = shape[:2]
    
    x = np.linspace(-np.pi, np.pi, w)
    y = np.linspace(-np.pi, np.pi, h)
    X, Y = np.meshgrid(x, y)
    
    # Original interference formula with FDM effects
    interference = 0.5 * (1 + np.cos(omega * 20 * X * (1 + kinetic_mixing)))
    return interference

def create_soliton_pattern(shape, omega):
    """Create soliton pattern matching the given shape."""
    if len(shape) == 2:
        h, w = shape
    else:
        h, w = shape[:2]
    
    x = np.linspace(-np.pi, np.pi, w)
    y = np.linspace(-np.pi, np.pi, h)
    X, Y = np.meshgrid(x, y)
    
    # Original soliton formula
    soliton = np.exp(-((X-0.5)**2 + (Y-0.5)**2) / 0.2) * omega
    return soliton

def pdp_entanglement_overlay(image: np.ndarray, interference: np.ndarray,
                              soliton: np.ndarray, omega: float,
                              fdm_mass: float = 1e-22, 
                              kinetic_mixing: float = 1e-12) -> np.ndarray:
    """
    PDP Entanglement Overlay - Original function with FDM mass and kinetic mixing.
    
    Formula: result = image * (1 - m*0.4) + interference * m*0.5 + soliton * m*0.4
    where m = omega * 0.6
    """
    if image is None or interference is None or soliton is None:
        return np.zeros((100, 100, 3))
    
    # Ensure all inputs are square
    image = ensure_square(image)
    interference = ensure_square(interference)
    soliton = ensure_square(soliton)
    
    # Convert to 3-channel if needed
    if len(image.shape) == 2:
        image = np.stack([image] * 3, axis=-1)
    if len(interference.shape) == 2:
        interference = np.stack([interference] * 3, axis=-1)
    if len(soliton.shape) == 2:
        soliton = np.stack([soliton] * 3, axis=-1)
    
    # Handle shape mismatches
    if image.shape != interference.shape or image.shape != soliton.shape:
        h, w = image.shape[:2]
        x = np.linspace(-np.pi, np.pi, w)
        y = np.linspace(-np.pi, np.pi, h)
        X, Y = np.meshgrid(x, y)
        
        interference = 0.5 * (1 + np.cos(omega * 20 * X * (1 + kinetic_mixing)))
        interference = np.stack([interference] * 3, axis=-1)
        
        soliton = np.exp(-((X-0.5)**2 + (Y-0.5)**2) / 0.2) * omega
        soliton = np.stack([soliton] * 3, axis=-1)
    
    # Apply FDM mass effect on fringe spacing
    mass_scale = 1.0 / (1.0 + fdm_mass / 1e-22)
    interference = interference * mass_scale
    
    # Kinetic mixing affects coupling strength
    mix_scale = 1.0 + kinetic_mixing / 1e-12
    interference = interference * mix_scale
    
    # Mixing strength parameter based on omega (magnetar B-field)
    m = omega * 0.6
    
    # Original blending formula
    result = np.clip(image * (1 - m * 0.4) + 
                     interference * m * 0.5 +
                     soliton * m * 0.4, 0, 1)
    
    return result

def blue_halo_fusion(img: np.ndarray, dark_mode: bool, entanglement: np.ndarray) -> np.ndarray:
    """Blue halo fusion effect from original pdp_radar_core.py"""
    if dark_mode:
        return np.clip(img * 0.7 + entanglement * 0.3, 0, 1)
    else:
        return np.clip(img * 0.9 + entanglement * 0.1, 0, 1)

def quantum_entanglement_entropy(wavefunction: np.ndarray) -> float:
    """Calculate quantum entanglement entropy from wavefunction"""
    # Normalize wavefunction
    prob = np.abs(wavefunction) ** 2
    prob = prob / (np.sum(prob) + 1e-10)
    
    # Von Neumann entropy: S = -Σ p_i log(p_i)
    entropy = -np.sum(prob * np.log(prob + 1e-10))
    return entropy

def pdp_radar_core(image: np.ndarray, interference: np.ndarray, 
                    soliton: np.ndarray, params: dict) -> dict:
    """
    Original PDP Radar Core function from your codebase.
    Computes various quantum metrics.
    """
    results = {}
    
    # Calculate quantum metrics
    results['entanglement_entropy'] = quantum_entanglement_entropy(interference)
    
    # Fringe visibility
    if len(interference.shape) > 2:
        interference_center = interference[interference.shape[0] // 2, :, 0]
    else:
        interference_center = interference[interference.shape[0] // 2, :]
    
    results['fringe_visibility'] = (np.max(interference_center) - np.min(interference_center)) / \
                                   (np.max(interference_center) + np.min(interference_center) + 1e-10)
    
    # Soliton amplitude
    results['soliton_amplitude'] = np.max(soliton)
    
    # Coherence length
    coherence = fft2(interference)
    coherence_shift = fftshift(coherence)
    results['coherence_length'] = np.sum(np.abs(coherence_shift) ** 2) / (np.sum(np.abs(interference)) + 1e-10)
    
    # PDP correlation function
    corr = np.correlate(interference_center, interference_center, mode='full')
    results['pdp_correlation'] = np.max(corr) / (np.sum(corr) + 1e-10)
    
    return results

def generate_quantum_spectrum(interference: np.ndarray, fdm_mass: float):
    """Generate quantum power spectrum with FDM effects using matplotlib"""
    # FFT of interference pattern
    fft_data = fft2(interference)
    fft_shift = fftshift(fft_data)
    power_spectrum = np.abs(fft_shift) ** 2
    
    # Apply FDM mass effect on spectrum
    h, w = power_spectrum.shape
    kx = np.fft.fftfreq(w) * w
    ky = np.fft.fftfreq(h) * h
    KX, KY = np.meshgrid(kx, ky)
    k_rad = np.sqrt(KX**2 + KY**2)
    
    # FDM modifies the power spectrum: P(k) → P(k) * (1 + (k/k_FDM)^4)^-1
    k_fdm = fdm_mass / 1e-22
    fdm_filter = 1.0 / (1.0 + (k_rad / (k_fdm + 1e-10))**4)
    modified_spectrum = power_spectrum * fdm_filter
    
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(np.log(modified_spectrum + 1), cmap='viridis', aspect='auto')
    ax.set_title('Quantum Power Spectrum with FDM Effects')
    ax.set_xlabel('k_x')
    ax.set_ylabel('k_y')
    plt.colorbar(im, ax=ax, label='log(Power)')
    
    return fig

def entanglement_fringe_analysis(image: np.ndarray, interference: np.ndarray, 
                                   omega: float, fdm_mass: float) -> dict:
    """
    Analyze entanglement fringes with FDM mass and B-field parameters.
    Original formula: Δx = λ/(2π) * (1 + m_FDM/m_0) / B_field
    """
    # Fringe spacing calculation
    if len(interference.shape) > 2:
        center_line = interference[interference.shape[0] // 2, :, 0]
    else:
        center_line = interference[interference.shape[0] // 2, :]
    
    # Find peaks in fringe pattern
    peaks, _ = find_peaks(center_line, height=0.5)
    
    if len(peaks) > 1:
        fringe_spacing = np.mean(np.diff(peaks))
    else:
        fringe_spacing = 0
    
    # FDM correction to fringe spacing
    fdm_correction = 1.0 + fdm_mass / 1e-22
    corrected_spacing = fringe_spacing * fdm_correction
    
    # Visibility vs B-field
    visibility = (np.max(center_line) - np.min(center_line)) / \
                 (np.max(center_line) + np.min(center_line) + 1e-10)
    
    return {
        'fringe_spacing': fringe_spacing,
        'fdm_corrected_spacing': corrected_spacing,
        'visibility': visibility,
        'peak_count': len(peaks),
        'b_field_effect': omega * 0.3
    }

# ============================================================================
# MAIN STREAMLIT APPLICATION
# ============================================================================

def main():
    """Main Streamlit application with all original panels"""
    
    try:
        st.set_page_config(
            page_title="Quantum Causality Analysis - PDP Entanglement",
            page_icon="🔬",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        pass
    
    # Title and header
    st.title("🔬 Quantum Causality Analysis - PDP Entanglement")
    st.markdown("### Probing Dark Matter through Quantum Entanglement Fringes")
    st.markdown("---")
    
    # Initialize session state
    if 'img_gray' not in st.session_state:
        st.session_state.img_gray = None
    if 'omega_pd' not in st.session_state:
        st.session_state.omega_pd = 1.0
    if 'kin_mix' not in st.session_state:
        st.session_state.kin_mix = 1e-12
    if 'ord_mode' not in st.session_state:
        st.session_state.ord_mode = False
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'fdm_mass' not in st.session_state:
        st.session_state.fdm_mass = 1e-22
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    
    # ========================================================================
    # SIDEBAR - Control Panels
    # ========================================================================
    
    with st.sidebar:
        st.header("🎛️ Control Parameters")
        st.markdown("---")
        
        # Image upload
        st.subheader("📁 Image Input")
        uploaded_file = st.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload an image for quantum entanglement analysis"
        )
        
        st.markdown("---")
        
        # Quantum Parameters Panel
        st.subheader("⚛️ Quantum Parameters")
        
        # Magnetar B-field (ω)
        omega_pd = st.slider(
            "Magnetar B-field (ω)",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.01,
            format="%.3f",
            help="Magnetic field strength in units of 10^15 Gauss"
        )
        
        # Kinetic Mixing (κ)
        kin_mix_log = st.slider(
            "Kinetic Mixing (log₁₀ κ)",
            min_value=-14.0,
            max_value=-8.0,
            value=-12.0,
            step=0.5,
            format="%.1f",
            help="Dark photon kinetic mixing parameter"
        )
        kin_mix = 10 ** kin_mix_log
        
        # FDM Mass (m_FDM)
        fdm_mass_log = st.slider(
            "FDM Mass (log₁₀ eV)",
            min_value=-23.0,
            max_value=-21.0,
            value=-22.0,
            step=0.1,
            format="%.1f",
            help="Fuzzy Dark Matter mass (typical: 10^-22 eV)"
        )
        fdm_mass = 10 ** fdm_mass_log
        
        st.markdown("---")
        
        # Display Options Panel
        st.subheader("🎨 Visualization")
        
        ord_mode = st.checkbox("Order Parameter Mode", value=False, 
                               help="Display quantum order parameter")
        dark_mode = st.checkbox("Dark Mode", value=False, 
                                help="Enable dark theme visualization")
        
        st.markdown("---")
        
        # Physics Formulas Panel
        with st.expander("📐 Physics Formulas"):
            st.latex(r"\omega = \frac{eB}{m_e c} \quad \text{(Magnetar B-field)}")
            st.latex(r"\kappa = \frac{\chi}{10^{-12}} \quad \text{(Kinetic Mixing)}")
            st.latex(r"m_{\text{FDM}} \sim 10^{-22} \text{ eV} \quad \text{(FDM Mass)}")
            st.latex(r"\text{Entanglement: } \rho = |\psi\rangle\langle\psi|")
            st.latex(r"S = -\text{Tr}(\rho \log \rho) \quad \text{(Entropy)}")
            st.latex(r"\text{Overlay: } I_{\text{out}} = I_0(1-0.4m) + I_{\text{int}}0.5m + I_{\text{sol}}0.4m")
            st.latex(r"m = 0.6\omega \quad \text{(Mixing Strength)}")
        
        # Update session state
        st.session_state.omega_pd = omega_pd
        st.session_state.kin_mix = kin_mix
        st.session_state.fdm_mass = fdm_mass
        st.session_state.ord_mode = ord_mode
        st.session_state.dark_mode = dark_mode
    
    # ========================================================================
    # MAIN CONTENT - Multiple Panels
    # ========================================================================
    
    # Create tabs for different analysis panels
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔮 PDP Entanglement", 
        "📊 Quantum Analysis", 
        "📈 Fringe Spectroscopy",
        "🎨 Advanced Visualization"
    ])
    
    # ========================================================================
    # TAB 1: PDP Entanglement Panel
    # ========================================================================
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Original Image")
            
            if uploaded_file is not None:
                try:
                    # Load and process image
                    image = Image.open(uploaded_file)
                    
                    # Convert to grayscale
                    img_gray = np.array(image.convert('L')) / 255.0
                    st.session_state.img_gray = img_gray
                    
                    # Display original
                    st.image(img_gray, use_container_width=True, clamp=True)
                    
                    # Image info
                    st.caption(f"Dimensions: {img_gray.shape[1]} x {img_gray.shape[0]}")
                    st.caption(f"File: {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Error loading image: {str(e)}")
                    st.session_state.img_gray = None
            else:
                # Placeholder when no image uploaded
                st.info("👈 Upload an image to begin analysis")
                # Create sample image
                sample_size = 512
                x = np.linspace(-2, 2, sample_size)
                y = np.linspace(-2, 2, sample_size)
                X, Y = np.meshgrid(x, y)
                sample_img = np.exp(-(X**2 + Y**2) / 2)
                st.image(sample_img, use_container_width=True, clamp=True)
                st.caption("Sample Gaussian Blob (upload your own image)")
                st.session_state.img_gray = sample_img
        
        with col2:
            st.subheader("🔮 PDP Entanglement Overlay")
            
            if st.session_state.img_gray is not None:
                try:
                    # Get current image
                    current_img = st.session_state.img_gray
                    img_shape = current_img.shape
                    
                    # Create patterns matching image dimensions
                    omega_val = st.session_state.omega_pd * 0.3
                    kin_val = st.session_state.kin_mix
                    
                    interference = create_interference_pattern(img_shape, omega_val, kin_val)
                    soliton = create_soliton_pattern(img_shape, omega_val)
                    
                    # Apply entanglement overlay
                    pdp_out = pdp_entanglement_overlay(
                        current_img,
                        interference,
                        soliton,
                        omega_val,
                        fdm_mass=st.session_state.fdm_mass,
                        kinetic_mixing=kin_val
                    )
                    
                    # Apply blue halo fusion
                    fusion = blue_halo_fusion(pdp_out, st.session_state.dark_mode, pdp_out)
                    
                    # Display result
                    st.image(fusion, use_container_width=True, clamp=True)
                    
                    # Show parameters used
                    st.caption(f"Parameters:")
                    st.caption(f"  • ω = {st.session_state.omega_pd:.3f} (B-field)")
                    st.caption(f"  • κ = {st.session_state.kin_mix:.2e} (Kinetic Mixing)")
                    st.caption(f"  • m_FDM = {st.session_state.fdm_mass:.2e} eV")
                    
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
                    st.info("Try adjusting parameters or uploading a different image")
            else:
                st.info("Waiting for image to be processed...")
    
    # ========================================================================
    # TAB 2: Quantum Analysis Panel
    # ========================================================================
    
    with tab2:
        st.subheader("📊 Quantum Metrics Analysis")
        
        if st.session_state.img_gray is not None:
            try:
                # Generate patterns for analysis
                current_img = st.session_state.img_gray
                img_shape = current_img.shape
                omega_val = st.session_state.omega_pd * 0.3
                kin_val = st.session_state.kin_mix
                
                interference = create_interference_pattern(img_shape, omega_val, kin_val)
                soliton = create_soliton_pattern(img_shape, omega_val)
                
                # Run PDP Radar Core analysis
                params = {
                    'omega': omega_val,
                    'kinetic_mixing': kin_val,
                    'fdm_mass': st.session_state.fdm_mass
                }
                
                analysis_results = pdp_radar_core(current_img, interference, soliton, params)
                st.session_state.analysis_results = analysis_results
                
                # Display metrics in columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Entanglement Entropy",
                        f"{analysis_results['entanglement_entropy']:.4f}",
                        help="Von Neumann entropy of the quantum state"
                    )
                    st.metric(
                        "Soliton Amplitude",
                        f"{analysis_results['soliton_amplitude']:.4f}",
                        help="Peak amplitude of soliton field"
                    )
                
                with col2:
                    st.metric(
                        "Fringe Visibility",
                        f"{analysis_results['fringe_visibility']:.3%}",
                        help="Contrast of interference fringes"
                    )
                    st.metric(
                        "PDP Correlation",
                        f"{analysis_results['pdp_correlation']:.4f}",
                        help="PDP correlation function"
                    )
                
                with col3:
                    st.metric(
                        "Coherence Length",
                        f"{analysis_results['coherence_length']:.2f}",
                        help="Quantum coherence length (pixels)"
                    )
                    st.metric(
                        "B-field Effect",
                        f"{omega_val:.3f}",
                        help="Effective B-field coupling"
                    )
                
                # Quantum Power Spectrum
                st.subheader("⚡ Quantum Power Spectrum")
                fig = generate_quantum_spectrum(interference, st.session_state.fdm_mass)
                st.pyplot(fig)
                
                # Additional analysis
                with st.expander("📐 Detailed Analysis"):
                    st.write("**Quantum State Parameters:**")
                    st.latex(rf"\rho = \text{{Density Matrix}}, \quad S = {analysis_results['entanglement_entropy']:.4f}")
                    st.latex(rf"\mathcal{{V}} = {analysis_results['fringe_visibility']:.3%} \quad \text{{(Visibility)}}")
                    st.latex(rf"\xi_c = {analysis_results['coherence_length']:.2f} \quad \text{{(Coherence Length)}}")
                    
                    # FDM effect explanation
                    st.write("**FDM Mass Effect:**")
                    st.latex(rf"\Delta k = k_0 \left(1 + \frac{{m_{{\text{{FDM}}}}}}{{10^{{-22}}\text{{ eV}}}}\right)")
                    st.latex(rf"m_{{\text{{FDM}}}} = {st.session_state.fdm_mass:.2e} \text{{ eV}}")
                    
            except Exception as e:
                st.error(f"Analysis error: {str(e)}")
        else:
            st.info("Upload an image to begin quantum analysis")
    
    # ========================================================================
    # TAB 3: Fringe Spectroscopy Panel
    # ========================================================================
    
    with tab3:
        st.subheader("📈 Fringe Pattern Analysis")
        
        if st.session_state.img_gray is not None:
            try:
                current_img = st.session_state.img_gray
                img_shape = current_img.shape
                omega_val = st.session_state.omega_pd * 0.3
                kin_val = st.session_state.kin_mix
                
                interference = create_interference_pattern(img_shape, omega_val, kin_val)
                
                # Fringe analysis
                fringe_analysis = entanglement_fringe_analysis(
                    current_img, interference, omega_val, st.session_state.fdm_mass
                )
                
                # Display fringe metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Fringe Spacing", f"{fringe_analysis['fringe_spacing']:.1f} px")
                    st.metric("FDM Corrected Spacing", f"{fringe_analysis['fdm_corrected_spacing']:.1f} px")
                    st.metric("Number of Peaks", fringe_analysis['peak_count'])
                
                with col2:
                    st.metric("Visibility", f"{fringe_analysis['visibility']:.3%}")
                    st.metric("B-field Effect", f"{fringe_analysis['b_field_effect']:.3f}")
                
                # Plot fringe profile
                st.subheader("📊 Fringe Intensity Profile")
                
                if len(interference.shape) > 2:
                    center_line = interference[interference.shape[0] // 2, :, 0]
                else:
                    center_line = interference[interference.shape[0] // 2, :]
                
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(center_line, 'b-', linewidth=2)
                ax.set_xlabel('Pixel Position')
                ax.set_ylabel('Intensity')
                ax.set_title('Fringe Pattern Profile')
                ax.grid(True, alpha=0.3)
                
                st.pyplot(fig)
                
                # Fringe spacing vs B-field simulation
                st.subheader("🎯 Fringe Spacing vs Magnetar B-field")
                
                b_fields = np.linspace(0, 2, 50)
                spacings = []
                visibilities = []
                
                for b in b_fields:
                    test_interference = create_interference_pattern(img_shape, b * 0.3, kin_val)
                    if len(test_interference.shape) > 2:
                        test_line = test_interference[test_interference.shape[0] // 2, :, 0]
                    else:
                        test_line = test_interference[test_interference.shape[0] // 2, :]
                    
                    peaks, _ = find_peaks(test_line, height=0.5)
                    if len(peaks) > 1:
                        spacing = np.mean(np.diff(peaks))
                    else:
                        spacing = 0
                    spacings.append(spacing)
                    
                    vis = (np.max(test_line) - np.min(test_line)) / (np.max(test_line) + np.min(test_line) + 1e-10)
                    visibilities.append(vis)
                
                fig2, ax2 = plt.subplots(1, 2, figsize=(12, 4))
                ax2[0].plot(b_fields, spacings, 'r-', linewidth=2)
                ax2[0].set_xlabel('B-field (ω)')
                ax2[0].set_ylabel('Fringe Spacing (pixels)')
                ax2[0].set_title('B-field Effect on Fringe Spacing')
                ax2[0].grid(True, alpha=0.3)
                
                ax2[1].plot(b_fields, visibilities, 'g-', linewidth=2)
                ax2[1].set_xlabel('B-field (ω)')
                ax2[1].set_ylabel('Visibility')
                ax2[1].set_title('B-field Effect on Visibility')
                ax2[1].grid(True, alpha=0.3)
                
                st.pyplot(fig2)
                
            except Exception as e:
                st.error(f"Fringe analysis error: {str(e)}")
        else:
            st.info("Upload an image to analyze fringe patterns")
    
    # ========================================================================
    # TAB 4: Advanced Visualization Panel
    # ========================================================================
    
    with tab4:
        st.subheader("🎨 Advanced Visualization")
        
        if st.session_state.img_gray is not None:
            try:
                current_img = st.session_state.img_gray
                img_shape = current_img.shape
                omega_val = st.session_state.omega_pd * 0.3
                kin_val = st.session_state.kin_mix
                
                interference = create_interference_pattern(img_shape, omega_val, kin_val)
                soliton = create_soliton_pattern(img_shape, omega_val)
                pdp_out = pdp_entanglement_overlay(
                    current_img, interference, soliton, omega_val,
                    st.session_state.fdm_mass, kin_val
                )
                
                # Create multiple visualization options
                viz_option = st.radio(
                    "Visualization Mode",
                    ["Entanglement Map", "Phase Portrait", "Quantum Interference", "Soliton Field"],
                    horizontal=True
                )
                
                fig, ax = plt.subplots(1, 2, figsize=(12, 5))
                
                if viz_option == "Entanglement Map":
                    ax[0].imshow(pdp_out, cmap='viridis')
                    ax[0].set_title('PDP Entanglement Map')
                    ax[0].axis('off')
                    
                    # Heatmap of entanglement density
                    if len(pdp_out.shape) == 3:
                        entanglement_density = np.mean(pdp_out, axis=2)
                    else:
                        entanglement_density = pdp_out
                    
                    im = ax[1].imshow(entanglement_density, cmap='hot')
                    ax[1].set_title('Entanglement Density')
                    ax[1].axis('off')
                    plt.colorbar(im, ax=ax[1])
                
                elif viz_option == "Phase Portrait":
                    # Phase portrait of interference pattern
                    if len(interference.shape) == 3:
                        phase_data = interference[:, :, 0]
                    else:
                        phase_data = interference
                    
                    ax[0].imshow(np.angle(np.exp(1j * phase_data * 2 * np.pi)), cmap='twilight')
                    ax[0].set_title('Phase Portrait')
                    ax[0].axis('off')
                    
                    # Gradient field
                    grad_y, grad_x = np.gradient(phase_data)
                    magnitude = np.sqrt(grad_x**2 + grad_y**2)
                    ax[1].imshow(magnitude, cmap='plasma')
                    ax[1].set_title('Gradient Magnitude')
                    ax[1].axis('off')
                
                elif viz_option == "Quantum Interference":
                    # Quantum interference pattern
                    if len(interference.shape) == 3:
                        interference_pattern = interference[:, :, 0]
                    else:
                        interference_pattern = interference
                    
                    ax[0].imshow(interference_pattern, cmap='coolwarm')
                    ax[0].set_title('Interference Pattern')
                    ax[0].axis('off')
                    
                    # Show profile
                    center_line = interference_pattern[interference_pattern.shape[0] // 2, :]
                    ax[1].plot(center_line, 'b-', linewidth=2)
                    ax[1].set_xlabel('Pixel')
                    ax[1].set_ylabel('Intensity')
                    ax[1].set_title('Central Profile')
                    ax[1].grid(True, alpha=0.3)
                
                else:  # Soliton Field
                    if len(soliton.shape) == 3:
                        soliton_field = soliton[:, :, 0]
                    else:
                        soliton_field = soliton
                    
                    ax[0].imshow(soliton_field, cmap='Blues')
                    ax[0].set_title('Soliton Field')
                    ax[0].axis('off')
                    
                    # Contour plot
                    contour = ax[1].contourf(soliton_field, levels=20, cmap='Blues')
                    ax[1].set_title('Soliton Contours')
                    ax[1].axis('off')
                    plt.colorbar(contour, ax=ax[1])
                
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Visualization error: {str(e)}")
        else:
            st.info("Upload an image to generate visualizations")
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("🔬 Quantum Causality Analysis Tool")
    with col2:
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col3:
        st.caption("⚛️ PDP Entanglement Module v2.0")

if __name__ == "__main__":
    main()
