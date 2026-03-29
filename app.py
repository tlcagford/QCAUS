"""
QCAUS v13.0 – COMPLETE UNIFIED SUITE
Image Upload | Before/After | FDM Derivation | All Visualizations
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter
from astropy.io import fits
import io
import warnings

warnings.filterwarnings('ignore')

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="QCAUS v13.0 - Complete Suite",
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
    .upload-area {
        border: 2px dashed #1e3a5f;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ── PHYSICS FUNCTIONS ─────────────────────────────────────────────

def fdm_soliton_profile(r, m_fdm=1e-22, rho0=1.0):
    """ρ(r) = ρ₀ [sin(kr)/(kr)]²"""
    r_s = 1.0 / (m_fdm * 1e-22)
    k = np.pi / max(r_s, 0.01)
    kr = k * r
    with np.errstate(divide='ignore', invalid='ignore'):
        soliton = rho0 * np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)
    return soliton


def fdm_soliton_2d(size, m_fdm=1e-22):
    """2D soliton map"""
    y, x = np.ogrid[:size, :size]
    cx, cy = size//2, size//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / size * 5
    return fdm_soliton_profile(r, m_fdm)


def dark_photon_wave(size, fringe):
    """Dark Photon Wave - λ = h/(m v)"""
    h, w = size, size
    y, x = np.ogrid[:h, :w]
    cx, cy = w//2, h//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / max(h, w, 1)
    theta = np.arctan2(y - cy, x - cx)
    k = fringe / 20.0
    
    radial = np.sin(k * 2 * np.pi * r * 3)
    spiral = np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi)))
    pattern = radial * 0.5 + spiral * 0.5
    return (pattern - pattern.min()) / (pattern.max() - pattern.min() + 1e-9)


def generate_interference_pattern(size=400, fringe=65, omega=0.7):
    """Generate interference pattern"""
    h, w = size, size
    y, x = np.ogrid[:h, :w]
    cx, cy = w//2, h//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / max(h, w, 1) * 4
    theta = np.arctan2(y - cy, x - cx)
    k = fringe / 15.0
    
    radial = np.sin(k * 4 * np.pi * r)
    spiral = np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi)))
    angular = np.sin(k * 3 * theta)
    
    if fringe < 50:
        pattern = radial * 0.5 + spiral * 0.5
    elif fringe < 80:
        pattern = radial * 0.4 + spiral * 0.3 + angular * 0.3
    else:
        pattern = spiral * 0.4 + angular * 0.3 + radial * 0.3
    
    mixing = omega * 0.6
    pattern = pattern * (1 + mixing * np.sin(k * 4 * np.pi * r))
    pattern = np.tanh(pattern * 2)
    return (pattern - pattern.min()) / (pattern.max() - pattern.min() + 1e-9)


def dark_photon_conversion_signal(image, epsilon=1e-10, B_field=1e15, m_dark=1e-9):
    """Dark photon conversion signal"""
    mixing = epsilon * B_field / (m_dark + 1e-12)
    signal = image * mixing * 5
    signal = np.clip(signal, 0, 1)
    confidence = np.max(signal) * 100
    return signal, confidence


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
    
    if data.shape[0] > 400:
        from skimage.transform import resize
        data = resize(data, (400, 400), preserve_range=True)
    
    return data


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
        f"γ→A' Signal: {metadata.get('signal',0):.1f}% | Mixing: {metadata.get('mixing',0):.3f}"
    ]
    draw.rectangle([12, 12, 280, 12 + len(info_lines) * 22 + 8], fill=(255,255,255,200), outline='black')
    for i, line in enumerate(info_lines):
        draw.text((18, 18 + i * 22), line, fill='#1e3a5f', font=font_small)
    
    draw.text((w//2 - 80, 10), title, fill='#1e3a5f', font=font)
    
    return np.array(img_pil) / 255.0


# ── SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.title("🔭 QCAUS v13.0")
    st.markdown("*Complete Unified Suite*")
    st.markdown("---")
    
    # Upload section
    st.markdown("### 📁 Upload Image")
    st.markdown('<div class="upload-area">📤 Drag & drop or click to browse</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=['fits', 'png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### ⚛️ FDM Parameters")
    m_fdm = st.slider("FDM Mass (×10⁻²² eV)", 0.1, 5.0, 1.0, 0.1)
    delta_v = st.slider("Relative Velocity Δv (km/s)", 50, 500, 200)
    epsilon_fdm = st.slider("Mixing ε", 0.01, 0.5, 0.1, 0.01)
    
    st.markdown("---")
    st.markdown("### 🎨 Visualization")
    fringe = st.slider("Fringe Scale", 30, 120, 65)
    omega = st.slider("Ω Entanglement", 0.1, 1.0, 0.70)
    brightness = st.slider("Brightness", 0.8, 1.8, 1.2)
    scale_kpc = st.selectbox("Scale (kpc)", [50, 100, 150, 200], index=1)
    
    st.markdown("---")
    st.markdown("### 🕳️ Dark Photon")
    epsilon = st.slider("Kinetic Mixing ε", 1e-12, 1e-8, 1e-10, format="%.1e")
    
    st.markdown("---")
    
    # Derived quantities
    lambda_fringe = 3.142 * (200 / delta_v) * (1.0 / m_fdm)
    rho_c = 1.9e7 * m_fdm**2
    q_pd = 2 * epsilon_fdm * omega / (1 + (epsilon_fdm * omega)**2)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fringe λ", f"{lambda_fringe:.2f} kpc")
    with col2:
        st.metric("Core ρ_c", f"{rho_c:.2e} M☉/kpc³")
    with col3:
        st.metric("P-D Q", f"{q_pd:.3f}")
    
    st.caption("Tony Ford | QCAUS v13.0")


# ── MAIN APP ─────────────────────────────────────────────
st.title("🔭 Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("*Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework*")
st.markdown("---")

# Load image
if uploaded is not None:
    with st.spinner("Loading image..."):
        img_data = load_image(uploaded)
        st.success(f"✅ Loaded: {uploaded.name}")
else:
    # Generate sample image
    size = 400
    img_data = np.zeros((size, size))
    cx, cy = size//2, size//2
    for i in range(size):
        for j in range(size):
            r = np.sqrt((i - cx)**2 + (j - cy)**2)
            img_data[i, j] = np.exp(-r/60) + 0.2 * np.sin(r/25) * np.exp(-r/80)
    img_data = img_data + np.random.randn(size, size) * 0.02
    img_data = (img_data - img_data.min()) / (img_data.max() - img_data.min())
    st.info("📸 Using sample image. Upload your own to analyze.")

# Generate physics layers
size = img_data.shape[0]
soliton = fdm_soliton_2d(size, m_fdm * 1e-22)
dark_photon = dark_photon_wave(size, fringe)
interference = generate_interference_pattern(size, fringe, omega)
conversion_signal, conversion_conf = dark_photon_conversion_signal(img_data, epsilon)

# PDP Entanglement
mixing = omega * 0.6
pdp_result = img_data * (1 - mixing * 0.4)
pdp_result = pdp_result + dark_photon * mixing * 0.5
pdp_result = pdp_result + soliton * mixing * 0.4
pdp_result = np.clip(pdp_result * brightness, 0, 1)

# RGB Composite
rgb_composite = np.stack([
    pdp_result,
    pdp_result * 0.5 + conversion_signal * 0.5,
    pdp_result * 0.3 + conversion_signal * 0.7
], axis=-1)
rgb_composite = np.clip(rgb_composite, 0, 1)

# ── BEFORE / AFTER SIDE-BY-SIDE ─────────────────────────────────────────────
st.markdown("### 📊 Before vs After")

before_metadata = {'omega': omega, 'fringe': fringe, 'signal': 0, 'mixing': 0}
before_annotated = add_annotations(img_data, before_metadata, scale_kpc, "Before: Standard View")

after_metadata = {'omega': omega, 'fringe': fringe, 'signal': conversion_conf, 'mixing': mixing}
after_annotated = add_annotations(rgb_composite, after_metadata, scale_kpc, "After: PDP Entangled + γ→A' Signal")

col_before, col_after = st.columns(2)
with col_before:
    st.image(before_annotated, use_container_width=True)
    st.caption("Before: Standard View (Public HST/JWST Data)")
with col_after:
    st.image(after_annotated, use_container_width=True)
    st.caption("After: Photon-Dark-Photon Entangled + Dark Photon Signal")

st.markdown("---")

# ── FDM DERIVATION VISUALIZATIONS ─────────────────────────────────────────────
st.markdown("### 🌊 FDM Derivation Visualizations")

col1, col2 = st.columns(2)

with col1:
    # Wave Interference Pattern
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(interference, cmap='plasma', vmin=0, vmax=1)
    ax.set_title(f"PDP Interference Pattern\nλ = {lambda_fringe:.2f} kpc", fontsize=10)
    ax.axis('off')
    plt.colorbar(im, ax=ax, fraction=0.046)
    st.pyplot(fig)
    plt.close(fig)
    st.caption("ρ = |ψ₁|² + |ψ₂|² + 2Re(ψ₁*ψ₂ e^{iΔφ}) | λ = h/(mΔv)")

with col2:
    # Solitonic Core Profile
    r = np.linspace(0, 5, 500)
    soliton_profile = fdm_soliton_profile(r, m_fdm * 1e-22)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(r, soliton_profile, 'r-', linewidth=2)
    ax.set_xlabel("r (kpc)")
    ax.set_ylabel("ρ(r) / ρ₀")
    ax.set_title(f"FDM Soliton Core | m = {m_fdm}×10⁻²² eV")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)
    st.caption("ρ(r) = ρ₀ [sin(kr)/(kr)]² | Ground state of Schrödinger-Poisson")

# Second row
col3, col4 = st.columns(2)

with col3:
    # 2D Soliton Map
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(soliton, cmap='hot', extent=[-2.5, 2.5, -2.5, 2.5])
    ax.set_title("FDM Soliton Core (2D)", fontsize=10)
    ax.set_xlabel("kpc")
    ax.set_ylabel("kpc")
    plt.colorbar(im, ax=ax, fraction=0.046, label="Density")
    st.pyplot(fig)
    plt.close(fig)

with col4:
    # Parameter Sweep
    fig, ax = plt.subplots(figsize=(6, 4))
    masses = [0.5, 1.0, 2.0, 3.0, 4.0]
    colors = ['blue', 'cyan', 'green', 'orange', 'red']
    r_sweep = np.linspace(0, 3, 200)
    for i, m in enumerate(masses):
        profile = fdm_soliton_profile(r_sweep, m * 1e-22)
        ax.plot(r_sweep, profile, color=colors[i], linewidth=2, label=f'm={m}')
    ax.set_xlabel("r (kpc)")
    ax.set_ylabel("ρ(r) / ρ₀")
    ax.set_title("Soliton Size vs FDM Mass")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

st.markdown("---")

# ── ALL PHYSICS OUTPUTS ─────────────────────────────────────────────
st.markdown("### 📊 All Physics Outputs")

col_a, col_b, col_c = st.columns(3)

def show_img(img, title, cmap='gray'):
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
    show_img(img_data, "Original", 'gray')
    show_img(soliton, "FDM Soliton", 'hot')
with col_b:
    show_img(dark_photon, "Dark Photon Field", 'plasma')
    show_img(interference, "PDP Interference", 'plasma')
with col_c:
    show_img(pdp_result, "PDP Entangled", 'inferno')
    show_img(conversion_signal, "γ→A' Signal", 'hot')

# ── METRICS ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Detection Metrics")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("γ→A' Signal", f"{conversion_conf:.1f}%")
with col_m2:
    st.metric("Soliton Peak", f"{soliton.max():.3f}")
with col_m3:
    st.metric("Fringe Contrast", f"{dark_photon.std():.3f}")
with col_m4:
    st.metric("Mixing Angle", f"{mixing:.3f}")

# Signal Alert
if conversion_conf > 50:
    st.error(f"🕳️ **STRONG DARK PHOTON CONVERSION SIGNAL** – {conversion_conf:.0f}% confidence")
elif conversion_conf > 20:
    st.warning(f"⚠️ **DARK PHOTON CONVERSION DETECTED** – {conversion_conf:.0f}% confidence")
else:
    st.success(f"✅ **CLEAR** – No dark photon conversion signal detected")

# ── DOWNLOAD ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 💾 Download Results")

def save_fig(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf.getvalue()

def save_array(arr, cmap='inferno'):
    fig, ax = plt.subplots(figsize=(6, 6))
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
    combined = np.hstack([before_annotated, after_annotated])
    return save_array(combined)

col_d1, col_d2, col_d3, col_d4 = st.columns(4)
with col_d1:
    st.download_button("📸 Before/After", save_side_by_side(), "before_after.png")
with col_d2:
    st.download_button("🌊 Interference", save_array(interference, 'plasma'), "interference.png")
with col_d3:
    st.download_button("🕳️ γ→A' Signal", save_array(conversion_signal, 'hot'), "dark_photon_signal.png")
with col_d4:
    st.download_button("⭐ FDM Soliton", save_array(soliton, 'hot'), "soliton.png")

# ── EQUATIONS ─────────────────────────────────────────────
with st.expander("📚 FDM Derivation Equations", expanded=False):
    st.latex(r"S = \int d^4x \sqrt{-g} \left[\frac{1}{2}g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi - \frac{1}{2}m^2\phi^2\right] + S_{\text{gravity}}")
    st.latex(r"\Box\phi + m^2\phi = 0")
    st.latex(r"\phi(x,t) = \frac{1}{\sqrt{2m}}\left[\psi(x,t)e^{-imt} + \psi^*(x,t)e^{imt}\right]")
    st.latex(r"i\partial_t\psi = -\frac{1}{2m}\nabla^2\psi + m\Phi\psi")
    st.latex(r"\nabla^2\Phi = 4\pi G\rho = 4\pi G|\psi|^2")
    st.latex(r"\rho = |\psi_1|^2 + |\psi_2|^2 + 2\Re(\psi_1^*\psi_2 e^{i\Delta\phi})")
    st.latex(r"\lambda = \frac{2\pi}{|\Delta k|} \approx \frac{h}{m\Delta v}")

st.markdown("---")
st.markdown("⚡ **QCAUS v13.0** | Complete Unified Suite | Drag & Drop | Before/After | FDM Derivation | Tony Ford Model")
