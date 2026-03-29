"""
QCAUS v7.0 – Lightweight Fast Loading
Optimized for speed | Lazy loading | Cached physics
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import time
import hashlib
import warnings
from functools import lru_cache

warnings.filterwarnings('ignore')

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="QCAUS v7.0 - Fast Loading",
    page_icon="🔭",
    initial_sidebar_state="expanded"
)

# Clean light theme
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #f5f7fb; }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e0e4e8; }
    .stTitle, h1, h2, h3 { color: #1e3a5f; }
    [data-testid="stMetricValue"] { color: #1e3a5f; }
    .stDownloadButton button { background-color: #1e3a5f; color: white; border-radius: 8px; }
    .stSpinner > div { border-top-color: #1e3a5f; }
</style>
""", unsafe_allow_html=True)


# ── CACHED PHYSICS FUNCTIONS (Fast!) ─────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def cached_fdm_soliton(size_hash, fringe, width=500):
    """Cached soliton generation"""
    h, w = width, width
    y, x = np.ogrid[:h, :w]
    cx, cy = w//2, h//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / max(h, w, 1)
    r_s = 0.2 * (50.0 / max(fringe, 1))
    k = np.pi / max(r_s, 0.01)
    kr = k * r
    with np.errstate(divide='ignore', invalid='ignore'):
        soliton = np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)
    return (soliton - soliton.min()) / (soliton.max() - soliton.min() + 1e-9)


@st.cache_data(ttl=3600, show_spinner=False)
def cached_dark_photon_wave(size_hash, fringe, width=500):
    """Cached wave pattern"""
    h, w = width, width
    y, x = np.ogrid[:h, :w]
    cx, cy = w//2, h//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / max(h, w, 1)
    theta = np.arctan2(y - cy, x - cx)
    k = fringe / 20.0
    radial = np.sin(k * 2 * np.pi * r * 3)
    spiral = np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi)))
    pattern = radial * 0.5 + spiral * 0.5
    return (pattern - pattern.min()) / (pattern.max() - pattern.min() + 1e-9)


@st.cache_data(show_spinner=False)
def load_image_fast(uploaded_file):
    """Fast image loading"""
    if uploaded_file.name.endswith('.fits'):
        try:
            from astropy.io import fits
            with fits.open(io.BytesIO(uploaded_file.read())) as hdul:
                data = hdul[0].data.astype(np.float32)
                if len(data.shape) > 2:
                    data = data[0] if data.shape[0] < data.shape[1] else data[:, :, 0]
        except ImportError:
            st.warning("Astropy not installed. Using fallback.")
            return None
    else:
        img = Image.open(uploaded_file).convert('L')
        data = np.array(img, dtype=np.float32)
    
    data = np.nan_to_num(data, nan=0.0)
    if data.max() > data.min():
        data = (data - data.min()) / (data.max() - data.min())
    
    # Fast resize
    if data.shape[0] > 400:
        from skimage.transform import resize
        data = resize(data, (400, 400), preserve_range=True)
    
    return data


def generate_sample_fast(width=400):
    """Fast sample generation"""
    img = np.zeros((width, width))
    cx, cy = width//2, width//2
    for i in range(width):
        for j in range(width):
            r = np.sqrt((i - cx)**2 + (j - cy)**2)
            img[i, j] = np.exp(-r/60) + 0.2 * np.sin(r/25) * np.exp(-r/80)
    img = img + np.random.randn(width, width) * 0.02
    return (img - img.min()) / (img.max() - img.min())


def compute_stealth(image, epsilon=1e-10):
    """Fast stealth detection"""
    mixing = epsilon * 1e15 / 1e-9
    dark_mode = image * mixing * 5
    dark_mode = np.clip(dark_mode, 0, 1)
    confidence = np.max(dark_mode) * 100
    return dark_mode, confidence


def add_simple_annotations(image_array, metadata, scale_kpc=100):
    """Fast annotations"""
    h, w = image_array.shape[:2]
    img_pil = Image.fromarray((np.clip(image_array, 0, 1) * 255).astype(np.uint8)).convert('RGB')
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img_pil)
    
    try:
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Simple scale bar
    bar_width = 100
    bar_kpc = (bar_width / w) * scale_kpc
    draw.rectangle([20, h-40, 20+bar_width, h-34], fill='black')
    draw.text((20+35, h-55), f"{bar_kpc:.0f} kpc", fill='black', font=font)
    
    # Info text
    text = f"Ω={metadata.get('omega',0):.2f} | Stealth={metadata.get('stealth_conf',0):.1f}%"
    draw.text((15, 15), text, fill='#1e3a5f', font=font)
    
    return np.array(img_pil) / 255.0


