"""
QCAUS v20.0 – Quantum Cosmology & Astrophysics Unified Suite
Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026

FULL REPLACEMENT APP FILE (FIXED)
- Fixed NameError (WAVE_HTML removed – replaced with clean matplotlib wave demo)
- Added os.makedirs("output") so all saves work
- Infographics on EVERY image + polished Before/After composite
- ZIP download of all annotated images
- 100% self-contained – no missing variables
"""

import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import io, zipfile, warnings, os
from datetime import datetime
from scipy.fft import fft2, ifft2, fftshift
from scipy.ndimage import gaussian_filter, convolve, uniform_filter

warnings.filterwarnings("ignore")

# Create output folder automatically
os.makedirs("output", exist_ok=True)

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="QCAUS v20.0",
    page_icon="🔭",
    initial_sidebar_state="expanded",
)
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f5f7fb; }
[data-testid="stSidebar"]          { background: #ffffff; border-right: 1px solid #e0e4e8; }
.stTitle, h1, h2, h3               { color: #1e3a5f; }
[data-testid="stMetricValue"]      { color: #1e3a5f; }
.stDownloadButton button           { background-color:#1e3a5f; color:white; border-radius:8px; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
#  FULL INFOGRAPHICS ENGINE (same as before)
# =============================================================================
def qcaus_full_infographic(
    img_input: np.ndarray | Image.Image,
    title: str,
    metrics: dict[str, str],
    scale_kpc_per_pixel: float | None = None,
    legend_items: list[tuple[tuple[int,int,int], str]] | None = None
) -> Image.Image:
    if isinstance(img_input, np.ndarray):
        if img_input.ndim == 2:
            img_input = np.stack([img_input]*3, axis=-1)
        arr = (img_input.clip(0,1) * 255).astype(np.uint8)
        img = Image.fromarray(arr)
    else:
        img = img_input.convert("RGB").copy()

    w, h = img.size
    if w > 800:
        ratio = 800 / w
        img = img.resize((800, int(h*ratio)), Image.Resampling.LANCZOS)
        w, h = img.size

    draw = ImageDraw.Draw(img)

    try:
        font_l = ImageFont.truetype("arial.ttf", 34)
        font_m = ImageFont.truetype("arial.ttf", 24)
        font_s = ImageFont.truetype("arial.ttf", 18)
    except:
        font_l = ImageFont.load_default(size=34)
        font_m = ImageFont.load_default(size=24)
        font_s = ImageFont.load_default(size=18)

    banner = Image.new("RGBA", (w, 95), (0,0,0,0))
    bd = ImageDraw.Draw(banner)
    bd.rectangle([0,0,w,95], fill=(0,0,0,210))
    img.paste(banner, (0,0), banner)

    draw.text((30, 18), title, fill=(255,255,255), font=font_l)

    metrics_txt = "\n".join(f"{k}: {v}" for k,v in metrics.items())
    panel_x = w - 400
    draw.rectangle([panel_x, 18, w-20, 88], fill=(0,0,0,230), outline=(0,255,140), width=4)
    draw.text((panel_x+20, 24), metrics_txt, fill=(0,255,140), font=font_m)

    if scale_kpc_per_pixel:
        bar_px = 220
        bar_kpc = bar_px * scale_kpc_per_pixel
        y = h - 72
        draw.line([(40, y), (40+bar_px, y)], fill=(255,255,255), width=10)
        draw.text((42, y+18), f"{bar_kpc:.1f} kpc", fill=(255,255,255), font=font_s)

    if legend_items:
        y = h - 130
        for i, (color, label) in enumerate(legend_items):
            draw.rectangle([(w-280, y+i*34), (w-250, y+i*34+26)], fill=color)
            draw.text((w-240, y+i*34+3), label, fill=(255,255,255), font=font_s)

    draw.text((w-410, h-34), f"QCAUS v20.0 • {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
              fill=(170,170,170), font=font_s)

    return img


def qcaus_before_after_composite(before_img: Image.Image, after_img: Image.Image, metrics: dict) -> Image.Image:
    w, h = before_img.size
    comp = Image.new("RGB", (w*2 + 40, h + 200), (15,15,35))

    comp.paste(before_img, (0, 0))
    comp.paste(after_img, (w + 40, 0))

    draw = ImageDraw.Draw(comp)
    try:
        f_big = ImageFont.truetype("arial.ttf", 38)
        f_med = ImageFont.truetype("arial.ttf", 24)
    except:
        f_big = ImageFont.load_default(size=38)
        f_med = ImageFont.load_default(size=24)

    draw.text((40, 15), "BEFORE — Raw HST/JWST", fill=(255,255,255), font=f_big)
    draw.text((w+80, 15), "AFTER — QCAUS PDP+FDM Enhanced", fill=(0,255,140), font=f_big)

    metrics_txt = "\n".join(f"• {k}: {v}" for k,v in metrics.items())
    draw.text((40, h+35), metrics_txt, fill=(200,255,200), font=f_med)

    return comp


# =============================================================================
#  PHYSICS LAYER  (unchanged)
# =============================================================================
def fdm_soliton_2d(size: int = 300, m_fdm: float = 1.0) -> np.ndarray:
    y, x = np.ogrid[:size, :size]
    cx, cy = size // 2, size // 2
    r   = np.sqrt((x - cx)**2 + (y - cy)**2) / size * 5
    r_s = 1.0 / m_fdm
    k   = np.pi / max(r_s, 0.1)
    kr  = k * r
    with np.errstate(divide="ignore", invalid="ignore"):
        sol = np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)
    mn, mx = sol.min(), sol.max()
    return (sol - mn) / (mx - mn + 1e-9)


def generate_interference(size: int = 300, fringe: float = 65, omega: float = 0.7) -> np.ndarray:
    y, x = np.ogrid[:size, :size]
    cx, cy = size // 2, size // 2
    r     = np.sqrt((x - cx)**2 + (y - cy)**2) / size * 4
    theta = np.arctan2(y - cy, x - cx)
    k     = fringe / 15.0
    pat   = np.sin(k * 4 * np.pi * r) * 0.5 + np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi))) * 0.5
    pat   = pat * (1 + omega * 0.6 * np.sin(k * 4 * np.pi * r))
    pat   = np.tanh(pat * 2)
    return (pat - pat.min()) / (pat.max() - pat.min() + 1e-9)


