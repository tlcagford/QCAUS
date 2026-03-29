"""
QCAUS v6.0 – Unified Quantum Cosmology Suite
Integrated: HST/JWST PSF Pipeline | Stealth Detection | IR Spectrum Mapping
All detection methods in main workflow
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter, zoom
from scipy.signal import wiener
from astropy.io import fits
from astropy.convolution import Gaussian2DKernel, convolve_fft
from astropy.stats import sigma_clip
from scipy.special import j1
from PIL import Image, ImageDraw, ImageFont
import io
import json
import pandas as pd
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# ── PAGE CONFIG – LIGHT THEME ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="QCAUS v6.0 - Unified Suite",
    page_icon="🔭",
    initial_sidebar_state="expanded"
)

# Professional light theme
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #f5f7fb; }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e0e4e8; }
    .stTitle, h1, h2, h3 { color: #1e3a5f; }
    [data-testid="stMetricValue"] { color: #1e3a5f; }
    .stDownloadButton button { background-color: #1e3a5f; color: white; border-radius: 8px; }
    .stButton button { background-color: #1e3a5f; color: white; }
</style>
""", unsafe_allow_html=True)


# ── PHYSICS CONSTANTS ─────────────────────────────────────────────
B_crit = 4.4e13  # G
alpha_fine = 1/137.036


# ── HST/JWST PSF MODELS ─────────────────────────────────────────────

def hst_psf_model(size, fwhm_pixels=2.0):
    """HST PSF model (Gaussian + Airy disk)"""
    y, x = np.ogrid[:size, :size]
    cx, cy = size//2, size//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2)
    
    sigma = fwhm_pixels / (2 * np.sqrt(2 * np.log(2)))
    gaussian = np.exp(-r**2 / (2 * sigma**2))
    k = 2 * np.pi / fwhm_pixels
    kr = k * r + 1e-9
    airy = (2 * j1(kr) / kr)**2
    
    psf = gaussian * 0.7 + airy * 0.3
    return psf / psf.sum()


def jwst_psf_model(size, fwhm_pixels=1.5):
    """JWST PSF model (Moffat + hexagonal spikes)"""
    y, x = np.ogrid[:size, :size]
    cx, cy = size//2, size//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2)
    
    beta = 3.5
    alpha = fwhm_pixels / (2 * np.sqrt(2**(1/beta) - 1))
    moffat = (1 + (r / alpha)**2)**(-beta)
    
    theta = np.arctan2(y - cy, x - cx)
    spikes = 1 + 0.2 * np.cos(6 * theta) * np.exp(-r / fwhm_pixels)
    
    return (moffat * spikes) / (moffat * spikes).sum()


