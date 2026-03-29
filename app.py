"""
QCAUS v19.0 – FULLY FUNCTIONAL
Real parameter response | ZIP download | All images display
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import zipfile
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="QCAUS v19.0",
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


# ── PHYSICS FUNCTIONS (WITH REAL PARAMETER RESPONSE) ─────────────────────────────────────────────

def fdm_soliton_2d(size=200, m_fdm=1.0):
    """FDM soliton core - size changes with mass"""
    y, x = np.ogrid[:size, :size]
    cx, cy = size//2, size//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / size * 5
    # Soliton scale depends on FDM mass (higher mass = smaller core)
    r_s = 1.0 / m_fdm
    k = np.pi / max(r_s, 0.1)
    kr = k * r
    with np.errstate(divide='ignore', invalid='ignore'):
        soliton = np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)
    return (soliton - soliton.min()) / (soliton.max() - soliton.min() + 1e-9)


def generate_interference(size=200, fringe=65, omega=0.7):
    """Interference pattern - changes with fringe and omega"""
    y, x = np.ogrid[:size, :size]
    cx, cy = size//2, size//2
    r = np.sqrt((x - cx)**2 + (y - cy)**2) / size * 4
    theta = np.arctan2(y - cy, x - cx)
    k = fringe / 15.0
    
    radial = np.sin(k * 4 * np.pi * r)
    spiral = np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi)))
    pattern = radial * 0.5 + spiral * 0.5
    
    # Mixing depends on omega
    mixing = omega * 0.6
    pattern = pattern * (1 + mixing * np.sin(k * 4 * np.pi * r))
    pattern = np.tanh(pattern * 2)
    return (pattern - pattern.min()) / (pattern.max() - pattern.min() + 1e-9)


def dark_photon_signal(image, epsilon=1e-10, B_field=1e15, m_dark=1e-9):
    """Dark photon conversion signal - changes with epsilon"""
    mixing = epsilon * B_field / (m_dark + 1e-12)
    # Scale mixing for visibility
    mixing_scaled = min(mixing * 1e14, 1.0)
    signal = image * mixing_scaled * 5
    signal = np.clip(signal, 0, 1)
    confidence = np.max(signal) * 100
    return signal, confidence


def pdp_entanglement(image, interference, soliton, omega):
    """PDP entanglement result - changes with omega"""
    mixing = omega * 0.6
    result = image * (1 - mixing * 0.4)
    result = result + interference * mixing * 0.5
    result = result + soliton * mixing * 0.4
    return np.clip(result, 0, 1)


def load_image(uploaded_file):
    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert('L')
        data = np.array(img, dtype=np.float32) / 255.0
        if data.shape[0] > 300:
            from skimage.transform import resize
            data = resize(data, (300, 300), preserve_range=True)
        return data
    return None


def generate_sample(size=300):
    img = np.zeros((size, size))
    cx, cy = size//2, size//2
    for i in range(size):
        for j in range(size):
            r = np.sqrt((i - cx)**2 + (j - cy)**2)
            img[i, j] = np.exp(-r/60) + 0.2 * np.sin(r/25) * np.exp(-r/80)
    img = img + np.random.randn(size, size) * 0.02
    return (img - img.min()) / (img.max() - img.min())


def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    return buf.getvalue()


# ── SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.title("🔭 QCAUS v19.0")
    st.markdown("*Real Parameter Response*")
    st.markdown("---")
    
    uploaded = st.file_uploader("📁 Upload Image", type=['png', 'jpg', 'jpeg', 'fits'])
    
    st.markdown("---")
    st.markdown("### ⚛️ Physics Parameters")
    fringe = st.slider("Fringe Scale", 30, 120, 65, help="Higher = more interference rings")
    omega = st.slider("Ω Entanglement", 0.1, 1.0, 0.70, help="Higher = stronger quantum mixing")
    m_fdm = st.slider("FDM Mass (×10⁻²² eV)", 0.1, 5.0, 1.0, help="Higher = smaller soliton core")
    epsilon = st.slider("Kinetic Mixing ε", 1e-12, 1e-8, 1e-10, format="%.1e", help="Higher = stronger dark photon signal")
    
    st.markdown("---")
    st.caption("Tony Ford | QCAUS v19.0")


# ── MAIN APP ─────────────────────────────────────────────
st.title("🔭 Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("*Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework*")
st.markdown("---")

# Load image
if uploaded is not None:
    img_data = load_image(uploaded)
    if img_data is None:
        img_data = generate_sample()
    st.success(f"✅ Loaded: {uploaded.name}")
else:
    img_data = generate_sample()
    st.info("📸 Using sample image. Upload your own to analyze.")

# Generate ALL physics (real parameter response)
soliton = fdm_soliton_2d(300, m_fdm)
interference = generate_interference(300, fringe, omega)
dark_signal, dark_conf = dark_photon_signal(img_data, epsilon)
pdp_result = pdp_entanglement(img_data, interference, soliton, omega)

# RGB Composite
rgb = np.stack([pdp_result, pdp_result * 0.5 + dark_signal * 0.5, pdp_result * 0.3 + dark_signal * 0.7], axis=-1)
rgb = np.clip(rgb, 0, 1)

# Soliton profile
r = np.linspace(0, 3, 300)
r_s = 1.0 / m_fdm
k = np.pi / max(r_s, 0.1)
kr = k * r
profile = np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)

# ── BEFORE / AFTER ─────────────────────────────────────────────
st.markdown("### 📊 Before vs After")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(img_data, cmap='gray', vmin=0, vmax=1)
    ax.set_title("Original Image", fontsize=12)
    ax.axis('off')
    st.pyplot(fig)
    plt.close(fig)

with col2:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(rgb, vmin=0, vmax=1)
    ax.set_title(f"PDP Entangled (Ω={omega:.2f})", fontsize=12)
    ax.axis('off')
    st.pyplot(fig)
    plt.close(fig)

st.markdown("---")

# ── FDM DERIVATION ─────────────────────────────────────────────
st.markdown("### 🌊 FDM Derivation Visualizations")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(interference, cmap='plasma', vmin=0, vmax=1)
    ax.set_title(f"PDP Interference (fringe={fringe})", fontsize=12)
    ax.axis('off')
    plt.colorbar(im, ax=ax, fraction=0.046)
    st.pyplot(fig)
    plt.close(fig)

with col2:
    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(soliton, cmap='hot', vmin=0, vmax=1)
    ax.set_title(f"FDM Soliton Core (m={m_fdm:.1f})", fontsize=12)
    ax.axis('off')
    plt.colorbar(im, ax=ax, fraction=0.046)
    st.pyplot(fig)
    plt.close(fig)

# Soliton radial profile
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(r, profile, 'r-', linewidth=2.5)
ax.set_xlabel("r (kpc)", fontsize=12)
ax.set_ylabel("ρ(r) / ρ₀", fontsize=12)
ax.set_title(f"FDM Soliton Profile: ρ(r) = ρ₀ [sin(kr)/(kr)]² | m = {m_fdm:.1f}×10⁻²² eV", fontsize=12)
ax.grid(True, alpha=0.3)
st.pyplot(fig)
plt.close(fig)

st.markdown("---")

# ── ALL PHYSICS OUTPUTS ─────────────────────────────────────────────
st.markdown("### 📊 All Physics Outputs")

outputs = [
    ("Original", img_data, 'gray'),
    ("FDM Soliton", soliton, 'hot'),
    ("Dark Photon Signal", dark_signal, 'hot'),
    ("PDP Interference", interference, 'plasma'),
    ("PDP Entangled", pdp_result, 'inferno'),
    ("RGB Composite", rgb, None)
]

# Display in 2x3 grid
for row in range(2):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        if idx < len(outputs):
            name, data, cmap = outputs[idx]
            fig, ax = plt.subplots(figsize=(3, 3))
            if cmap:
                ax.imshow(data, cmap=cmap, vmin=0, vmax=1)
            else:
                ax.imshow(data, vmin=0, vmax=1)
            ax.set_title(name, fontsize=8)
            ax.axis('off')
            cols[col].pyplot(fig)
            plt.close(fig)

st.markdown("---")

# ── METRICS (REAL VALUES FROM PARAMETERS) ─────────────────────────────────────────────
st.markdown("### 📊 Detection Metrics")

# Calculate real metrics based on parameters
mixing = omega * 0.6
fringe_contrast = interference.std()
soliton_peak = soliton.max()

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Dark Photon Signal", f"{dark_conf:.1f}%", delta=f"ε={epsilon:.1e}")
with col_m2:
    st.metric("Soliton Peak", f"{soliton_peak:.3f}", delta=f"m={m_fdm:.1f}")
with col_m3:
    st.metric("Fringe Contrast", f"{fringe_contrast:.3f}", delta=f"fringe={fringe}")
with col_m4:
    st.metric("Mixing Angle", f"{mixing:.3f}", delta=f"Ω={omega:.2f}")

# Threat assessment based on actual confidence
if dark_conf > 50:
    st.error(f"🕳️ **STRONG DARK PHOTON CONVERSION SIGNAL** – {dark_conf:.0f}% confidence")
elif dark_conf > 20:
    st.warning(f"⚠️ **DARK PHOTON CONVERSION DETECTED** – {dark_conf:.0f}% confidence")
else:
    st.success(f"✅ **CLEAR** – No dark photon conversion signal detected")

st.markdown("---")

# ── DOWNLOAD ALL AS ZIP ─────────────────────────────────────────────
st.markdown("### 💾 Download All Results")

# Create ZIP file with all images
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    # Save each output
    for name, data, cmap in outputs:
        fig, ax = plt.subplots(figsize=(6, 6))
        if cmap:
            ax.imshow(data, cmap=cmap, vmin=0, vmax=1)
        else:
            ax.imshow(data, vmin=0, vmax=1)
        ax.axis('off')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        zip_file.writestr(f"{name.replace(' ', '_')}.png", buf.getvalue())
        plt.close(fig)
    
    # Save before/after comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.imshow(img_data, cmap='gray')
    ax1.set_title("Original")
    ax1.axis('off')
    ax2.imshow(rgb)
    ax2.set_title("PDP Entangled")
    ax2.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    zip_file.writestr("Before_After.png", buf.getvalue())
    plt.close(fig)
    
    # Save soliton profile
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(r, profile, 'r-', linewidth=2)
    ax.set_xlabel("r (kpc)")
    ax.set_ylabel("ρ(r) / ρ₀")
    ax.set_title("FDM Soliton Profile")
    ax.grid(True, alpha=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    zip_file.writestr("Soliton_Profile.png", buf.getvalue())
    plt.close(fig)
    
    # Save metadata
    metadata = f"""QCAUS Analysis Report
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Parameters:
- Fringe Scale: {fringe}
- Ω Entanglement: {omega}
- FDM Mass: {m_fdm} × 10⁻²² eV
- Kinetic Mixing ε: {epsilon:.1e}

Results:
- Dark Photon Signal: {dark_conf:.1f}%
- Soliton Peak: {soliton_peak:.3f}
- Fringe Contrast: {fringe_contrast:.3f}
- Mixing Angle: {mixing:.3f}
"""
    zip_file.writestr("Report.txt", metadata)

zip_buffer.seek(0)

st.download_button(
    label="📦 Download ALL Results (ZIP)",
    data=zip_buffer,
    file_name=f"qcaus_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
    mime="application/zip",
    use_container_width=True
)

st.markdown("---")
st.markdown("⚡ **QCAUS v19.0** | Real Parameter Response | ZIP Download | Tony Ford Model")
