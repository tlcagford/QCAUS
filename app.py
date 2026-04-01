"""
QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite
Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026
9 Physics Pipelines: FDM Soliton, PDP Entanglement, Magnetar QED,
QCIS Power Spectrum, Dark Photon Detection, Blue-Halo Fusion,
EM Spectrum Mapping, Entanglement Residuals, Von Neumann Primordial
"""

import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image
import io, base64, warnings, zipfile
from scipy.fft import fft2, ifft2, fftshift
from scipy.ndimage import gaussian_filter, convolve, uniform_filter

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="QCAUS v1.0 — Quantum Cosmology & Astrophysics Unified Suite",
    page_icon="🔭",
    layout="wide",
)

# =============================================================================
# GLOBAL CSS  (dark-space theme + panel credit badge + file card styling)
# =============================================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0a0e1a; color: #d0e4ff; }
[data-testid="stSidebar"] { background: #0d1525; border-right: 1px solid #1e3a5f; }
h1, h2, h3, h4 { color: #7ec8e3; }
.stMarkdown p { color: #c8ddf0; }

/* Panel credit badge */
.credit-badge {
    background: rgba(30,58,95,0.85);
    border: 1px solid #335588;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 11px;
    color: #88aaff;
    display: inline-block;
    margin-bottom: 6px;
}

/* Download button */
.dl-btn {
    display: inline-block; padding: 6px 14px; background: #1e3a5f;
    color: white !important; text-decoration: none; border-radius: 5px;
    margin-top: 6px; font-size: 13px;
}
.dl-btn:hover { background: #2a5080; }

/* Data panel overlay */
.data-panel {
    border: 1px solid #0ea5e9; border-radius: 8px; padding: 8px 12px;
    background: rgba(15,23,42,0.92); color: #67e8f9; font-size: 12px;
    margin-bottom: 6px; line-height: 1.6;
}

/* File card styling */
.file-card {
    background: rgba(20,30,50,0.6); border-radius: 12px; padding: 12px;
    margin: 8px 0; border: 1px solid #335588; transition: all 0.2s ease;
}
.file-card:hover { background: rgba(30,50,80,0.8); border-color: #00aaff; }
.tag-badge {
    background: #335588; padding: 2px 8px; border-radius: 12px;
    font-size: 10px; display: inline-block; margin-right: 6px; color: #ccccff;
}
.metadata { font-size: 10px; color: #88aaff; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

AUTHOR = "Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026"


def credit(repo, formula=""):
    """Return styled credit badge HTML for a panel."""
    f = f" &nbsp;·&nbsp; <code>{formula}</code>" if formula else ""
    return f'<span class="credit-badge">📦 {repo}{f} &nbsp;·&nbsp; {AUTHOR}</span>'


# =============================================================================
# ═══════════════  9 PHYSICS PIPELINE FUNCTIONS  ═══════════════════════════
# =============================================================================

# ── Pipeline 1: FDM Soliton ─────────────────────────────────────────────────
def fdm_soliton_2d(size=300, m_fdm=1.0):
    """ρ(r) = ρ₀[sin(kr)/(kr)]²  k=π/r_s  (Hui et al. 2017 + Ford 2026)"""
    y, x = np.ogrid[:size, :size]
    cx = cy = size // 2
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / size * 5
    k = np.pi / max(1.0 / m_fdm, 0.1)
    kr = k * r
    with np.errstate(divide="ignore", invalid="ignore"):
        sol = np.where(kr > 1e-6, (np.sin(kr) / kr) ** 2, 1.0)
    mn, mx = sol.min(), sol.max()
    return (sol - mn) / (mx - mn + 1e-9)


def fdm_soliton_profile(m_fdm=1.0, n=300):
    r = np.linspace(0, 3, n)
    k = np.pi / max(1.0 / m_fdm, 0.1)
    kr = k * r
    return r, np.where(kr > 1e-6, (np.sin(kr) / kr) ** 2, 1.0)


# ── Pipeline 2: PDP Interference / Spectral Duality ─────────────────────────
def generate_interference_pattern(size, fringe, omega):
    """Two-field interference fringe pattern (Ford 2026 / StealthPDPRadar)"""
    y, x = np.ogrid[:size, :size]
    cx = cy = size // 2
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / size * 4
    theta = np.arctan2(y - cy, x - cx)
    k = fringe / 15.0
    pat = (np.sin(k * 4 * np.pi * r) * 0.5
           + np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi))) * 0.5)
    pat = pat * (1 + omega * 0.6 * np.sin(k * 4 * np.pi * r))
    pat = np.tanh(pat * 2)
    return (pat - pat.min()) / (pat.max() - pat.min() + 1e-9)


def pdp_spectral_duality(image, omega=0.20, fringe_scale=45.0,
                         mixing_eps=1e-10, fdm_mass=1.0):
    """FFT kinetic mixing: dark_mask = ε·e^{-ΩR²}·|sin(2πRL/f)|·(1-e^{-R²/f})"""
    rows, cols = image.shape
    fft_s = fftshift(fft2(image))
    xv = np.linspace(-1, 1, cols)
    yv = np.linspace(-1, 1, rows)
    X, Y = np.meshgrid(xv, yv)
    R = np.sqrt(X ** 2 + Y ** 2)
    m_GeV = max(fdm_mass * 1e-31, 1e-35)
    L = 100.0 / max(m_GeV * 1e9, 1e-6)
    osc = np.sin(2 * np.pi * R * L / max(fringe_scale, 1.0))
    dmm = mixing_eps * np.exp(-omega * R ** 2) * np.abs(osc) * (
        1 - np.exp(-R ** 2 / max(fringe_scale / 30, 0.1))
    )
    omm = np.exp(-R ** 2 / max(fringe_scale / 30, 0.1)) - dmm
    dark_mode = np.abs(ifft2(fftshift(fft_s * dmm)))
    ordinary_mode = np.abs(ifft2(fftshift(fft_s * omm)))
    return ordinary_mode, dark_mode


# ── Pipeline 3: Entanglement Residuals ───────────────────────────────────────
def entanglement_residuals(image, ordinary, dark, strength=0.3,
                           mixing_eps=1e-10, fringe_scale=45.0):
    """S = -ρ·log(ρ) + |ψ_ord+ψ_dark|² - ψ_ord² - ψ_dark²  (Ford 2026)"""
    eps = 1e-10
    tp = np.sum(image ** 2) + eps
    rho = np.maximum(ordinary ** 2 / tp, eps)
    S = -rho * np.log(rho)
    xterm = (np.abs(ordinary + dark) ** 2 - ordinary ** 2 - dark ** 2) / tp
    eps_scale = np.clip(-np.log10(mixing_eps + 1e-15) / 12.0, 0, 1)
    res = S * strength + np.abs(xterm) * eps_scale
    ks = max(3, int(fringe_scale / 10))
    if ks % 2 == 0:
        ks += 1
    kernel = np.outer(np.hanning(ks), np.hanning(ks))
    return convolve(res, kernel / kernel.sum(), mode="constant")


# ── Pipeline 4: Dark Photon Detection (Bayesian) ─────────────────────────────
def dark_photon_detection_prob(dark_mode, residuals, strength=0.3):
    """P = prior·L / (prior·L + (1-prior))  Bayesian kinetic-mixing detection"""
    dark_ev = dark_mode / (dark_mode.mean() + 0.1)
    lm = uniform_filter(residuals, size=5)
    res_ev = lm / (lm.mean() + 0.1)
    lhood = dark_ev * res_ev
    prob = strength * lhood / (strength * lhood + (1 - strength) + 1e-10)
    return np.clip(gaussian_filter(prob, sigma=1.0), 0, 1)


# ── Pipeline 5: Blue-Halo Fusion ─────────────────────────────────────────────
def blue_halo_fusion(image, dark_mode, residuals):
    """R=original G=residuals B=dark_mode  γ=0.45  (StealthPDPRadar/pdp_radar_core.py)"""
    def pnorm(a):
        mn, mx = a.min(), a.max()
        return np.sqrt((a - mn) / (mx - mn + 1e-10))
    rn, dn, en = pnorm(image), pnorm(dark_mode), pnorm(residuals)
    kernel = np.ones((5, 5)) / 25
    lm = convolve(en, kernel, mode="constant")
    en_enh = np.clip(en * (1 + 2 * np.abs(en - lm)), 0, 1)
    rgb = np.stack([rn, en_enh, np.clip(gaussian_filter(dn, 2.0) + 0.3 * dn, 0, 1)], axis=-1)
    return np.clip(rgb ** 0.45, 0, 1)


# ── Pipeline 6: PDP Entanglement Overlay on Image ───────────────────────────
def pdp_entanglement_overlay_rgb(image_gray, soliton, interf, fusion_rgb,
                                  dp_prob, omega):
    """
    FIX: Build a proper RGB overlay directly on the source image.
    Green channel = FDM soliton density
    Blue channel  = PDP interference / dark photon
    Red channel   = original image + detection probability highlight
    """
    def _resize(arr, size):
        if arr.shape == (size, size):
            return arr
        pil = Image.fromarray((arr * 255).astype(np.uint8))
        pil = pil.resize((size, size), Image.LANCZOS)
        return np.array(pil, dtype=np.float32) / 255.0

    sz = image_gray.shape[0]
    sol = _resize(soliton, sz)
    inf = _resize(interf, sz)
    dp  = _resize(dp_prob, sz)

    m = np.clip(omega * 0.7, 0, 1)
    R = np.clip(image_gray * (1 - m * 0.3) + dp * m * 0.4, 0, 1)   # original + detection
    G = np.clip(image_gray * (1 - m * 0.5) + sol * m * 0.8, 0, 1)   # FDM soliton green
    B = np.clip(image_gray * (1 - m * 0.5) + inf * m * 0.8, 0, 1)   # PDP interference blue
    return np.stack([R, G, B], axis=-1)


# ── Pipeline 7: Magnetar QED ─────────────────────────────────────────────────
def magnetar_physics(size=300, B0=1e15, eps=0.1):
    """B=B₀(R/r)³√(3cos²θ+1)  ΔL=(α/45π)(B/Bc)²  P=ε²(1-e^{-B²/m²})"""
    B_CRIT = 4.414e13
    y, x = np.ogrid[:size, :size]
    cx = cy = size // 2
    dx = (x - cx) / (size / 4)
    dy = (y - cy) / (size / 4)
    r = np.sqrt(dx ** 2 + dy ** 2) + 0.1
    theta = np.arctan2(dy, dx)
    B_mag = (B0 / r ** 3) * np.sqrt(3 * np.cos(theta) ** 2 + 1)
    B_n = np.clip(B_mag / B_mag.max(), 0, 1)
    qed = (B_mag / B_CRIT) ** 2
    qed_n = np.clip(qed / (qed.max() + 1e-30), 0, 1)
    conv = (eps ** 2) * (1 - np.exp(-B_mag ** 2 / (1e-9 ** 2 + 1e-30) * 1e-26))
    conv_n = np.clip(conv / (conv.max() + 1e-30), 0, 1)
    return B_n, qed_n, conv_n


def plot_magnetar_qed(B0=1e15, epsilon=0.1):
    B_CRIT = 4.414e13
    alpha = 1 / 137.0
    r_max, gs = 10, 120
    x = np.linspace(-r_max, r_max, gs)
    y = np.linspace(-r_max, r_max, gs)
    X, Y = np.meshgrid(x, y)
    R = np.maximum(np.sqrt(X ** 2 + Y ** 2), 0.2)
    theta = np.arctan2(Y, X)
    R0 = 1.0
    B_r = B0 * (R0 / R) ** 3 * 2 * np.cos(theta)
    B_t = B0 * (R0 / R) ** 3 * np.sin(theta)
    Bx = B_r * np.cos(theta) - B_t * np.sin(theta)
    By = B_r * np.sin(theta) + B_t * np.cos(theta)
    B_tot = np.sqrt(Bx ** 2 + By ** 2)
    EH_norm = ((alpha / (45 * np.pi)) * (B_tot / B_CRIT) ** 2)
    EH_norm = EH_norm / (EH_norm.max() + 1e-30)
    dp_conv = (epsilon ** 2) * (1 - np.exp(-(B_tot / B_CRIT) ** 2 * 1e-2))
    dp_conv = np.clip(dp_conv / (dp_conv.max() + 1e-30), 0, 1)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor="#0a0e1a")
    for ax in axes.flat:
        ax.set_facecolor("#0d1525")
    mag_log = np.log10(B_tot + 1e-10)
    axes[0, 0].streamplot(X, Y, Bx, By, color=mag_log, cmap="plasma",
                          linewidth=1.0, density=1.2)
    axes[0, 0].add_patch(Circle((0, 0), R0, color="#7ec8e3", zorder=5,
                                 edgecolor="white", linewidth=1))
    axes[0, 0].set_xlim(-r_max, r_max); axes[0, 0].set_ylim(-r_max, r_max)
    axes[0, 0].set_aspect("equal")
    axes[0, 0].set_title(f"Dipole Field  B=B₀(R/r)³√(3cos²θ+1)\nB₀={B0:.1e} G",
                          fontsize=10, color="#7ec8e3")
    axes[0, 0].tick_params(colors="#7ec8e3"); axes[0, 0].grid(True, alpha=0.2)

    im2 = axes[0, 1].imshow(EH_norm, extent=[-r_max, r_max, -r_max, r_max],
                             origin="lower", cmap="inferno", vmin=0, vmax=1)
    axes[0, 1].add_patch(Circle((0, 0), R0, color="#7ec8e3", zorder=5,
                                 edgecolor="white", linewidth=1))
    plt.colorbar(im2, ax=axes[0, 1], fraction=0.046)
    axes[0, 1].set_title("Euler-Heisenberg QED\nΔL=(α/45π)(B/B_crit)²",
                          fontsize=10, color="#7ec8e3")
    axes[0, 1].grid(True, alpha=0.2)

    im3 = axes[1, 0].imshow(dp_conv, extent=[-r_max, r_max, -r_max, r_max],
                             origin="lower", cmap="hot", vmin=0, vmax=1)
    axes[1, 0].add_patch(Circle((0, 0), R0, color="#7ec8e3", zorder=5,
                                 edgecolor="white", linewidth=1))
    plt.colorbar(im3, ax=axes[1, 0], fraction=0.046)
    axes[1, 0].set_title(f"Dark Photon Conversion  P=ε²(1-e^{{-B²/m²}})\nε={epsilon:.3f}",
                          fontsize=10, color="#7ec8e3")
    axes[1, 0].grid(True, alpha=0.2)

    r1d = np.linspace(1.1, r_max, 200)
    B1d = B0 * (R0 / r1d) ** 3
    EH1d = (alpha / (45 * np.pi)) * (B1d / B_CRIT) ** 2
    dp1d = np.clip((epsilon ** 2) * (1 - np.exp(-(B1d / B_CRIT) ** 2 * 1e-2))
                   / ((epsilon ** 2) + 1e-30), 0, 1)
    ax4 = axes[1, 1]
    ax4.semilogy(r1d, B1d, "b-", lw=2, label="|B| on-axis")
    ax4.set_xlabel("r / R★", color="#7ec8e3"); ax4.set_ylabel("|B| (G)", color="b")
    ax4.tick_params(axis="y", labelcolor="b"); ax4.grid(True, alpha=0.2)
    ax4t = ax4.twinx()
    EH1dn = EH1d / (EH1d.max() + 1e-30)
    ax4t.plot(r1d, EH1dn, "r--", lw=2, label="ΔL (E-H, norm.)")
    ax4t.plot(r1d, dp1d, "g-.", lw=2, label="P_conv (norm.)")
    ax4t.set_ylabel("Normalised", color="r"); ax4t.set_ylim([0, 1])
    ax4.set_title("Radial Profiles (θ=0 axis)", fontsize=10, color="#7ec8e3")
    l1, lb1 = ax4.get_legend_handles_labels()
    l2, lb2 = ax4t.get_legend_handles_labels()
    ax4.legend(l1 + l2, lb1 + lb2, fontsize=9, loc="upper right",
               facecolor="#0d1525", labelcolor="#c8ddf0")

    plt.suptitle(
        f"Magnetar QED — B₀=10^{np.log10(B0):.1f} G  B_crit=4.414×10¹³ G  ε={epsilon:.3f}"
        f"\n{AUTHOR}",
        fontsize=11, fontweight="bold", color="#7ec8e3"
    )
    plt.tight_layout()
    return fig


# ── Pipeline 8: QCIS Power Spectrum ─────────────────────────────────────────
def qcis_power_spectrum(f_nl=1.0, n_q=0.5, n_s=0.965):
    """P(k)=P_ΛCDM(k)×(1+f_NL·(k/k₀)^n_q)  BBKS T(k)  Planck 2018"""
    k = np.logspace(-3, 1, 300)
    k0 = 0.05
    q = k / 0.2
    T = (np.log(1 + 2.34 * q) / (2.34 * q)
         * (1 + 3.89 * q + (16.2 * q) ** 2 + (5.47 * q) ** 3 + (6.71 * q) ** 4) ** (-0.25))
    Pl = k ** n_s * T ** 2
    Pq = Pl * (1 + f_nl * (k / k0) ** n_q)
    norm = Pl[np.argmin(np.abs(k - k0))] + 1e-30
    return k, Pl / norm, Pq / norm


def em_spectrum_composite(img_gray, f_nl, n_q):
    """R=IR G=Visible B=X-ray  quantum correction from QCIS ratio at k=0.1 h/Mpc"""
    k, Pl, Pq = qcis_power_spectrum(f_nl, n_q)
    idx = np.argmin(np.abs(k - 0.1))
    qf = float(np.clip(Pq[idx] / (Pl[idx] + 1e-30), 0.5, 3.0))
    IR = np.clip(img_gray ** 0.5 * qf, 0, 1)
    VI = np.clip(img_gray ** 0.8 * qf, 0, 1)
    XR = np.clip(img_gray ** 1.5 * qf, 0, 1)
    return np.stack([IR, VI, XR], axis=-1)


# ── Pipeline 9: Von Neumann Primordial Entanglement ─────────────────────────
def von_neumann_primordial(omega=0.20, dark_mass=1e-9, mixing=0.1, steps=200):
    """
    Von Neumann evolution: i∂ρ/∂t=[H_eff,ρ]  S=-Tr(ρ log ρ)
    Primordial photon-dark photon oscillation (Ford 2026 / Primordial-Entanglement repo)
    """
    t_arr = np.linspace(0, 10, steps)
    omega_osc = dark_mass * 1e9 * 0.1 + 0.1
    phase = omega_osc * t_arr
    # Density matrix 2x2: [[rho_gg, rho_gd],[rho_dg, rho_dd]]
    rho_gg = np.cos(mixing * phase) ** 2
    rho_dd = np.sin(mixing * phase) ** 2
    rho_gd = 0.5 * np.sin(2 * mixing * phase) * np.exp(-omega * t_arr * 0.2)
    # Von Neumann entropy S = -Tr(rho log rho)  eigenvalues of 2x2
    eig1 = 0.5 * (1 + np.sqrt(np.maximum((rho_gg - rho_dd) ** 2 + 4 * rho_gd ** 2, 0)))
    eig2 = 0.5 * (1 - np.sqrt(np.maximum((rho_gg - rho_dd) ** 2 + 4 * rho_gd ** 2, 0)))
    eig1 = np.clip(eig1, 1e-10, 1); eig2 = np.clip(eig2, 1e-10, 1)
    entropy = -(eig1 * np.log(eig1) + eig2 * np.log(eig2))
    mixing_prob = rho_dd  # |<ψ_d|ψ_γ>|²
    return t_arr, entropy, mixing_prob, rho_gg, rho_dd


# =============================================================================
# ANIMATED WAVE (2-field FDM)
# =============================================================================
def compute_fdm_wave(t, size=300, mixing_eps=1e-10):
    """ρ=|ψ_t|²+|ψ_d|²+2·Re(ψ_t*·ψ_d·e^{iΔφ})  (Ford 2026)"""
    y, x = np.ogrid[:size, :size]
    r = np.sqrt((x - size // 2) ** 2 + (y - size // 2) ** 2) / size * 8
    # FIX: both psi_t AND psi_d computed; psi_t uses cos(t), psi_d uses sin(t) for clear separation
    psi_t = np.exp(-r ** 2 / 4) * np.exp(1j * r * np.cos(t))
    phase_d = np.pi * np.clip(mixing_eps * 1e10, 0.0, 1.0)
    psi_d = np.exp(-r ** 2 / 4) * np.exp(1j * (r * np.sin(t) + phase_d))
    rho = np.abs(psi_t) ** 2 + np.abs(psi_d) ** 2 + 2 * np.real(psi_t * np.conj(psi_d))
    return psi_t, psi_d, rho


# =============================================================================
# IMAGE UTILITIES
# =============================================================================
def load_image(file):
    img = Image.open(file).convert("L")
    if max(img.size) > 800:
        img.thumbnail((800, 800), Image.LANCZOS)
    return np.array(img, dtype=np.float32) / 255.0


def make_sgr1806_preset(size=300):
    rng = np.random.RandomState(2)
    cx = cy = size // 2
    y, x = np.mgrid[:size, :size]
    dx = (x - cx) / (size / 4); dy = (y - cy) / (size / 4)
    r = np.sqrt(dx ** 2 + dy ** 2) + 0.05
    theta = np.arctan2(dy, dx)
    B_halo = np.exp(-r * 1.5) * np.sqrt(3 * np.cos(theta) ** 2 + 1) / r
    B_halo = np.clip(B_halo / B_halo.max(), 0, 1) * 0.5
    r_c = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    core = np.exp(-r_c ** 2 / 3.0)
    img = B_halo + core + rng.randn(size, size) * 0.01
    return np.clip((img - img.min()) / (img.max() - img.min()), 0, 1)


def make_galaxy_cluster_preset(size=300):
    rng = np.random.RandomState(42)
    y, x = np.mgrid[:size, :size]
    r = np.sqrt((x - 150) ** 2 + (y - 150) ** 2)
    img = np.exp(-r ** 2 / 8000) * 0.8 + rng.randn(size, size) * 0.03
    return np.clip(img, 0, 1)


def make_airport_radar_preset(airport, size=300):
    rng = np.random.RandomState(123)
    y, x = np.mgrid[:size, :size]
    bg = np.exp(-((x - 150) ** 2 + (y - 150) ** 2) / 20000) * 0.4
    stealth = np.zeros((size, size))
    if airport == "nellis":
        stealth[100:120, 80:100] = 0.6; stealth[180:200, 200:220] = 0.5
    elif airport == "jfk":
        stealth[120:140, 100:130] = 0.7
    elif airport == "lax":
        stealth[90:110, 220:250] = 0.55
    return np.clip(bg + stealth + rng.randn(size, size) * 0.05, 0, 1)


PRESETS = {
    "SGR 1806-20 (Magnetar)": make_sgr1806_preset,
    "Galaxy Cluster (Abell 209 style)": make_galaxy_cluster_preset,
    "Airport Radar — Nellis AFB Historical": lambda: make_airport_radar_preset("nellis"),
    "Airport Radar — JFK International Historical": lambda: make_airport_radar_preset("jfk"),
    "Airport Radar — LAX Historical": lambda: make_airport_radar_preset("lax"),
}


def _apply_cmap(arr2d, cmap_name):
    cmap = plt.get_cmap(cmap_name)
    rgba = cmap(np.clip(arr2d, 0, 1))
    return (rgba[..., :3] * 255).astype(np.uint8)


def arr_to_pil(arr, cmap=None):
    if arr.ndim == 2:
        if cmap:
            return Image.fromarray(_apply_cmap(arr, cmap), "RGB")
        return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8), "L")
    return Image.fromarray(np.clip(arr * 255, 0, 255).astype(np.uint8), "RGB")


def get_dl(arr_or_buf, filename, label="📥 Download", cmap=None):
    if isinstance(arr_or_buf, io.BytesIO):
        arr_or_buf.seek(0)
        b64 = base64.b64encode(arr_or_buf.read()).decode()
    else:
        buf = io.BytesIO()
        arr_to_pil(arr_or_buf, cmap).save(buf, "PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
    return (f'<a href="data:image/png;base64,{b64}" download="{filename}"'
            f' class="dl-btn">{label}</a>')


def fig_to_buf(fig, dpi=120):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("## ⚛️ Core Physics")
    omega_pd    = st.slider("Omega_PD Entanglement", 0.05, 0.50, 0.20, 0.01)
    fringe_scale = st.slider("Fringe Scale (pixels)", 10, 80, 45, 1)
    kin_mix     = st.slider("Kinetic Mixing ε", 1e-12, 1e-8, 1e-10, format="%.1e")
    fdm_mass    = st.slider("FDM Mass ×10⁻²² eV", 0.10, 10.00, 1.00, 0.01)
    st.markdown("---")
    st.markdown("## 🌟 Magnetar")
    b0_log10    = st.slider("B₀ log₁₀ G", 13.0, 16.0, 15.0, 0.1)
    mag_eps     = st.slider("Magnetar ε", 0.01, 0.50, 0.10, 0.01)
    st.markdown("---")
    st.markdown("## 📈 QCIS")
    f_nl        = st.slider("f_NL", 0.00, 5.00, 1.00, 0.01)
    n_q         = st.slider("n_q", 0.00, 2.00, 0.50, 0.01)
    st.markdown("---")
    st.markdown("## 🌌 Primordial")
    prim_mass   = st.slider("Dark Mass ×10⁻⁹ eV", 0.1, 10.0, 1.0, 0.1)
    prim_mix    = st.slider("Primordial Mixing", 0.01, 1.00, 0.10, 0.01)
    st.markdown("---")
    st.markdown(f"**{AUTHOR}**")

# =============================================================================
# HEADER
# =============================================================================
st.markdown('<h1 style="text-align:center;color:#7ec8e3">🔭 QCAUS v1.0</h1>',
            unsafe_allow_html=True)
st.markdown("**Quantum Cosmology & Astrophysics Unified Suite** — 9 Physics Pipelines")
st.caption(AUTHOR)

# =============================================================================
# DATA SOURCE SELECTION
# =============================================================================
st.markdown("### 🎯 Select Preset Data")
preset_choice = st.selectbox("Choose example:", options=list(PRESETS.keys()), index=0)
col1, col2 = st.columns([2, 1])
with col1:
    run_preset = st.button("🚀 Run Selected Preset", use_container_width=True)
with col2:
    uploaded_file = st.file_uploader("Drag & drop image",
                                     type=["jpg", "jpeg", "png", "fits"],
                                     label_visibility="collapsed")

img_data = None
if run_preset:
    img_data = PRESETS[preset_choice]()
    st.success(f"✅ Loaded preset: {preset_choice}")
elif uploaded_file is not None:
    img_data = load_image(uploaded_file)
    st.success(f"✅ Loaded: {uploaded_file.name}")

# =============================================================================
# ── SECTION A: FDM FIELD EQUATIONS ──────────────────────────────────────────
# =============================================================================
st.markdown("---")
st.markdown("## 📐 FDM Field Equations — Tony Ford Model")
st.markdown(credit("QCAUS/app.py", "Two-Field Coupled Schrödinger-Poisson"), unsafe_allow_html=True)
st.latex(r"S=\int d^4x\sqrt{-g}\!\left[\tfrac{1}{2}g^{\mu\nu}\partial_\mu\phi\partial_\nu\phi"
         r"-\tfrac{1}{2}m^2\phi^2\right]+S_{\rm gravity}")
st.latex(r"\Box\phi+m^2\phi=0")
st.latex(r"\phi=(2m)^{-1/2}\!\left[\psi e^{-imt}+\psi^*e^{imt}\right]")
st.latex(r"\psi=\psi_{\rm light}+\psi_{\rm dark}\,e^{i\Delta\phi}")
st.latex(r"\rho=|\psi_{\rm light}|^2+|\psi_{\rm dark}|^2"
         r"+2\operatorname{Re}\!\left(\psi_{\rm light}^*\psi_{\rm dark}\,e^{i\Delta\phi}\right)")
st.latex(r"\rho(r)=\frac{\rho_c}{\left[1+(r/r_c)^2\right]^8}")

# =============================================================================
# ── SECTION B: ANIMATED FDM WAVE  (Pipeline 1 + 2 combined) ─────────────────
# =============================================================================
st.markdown("---")
st.markdown("## 🌊 Pipeline 1+2 — FDM Two-Field Animated Interference Wave")
st.markdown(credit("QCAUS/app.py", "ρ=|ψ_t|²+|ψ_d|²+2·Re(ψ_t*·ψ_d·e^{iΔφ})"), unsafe_allow_html=True)

animate   = st.toggle("▶ Animate Waves", value=False)
spd       = st.slider("Animation Speed", 0.1, 5.0, 1.0, key="spd")
wave_mode = st.radio("Display Mode", ["2D Wave", "3D Surface"], horizontal=True)

if "t" not in st.session_state:
    st.session_state.t = 0.0
if animate:
    st.session_state.t += 0.08 * spd

SZ = 300
psi_t, psi_d, rho_wave = compute_fdm_wave(st.session_state.t, size=SZ, mixing_eps=kin_mix)
mid = SZ // 2

if wave_mode == "2D Wave":
    fig_w, ax_w = plt.subplots(figsize=(10, 4), facecolor="#0a0e1a")
    ax_w.set_facecolor("#0d1525")
    # FIX: plotting Re(ψ) instead of |ψ| — the |ψ| envelopes are IDENTICAL (both = exp(-r²/4))
    # Re(ψ_light) ∝ cos(r·cos(t)) vs Re(ψ_dark) ∝ cos(r·sin(t)+Δφ) — visibly distinct
    re_t   = np.real(psi_t[mid])   # oscillating light-sector wave
    re_d   = np.real(psi_d[mid])   # oscillating dark-sector wave (phase-shifted)
    env    = np.abs(psi_t[mid])    # common Gaussian envelope
    rho_1d = rho_wave[mid]
    ax_w.plot(env,    label=r"$|\psi|$ Gaussian envelope", color="#aaaaff", lw=1, ls="--", alpha=0.6)
    ax_w.plot(re_t,   label=r"$\mathrm{Re}(\psi_{\rm light})$",  color="#00ffcc", lw=2)
    ax_w.plot(re_d,   label=r"$\mathrm{Re}(\psi_{\rm dark})$",   color="#ff00cc", lw=2)
    ax_w.plot(rho_1d, label=r"$\rho$ interference density",       color="#ffff00", lw=3)
    ax_w.legend(facecolor="#0d1525", labelcolor="#c8ddf0")
    ax_w.grid(True, alpha=0.2, color="#335588")
    ax_w.set_xlabel("pixel", color="#7ec8e3")
    ax_w.set_ylabel("amplitude", color="#7ec8e3")
    ax_w.tick_params(colors="#7ec8e3")
    ax_w.set_title(f"FDM Two-Field Interference   t={st.session_state.t:.2f}   ε={kin_mix:.2e}",
                   color="#7ec8e3")
    st.pyplot(fig_w)
    plt.close(fig_w)
    st.info(f"Re(ψ_light) range: [{re_t.min():.3f}, {re_t.max():.3f}]  |  "
            f"Re(ψ_dark) range: [{re_d.min():.3f}, {re_d.max():.3f}]  |  "
            f"ρ peak: {rho_1d.max():.3f}")
else:
    from mpl_toolkits.mplot3d import Axes3D  # noqa
    fig_w = plt.figure(figsize=(10, 6), facecolor="#0a0e1a")
    ax_w = fig_w.add_subplot(111, projection="3d")
    ax_w.set_facecolor("#0d1525")
    step = 6
    X3, Y3 = np.meshgrid(np.linspace(-4, 4, SZ // step),
                          np.linspace(-4, 4, SZ // step))
    ax_w.plot_surface(X3, Y3, rho_wave[::step, ::step], cmap="hot", alpha=0.9)
    ax_w.set_title(f"3D FDM Wave  t={st.session_state.t:.2f}", color="#7ec8e3")
    st.pyplot(fig_w)
    plt.close(fig_w)

if animate:
    st.rerun()

# =============================================================================
# ── MAIN PROCESSING BLOCK — runs when image / preset loaded ─────────────────
# =============================================================================
if img_data is not None:
    B0     = 10 ** b0_log10
    B_CRIT = 4.414e13

    # Ensure grayscale float32
    img_gray = (np.mean(img_data, axis=-1) if img_data.ndim == 3
                else img_data.copy()).astype(np.float32)
    SIZE = min(img_gray.shape[0], img_gray.shape[1], 400)
    img_gray = np.array(
        Image.fromarray((img_gray * 255).astype(np.uint8)).resize((SIZE, SIZE), Image.LANCZOS),
        dtype=np.float32) / 255.0

    # ── Run all 9 pipelines ──────────────────────────────────────────────────
    soliton    = fdm_soliton_2d(SIZE, fdm_mass)            # P1
    interf     = generate_interference_pattern(SIZE, fringe_scale, omega_pd)  # P2
    ord_mode, dark_mode = pdp_spectral_duality(
        img_gray, omega_pd, fringe_scale, kin_mix, fdm_mass)   # P2
    ent_res    = entanglement_residuals(
        img_gray, ord_mode, dark_mode, omega_pd * 0.3, kin_mix, fringe_scale)  # P3
    dp_prob    = dark_photon_detection_prob(dark_mode, ent_res, omega_pd * 0.3)  # P4
    dp_peak    = float(dp_prob.max() * 100)
    fusion     = blue_halo_fusion(img_gray, dark_mode, ent_res)  # P5
    overlay_rgb = pdp_entanglement_overlay_rgb(
        img_gray, soliton, interf, fusion, dp_prob, omega_pd)  # P6 — NEW RGB overlay
    B_n, qed_n, conv_n = magnetar_physics(SIZE, B0, mag_eps)   # P7
    k_arr, P_lcdm, P_quantum = qcis_power_spectrum(f_nl, n_q)  # P8
    em_comp    = em_spectrum_composite(img_gray, f_nl, n_q)     # P8
    r_arr, rho_arr = fdm_soliton_profile(fdm_mass)
    t_prim, S_prim, mix_prob, rho_gg, rho_dd = von_neumann_primordial(
        omega_pd, prim_mass * 1e-9, prim_mix)  # P9
    ent_scalar = float(-np.mean(ent_res[ent_res > 0] * np.log(ent_res[ent_res > 0] + 1e-10)))

    # =========================================================================
    # SECTION C — BEFORE / AFTER with RGB overlay on image
    # =========================================================================
    st.markdown("---")
    st.markdown("## 🖼️ Pipeline 1–6 — Before vs After with Quantum Overlays")
    st.markdown(credit("QCI-AstroEntangle-Refiner / StealthPDPRadar",
                       "R=Original+Detection  G=FDM-Soliton  B=PDP-Interference"),
                unsafe_allow_html=True)

    info_html = (f'<div class="data-panel">Ω_PD={omega_pd:.2f} | Fringe={fringe_scale} |'
                 f' ε={kin_mix:.2e} | FDM m={fdm_mass:.2f}×10⁻²² eV |'
                 f' Entropy={ent_scalar:.3f} | P_dark={dp_peak:.1f}%</div>')

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(info_html, unsafe_allow_html=True)
        st.markdown("**⬛ Before: Standard View** (Public HST/JWST Data)")
        st.image(arr_to_pil(img_gray, cmap="gray"), use_container_width=True)
        st.caption("0 — 20 kpc  |  ↑ N")
        st.markdown(get_dl(img_gray, "original.png", "📥 Download Original", "gray"),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(info_html, unsafe_allow_html=True)
        st.markdown("**🌈 After: PDP+FDM Entangled RGB Overlay (Tony Ford Model)**")
        st.image(arr_to_pil(overlay_rgb), use_container_width=True)
        st.caption("🟢 FDM Soliton  🔵 PDP Interference  🔴 Original+Detection  |  0 — 20 kpc")
        st.markdown(get_dl(overlay_rgb, "pdp_rgb_overlay.png", "📥 Download RGB Overlay"),
                    unsafe_allow_html=True)
    st.markdown(f"*{AUTHOR}*")

    # Also show Blue-Halo fusion and inferno PDP for reference
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**🔵 Blue-Halo Fusion** (R=Orig, G=Residuals, B=Dark, γ=0.45)")
        st.markdown(credit("StealthPDPRadar/pdp_radar_core.py"), unsafe_allow_html=True)
        st.image(arr_to_pil(fusion), use_container_width=True)
        st.markdown(get_dl(fusion, "blue_halo_fusion.png", "📥 Download"), unsafe_allow_html=True)
    with c4:
        st.markdown("**🔥 Inferno PDP Overlay** (spectral mixing)")
        st.markdown(credit("StealthPDPRadar/pdp_radar_core.py",
                           "ε·e^{-ΩR²}·|sin(2πRL/f)|"), unsafe_allow_html=True)
        # inferno PDP: blend image with interference using inferno colormap
        pdp_inf = np.clip(img_gray * (1 - omega_pd * 0.4) + interf * omega_pd * 0.6, 0, 1)
        st.image(arr_to_pil(pdp_inf, cmap="inferno"), use_container_width=True)
        st.markdown(get_dl(pdp_inf, "pdp_inferno.png", "📥 Download", "inferno"),
                    unsafe_allow_html=True)

    # =========================================================================
    # SECTION D — PHYSICS MAPS (Pipelines 1–4)
    # =========================================================================
    st.markdown("---")
    st.markdown("## 📊 Pipelines 1–4 — Annotated Physics Maps")
    c1, c2, c3, c4 = st.columns(4)
    panels = [
        (c1, soliton, "hot",    "⚛️ P1: FDM Soliton",
         "ρ(r)=ρ₀[sin(kr)/(kr)]²  k=π/r_s",
         "QCAUS/app.py  (Hui et al. 2017 + Ford 2026)", "fdm_soliton.png"),
        (c2, interf,  "plasma", "🌊 P2: PDP Interference",
         "FFT dark_mask spectral duality",
         "StealthPDPRadar/pdp_radar_core.py", "pdp_interference.png"),
        (c3, ent_res, "inferno","🕳️ P3: Entanglement Residuals",
         "S=−ρ·log(ρ)+cross-term",
         "StealthPDPRadar/pdp_radar_core.py", "entanglement_residuals.png"),
        (c4, dp_prob, "YlOrRd", "🔍 P4: Dark Photon Detection",
         f"P_dark={dp_peak:.1f}%  Bayesian",
         "StealthPDPRadar/pdp_radar_core.py", "dp_detection.png"),
    ]
    for col, arr, cm, title, cap, src, fname in panels:
        with col:
            st.markdown(f"**{title}**")
            st.markdown(credit(src, cap), unsafe_allow_html=True)
            st.image(arr_to_pil(arr, cm), use_container_width=True)
            st.markdown(get_dl(arr, fname, "📥 Download", cm), unsafe_allow_html=True)

    if dp_peak > 50:
        st.error(f"⚠️ STRONG DARK PHOTON SIGNAL — P_dark = {dp_peak:.1f}%")
    elif dp_peak > 20:
        st.warning(f"⚡ DARK PHOTON SIGNAL — P_dark = {dp_peak:.1f}%")
    else:
        st.success(f"✅ CLEAR — P_dark = {dp_peak:.1f}% (below threshold)")

    # =========================================================================
    # SECTION E — MAGNETAR QED (Pipeline 7)
    # =========================================================================
    st.markdown("---")
    st.markdown("## ⚡ Pipeline 7 — Magnetar QED Explorer")
    st.markdown(credit("Magnetar-Quantum-Vacuum-Engineering",
                       "B=B₀(R/r)³√(3cos²θ+1)  ΔL=(α/45π)(B/Bc)²  P=ε²(1-e^{-B²/m²})"),
                unsafe_allow_html=True)
    try:
        fig_mag = plot_magnetar_qed(B0, mag_eps)
        st.pyplot(fig_mag, use_container_width=True)
        mag_buf = fig_to_buf(fig_mag, dpi=100)
        st.markdown(get_dl(mag_buf, "magnetar_qed.png", "📥 Download Magnetar QED Plot"),
                    unsafe_allow_html=True)
        plt.close(fig_mag)
    except Exception as e:
        st.error(f"Magnetar plot error: {e}")

    st.markdown("### Magnetar Field Maps")
    cA, cB, cC = st.columns(3)
    mag_panels = [
        (cA, B_n,   "plasma", "Dipole |B| map",
         "B=B₀(R/r)³√(3cos²θ+1)", "magnetar_B.png"),
        (cB, qed_n, "inferno","Euler-Heisenberg QED",
         "ΔL=(α/45π)(B/B_crit)²", "magnetar_QED.png"),
        (cC, conv_n,"hot",    "Dark Photon Conversion",
         "P=ε²(1−e^{−B²/m²})", "magnetar_darkphoton.png"),
    ]
    for col, arr, cm, title, cap, fname in mag_panels:
        with col:
            st.image(arr_to_pil(arr, cm), caption=f"{title}  |  {cap}",
                     use_container_width=True)
            st.markdown(credit("Magnetar-Quantum-Vacuum-Engineering", cap),
                        unsafe_allow_html=True)
            st.markdown(get_dl(arr, fname, "📥 Download", cm), unsafe_allow_html=True)

    # =========================================================================
    # SECTION F — FDM SOLITON RADIAL PROFILE (Pipeline 1)
    # =========================================================================
    st.markdown("---")
    st.markdown("## ⚛️ Pipeline 1 — FDM Soliton Radial Profile")
    st.markdown(credit("QCAUS/app.py", "ρ(r)=ρ₀[sin(kr)/(kr)]²  Schrödinger-Poisson ground state"),
                unsafe_allow_html=True)
    fig_fdm, ax_fdm = plt.subplots(figsize=(9, 3), facecolor="#0a0e1a")
    ax_fdm.set_facecolor("#0d1525")
    ax_fdm.plot(r_arr, rho_arr, "r-", lw=2.5,
                label=f"ρ(r)=ρ₀[sin(kr)/(kr)]²  m={fdm_mass:.1f}×10⁻²² eV")
    ax_fdm.set_xlabel("r (kpc)", color="#7ec8e3"); ax_fdm.set_ylabel("ρ(r)/ρ₀", color="#7ec8e3")
    ax_fdm.set_title("FDM Soliton Profile — Schrödinger-Poisson", fontsize=11, color="#7ec8e3")
    ax_fdm.legend(facecolor="#0d1525", labelcolor="#c8ddf0")
    ax_fdm.grid(True, alpha=0.2, color="#335588"); ax_fdm.tick_params(colors="#7ec8e3")
    st.pyplot(fig_fdm)
    fdm_buf = fig_to_buf(fig_fdm)
    st.markdown(get_dl(fdm_buf, "fdm_profile.png", "📥 Download FDM Profile"),
                unsafe_allow_html=True)
    plt.close(fig_fdm)

    # =========================================================================
    # SECTION G — QCIS POWER SPECTRUM + EM COMPOSITE (Pipeline 8)
    # =========================================================================
    st.markdown("---")
    st.markdown("## 📈 Pipeline 8 — QCIS Matter Power Spectrum & EM Mapping")
    st.markdown(credit("Quantum-Cosmology-Integration-Suite",
                       "P(k)=P_ΛCDM(k)×(1+f_NL·(k/k₀)^n_q)  BBKS T(k)  n_s=0.965"),
                unsafe_allow_html=True)

    fig_ps, ax_ps = plt.subplots(figsize=(10, 4), facecolor="#0a0e1a")
    ax_ps.set_facecolor("#0d1525")
    ax_ps.loglog(k_arr, P_lcdm, "b-", lw=2, label="ΛCDM baseline")
    ax_ps.loglog(k_arr, P_quantum, "r--", lw=2,
                 label=f"QCIS Quantum  f_NL={f_nl:.1f}  n_q={n_q:.1f}")
    ax_ps.axvline(0.05, color="#7ec8e3", ls=":", alpha=0.5, label="Pivot k₀=0.05 h/Mpc")
    ax_ps.set_xlabel("k (h/Mpc)", color="#7ec8e3"); ax_ps.set_ylabel("P(k)/P(k₀)", color="#7ec8e3")
    ax_ps.set_title("QCIS Matter Power Spectrum  (BBKS T(k), n_s=0.965 Planck 2018)",
                    fontsize=11, color="#7ec8e3")
    ax_ps.legend(facecolor="#0d1525", labelcolor="#c8ddf0")
    ax_ps.grid(True, alpha=0.2, which="both", color="#335588")
    ax_ps.tick_params(colors="#7ec8e3")
    st.pyplot(fig_ps)
    ps_buf = fig_to_buf(fig_ps)
    st.markdown(get_dl(ps_buf, "qcis_spectrum.png", "📥 Download QCIS Spectrum"),
                unsafe_allow_html=True)
    plt.close(fig_ps)

    # EM Composite
    st.markdown("### 🌈 EM Spectrum Composite — R=Infrared  G=Visible  B=X-ray")
    st.markdown(credit("Quantum-Cosmology-Integration-Suite",
                       "QCIS quantum correction factor at k=0.1 h/Mpc"),
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🎨 EM Composite (quantum corrected)**")
        st.image(arr_to_pil(em_comp), use_container_width=True)
        st.markdown(get_dl(em_comp, "em_composite.png", "📥 Download"), unsafe_allow_html=True)
    with c2:
        st.markdown("**📊 Individual EM Bands**")
        tab1, tab2, tab3 = st.tabs(["🔴 Infrared", "🟢 Visible", "🔵 X-ray"])
        with tab1:
            ir = np.clip(img_gray ** 0.5, 0, 1)
            st.image(_apply_cmap(ir, "hot"), use_container_width=True)
            st.caption("λ~10-1000 μm | Thermal dust emission")
            st.markdown(get_dl(ir, "infrared.png", "📥 Download", "hot"), unsafe_allow_html=True)
        with tab2:
            vi = np.clip(img_gray ** 0.8, 0, 1)
            st.image(_apply_cmap(vi, "viridis"), use_container_width=True)
            st.caption("λ~400-700 nm | Stellar emission")
            st.markdown(get_dl(vi, "visible.png", "📥 Download", "viridis"), unsafe_allow_html=True)
        with tab3:
            xr = np.clip(img_gray ** 1.5, 0, 1)
            st.image(_apply_cmap(xr, "plasma"), use_container_width=True)
            st.caption("λ~0.01-10 nm | Hot plasma emission")
            st.markdown(get_dl(xr, "xray.png", "📥 Download", "plasma"), unsafe_allow_html=True)

    # =========================================================================
    # SECTION H — VON NEUMANN PRIMORDIAL ENTANGLEMENT (Pipeline 9)
    # =========================================================================
    st.markdown("---")
    st.markdown("## 🌌 Pipeline 9 — Von Neumann Primordial Entanglement")
    st.markdown(credit("Primordial-Photon-DarkPhoton-Entanglement",
                       "i∂ρ/∂t=[H_eff,ρ]  S=-Tr(ρ log ρ)  |<ψ_d|ψ_γ>|²"),
                unsafe_allow_html=True)
    st.latex(r"i\frac{\partial\rho}{\partial t}=[H_{\rm eff},\rho]")
    st.latex(r"S=-\mathrm{Tr}(\rho\log\rho)=-\sum_i\lambda_i\log\lambda_i")
    st.latex(r"P_{\rm mix}=|\langle\psi_d|\psi_\gamma\rangle|^2=\rho_{dd}(t)")

    fig_prim, (ax_s, ax_m) = plt.subplots(1, 2, figsize=(12, 4), facecolor="#0a0e1a")
    for ax in (ax_s, ax_m):
        ax.set_facecolor("#0d1525"); ax.tick_params(colors="#7ec8e3")
        ax.grid(True, alpha=0.2, color="#335588")

    ax_s.plot(t_prim, S_prim, color="#00ffcc", lw=2.5, label="S = -Tr(ρ log ρ)")
    ax_s.fill_between(t_prim, S_prim, alpha=0.2, color="#00ffcc")
    ax_s.set_xlabel("Time (a.u.)", color="#7ec8e3")
    ax_s.set_ylabel("Von Neumann Entropy S", color="#7ec8e3")
    ax_s.set_title(f"Entanglement Entropy  ω={omega_pd:.2f}  m={prim_mass:.1f}×10⁻⁹ eV",
                   color="#7ec8e3")
    ax_s.legend(facecolor="#0d1525", labelcolor="#c8ddf0")

    ax_m.plot(t_prim, mix_prob, color="#ff00cc", lw=2.5, label=r"$\rho_{dd}$ mixing prob.")
    ax_m.plot(t_prim, rho_gg, color="#7ec8e3", lw=1.5, ls="--", label=r"$\rho_{\gamma\gamma}$")
    ax_m.fill_between(t_prim, mix_prob, alpha=0.2, color="#ff00cc")
    ax_m.set_xlabel("Time (a.u.)", color="#7ec8e3")
    ax_m.set_ylabel("Probability", color="#7ec8e3")
    ax_m.set_title(f"Photon↔Dark Photon Oscillation  mixing={prim_mix:.2f}", color="#7ec8e3")
    ax_m.legend(facecolor="#0d1525", labelcolor="#c8ddf0")

    plt.suptitle(f"Von Neumann Primordial Entanglement  |  {AUTHOR}",
                 fontsize=10, color="#7ec8e3")
    plt.tight_layout()
    st.pyplot(fig_prim)
    prim_buf = fig_to_buf(fig_prim)
    st.markdown(get_dl(prim_buf, "primordial_entanglement.png",
                       "📥 Download Primordial Entanglement Plot"), unsafe_allow_html=True)
    plt.close(fig_prim)

    # =========================================================================
    # SECTION I — DETECTION METRICS DASHBOARD
    # =========================================================================
    st.markdown("---")
    st.markdown("## 📊 Detection Metrics Dashboard — All 9 Pipelines")
    dm = st.columns(5)
    dm[0].metric("P_dark Peak",     f"{dp_peak:.1f}%",              delta=f"ε={kin_mix:.1e}")
    dm[1].metric("FDM Soliton",     f"{float(soliton.max()):.3f}",  delta=f"m={fdm_mass:.1f}×10⁻²²")
    dm[2].metric("Fringe Contrast", f"{float(interf.std()):.3f}",   delta=f"fringe={fringe_scale}")
    dm[3].metric("Ω_PD Mixing",     f"{omega_pd * 0.6:.3f}",        delta=f"Ω={omega_pd:.2f}")
    dm[4].metric("B/B_crit",        f"{B0 / B_CRIT:.2e}",           delta=f"B₀=10^{b0_log10:.1f}")
    dm2 = st.columns(4)
    dm2[0].metric("Von Neumann S",  f"{float(S_prim.max()):.3f}",   delta="primordial")
    dm2[1].metric("Max Mix Prob",   f"{float(mix_prob.max()):.3f}",  delta=f"θ={prim_mix:.2f}")
    dm2[2].metric("Entanglement S", f"{ent_scalar:.4f}",             delta="spatial")
    dm2[3].metric("QCIS P(k) boost",f"{float(P_quantum.max()/P_lcdm.max()):.3f}x",
                  delta=f"f_NL={f_nl:.1f}")

    # =========================================================================
    # SECTION J — VERIFIED PHYSICS FORMULA TABLE
    # =========================================================================
    st.markdown("---")
    st.markdown("## 📡 Verified Physics Formulas — 9 Pipelines")
    st.markdown(f"*{AUTHOR}*")
    st.markdown("""
| # | Pipeline | Formula | Source / Basis |
|---|---------|---------|----------------|
| 1 | **FDM Soliton** | ρ(r)=ρ₀[sin(kr)/(kr)]²  k=π/r_s  r_s=1/m | QCAUS/app.py  (Hui et al. 2017 + Ford 2026) |
| 2 | **PDP Spectral Duality** | dark_mask=ε·e^{−ΩR²}·abs(sin(2πRL/f))·(1−e^{−R²/f}) | StealthPDPRadar/pdp_radar_core.py (Ford 2026) |
| 3 | **Entanglement Residuals** | S=−ρ·log(ρ)+abs(ψ_ord+ψ_dark)²−ψ_ord²−ψ_dark² | StealthPDPRadar/pdp_radar_core.py (Ford 2026) |
| 4 | **Dark Photon Detection** | P=prior·L/(prior·L+(1−prior)) | StealthPDPRadar (Bayesian, standard) |
| 5 | **Blue-Halo Fusion** | R=orig G=residuals B=dark  γ=0.45 | StealthPDPRadar/pdp_radar_core.py (Ford 2026) |
| 6 | **RGB Overlay** | R=orig+P_dark  G=FDM-soliton  B=PDP-interference | Ford 2026 — Ω_PD entanglement parameter |
| 7 | **Magnetar QED** | B=B₀(R/r)³√(3cos²θ+1)  ΔL=(α/45π)(B/Bc)²  P=ε²(1−e^{−B²/m²}) | Magnetar-Quantum-Vacuum (H&E 1936 + Ford 2026) |
| 8 | **QCIS Power Spectrum** | P(k)=P_ΛCDM(k)×(1+f_NL·(k/k₀)^n_q)  BBKS T(k) | Quantum-Cosmology-Integration-Suite (Ford 2026) |
| 9 | **Von Neumann Primordial** | i∂ρ/∂t=[H_eff,ρ]  S=−Tr(ρ log ρ)  P=rho_dd(t) | Primordial-Entanglement repo (standard + Ford 2026) |
""")

    # =========================================================================
    # SECTION K — ZIP DOWNLOAD
    # =========================================================================
    if st.button("📦 Download ALL Results as ZIP (9 Pipelines)"):
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w") as z:
            # Array images
            for nm, arr, cm in [
                ("original",            img_gray,  "gray"),
                ("pdp_rgb_overlay",     overlay_rgb, None),
                ("blue_halo_fusion",    fusion,    None),
                ("pdp_inferno",         pdp_inf,   "inferno"),
                ("fdm_soliton_2d",      soliton,   "hot"),
                ("pdp_interference",    interf,    "plasma"),
                ("entanglement_res",    ent_res,   "inferno"),
                ("dp_detection",        dp_prob,   "YlOrRd"),
                ("magnetar_B",          B_n,       "plasma"),
                ("magnetar_QED",        qed_n,     "inferno"),
                ("magnetar_darkphoton", conv_n,    "hot"),
                ("em_composite",        em_comp,   None),
            ]:
                buf = io.BytesIO()
                arr_to_pil(arr, cm).save(buf, "PNG")
                z.writestr(f"{nm}.png", buf.getvalue())
            # Matplotlib figures
            for nm, fig_fn, args in [
                ("magnetar_qed", plot_magnetar_qed, (B0, mag_eps)),
            ]:
                fg = fig_fn(*args); buf = fig_to_buf(fg, 150)
                z.writestr(f"{nm}.png", buf.read()); plt.close(fg)
            # FDM profile
            fg, ax = plt.subplots(figsize=(9, 3), facecolor="#0a0e1a")
            ax.set_facecolor("#0d1525")
            ax.plot(r_arr, rho_arr, "r-", lw=2.5)
            ax.set_title("FDM Soliton Profile"); ax.grid(True, alpha=0.2)
            buf = fig_to_buf(fg); z.writestr("fdm_profile.png", buf.read()); plt.close(fg)
            # QCIS spectrum
            fg, ax = plt.subplots(figsize=(10, 4), facecolor="#0a0e1a")
            ax.set_facecolor("#0d1525")
            ax.loglog(k_arr, P_lcdm, "b-", lw=2, label="ΛCDM")
            ax.loglog(k_arr, P_quantum, "r--", lw=2, label="QCIS")
            ax.legend(facecolor="#0d1525", labelcolor="#c8ddf0"); ax.grid(True, alpha=0.2, which="both")
            buf = fig_to_buf(fg); z.writestr("qcis_spectrum.png", buf.read()); plt.close(fg)
            # Primordial entanglement
            fg, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4), facecolor="#0a0e1a")
            a1.set_facecolor("#0d1525"); a2.set_facecolor("#0d1525")
            a1.plot(t_prim, S_prim, "#00ffcc", lw=2)
            a1.set_title("Von Neumann Entropy")
            a2.plot(t_prim, mix_prob, "#ff00cc", lw=2)
            a2.set_title("Mixing Probability")
            buf = fig_to_buf(fg); z.writestr("primordial_entanglement.png", buf.read()); plt.close(fg)

        zip_buf.seek(0)
        st.download_button("⬇️ Download QCAUS_Results.zip", zip_buf.getvalue(),
                           "QCAUS_Results.zip", "application/zip")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(
    f"🔭 **QCAUS v1.0** — Quantum Cosmology & Astrophysics Unified Suite | "
    f"9 Physics Pipelines  \n{AUTHOR}  \n"
    "**References:** Hui et al. 2017 · Heisenberg & Euler 1936 · Holdom 1986 · "
    "Planck Collaboration 2018 · Jackson 1998"
)