def apply_psf_pipeline(image_data, instrument='HST', psf_fwhm=2.0):
    """Complete PSF pipeline"""
    background = np.median(image_data)
    image_bgsub = image_data - background
    
    clipped = sigma_clip(image_bgsub, sigma=3.0, maxiters=5)
    image_clean = np.where(clipped.mask, np.median(image_bgsub), image_bgsub)
    
    psf_size = min(51, image_data.shape[0] // 4)
    if instrument == 'JWST':
        psf = jwst_psf_model(psf_size, psf_fwhm)
    else:
        psf = hst_psf_model(psf_size, psf_fwhm)
    
    from scipy.signal import convolve2d
    image_psf = convolve2d(image_clean, psf, mode='same')
    
    image_final = (image_psf - image_psf.min()) / (image_psf.max() - image_psf.min() + 1e-9)
    
    return image_final, psf, {
        'background': background,
        'clipped_fraction': np.mean(clipped.mask)
    }


# ── IR TO VISIBLE SPECTRUM MAPPING ─────────────────────────────────────────────

def ir_to_visible_colormap():
    """Create colormap mapping IR (cold) to visible (hot) spectrum"""
    colors = [
        (0, 0, 1),      # Blue - cold (IR)
        (0, 1, 1),      # Cyan
        (0, 1, 0),      # Green
        (1, 1, 0),      # Yellow
        (1, 0, 0),      # Red - hot (visible)
    ]
    return LinearSegmentedColormap.from_list('ir_visible', colors, N=256)


def map_ir_to_visible(image, temperature_map=None):
    """Map IR intensity to visible spectrum (blue=cold, red=hot)"""
    if temperature_map is None:
        # Use image intensity as temperature proxy
        temp = np.clip(image, 0, 1)
    else:
        temp = temperature_map
    
    # Create RGB mapping
    rgb = np.zeros((*temp.shape, 3))
    
    # Cold (blue) to hot (red) gradient
    rgb[:, :, 0] = temp  # Red channel increases with temperature
    rgb[:, :, 1] = temp * 0.8  # Green peaks mid-range
    rgb[:, :, 2] = 1 - temp  # Blue decreases with temperature
    
    return np.clip(rgb, 0, 1)


# ── STEALTH DETECTION METHODS (from StealthPDPRadar) ─────────────────────────────────────────────

def dark_mode_leakage_detection(image, epsilon=1e-10, B_field=1e15, m_dark=1e-9):
    """
    Dark-mode leakage detection from StealthPDPRadar
    Extracts quantum signatures that reveal stealth objects
    """
    mixing = epsilon * B_field / (m_dark + 1e-12)
    
    # Quantum oscillation
    quantum_sig = image * mixing * 5
    dark_mode = np.clip(quantum_sig, 0, 1)
    
    # Enhanced detection (blue-halo IR fusion)
    enhanced = image + dark_mode * 0.8
    
    # Detection confidence
    confidence = np.max(dark_mode) * 100
    
    return dark_mode, enhanced, confidence


def green_speck_entanglement(image, fringe=65):
    """
    Green-speck entanglement residuals
    Extracts interference patterns from PDP mixing
    """
    # Create interference pattern
    h, w = image.shape
    y, x = np.ogrid[:h, :w]
    cx, cy = w//2, h//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / max(h, w, 1)
    theta = np.arctan2(y - cy, x - cx)
    k = fringe / 20.0
    
    radial = np.sin(k * 2 * np.pi * r * 3)
    spiral = np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi)))
    pattern = (radial * 0.5 + spiral * 0.5) * image
    
    return np.clip(pattern, 0, 1)


def blue_halo_fusion(image, dark_mode):
    """
    Blue-halo IR fusion visualization
    Combines conventional and quantum signatures
    """
    # Blue halo around detected quantum signatures
    from scipy.ndimage import gaussian_filter
    halo = gaussian_filter(dark_mode, sigma=5)
    
    # RGB: R=conventional, G=quantum, B=halo
    rgb = np.stack([
        image,
        dark_mode * 0.8,
        halo * 0.6
    ], axis=-1)
    
    return np.clip(rgb, 0, 1)


# ── QCI PHYSICS FUNCTIONS ─────────────────────────────────────────────

def fdm_soliton(size, fringe):
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
    """Dark Photon Wave - λ = h/(m v)"""
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


def generate_sample(size=400):
    """Generate sample astronomical image"""
    img = np.zeros((size, size))
    cx, cy = size//2, size//2
    for i in range(size):
        for j in range(size):
            r = np.sqrt((i - cx)**2 + (j - cy)**2)
            img[i, j] = np.exp(-r/60) + 0.2 * np.sin(r/25) * np.exp(-r/80)
    img = img + np.random.randn(size, size) * 0.02
    return (img - img.min()) / (img.max() - img.min())


def add_annotations(image_array, metadata, scale_kpc=100):
    """Add annotations to image"""
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
    draw.rectangle([20, bar_y, 20 + scale_bar_px, bar_y + 6], fill='black')
    draw.text((20 + 35, bar_y - 20), f"{scale_bar_kpc:.0f} kpc", fill='black', font=font_tiny)
    
    # North indicator
    draw.line([w - 35, 30, w - 35, 65], fill='black', width=3)
    draw.text((w - 45, 12), "N", fill='black', font=font_small)
    
    # Info box
    info_lines = [
        f"Ω = {metadata.get('omega', 0):.2f} | Fringe = {metadata.get('fringe', 0)}",
        f"Stealth Confidence: {metadata.get('stealth_conf', 0):.1f}%",
        f"λ_FDM = {scale_bar_kpc / max(metadata.get('fringe', 1), 1) * 8:.1f} kpc"
    ]
    if metadata.get('instrument'):
        info_lines.append(f"Instrument: {metadata['instrument']} | PSF: {metadata.get('psf_fwhm', 2.0):.1f} pix")
    
    draw.rectangle([12, 12, 280, 12 + len(info_lines) * 24 + 8], fill=(255, 255, 255, 200), outline='black')
    for i, line in enumerate(info_lines):
        draw.text((18, 18 + i * 24), line, fill='#1e3a5f', font=font_tiny)
    
    return np.array(img_pil) / 255.0


# ── SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.title("🔭 QCAUS v6.0")
    st.markdown("*Unified Quantum Suite*")
    st.markdown("---")
    
    # File upload
    uploaded = st.file_uploader("📁 Upload FITS/Image", type=['fits', 'png', 'jpg', 'jpeg'])
    
    st.markdown("---")
    st.markdown("### ⚛️ Physics Parameters")
    omega = st.slider("Ω Entanglement", 0.1, 1.0, 0.70, 0.05)
    fringe = st.slider("Fringe Scale", 20, 120, 65, 5)
    brightness = st.slider("Brightness", 0.8, 1.8, 1.2, 0.05)
    scale_kpc = st.selectbox("Scale (kpc)", [50, 100, 150, 200], index=1)
    
    st.markdown("---")
    st.markdown("### 🔭 PSF Pipeline")
    use_pipeline = st.checkbox("Enable HST/JWST Pipeline", value=False)
    if use_pipeline:
        instrument = st.selectbox("Instrument", ["HST", "JWST"])
        psf_fwhm = st.slider("PSF FWHM (pixels)", 1.0, 5.0, 2.0 if instrument == "HST" else 1.5)
    
    st.markdown("---")
    st.markdown("### 🛸 Stealth Detection")
    epsilon = st.slider("Kinetic Mixing ε", 1e-12, 1e-8, 1e-10, format="%.1e")
    m_dark = st.slider("Dark Photon Mass (eV)", 1e-12, 1e-6, 1e-9, format="%.1e")
    B_field = st.number_input("B Field (G)", value=1e15, format="%.1e")
    
    st.caption("Tony Ford | QCAUS v6.0")


