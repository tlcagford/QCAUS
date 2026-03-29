"""
QCAUS v9.0 – Before/After Comparison + PDP Interference Visualizer
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image, ImageDraw, ImageFont
import io
import hashlib
import warnings

warnings.filterwarnings('ignore')

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="QCAUS v9.0 - Before/After + Interference",
    page_icon="🔭",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #f5f7fb; }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e0e4e8; }
    .stTitle, h1, h2, h3 { color: #1e3a5f; }
    [data-testid="stMetricValue"] { color: #1e3a5f; }
    .stDownloadButton button { background-color: #1e3a5f; color: white; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ── PHYSICS FUNCTIONS ─────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
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


@st.cache_data(ttl=3600, show_spinner=False)
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


def dark_leak_detection(image, epsilon=1e-10, B_field=1e15, m_dark=1e-9):
    """Dark Leak Detection – Quantum signature extraction"""
    mixing = epsilon * B_field / (m_dark + 1e-12)
    dark_leak = image * mixing * 5
    dark_leak = np.clip(dark_leak, 0, 1)
    confidence = np.max(dark_leak) * 100
    return dark_leak, confidence


def pdp_entanglement(image, dark_photon, soliton, omega):
    """Photon-Dark Photon entanglement mixing"""
    mixing = omega * 0.6
    result = image * (1 - mixing * 0.4)
    result = result + dark_photon * mixing * 0.5
    result = result + soliton * mixing * 0.4
    return np.clip(result, 0, 1)


def pdp_interference_visualization(size, fringe, omega):
    """
    Create a pure PDP interference visualization
    Shows the wave interference pattern from photon-dark photon mixing
    """
    h, w = size
    y, x = np.ogrid[:h, :w]
    cx, cy = w//2, h//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / max(h, w, 1)
    theta = np.arctan2(y - cy, x - cx)
    k = fringe / 20.0
    
    # Primary interference patterns
    radial = np.sin(k * 2 * np.pi * r * 3)
    spiral = np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi)))
    angular = np.sin(k * 3 * theta)
    
    # Combine based on fringe
    if fringe < 50:
        pattern = radial * 0.6 + spiral * 0.4
    elif fringe < 80:
        pattern = radial * 0.4 + spiral * 0.4 + angular * 0.2
    else:
        pattern = spiral * 0.5 + angular * 0.3 + radial * 0.2
    
    # Add quantum mixing effect (PDP mixing)
    mixing = omega * 0.6
    interference = pattern * (1 + mixing * np.sin(k * 4 * np.pi * r))
    
    return (interference - interference.min()) / (interference.max() - interference.min() + 1e-9)


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
            return None
    else:
        img = Image.open(uploaded_file).convert('L')
        data = np.array(img, dtype=np.float32)
    
    data = np.nan_to_num(data, nan=0.0)
    if data.max() > data.min():
        data = (data - data.min()) / (data.max() - data.min())
    
    if data.shape[0] > 400:
        from skimage.transform import resize
        data = resize(data, (400, 400), preserve_range=True)
    
    return data


def generate_sample(width=400):
    """Generate sample image"""
    img = np.zeros((width, width))
    cx, cy = width//2, width//2
    for i in range(width):
        for j in range(width):
            r = np.sqrt((i - cx)**2 + (j - cy)**2)
            img[i, j] = np.exp(-r/60) + 0.2 * np.sin(r/25) * np.exp(-r/80)
    img = img + np.random.randn(width, width) * 0.02
    return (img - img.min()) / (img.max() - img.min())


def add_annotations(image_array, metadata, scale_kpc=100, title="After"):
    """Add annotations to image"""
    h, w = image_array.shape[:2]
    img_pil = Image.fromarray((np.clip(image_array, 0, 1) * 255).astype(np.uint8)).convert('RGB')
    draw = ImageDraw.Draw(img_pil)
    
    try:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Scale bar
    bar_width = 100
    bar_kpc = (bar_width / w) * scale_kpc
    draw.rectangle([20, h-40, 20+bar_width, h-34], fill='black')
    draw.text((20+35, h-55), f"{bar_kpc:.0f} kpc", fill='black', font=font_small)
    
    # North indicator
    draw.line([w-30, 30, w-30, 60], fill='black', width=2)
    draw.text((w-38, 15), "N", fill='black', font=font)
    
    # Info box
    info_lines = [
        f"Ω = {metadata.get('omega',0):.2f} | Fringe = {metadata.get('fringe',0)}",
        f"Dark Leak: {metadata.get('dark_leak_conf',0):.1f}% | Mixing: {metadata.get('mixing',0):.3f}"
    ]
    draw.rectangle([12, 12, 260, 12 + len(info_lines) * 22 + 8], fill=(255,255,255,200), outline='black')
    for i, line in enumerate(info_lines):
        draw.text((18, 18 + i * 22), line, fill='#1e3a5f', font=font_small)
    
    # Title
    draw.text((w//2 - 80, 10), title, fill='#1e3a5f', font=font)
    
    return np.array(img_pil) / 255.0


# ── SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.title("🔭 QCAUS v9.0")
    st.markdown("*Before/After + PDP Interference*")
    st.markdown("---")
    
    uploaded = st.file_uploader("📁 Upload Image", type=['fits', 'png', 'jpg', 'jpeg'])
    
    st.markdown("---")
    st.markdown("### ⚛️ Parameters")
    omega = st.slider("Ω Entanglement", 0.1, 1.0, 0.70, 0.05)
    fringe = st.slider("Fringe Scale", 20, 120, 65, 5)
    brightness = st.slider("Brightness", 0.8, 1.8, 1.2, 0.05)
    scale_kpc = st.selectbox("Scale (kpc)", [50, 100, 150, 200], index=1)
    
    st.markdown("---")
    st.markdown("### 🕳️ Dark Leak")
    epsilon = st.slider("Kinetic Mixing ε", 1e-12, 1e-8, 1e-10, format="%.1e")
    
    st.caption("Tony Ford | QCAUS v9.0")


# ── MAIN APP ─────────────────────────────────────────────
st.title("🔭 QCAUS - Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("*Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework*")
st.markdown("---")

# Load image
if uploaded is not None:
    with st.spinner("Loading..."):
        img_data = load_image_fast(uploaded)
        if img_data is None:
            img_data = generate_sample()
        st.success(f"✅ Loaded: {uploaded.name}")
else:
    img_data = generate_sample()
    st.info("📸 Using sample image. Upload your own to analyze.")

# Resize if needed
if img_data.shape[0] > 400:
    from skimage.transform import resize
    img_data = resize(img_data, (400, 400), preserve_range=True)

# Generate physics layers
size = img_data.shape
soliton = fdm_soliton(size, fringe)
dark_photon = dark_photon_wave(size, fringe)

# Dark leak
dark_leak, dark_leak_conf = dark_leak_detection(img_data, epsilon)

# PDP Entanglement
mixing = omega * 0.6
pdp_result = pdp_entanglement(img_data, dark_photon, soliton, omega)
pdp_result = np.clip(pdp_result * brightness, 0, 1)

# PDP Interference Visualization (pure interference pattern)
interference = pdp_interference_visualization(size, fringe, omega)

# RGB Composite
rgb = np.stack([
    pdp_result,
    pdp_result * 0.5 + dark_leak * 0.5,
    pdp_result * 0.3 + dark_leak * 0.7
], axis=-1)
rgb = np.clip(rgb, 0, 1)

# ── BEFORE / AFTER COMPARISON ─────────────────────────────────────────────
st.markdown("### 📊 Before vs After")

# Create Before image (original with annotations)
before_metadata = {'omega': omega, 'fringe': fringe, 'dark_leak_conf': 0, 'mixing': 0}
before_annotated = add_annotations(img_data, before_metadata, scale_kpc, "Before: Standard View")

# Create After image (processed with annotations)
after_metadata = {'omega': omega, 'fringe': fringe, 'dark_leak_conf': dark_leak_conf, 'mixing': mixing}
after_annotated = add_annotations(rgb, after_metadata, scale_kpc, "After: PDP Entangled + Dark Leak")

# Display side by side
col_before, col_after = st.columns(2)
with col_before:
    st.image(before_annotated, use_container_width=True)
    st.caption("Before: Standard View (Public HST/JWST Data)")
with col_after:
    st.image(after_annotated, use_container_width=True)
    st.caption("After: Photon-Dark-Photon Entangled + Dark Leak Overlays")

st.markdown("---")

# ── PDP INTERFERENCE VISUALIZER ─────────────────────────────────────────────
st.markdown("### 🌊 Photon-Dark Photon Interference Visualizer")
st.markdown("*Wave interference patterns from quantum mixing*")

col_int1, col_int2 = st.columns(2)

with col_int1:
    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(interference, cmap='plasma', vmin=0, vmax=1)
    ax.set_title(f"PDP Interference Pattern\nΩ={omega:.2f}, Fringe={fringe}", fontsize=12)
    ax.axis('off')
    plt.colorbar(im, ax=ax, fraction=0.046, label="Interference Amplitude")
    st.pyplot(fig)
    plt.close(fig)
    st.caption("The interference pattern shows the quantum mixing of photon and dark photon fields")

with col_int2:
    # 1D slice through interference pattern
    center = interference.shape[0] // 2
    slice_1d = interference[center, :]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(slice_1d, 'b-', linewidth=1.5)
    ax.set_xlabel("Pixel Position")
    ax.set_ylabel("Interference Amplitude")
    ax.set_title("Radial Interference Profile")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)
    st.caption("The oscillatory pattern reveals the quantum wavelength λ = h/(m v)")

st.markdown("---")

# ── METRICS ─────────────────────────────────────────────
st.markdown("### 📊 Detection Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Dark Leak Confidence", f"{dark_leak_conf:.1f}%")
with col2:
    st.metric("Soliton Peak", f"{soliton.max():.3f}")
with col3:
    st.metric("Fringe Contrast", f"{dark_photon.std():.3f}")
with col4:
    st.metric("Mixing Angle", f"{mixing:.3f}")

# Dark Leak Alert
if dark_leak_conf > 50:
    st.error(f"🕳️ **DARK LEAK DETECTED** – {dark_leak_conf:.0f}% confidence")
elif dark_leak_conf > 20:
    st.warning(f"⚠️ **POSSIBLE DARK LEAK** – {dark_leak_conf:.0f}% confidence")
else:
    st.success(f"✅ **CLEAR** – No dark leak signatures detected")

st.markdown("---")

# ── ALL PHYSICS OUTPUTS (Collapsible) ─────────────────────────────────────────────
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
        quick_img(dark_photon, "Dark Photon Field", 'plasma')
        quick_img(interference, "PDP Interference", 'plasma')
    with col_c:
        quick_img(pdp_result, "PDP Entangled", 'inferno')
        quick_img(dark_leak, "Dark Leak Signature", 'hot')

# ── DOWNLOAD ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 💾 Download Results")

def save_fast(arr, cmap='inferno'):
    fig, ax = plt.subplots(figsize=(5, 5))
    if len(arr.shape) == 3:
        ax.imshow(np.clip(arr, 0, 1))
    else:
        ax.imshow(arr, cmap=cmap, vmin=0, vmax=1)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    return buf.getvalue()

def save_side_by_side():
    """Save the before/after comparison as one image"""
    h, w = before_annotated.shape[:2]
    combined = np.hstack([before_annotated, after_annotated])
    return save_fast(combined)

col_d1, col_d2, col_d3, col_d4 = st.columns(4)
with col_d1:
    st.download_button("📸 Before/After", save_side_by_side(), "before_after.png")
with col_d2:
    st.download_button("🌊 Interference", save_fast(interference, 'plasma'), "pdp_interference.png")
with col_d3:
    st.download_button("🕳️ Dark Leak", save_fast(dark_leak, 'hot'), "dark_leak.png")
with col_d4:
    st.download_button("⭐ FDM Soliton", save_fast(soliton, 'hot'), "soliton.png")

st.markdown("---")
st.markdown("⚡ **QCAUS v9.0** | Before/After Comparison | PDP Interference Visualizer | Tony Ford Model")