def dark_photon_signal(image: np.ndarray, epsilon: float = 1e-10, B_field: float = 1e15, m_dark: float = 1e-9) -> tuple:
    mixing  = epsilon * B_field / (m_dark + 1e-12)
    mscaled = min(mixing * 1e14, 1.0)
    sig     = np.clip(image * mscaled * 5, 0, 1)
    return sig, float(sig.max() * 100)


def pdp_entanglement(image, interference, soliton, omega) -> np.ndarray:
    m = omega * 0.6
    return np.clip(image * (1 - m * 0.4) + interference * m * 0.5 + soliton * m * 0.4, 0, 1)


def spectral_duality_filter(image: np.ndarray, omega: float = 0.5, fringe_scale: float = 1.0, mixing_angle: float = 0.1, dark_photon_mass: float = 1e-9) -> tuple:
    rows, cols = image.shape
    fft_s = fftshift(fft2(image))
    x = np.linspace(-1, 1, cols)
    y = np.linspace(-1, 1, rows)
    X, Y = np.meshgrid(x, y)
    R    = np.sqrt(X**2 + Y**2)
    L    = 100.0 / max(dark_photon_mass * 1e9, 1e-6)
    osc  = np.sin(2 * np.pi * R * L / max(fringe_scale, 0.1))
    dmm  = (mixing_angle * np.exp(-omega * R**2) * np.abs(osc) * (1 - np.exp(-R**2 / max(fringe_scale, 0.1))))
    omm  = np.exp(-R**2 / max(fringe_scale, 0.1)) - dmm
    dark_mode     = np.abs(ifft2(fftshift(fft_s * dmm)))
    ordinary_mode = np.abs(ifft2(fftshift(fft_s * omm)))
    return ordinary_mode, dark_mode


def entanglement_residuals(image, ordinary, dark, strength: float = 0.3, mixing_angle: float = 0.1, fringe_scale: float = 1.0) -> np.ndarray:
    eps   = 1e-10
    tp    = np.sum(image**2) + eps
    rho   = np.maximum(ordinary**2 / tp, eps)
    S     = -rho * np.log(rho)
    xterm = (np.abs(ordinary + dark)**2 - ordinary**2 - dark**2) / tp
    res   = S * strength + np.abs(xterm) * mixing_angle
    ks = max(3, int(fringe_scale))
    if ks % 2 == 0: ks += 1
    kernel = np.outer(np.hanning(ks), np.hanning(ks))
    return convolve(res, kernel / kernel.sum(), mode="constant")