# ── MAIN APP ─────────────────────────────────────────────
st.title("🔭 Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("*HST/JWST Pipeline | IR Spectrum Mapping | Quantum Stealth Detection*")
st.markdown("---")

# Load image
if uploaded is not None:
    with st.spinner("Loading image..."):
        img_data = load_image(uploaded)
        st.success(f"✅ Loaded: {uploaded.name}")
else:
    img_data = generate_sample()
    st.info("📸 Using sample image. Upload your own FITS/Image to analyze.")

# Resize
if img_data.shape[0] > 500:
    from skimage.transform import resize
    img_data = resize(img_data, (500, 500), preserve_range=True)

# Apply PSF pipeline if enabled
if use_pipeline:
    with st.spinner("Applying HST/JWST PSF pipeline..."):
        img_processed, psf, pipeline_stats = apply_psf_pipeline(img_data, instrument, psf_fwhm)
        st.caption(f"🔧 {instrument} PSF: background={pipeline_stats['background']:.4f}, cosmic rays={pipeline_stats['clipped_fraction']:.1%}")
else:
    img_processed = img_data
    psf = None

# Generate all physics layers
size = img_processed.shape
soliton = fdm_soliton(size, fringe)
dark_photon = dark_photon_wave(size, fringe)

# Stealth detection methods
dark_mode, stealth_enhanced, stealth_conf = dark_mode_leakage_detection(img_processed, epsilon, B_field, m_dark)
green_speck = green_speck_entanglement(img_processed, fringe)
blue_halo_rgb = blue_halo_fusion(img_processed, dark_mode)

# PDP entanglement result
mixing = omega * 0.6
pdp_result = img_processed * (1 - mixing * 0.4)
pdp_result = pdp_result + dark_photon * mixing * 0.5
pdp_result = pdp_result + soliton * mixing * 0.4
pdp_result = np.clip(pdp_result * brightness, 0, 1)

# IR to Visible mapping
ir_visible = map_ir_to_visible(pdp_result)

# RGB composite with all detection methods
rgb_composite = np.stack([
    pdp_result * 0.6 + dark_mode * 0.4,      # Red: PDP + dark-mode
    pdp_result * 0.3 + green_speck * 0.5,    # Green: green-speck entanglement
    pdp_result * 0.2 + dark_mode * 0.5       # Blue: dark-mode halo
], axis=-1)
rgb_composite = np.clip(rgb_composite, 0, 1)

# Annotations
metadata = {
    'omega': omega, 'fringe': fringe,
    'stealth_conf': stealth_conf,
    'instrument': instrument if use_pipeline else None,
    'psf_fwhm': psf_fwhm if use_pipeline else None
}
annotated = add_annotations(rgb_composite, metadata, scale_kpc)

# ── DISPLAY RESULTS ─────────────────────────────────────────────
st.markdown("### 🔭 Enhanced Quantum View")
st.image(annotated, use_container_width=True)

# Metrics row
st.markdown("### 📊 Detection Metrics")
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    st.metric("Stealth Confidence", f"{stealth_conf:.1f}%")
with col_m2:
    st.metric("Soliton Peak", f"{soliton.max():.3f}")
with col_m3:
    st.metric("Fringe Contrast", f"{dark_photon.std():.3f}")
with col_m4:
    st.metric("Mixing Angle", f"{mixing:.3f}")
with col_m5:
    st.metric("Quantum Signature", f"{dark_mode.max():.4f}")

# Threat assessment
if stealth_conf > 50:
    st.error(f"⚠️ HIGH ALERT: Stealth signature detected with {stealth_conf:.0f}% confidence")
elif stealth_conf > 20:
    st.warning(f"⚠️ MEDIUM ALERT: Possible stealth signature ({stealth_conf:.0f}% confidence)")
elif stealth_conf > 5:
    st.info(f"ℹ️ LOW ALERT: Weak quantum signature detected")
else:
    st.success(f"✅ CLEAR: No stealth signatures detected")

st.markdown("---")

# ── ALL PHYSICS OUTPUTS (Grid) ─────────────────────────────────────────────
st.markdown("### 📊 All Physics Outputs")

col1, col2, col3 = st.columns(3)

def show_img(img, title, cmap=None):
    fig, ax = plt.subplots(figsize=(4, 4))
    if len(img.shape) == 3:
        ax.imshow(np.clip(img, 0, 1))
    else:
        ax.imshow(img, cmap=cmap, vmin=0, vmax=1)
    ax.set_title(title)
    ax.axis('off')
    st.pyplot(fig)
    plt.close(fig)

with col1:
    show_img(img_data, "Original Image", 'gray')
    show_img(soliton, "FDM Soliton Core", 'hot')
    show_img(dark_photon, "Dark Photon Field", 'plasma')

with col2:
    show_img(pdp_result, "PDP Entangled", 'inferno')
    show_img(dark_mode, "Dark-Mode Leakage", 'hot')
    show_img(green_speck, "Green-Speck Entanglement", 'viridis')

with col3:
    show_img(ir_visible, "IR → Visible Spectrum", None)
    show_img(blue_halo_rgb, "Blue-Halo IR Fusion", None)
    show_img(rgb_composite, "Full Quantum Composite", None)

# Show PSF if available
if use_pipeline and psf is not None:
    st.markdown("---")
    st.markdown("### 🔭 PSF Model")
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(psf, cmap='hot')
    ax.set_title(f"{instrument} PSF Model (FWHM={psf_fwhm:.1f} pix)")
    ax.axis('off')
    st.pyplot(fig)
    plt.close(fig)

# ── DOWNLOAD ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 💾 Download Results")

def save_array_png(arr, cmap='inferno'):
    fig, ax = plt.subplots(figsize=(8, 8))
    if len(arr.shape) == 3:
        ax.imshow(np.clip(arr, 0, 1))
    else:
        ax.imshow(arr, cmap=cmap, vmin=0, vmax=1)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    return buf.getvalue()

col_d1, col_d2, col_d3, col_d4 = st.columns(4)

with col_d1:
    st.download_button("📸 Quantum Composite", save_array_png(rgb_composite), "qcaus_composite.png")
with col_d2:
    st.download_button("🌊 Dark-Mode Leakage", save_array_png(dark_mode, 'hot'), "dark_mode.png")
with col_d3:
    st.download_button("⭐ FDM Soliton", save_array_png(soliton, 'hot'), "soliton.png")
with col_d4:
    st.download_button("🌈 IR Visible Map", save_array_png(ir_visible), "ir_visible.png")

st.markdown("---")
st.markdown("🔭 **QCAUS v6.0** | HST/JWST Pipeline | IR Spectrum | Stealth Detection | Tony Ford Model")
