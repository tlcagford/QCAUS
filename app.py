"""
QCAUS v4.0 – Unified Quantum Cosmology Suite
One image upload → All physics outputs | Interactive layer toggles
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.ndimage import gaussian_filter, convolve
from astropy.io import fits
from PIL import Image, ImageDraw, ImageFont
import io
import json
import pandas as pd
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="QCAUS v4.0 - Unified Suite",
    page_icon="🔭",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #0a0a1a; }
    [data-testid="stSidebar"] { background: #0f0f1f; border-right: 2px solid #00aaff; }
    .stTitle, h1, h2, h3 { color: #00aaff; }
    [data-testid="stMetricValue"] { color: #00aaff; }
    .stDownloadButton button { background-color: #00aaff; color: white; border-radius: 8px; }
    .stButton button { background-color: #00aaff; color: white; }
    .layer-toggle {
        background-color: #1a1a3a;
        padding: 5px 10px;
        border-radius: 8px;
        margin: 2px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)


# ── PHYSICS CONSTANTS ─────────────────────────────────────────────
B_crit = 4.4e13
alpha_fine = 1/137.036


# ── CORE PHYSICS FUNCTIONS ─────────────────────────────────────────────

def fdm_soliton_core(size, fringe):
    """FDM Soliton - ρ(r) ∝ [sin(kr)/(kr)]²"""
    h, w = size
    y, x = np.ogrid[:h, :w]
    cx, cy = w//2, h//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / max(h, w, 1)
    r_s = 0.2 * (50.0 / max(fringe, 1))
    k = np.pi / max(r_s, 0.01)
    kr = k * r
    
    with np.errstate(divide='ignore', invalid='ignore'):
        soliton = np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)
    return (soliton - soliton.min()) / (soliton.max() - soliton.min() + 1e-9)


def dark_photon_wave(size, fringe):
    """Dark Photon Wave - λ = h/(m v) interference"""
    h, w = size
    y, x = np.ogrid[:h, :w]
    cx, cy = w//2, h//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / max(h, w, 1)
    theta = np.arctan2(y - cy, x - cx)
    k = fringe / 20.0
    
    radial = np.sin(k * 2 * np.pi * r * 3)
    spiral = np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi)))
    pattern = radial * 0.5 + spiral * 0.5
    return (pattern - pattern.min()) / (pattern.max() - pattern.min() + 1e-9)


def dark_matter_density(image, soliton):
    """Dark Matter Density from gradients"""
    smoothed = gaussian_filter(image, sigma=8)
    grad_x = np.gradient(smoothed, axis=0)
    grad_y = np.gradient(smoothed, axis=1)
    gradient = np.sqrt(grad_x**2 + grad_y**2)
    gradient = (gradient - gradient.min()) / (gradient.max() - gradient.min() + 1e-9)
    return soliton * 0.6 + gradient * 0.4


def pdp_entanglement(image, dark_photon, soliton, omega):
    """Photon-Dark Photon entanglement mixing"""
    mixing = omega * 0.6
    result = image * (1 - mixing * 0.4)
    result = result + dark_photon * mixing * 0.5
    result = result + soliton * mixing * 0.4
    return np.clip(result, 0, 1)


def magnetar_field(B_surface, size=200, range_km=300):
    """Magnetar dipole field visualization"""
    x = np.linspace(-range_km, range_km, size)
    y = np.linspace(-range_km, range_km, size)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2) + 1e-9
    Theta = np.arctan2(Y, X)
    B0 = B_surface * (10 / R)**3
    B_mag = B0 * np.sqrt(4 * np.cos(Theta)**2 + np.sin(Theta)**2)
    return B_mag


def stealth_radar_detection(image, epsilon=1e-10, B_field=1e15, m_dark=1e-9):
    """PDP quantum radar detection"""
    mixing = epsilon * B_field / (m_dark + 1e-12)
    
    # Use image as radar return proxy
    quantum_sig = image * mixing * 5
    dark_mode_leakage = np.clip(quantum_sig, 0, 1)
    confidence = np.max(dark_mode_leakage) * 100
    
    return dark_mode_leakage, confidence


def power_spectrum(image):
    """Compute power spectrum P(k)"""
    from scipy.fft import fft2, fftshift
    fft = fft2(image)
    power = np.abs(fft)**2
    return fftshift(power)


# ── ANNOTATION FUNCTION ─────────────────────────────────────────────

def add_annotations(image_array, metadata, scale_kpc=100):
    """Add physics annotations to image"""
    img_pil = Image.fromarray((np.clip(image_array, 0, 1) * 255).astype(np.uint8)).convert('RGB')
    draw = ImageDraw.Draw(img_pil)
    
    try:
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    except:
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
    
    h, w = image_array.shape[:2]
    
    # Scale bar
    scale_bar_px = 100
    scale_bar_kpc = (scale_bar_px / w) * scale_kpc
    bar_y = h - 45
    draw.rectangle([20, bar_y, 20 + scale_bar_px, bar_y + 6], fill='white')
    draw.text((20 + 35, bar_y - 20), f"{scale_bar_kpc:.0f} kpc", fill='white', font=font_tiny)
    
    # North indicator
    draw.line([w - 35, 30, w - 35, 65], fill='white', width=3)
    draw.text((w - 45, 12), "N", fill='white', font=font_small)
    
    # Info box
    info_lines = [
        f"Ω = {metadata.get('omega', 0):.2f} | Fringe = {metadata.get('fringe', 0)}",
        f"Mixing = {metadata.get('mixing', 0):.3f} | Entropy = {metadata.get('entropy', 0):.3f}",
        f"λ_FDM = {scale_bar_kpc / max(metadata.get('fringe', 1), 1) * 8:.1f} kpc"
    ]
    
    draw.rectangle([12, 12, 280, 12 + len(info_lines) * 24 + 8], fill=(0, 0, 0, 180), outline='white')
    for i, line in enumerate(info_lines):
        draw.text((18, 18 + i * 24), line, fill='cyan', font=font_tiny)
    
    return np.array(img_pil) / 255.0


def load_image(uploaded_file):
    """Load image from uploaded file"""
    if uploaded_file.name.endswith('.fits'):
        with fits.open(io.BytesIO(uploaded_file.read())) as hdul:
            data = hdul[0].data.astype(np.float32)
            if len(data.shape) > 2:
                data = data[0] if data.shape[0] < data.shape[1] else data[:, :, 0]
    else:
        img = Image.open(uploaded_file).convert('L')
        data = np.array(img, dtype=np.float32)
    
    data = np.nan_to_num(data, nan=0.0)
    if data.max() > data.min():
        data = (data - data.min()) / (data.max() - data.min())
    return data


# ── SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.title("🌌 QCAUS v4.0")
    st.markdown("*Unified Quantum Suite*")
    st.markdown("---")
    
    # File upload
    uploaded = st.file_uploader("📁 Upload Image", type=['fits', 'png', 'jpg', 'jpeg'])
    
    st.markdown("---")
    st.markdown("### ⚛️ Physics Parameters")
    omega = st.slider("Ω Entanglement", 0.1, 1.0, 0.70, 0.05)
    fringe = st.slider("Fringe Scale", 20, 120, 65, 5)
    brightness = st.slider("Brightness", 0.8, 1.8, 1.2, 0.05)
    scale_kpc = st.selectbox("Scale (kpc)", [50, 100, 150, 200], index=1)
    
    st.markdown("---")
    st.markdown("### 🛸 Stealth Parameters")
    epsilon = st.slider("Kinetic Mixing ε", 1e-12, 1e-8, 1e-10, format="%.1e")
    m_dark = st.slider("Dark Photon Mass (eV)", 1e-12, 1e-6, 1e-9, format="%.1e")
    
    st.markdown("---")
    st.markdown("### 🎛️ Layer Controls")
    st.markdown("*Click checkboxes to toggle layers*")
    
    st.caption("Tony Ford | QCAUS v4.0 | One Image → All Physics")


# ── MAIN APP ─────────────────────────────────────────────
st.title("🌌 Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("*Upload one image → See all physics outputs | Toggle layers interactively*")
st.markdown("---")

if uploaded is not None:
    # Load image
    with st.spinner("Loading image..."):
        img_data = load_image(uploaded)
        
        # Resize
        MAX_SIZE = 400
        if img_data.shape[0] > MAX_SIZE or img_data.shape[1] > MAX_SIZE:
            from skimage.transform import resize
            img_data = resize(img_data, (MAX_SIZE, MAX_SIZE), preserve_range=True)
    
    st.success(f"✅ Loaded: {uploaded.name}")
    
    # ── GENERATE ALL PHYSICS LAYERS ─────────────────────────────────────────────
    with st.spinner("Generating physics layers..."):
        size = img_data.shape
        soliton = fdm_soliton_core(size, fringe)
        dark_photon = dark_photon_wave(size, fringe)
        dark_matter = dark_matter_density(img_data, soliton)
        pdp_result = pdp_entanglement(img_data, dark_photon, soliton, omega)
        pdp_result = np.clip(pdp_result * brightness, 0, 1)
        
        # RGB composite (R=Image, G=Dark Photon, B=Dark Matter)
        rgb_composite = np.stack([
            pdp_result,
            pdp_result * 0.3 + dark_photon * 0.5 + soliton * 0.2,
            pdp_result * 0.2 + dark_matter * 0.6 + soliton * 0.2
        ], axis=-1)
        rgb_composite = np.clip(rgb_composite, 0, 1)
        
        # Magnetar field
        magnetar = magnetar_field(1e15, size[0])
        
        # Stealth detection
        stealth_map, stealth_conf = stealth_radar_detection(pdp_result, epsilon, 1e15, m_dark)
        
        # Power spectrum
        power_spec = power_spectrum(pdp_result)
        
        # Entropy
        mixing = omega * 0.6
        entropy = -mixing * np.log(mixing + 1e-12)
    
    # Metrics row
    st.markdown("### 📊 Physics Metrics")
    col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)
    with col_m1:
        st.metric("Soliton Peak", f"{soliton.max():.3f}")
    with col_m2:
        st.metric("Fringe Contrast", f"{dark_photon.std():.3f}")
    with col_m3:
        st.metric("Mixing Angle", f"{mixing:.3f}")
    with col_m4:
        st.metric("Entanglement Entropy", f"{entropy:.3f}")
    with col_m5:
        st.metric("Stealth Confidence", f"{stealth_conf:.1f}%")
    with col_m6:
        st.metric("DM Mean", f"{dark_matter.mean():.3f}")
    
    st.markdown("---")
    
    # ── INTERACTIVE LAYER TOGGLES ─────────────────────────────────────────────
    st.markdown("### 🎨 Interactive Layers")
    st.markdown("*Toggle layers on/off to see individual physics components*")
    
    # Layer toggles
    col_t1, col_t2, col_t3, col_t4, col_t5, col_t6 = st.columns(6)
    with col_t1:
        show_original = st.checkbox("📷 Original", value=True)
    with col_t2:
        show_soliton = st.checkbox("⭐ Soliton", value=False)
    with col_t3:
        show_dark_photon = st.checkbox("🌊 Dark Photon", value=False)
    with col_t4:
        show_dark_matter = st.checkbox("🌌 Dark Matter", value=False)
    with col_t5:
        show_pdp = st.checkbox("✨ PDP Entangled", value=True)
    with col_t6:
        show_stealth = st.checkbox("🛸 Stealth Map", value=False)
    
    # Build composite image based on toggles
    composite = np.zeros((*size, 3))
    
    if show_original:
        composite[:, :, 0] += img_data * 0.8
        composite[:, :, 1] += img_data * 0.8
        composite[:, :, 2] += img_data * 0.8
    
    if show_soliton:
        composite[:, :, 0] += soliton * 0.7
        composite[:, :, 1] += soliton * 0.3
        composite[:, :, 2] += soliton * 0.2
    
    if show_dark_photon:
        composite[:, :, 0] += dark_photon * 0.3
        composite[:, :, 1] += dark_photon * 0.7
        composite[:, :, 2] += dark_photon * 0.2
    
    if show_dark_matter:
        composite[:, :, 0] += dark_matter * 0.2
        composite[:, :, 1] += dark_matter * 0.3
        composite[:, :, 2] += dark_matter * 0.8
    
    if show_pdp:
        composite[:, :, 0] += pdp_result * 0.9
        composite[:, :, 1] += pdp_result * 0.7
        composite[:, :, 2] += pdp_result * 0.5
    
    if show_stealth:
        composite[:, :, 0] += stealth_map * 0.9
        composite[:, :, 1] += stealth_map * 0.3
        composite[:, :, 2] += stealth_map * 0.2
    
    composite = np.clip(composite, 0, 1)
    
    # Display composite with annotations
    metadata = {'omega': omega, 'fringe': fringe, 'mixing': mixing, 'entropy': entropy}
    annotated = add_annotations(composite, metadata, scale_kpc)
    
    st.markdown("### 🔭 Live Composite View")
    st.image(annotated, use_container_width=True)
    
    # Legend
    st.markdown("""
    <div style="background-color: #1a1a3a; padding: 10px; border-radius: 8px; margin-top: 10px;">
    <b>🎨 Layer Legend:</b>
    <span style="color:#ff8888"> Red: PDP Entangled / Original</span> • 
    <span style="color:#88ff88"> Green: Dark Photon Field</span> • 
    <span style="color:#8888ff"> Blue: Dark Matter Density</span> • 
    <span style="color:#ffaa44"> Orange/Yellow: FDM Soliton</span> • 
    <span style="color:#ff4444"> Bright Red: Stealth Detection</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ── ALL PHYSICS OUTPUTS (Grid View) ─────────────────────────────────────────────
    st.markdown("### 📊 All Physics Outputs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='#0a0a1a')
        ax.imshow(img_data, cmap='gray')
        ax.set_title("Original Image", color='white')
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)
        
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='#0a0a1a')
        ax.imshow(soliton, cmap='hot')
        ax.set_title("FDM Soliton Core", color='white')
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='#0a0a1a')
        ax.imshow(dark_photon, cmap='plasma')
        ax.set_title("Dark Photon Field", color='white')
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)
        
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='#0a0a1a')
        ax.imshow(dark_matter, cmap='viridis')
        ax.set_title("Dark Matter Density", color='white')
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)
    
    with col3:
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='#0a0a1a')
        ax.imshow(pdp_result, cmap='inferno')
        ax.set_title("PDP Entangled", color='white')
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)
        
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='#0a0a1a')
        ax.imshow(stealth_map, cmap='hot')
        ax.set_title(f"Stealth Map ({stealth_conf:.0f}% confidence)", color='white')
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)
    
    # ── ADDITIONAL PHYSICS VISUALIZATIONS ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔬 Advanced Physics")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Magnetar Field**")
        fig, ax = plt.subplots(figsize=(6, 5), facecolor='#0a0a1a')
        im = ax.imshow(magnetar, cmap='plasma')
        ax.set_title("Magnetar Dipole Field", color='white')
        ax.axis('off')
        plt.colorbar(im, ax=ax, fraction=0.046, label="|B| (G)")
        st.pyplot(fig)
        plt.close(fig)
        
        st.markdown("**Power Spectrum**")
        fig, ax = plt.subplots(figsize=(6, 5), facecolor='#0a0a1a')
        ax.imshow(np.log(power_spec + 1), cmap='hot')
        ax.set_title("P(k) Power Spectrum", color='white')
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)
    
    with col_b:
        st.markdown("**Primordial Entanglement Evolution**")
        t = np.linspace(0, 1, 200)
        mixing_evo = 0.6 * (1 - np.exp(-70 * t))
        entropy_evo = -mixing_evo * np.log(mixing_evo + 1e-12)
        
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#0a0a1a')
        ax.plot(t, mixing_evo, 'r-', linewidth=2, label='Mixing')
        ax.plot(t, entropy_evo, 'b-', linewidth=2, label='Entropy')
        ax.set_xlabel("Scale Factor", color='white')
        ax.set_ylabel("Amplitude", color='white')
        ax.set_title("von Neumann Evolution", color='#00aaff')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
        
        st.markdown("**Quantum-Corrected Power Spectrum**")
        k = np.logspace(-3, 0, 100)
        P_lcdm = 2.1e-9 * (k / 0.05)**(0.965 - 1)
        P_quantum = P_lcdm * (1 + omega * (k / 0.05)**0.8)
        
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#0a0a1a')
        ax.loglog(k, P_lcdm, 'b-', linewidth=2, label='ΛCDM')
        ax.loglog(k, P_quantum, 'r-', linewidth=2, label='Quantum-corrected')
        ax.fill_between(k, P_lcdm, P_quantum, alpha=0.3, color='red')
        ax.set_xlabel("k (Mpc⁻¹)", color='white')
        ax.set_ylabel("P(k)", color='white')
        ax.set_title("Matter Power Spectrum", color='#00aaff')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    
    # ── DOWNLOAD ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 💾 Download Results")
    
    def save_array_png(arr, cmap='inferno'):
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
        if len(arr.shape) == 3:
            ax.imshow(np.clip(arr, 0, 1))
        else:
            ax.imshow(arr, cmap=cmap, vmin=0, vmax=1)
        ax.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='black')
        plt.close(fig)
        return buf.getvalue()
    
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    
    with col_d1:
        st.download_button("📸 Composite View", save_array_png(annotated), "qcaus_composite.png")
    with col_d2:
        st.download_button("⭐ FDM Soliton", save_array_png(soliton, 'hot'), "soliton.png")
    with col_d3:
        st.download_button("🌊 Dark Photon", save_array_png(dark_photon, 'plasma'), "dark_photon.png")
    with col_d4:
        st.download_button("🛸 Stealth Map", save_array_png(stealth_map, 'hot'), "stealth_map.png")