def stealth_probability(dark_mode, residuals, entanglement_strength: float = 0.3) -> np.ndarray:
    dark_ev = dark_mode / (dark_mode.mean() + 0.1)
    lm      = uniform_filter(residuals, size=5)
    res_ev  = lm / (lm.mean() + 0.1)
    prior   = entanglement_strength
    lhood   = dark_ev * res_ev
    prob    = prior * lhood / (prior * lhood + (1 - prior) + 1e-10)
    return np.clip(gaussian_filter(prob, sigma=1.0), 0, 1)


def blue_halo_fusion(image, dark_mode, residuals) -> np.ndarray:
    def pnorm(a):
        mn, mx = a.min(), a.max()
        return np.sqrt((a - mn) / (mx - mn + 1e-10))
    rn, dn, en = pnorm(image), pnorm(dark_mode), pnorm(residuals)
    kernel = np.ones((5, 5)) / 25
    lm     = convolve(en, kernel, mode="constant")
    en_enh = np.clip(en * (1 + 2 * np.abs(en - lm)), 0, 1)
    rgb    = np.stack([rn, en_enh, np.clip(gaussian_filter(dn, 2.0) + 0.3 * dn, 0, 1)], axis=-1)
    return np.clip(rgb ** 0.45, 0, 1)


def magnetar_fields(size: int = 300, B0: float = 1e15, mixing_angle: float = 0.1) -> tuple:
    B_CRIT = 4.414e13
    y, x   = np.ogrid[:size, :size]
    cx, cy = size // 2, size // 2
    dx = (x - cx) / (size / 4)
    dy = (y - cy) / (size / 4)
    r     = np.sqrt(dx**2 + dy**2) + 0.1
    theta = np.arctan2(dy, dx)
    B_mag = (B0 / r**3) * np.sqrt(3 * np.cos(theta)**2 + 1)
    B_n   = np.clip(B_mag / B_mag.max(), 0, 1)
    qed   = (B_mag / B_CRIT)**2
    qed_n = np.clip(qed / (qed.max() + 1e-30), 0, 1)
    m_eff = 1e-9
    conv  = (mixing_angle**2) * (1 - np.exp(-B_mag**2 / (m_eff**2 + 1e-30) * 1e-26))
    conv_n = np.clip(conv / (conv.max() + 1e-30), 0, 1)
    return B_n, qed_n, conv_n


def load_image(f):
    if f is None:
        return None
    img  = Image.open(f).convert("L")
    data = np.array(img, dtype=np.float32) / 255.0
    if max(data.shape) > 300:
        img2 = Image.fromarray((data * 255).astype(np.uint8)).resize((300, 300), Image.LANCZOS)
        data = np.array(img2, dtype=np.float32) / 255.0
    return data


def generate_sample(size: int = 300) -> np.ndarray:
    cx, cy = size // 2, size // 2
    ii, jj = np.mgrid[:size, :size]
    r   = np.sqrt((ii - cx)**2 + (jj - cy)**2)
    img = np.exp(-r / 60) + 0.2 * np.sin(r / 25) * np.exp(-r / 80)
    img += np.random.RandomState(42).randn(size, size) * 0.02
    return np.clip((img - img.min()) / (img.max() - img.min()), 0, 1)