# ── SIDEBAR (Fast UI) ─────────────────────────────────────────────
with st.sidebar:
    st.title("🔭 QCAUS v7.0")
    st.markdown("*Fast Loading*")
    st.markdown("---")
    
    uploaded = st.file_uploader("📁 Upload Image", type=['fits', 'png', 'jpg', 'jpeg'], key="fast_upload")
    
    st.markdown("---")
    st.markdown("### ⚛️ Parameters")
    omega = st.slider("Ω Entanglement", 0.1, 1.0, 0.70, 0.05, key="fast_omega")
    fringe = st.slider("Fringe Scale", 20, 120, 65, 5, key="fast_fringe")
    brightness = st.slider("Brightness", 0.8, 1.8, 1.2, 0.05, key="fast_bright")
    scale_kpc = st.selectbox("Scale (kpc)", [50, 100, 150, 200], index=1, key="fast_scale")
    
    st.markdown("---")
    st.markdown("### 🛸 Stealth")
    epsilon = st.slider("ε Mixing", 1e-12, 1e-8, 1e-10, format="%.1e", key="fast_eps")
    
    st.caption("Tony Ford | QCAUS v7.0 | Fast Loading")


# ── MAIN APP ─────────────────────────────────────────────
st.title("🔭 QCAUS - Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("*Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework*")
st.markdown("---")

# Load image (fast)
if uploaded is not None:
    with st.spinner("Loading..."):
        img_data = load_image_fast(uploaded)
        if img_data is None:
            img_data = generate_sample_fast()
        st.success(f"✅ Loaded: {uploaded.name}")
else:
    img_data = generate_sample_fast()
    st.info("📸 Using sample. Upload your own image to analyze.")

# Generate size hash for caching
size_hash = hashlib.md5(str(img_data.shape).encode()).hexdigest()

# Generate layers (cached for speed)
with st.spinner("Processing..."):
    # Get cached physics
    soliton = cached_fdm_soliton(size_hash, fringe, img_data.shape[0])
    dark_photon = cached_dark_photon_wave(size_hash, fringe, img_data.shape[0])
    
    # Fast computations
    dark_mode, stealth_conf = compute_stealth(img_data, epsilon)
    
    # PDP result (simple)
    mixing = omega * 0.6
    pdp_result = img_data * (1 - mixing * 0.4)
    pdp_result = pdp_result + dark_photon * mixing * 0.5
    pdp_result = pdp_result + soliton * mixing * 0.4
    pdp_result = np.clip(pdp_result * brightness, 0, 1)
    
    # Simple RGB composite
    rgb = np.stack([pdp_result, pdp_result * 0.5 + dark_mode * 0.5, pdp_result * 0.3 + dark_mode * 0.7], axis=-1)
    rgb = np.clip(rgb, 0, 1)
    
    # Annotate
    metadata = {'omega': omega, 'fringe': fringe, 'stealth_conf': stealth_conf}
    annotated = add_simple_annotations(rgb, metadata, scale_kpc)

# Display
st.markdown("### 🔭 Enhanced Quantum View")
st.image(annotated, use_container_width=True)

# Quick metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Stealth Confidence", f"{stealth_conf:.1f}%")
with col2:
    st.metric("Soliton Peak", f"{soliton.max():.3f}")
with col3:
    st.metric("Fringe Contrast", f"{dark_photon.std():.3f}")
with col4:
    st.metric("Mixing Angle", f"{mixing:.3f}")

# Threat assessment (fast)
if stealth_conf > 50:
    st.error(f"⚠️ HIGH ALERT: Stealth detected ({stealth_conf:.0f}% confidence)")
elif stealth_conf > 20:
    st.warning(f"⚠️ MEDIUM ALERT: Possible stealth ({stealth_conf:.0f}% confidence)")
elif stealth_conf > 5:
    st.info(f"ℹ️ LOW ALERT: Weak quantum signature")
else:
    st.success(f"✅ CLEAR: No stealth signatures")

st.markdown("---")

# Quick grid of outputs (collapsible for speed)
with st.expander("📊 View All Physics Outputs", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    
    def quick_img(img, title, cmap='gray'):
        fig, ax = plt.subplots(figsize=(3, 3))
        if len(img.shape) == 3:
            ax.imshow(np.clip(img, 0, 1))
        else:
            ax.imshow(img, cmap=cmap, vmin=0, vmax=1)
        ax.set_title(title, fontsize=8)
        ax.axis('off')
        st.pyplot(fig)
        plt.close(fig)
    
    with col_a:
        quick_img(img_data, "Original", 'gray')
        quick_img(soliton, "FDM Soliton", 'hot')
    with col_b:
        quick_img(dark_photon, "Dark Photon", 'plasma')
        quick_img(pdp_result, "PDP Entangled", 'inferno')
    with col_c:
        quick_img(dark_mode, "Dark-Mode Leakage", 'hot')
        quick_img(rgb, "Quantum Composite", None)

# Simple download
st.markdown("---")
st.markdown("### 💾 Download")

def save_fast(arr):
    fig, ax = plt.subplots(figsize=(5, 5))
    if len(arr.shape) == 3:
        ax.imshow(np.clip(arr, 0, 1))
    else:
        ax.imshow(arr, cmap='inferno', vmin=0, vmax=1)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    return buf.getvalue()

col_d1, col_d2 = st.columns(2)
with col_d1:
    st.download_button("📸 Download Composite", save_fast(rgb), "qcaus_composite.png")
with col_d2:
    st.download_button("🌊 Download Dark-Mode", save_fast(dark_mode), "dark_mode.png")

st.markdown("---")
st.markdown("⚡ **QCAUS v7.0** | Fast Loading | Tony Ford Model | tlcagford@gmail.com")
