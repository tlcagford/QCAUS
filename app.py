import numpy as np
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

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
    
    soliton = np.exp(-((X-0.5)**2 + (Y-0.5)**2) / 0.2) * omega
    return soliton

def pdp_entanglement_overlay(image: np.ndarray, interference: np.ndarray,
                              soliton: np.ndarray, omega: float,
                              fdm_mass: float = 1e-22, 
                              kinetic_mixing: float = 1e-12) -> np.ndarray:
    """Create entanglement overlay with FDM mass and kinetic mixing effects."""
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
    
    # Apply FDM and kinetic mixing scaling
    mass_scale = 1.0 / (1.0 + fdm_mass / 1e-22)
    interference = interference * mass_scale
    
    mix_scale = 1.0 + kinetic_mixing / 1e-12
    interference = interference * mix_scale
    
    m = omega * 0.6
    
    # Blend components
    result = np.clip(image * (1 - m * 0.4) + 
                     interference * m * 0.5 +
                     soliton * m * 0.4, 0, 1)
    
    return result

def blue_halo_fusion(img, dark_mode, entanglement):
    """Blue halo fusion effect."""
    if dark_mode:
        return np.clip(img * 0.7 + entanglement * 0.3, 0, 1)
    else:
        return np.clip(img * 0.9 + entanglement * 0.1, 0, 1)

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Quantum Causality Analysis",
        page_icon="🔬",
        layout="wide"
    )
    
    st.title("🔬 Quantum Causality Analysis - PDP Entanglement")
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
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Control Parameters")
        
        uploaded_file = st.file_uploader(
            "📁 Upload Image",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload an image for quantum entanglement analysis"
        )
        
        st.markdown("---")
        st.header("⚛️ Quantum Parameters")
        
        omega_pd = st.slider(
            "Magnetar B-field (ω)",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.01,
            help="Controls the magnetar magnetic field strength"
        )
        
        kin_mix_log = st.slider(
            "Kinetic Mixing (log₁₀)",
            min_value=-14,
            max_value=-8,
            value=-12,
            step=0.5,
            help="Kinetic mixing parameter for dark photon coupling"
        )
        kin_mix = 10 ** kin_mix_log
        
        fdm_mass_log = st.slider(
            "FDM Mass (log₁₀ eV)",
            min_value=-23,
            max_value=-21,
            value=-22,
            step=0.1,
            help="Fuzzy Dark Matter mass scale"
        )
        fdm_mass = 10 ** fdm_mass_log
        
        st.markdown("---")
        st.header("🎨 Display Options")
        
        ord_mode = st.toggle("Order Mode", help="Toggle order parameter visualization")
        dark_mode = st.toggle("Dark Mode", help="Enable dark mode visualization")
        
        # Update session state
        st.session_state.omega_pd = omega_pd
        st.session_state.kin_mix = kin_mix
        st.session_state.fdm_mass = fdm_mass
        st.session_state.ord_mode = ord_mode
        st.session_state.dark_mode = dark_mode
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Original Image")
        
        if uploaded_file is not None:
            # Load and process image
            image = Image.open(uploaded_file)
            
            # Convert to grayscale
            img_gray = np.array(image.convert('L')) / 255.0
            st.session_state.img_gray = img_gray
            
            # Display original
            st.image(img_gray, use_container_width=True, clamp=True)
            
            # Image info
            st.caption(f"Dimensions: {img_gray.shape[1]} x {img_gray.shape[0]}")
        else:
            # Placeholder when no image uploaded
            st.info("👈 Please upload an image to begin analysis")
            # Create a sample image
            sample_size = 512
            x = np.linspace(-2, 2, sample_size)
            y = np.linspace(-2, 2, sample_size)
            X, Y = np.meshgrid(x, y)
            sample_img = np.exp(-(X**2 + Y**2) / 2)
            st.image(sample_img, use_container_width=True, clamp=True)
            st.caption("Sample Gaussian Blob (upload your own image for custom analysis)")
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
                st.caption(f"Parameters: ω={st.session_state.omega_pd:.2f}, "
                          f"κ={st.session_state.kin_mix:.2e}, "
                          f"m_FDM={st.session_state.fdm_mass:.2e} eV")
                
                # Optional: Add metrics
                with st.expander("📊 Analysis Metrics"):
                    col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
                    with col_metrics1:
                        st.metric("Omega (B-field)", f"{st.session_state.omega_pd:.3f}")
                    with col_metrics2:
                        st.metric("Kinetic Mixing", f"{st.session_state.kin_mix:.2e}")
                    with col_metrics3:
                        st.metric("FDM Mass", f"{st.session_state.fdm_mass:.2e} eV")
                    
                    # Calculate fringe visibility
                    center_y = fusion.shape[0] // 2
                    center_line = fusion[center_y, :, 0] if len(fusion.shape) == 3 else fusion[center_y, :]
                    visibility = (np.max(center_line) - np.min(center_line)) / (np.max(center_line) + np.min(center_line) + 1e-10)
                    st.metric("Fringe Visibility", f"{visibility:.3f}")
                    
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                st.info("Try uploading a different image or adjusting parameters")
        else:
            st.info("Waiting for image to be processed...")
    
    # Footer
    st.markdown("---")
    st.caption(f"Quantum Causality Analysis Tool | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