# =============================================================================
#  STREAMLIT UI
# =============================================================================
st.title("🔭 QCAUS v20.0 — Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("**Infographics enabled on every image + Before/After composite**")

with st.sidebar:
    st.header("Parameters")
    omega = st.slider("Entanglement ω", 0.1, 1.0, 0.7, 0.01)
    fringe = st.slider("Fringe scale", 10, 120, 65, 1)
    epsilon = st.slider("Kinetic mixing ε", 1e-12, 1e-8, 1e-10, 1e-12, format="%.1e")
    m_fdm = st.slider("FDM mass m (10⁻²² eV)", 0.1, 10.0, 1.0, 0.1)
    scale_kpc = st.number_input("Scale (kpc/px)", value=0.42, step=0.01)
    uploaded = st.file_uploader("Upload FITS/JPEG/PNG", type=["fits","jpg","jpeg","png","bmp"])

    if st.button("Run Full QCAUS Pipeline"):
        st.session_state["run"] = True

if "run" in st.session_state or uploaded is not None:
    if uploaded is not None:
        img_data = load_image(uploaded)
    else:
        img_data = generate_sample()

    soliton = fdm_soliton_2d(m_fdm=m_fdm)
    interference = generate_interference(omega=omega, fringe=fringe)
    dp_signal, dark_conf = dark_photon_signal(img_data, epsilon=epsilon)
    rgb = pdp_entanglement(img_data, interference, soliton, omega)

    ordinary, dark_mode = spectral_duality_filter(img_data, omega=omega)
    ent_res = entanglement_residuals(img_data, ordinary, dark_mode)
    stealth = stealth_probability(dark_mode, ent_res)
    blue_halo = blue_halo_fusion(img_data, dark_mode, ent_res)
    B_n, qed_n, conv_n = magnetar_fields()

    metrics = {
        "FDM Max Density": f"{soliton.max():.3f}",
        "PDP Mixing Ratio": f"{omega:.3f}",
        "Min Entropy": f"{ent_res.min():.2f}",
        "Dark Photon Conf.": f"{dark_conf:.1f}%",
        "Scale": f"{scale_kpc:.2f} kpc/px"
    }

    legend = [
        ((0, 255, 0),   "FDM Soliton"),
        ((0, 100, 255), "PDP Entanglement"),
        ((255, 80, 80), "Original Signal")
    ]

    st.markdown("### Before vs After — Full Infographic Composite")
    before_ann = qcaus_full_infographic(img_data, "BEFORE — Raw Data", metrics, scale_kpc, legend)
    after_ann  = qcaus_full_infographic(rgb, "AFTER — QCAUS Enhanced", metrics, scale_kpc, legend)
    composite  = qcaus_before_after_composite(before_ann, after_ann, metrics)

    st.image(composite, use_container_width=True)
    composite.save("output/composite_before_after_infographic.png")

    st.markdown("### Additional Annotated Maps")
    col1, col2, col3 = st.columns(3)

    with col1:
        soliton_ann = qcaus_full_infographic(soliton, "FDM SOLITON MAP", metrics, legend_items=[((0,255,0),"FDM Density")])
        st.image(soliton_ann, use_container_width=True)
        soliton_ann.save("output/fdm_soliton_infographic.png")

    with col2:
        pdp_ann = qcaus_full_infographic(ent_res, "PDP ENTANGLEMENT MAP", metrics, legend_items=[((0,100,255),"PDP Halo")])
        st.image(pdp_ann, use_container_width=True)
        pdp_ann.save("output/pdp_entanglement_infographic.png")

    with col3:
        stealth_ann = qcaus_full_infographic(stealth, "STEALTH PROBABILITY MAP", metrics, legend_items=[((255,100,0),"Stealth Mode")])
        st.image(stealth_ann, use_container_width=True)
        stealth_ann.save("output/stealth_infographic.png")

    st.markdown("### Blue Halo Fusion & Magnetar Fields")
    colA, colB = st.columns(2)
    with colA:
        halo_ann = qcaus_full_infographic(blue_halo, "BLUE HALO FUSION", metrics)
        st.image(halo_ann, use_container_width=True)
        halo_ann.save("output/blue_halo_infographic.png")
    with colB:
        mag_ann = qcaus_full_infographic(B_n, "MAGNETAR B-FIELD", metrics, legend_items=[((255,0,0),"B-Field")])
        st.image(mag_ann, use_container_width=True)
        mag_ann.save("output/magnetar_infographic.png")

    if st.button("📦 Download All Infographic Images as ZIP"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as z:
            for fname in [
                "composite_before_after_infographic.png",
                "fdm_soliton_infographic.png",
                "pdp_entanglement_infographic.png",
                "stealth_infographic.png",
                "blue_halo_infographic.png",
                "magnetar_infographic.png"
            ]:
                z.write(f"output/{fname}", fname)
        zip_buffer.seek(0)
        st.download_button("⬇️ Download QCAUS_Infographics.zip", zip_buffer, "QCAUS_Infographics.zip", "application/zip")

    st.success("✅ All images now have full infographics + composite saved!")

    # ── REPLACED WAVE PANEL (simple matplotlib demo – no NameError) ─────────────
    st.markdown("### FDM Wave Interference")
    fig, ax = plt.subplots(figsize=(10, 4))
    t = np.linspace(0, 10, 500)
    wave1 = np.sin(2 * np.pi * t * 0.5) * np.exp(-0.1 * t)
    wave2 = np.sin(2 * np.pi * t * 0.7 + omega * np.pi) * np.exp(-0.1 * t)
    ax.plot(t, wave1, label="ψ_light", color="#9b7cf6", linewidth=2)
    ax.plot(t, wave2, label="ψ_dark", color="#4ecdc4", linewidth=2)
    ax.plot(t, wave1 + wave2, label="|ψ|² interference", color="#f06292", linewidth=2)
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"FDM Wave Interference (ω = {omega:.2f})")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

st.caption("QCAUS v20.0 — Infographics fully enabled on every image")