else:
    st.info("""
    ## 📁 **Upload an image to get started**
    
    **This unified app combines all QCAUS physics in one page:**
    
    | Layer | Physics | Visualization |
    |-------|---------|---------------|
    | **FDM Soliton** | ρ(r) ∝ [sin(kr)/kr]² | Orange/Yellow core |
    | **Dark Photon** | λ = h/(m v) interference | Green wave patterns |
    | **Dark Matter** | ∇²Φ = 4πGρ | Blue density map |
    | **PDP Entangled** | Quantum mixing | Red/Purple enhanced |
    | **Stealth Map** | Dark-mode leakage | Bright red detection |
    
    **Interactive Features:**
    - ✅ Toggle layers on/off
    - ✅ Real-time composite view
    - ✅ All physics outputs displayed
    - ✅ Download any layer as PNG
    """)
    
    # Show example of what to expect
    with st.expander("📖 Quick Start Guide"):
        st.markdown("""
        1. **Upload an image** (FITS, PNG, JPG)
        2. **Adjust physics parameters** in sidebar
        3. **Toggle layers** to see individual components
        4. **View all outputs** in the grid below
        5. **Download results** as PNG files
        
        **Recommended first image:** Any galaxy cluster (Bullet Cluster, Abell 1689) or nebula (Crab Nebula)
        """)

st.markdown("---")
st.markdown("🔭 **QCAUS v4.0** | Unified Quantum Suite | One Image → All Physics | Tony Ford Model")
