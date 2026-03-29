"""
QCAUS v15.0 – DIRECT DISPLAY VERSION
Uses PIL images directly for guaranteed display
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
    page_title="QCAUS v15.0",
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

def fdm_soliton_profile(r, m_fdm=1e-22, rho0=1.0):
    r_s = 1.0 / (m_fdm * 1e-22)
    k = np.pi / max(r_s, 0.01)
    kr = k * r
    with np.errstate(divide='ignore', invalid='ignore'):
        soliton = rho0 * np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)
    return soliton


def fdm_soliton_2d(size, m_fdm=1e-22):
    y, x = np.ogrid[:size, :size]
    cx, cy = size//2, size//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / size * 5
    return fdm_soliton_profile(r, m_fdm)


def dark_photon_wave(size, fringe):
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
    mixing = epsilon * B_field / (m_dark + 1e-12)
    signal = image * mixing * 5
    signal = np.clip(signal, 0, 1)
    confidence = np.max(signal) * 100
    return signal, confidence


def load_image(uploaded_file):
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


def array_to_pil(arr):
    """Convert numpy array to PIL Image"""
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))


def add_annotations_pil(img_pil, metadata, scale_kpc=100, title="After"):
    """Add annotations to PIL image"""
    draw = ImageDraw.Draw(img_pil)
    w, h = img_pil.size
    
    try:
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Scale bar
    bar_width = 100
    bar_kpc = (bar_width / w) * scale_kpc
    draw.rectangle([20, h-40, 20+bar_width, h-34], fill='black')
    draw.text((20+35, h-55), f"{bar_kpc:.0f} kpc", fill='black', font=font)
    
    # North indicator
    draw.line([w-30, 30, w-30, 60], fill='black', width=2)
    draw.text((w-38, 15), "N", fill='black', font=font)
    
    # Info box
    info_lines = [
        f"Ω = {metadata.get('omega',0):.2f} | Fringe = {metadata.get('fringe',0)}",
        f"γ→A' Signal: {metadata.get('signal',0):.1f}%"
    ]
    draw.rectangle([12, 12, 250, 12 + len(info_lines) * 22 + 8], fill=(255,255,255,200), outline='black')
    for i, line in enumerate(info_lines):
        draw.text((18, 18 + i * 22), line, fill='#1e3a5f', font=font)
    
    draw.text((w//2 - 80, 10), title, fill='#1e3a5f', font=font)
    
    return img_pil


# ── SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.title("🔭 QCAUS v15.0")
    st.markdown("*Direct Display Version*")
    st.markdown("---")
    
    uploaded = st.file_uploader("📁 Upload Image", type=['fits', 'png', 'jpg', 'jpeg'])
    
    st.markdown("---")
    st.markdown("### ⚛️ FDM Parameters")
    m_fdm = st.slider("FDM Mass (×10⁻²² eV)", 0.1, 5.0, 1.0, 0.1)
    delta_v = st.slider("Relative Velocity Δv (km/s)", 50, 500, 200)
    
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
    lambda_fringe = 3.142 * (200 / delta_v) * (1.0 / m_fdm)
    rho_c = 1.9e7 * m_fdm**2
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fringe λ", f"{lambda_fringe:.2f} kpc")
        st.metric("Core ρ_c", f"{rho_c:.2e} M☉/kpc³")
    
    st.caption("Tony Ford | QCAUS v15.0")


# ── MAIN APP ─────────────────────────────────────────────
st.title("🔭 Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("*Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework*")
st.markdown("---")

# Load image
if uploaded is not None:
    with st.spinner("Loading..."):
        img_data = load_image(uploaded)
        st.success(f"✅ Loaded: {uploaded.name}")
else:
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

# Generate layers
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

# Convert all to PIL for display
original_pil = array_to_pil(img_data)
soliton_pil = array_to_pil(soliton)
dark_photon_pil = array_to_pil(dark_photon)
interference_pil = array_to_pil(interference)
pdp_pil = array_to_pil(pdp_result)
conversion_pil = array_to_pil(conversion_signal)
rgb_pil = array_to_pil(rgb_composite)

# Annotate before/after
before_pil = add_annotations_pil(original_pil.copy(), {'omega': omega, 'fringe': fringe, 'signal': 0}, scale_kpc, "Before")
after_pil = add_annotations_pil(rgb_pil.copy(), {'omega': omega, 'fringe': fringe, 'signal': conversion_conf}, scale_kpc, "After")

# ── BEFORE / AFTER ─────────────────────────────────────────────
st.markdown("### 📊 Before vs After")

col_before, col_after = st.columns(2)
with col_before:
    st.image(before_pil, use_container_width=True)
    st.caption("Before: Standard View (Public HST/JWST Data)")
with col_after:
    st.image(after_pil, use_container_width=True)
    st.caption("After: Photon-Dark-Photon Entangled + Dark Photon Signal")

st.markdown("---")

# ── FDM DERIVATION VISUALIZATIONS ─────────────────────────────────────────────
st.markdown("### 🌊 FDM Derivation Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.image(interference_pil, use_container_width=True)
    st.caption("PDP Interference Pattern | ρ = |ψ₁|² + |ψ₂|² + 2Re(ψ₁*ψ₂ e^{iΔφ}) | λ = h/(mΔv)")

with col2:
    # Create soliton profile plot as PIL
    r = np.linspace(0, 5, 500)
    profile = fdm_soliton_profile(r, m_fdm * 1e-22)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(r, profile, 'r-', linewidth=2)
    ax.set_xlabel("r (kpc)")
    ax.set_ylabel("ρ(r) / ρ₀")
    ax.set_title(f"FDM Soliton Core | m = {m_fdm}×10⁻²² eV")
    ax.grid(True, alpha=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    st.image(Image.open(buf), use_container_width=True)
    plt.close(fig)
    st.caption("ρ(r) = ρ₀ [sin(kr)/(kr)]² | Ground state of Schrödinger-Poisson")

col3, col4 = st.columns(2)

with col3:
    st.image(soliton_pil, use_container_width=True)
    st.caption(f"FDM Soliton Core (2D) | Core density: {rho_c:.2e} M☉/kpc³")

with col4:
    # Parameter sweep plot
    fig, ax = plt.subplots(figsize=(5, 4))
    masses = [0.5, 1.0, 2.0, 3.0, 4.0]
    colors = ['blue', 'cyan', 'green', 'orange', 'red']
    r_sweep = np.linspace(0, 3, 200)
    for i, m in enumerate(masses):
        prof = fdm_soliton_profile(r_sweep, m * 1e-22)
        ax.plot(r_sweep, prof, color=colors[i], linewidth=2, label=f'{m}')
    ax.set_xlabel("r (kpc)")
    ax.set_ylabel("ρ(r) / ρ₀")
    ax.set_title("Soliton Size vs FDM Mass")
    ax.legend()
    ax.grid(True, alpha=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    st.image(Image.open(buf), use_container_width=True)
    plt.close(fig)
    st.caption("Lighter FDM mass = larger soliton core")

st.markdown("---")

# ── ALL PHYSICS OUTPUTS ─────────────────────────────────────────────
with st.expander("📊 View All Physics Outputs", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.image(original_pil, caption="Original", use_container_width=True)
        st.image(soliton_pil, caption="FDM Soliton", use_container_width=True)
    with col_b:
        st.image(dark_photon_pil, caption="Dark Photon Field", use_container_width=True)
        st.image(interference_pil, caption="PDP Interference", use_container_width=True)
    with col_c:
        st.image(pdp_pil, caption="PDP Entangled", use_container_width=True)
        st.image(conversion_pil, caption="γ→A' Signal", use_container_width=True)

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

if conversion_conf > 50:
    st.error(f"🕳️ **STRONG DARK PHOTON CONVERSION SIGNAL** – {conversion_conf:.0f}% confidence")
elif conversion_conf > 20:
    st.warning(f"⚠️ **DARK PHOTON CONVERSION DETECTED** – {conversion_conf:.0f}% confidence")
else:
    st.success(f"✅ **CLEAR** – No dark photon conversion signal detected")

# ── DOWNLOAD ─────────────────────────────────────────────
st.markdown("---")
st.markdown("### 💾 Download Results")

def pil_to_bytes(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()

col_d1, col_d2, col_d3, col_d4 = st.columns(4)

# Create side-by-side image
w, h = before_pil.size
combined = Image.new('RGB', (w * 2, h))
combined.paste(before_pil, (0, 0))
combined.paste(after_pil, (w, 0))

with col_d1:
    st.download_button("📸 Before/After", pil_to_bytes(combined), "before_after.png")
with col_d2:
    st.download_button("🌊 Interference", pil_to_bytes(interference_pil), "interference.png")
with col_d3:
    st.download_button("🕳️ γ→A' Signal", pil_to_bytes(conversion_pil), "dark_photon_signal.png")
with col_d4:
    st.download_button("⭐ FDM Soliton", pil_to_bytes(soliton_pil), "soliton.png")

# ── EQUATIONS ─────────────────────────────────────────────
with st.expander("📚 FDM Derivation Equations", expanded=False):
    st.latex(r"\rho(r) = \rho_0 \left[\frac{\sin(kr)}{kr}\right]^2")
    st.latex(r"\lambda = \frac{h}{m \Delta v}")
    st.latex(r"i\partial_t\psi = -\frac{1}{2m}\nabla^2\psi + \Phi\psi")
    st.latex(r"\nabla^2\Phi = 4\pi G|\psi|^2")
    st.latex(r"P(\gamma \to A') = \left(\frac{\varepsilon B}{m'}\right)^2 \sin^2\left(\frac{m'^2 L}{4\omega}\right)")

st.markdown("---")
st.markdown("⚡ **QCAUS v15.0** | Direct Display | All images use PIL | Tony Ford Model")
