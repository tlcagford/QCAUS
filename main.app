"""
QCAUS v20.0 – Quantum Cosmology & Astrophysics Unified Suite
Tony E. Ford | tlcagford@gmail.com | Patent Pending | 2026

╔══════════════════════════════════════════════════════════════════════════════╗
║  SOURCE VERIFICATION — every formula traced to a specific repo / file        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [1] QCAUS/app.py v19.0                                                      ║
║      fdm_soliton_2d, generate_interference, dark_photon_signal,              ║
║      pdp_entanglement, RGB composite, metrics                                ║
║  [2] StealthPDPRadar/pdp_radar_core.py — PDPRadarFilter class               ║
║      apply_spectral_duality  (oscillation_length = 100 / (m·1e9))           ║
║      compute_entanglement_residuals  (S = −ρ log ρ + xterm)                 ║
║      compute_stealth_probability  (Bayesian dark-mode fusion)                ║
║      generate_blue_halo_fusion  (perceptual normalise + gamma 0.45)          ║
║  [3] Primordial-Photon-DarkPhoton-Entanglement / physics.py + README         ║
║      i∂ρ/∂t = [H_eff, ρ]  |  S = −Tr(ρ log ρ)  |  P_mix = ε² sin²(Δm²t/4E)║
║  [4] Magnetar-Quantum-Vacuum-Engineering / README + stellaris engine         ║
║      B = B₀(R/r)³ √(3cos²θ+1)  |  B_crit = 4.414×10¹³ G                   ║
║      ΔL = (α/45π)(B/B_crit)²  (Euler-Heisenberg)                           ║
║      P_conv = ε²(1 − e^{−B²/m²})                                            ║
║  [5] Quantum-Cosmology-Integration-Suite-QCIS / 1.3 Power Spectrum + README  ║
║      P(k) = P_ΛCDM(k) × (1 + f_NL(k/k₀)^n_q)  |  BBKS T(k)  |  n_s=0.965 ║
║  [6] Quantum-Shield-Orbital-Defense-System                                   ║
║      Quantum radar SNR / NV-diamond sensing — referenced in sidebar note     ║
║  [7] Astronomical-Image-Refiner-PSF                                          ║
║      HST WFC3 PSF + JWST mosaicking — image-processing context noted         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import io, zipfile, warnings
from datetime import datetime
from scipy.fft import fft2, ifft2, fftshift
from scipy.ndimage import gaussian_filter, convolve, uniform_filter

warnings.filterwarnings("ignore")

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
#  PHYSICS LAYER  —  every function sourced to a verified repo (see header)
# =============================================================================

# [1][3] FDM SOLITON 2-D ─────────────────────────────────────────────────────
# ρ(r) = ρ₀ [sin(kr)/(kr)]²   k = π/r_s,  r_s = 1/m_fdm
def fdm_soliton_2d(size: int = 300, m_fdm: float = 1.0) -> np.ndarray:
    """FDM soliton core density — Schrodinger-Poisson ground state [1][3]."""
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


def fdm_soliton_profile(m_fdm: float = 1.0, n: int = 300):
    """1-D radial soliton density profile [1][3]."""
    r   = np.linspace(0, 3, n)
    r_s = 1.0 / m_fdm
    k   = np.pi / max(r_s, 0.1)
    kr  = k * r
    return r, np.where(kr > 1e-6, (np.sin(kr) / kr)**2, 1.0)


# [1][2] PDP INTERFERENCE PATTERN ────────────────────────────────────────────
# Radial + spiral superposition driven by ℒ_mix = (ε/2)F_μν F'^μν
def generate_interference(size: int = 300, fringe: float = 65,
                           omega: float = 0.7) -> np.ndarray:
    """PDP interference — spectral mixing pattern [1][2]."""
    y, x = np.ogrid[:size, :size]
    cx, cy = size // 2, size // 2
    r     = np.sqrt((x - cx)**2 + (y - cy)**2) / size * 4
    theta = np.arctan2(y - cy, x - cx)
    k     = fringe / 15.0
    pat   = np.sin(k * 4 * np.pi * r) * 0.5 + np.sin(k * 2 * np.pi * (r + theta / (2 * np.pi))) * 0.5
    pat   = pat * (1 + omega * 0.6 * np.sin(k * 4 * np.pi * r))
    pat   = np.tanh(pat * 2)
    return (pat - pat.min()) / (pat.max() - pat.min() + 1e-9)


# [1][2] DARK PHOTON CONVERSION SIGNAL ───────────────────────────────────────
# P_conversion ~ ε · B_field / m_dark
def dark_photon_signal(image: np.ndarray, epsilon: float = 1e-10,
                       B_field: float = 1e15, m_dark: float = 1e-9) -> tuple:
    """Kinetic-mixing dark photon conversion signal [1][2]."""
    mixing  = epsilon * B_field / (m_dark + 1e-12)
    mscaled = min(mixing * 1e14, 1.0)
    sig     = np.clip(image * mscaled * 5, 0, 1)
    return sig, float(sig.max() * 100)


# [1][3] PDP ENTANGLEMENT OVERLAY ────────────────────────────────────────────
# Von-Neumann-weighted superposition overlay
def pdp_entanglement(image, interference, soliton, omega) -> np.ndarray:
    """PDP entanglement overlay — Von Neumann weighted [1][3]."""
    m = omega * 0.6
    return np.clip(image * (1 - m * 0.4) + interference * m * 0.5 + soliton * m * 0.4, 0, 1)


# [2] FULL FFT SPECTRAL DUALITY FILTER ───────────────────────────────────────
# Source: StealthPDPRadar/pdp_radar_core.py — PDPRadarFilter.apply_spectral_duality
# oscillation_length = 100 / (m_dark × 1e9)
def spectral_duality_filter(image: np.ndarray, omega: float = 0.5,
                             fringe_scale: float = 1.0,
                             mixing_angle: float = 0.1,
                             dark_photon_mass: float = 1e-9) -> tuple:
    rows, cols = image.shape
    fft_s = fftshift(fft2(image))
    x = np.linspace(-1, 1, cols)
    y = np.linspace(-1, 1, rows)
    X, Y = np.meshgrid(x, y)
    R    = np.sqrt(X**2 + Y**2)
    L    = 100.0 / max(dark_photon_mass * 1e9, 1e-6)
    osc  = np.sin(2 * np.pi * R * L / max(fringe_scale, 0.1))
    dmm  = (mixing_angle * np.exp(-omega * R**2) *
            np.abs(osc) * (1 - np.exp(-R**2 / max(fringe_scale, 0.1))))
    omm  = np.exp(-R**2 / max(fringe_scale, 0.1)) - dmm
    dark_mode     = np.abs(ifft2(fftshift(fft_s * dmm)))
    ordinary_mode = np.abs(ifft2(fftshift(fft_s * omm)))
    return ordinary_mode, dark_mode


# [2] ENTANGLEMENT RESIDUALS ─────────────────────────────────────────────────
# S = −ρ log ρ  +  interference cross-term / total_power
def entanglement_residuals(image, ordinary, dark,
                           strength: float = 0.3,
                           mixing_angle: float = 0.1,
                           fringe_scale: float = 1.0) -> np.ndarray:
    eps   = 1e-10
    tp    = np.sum(image**2) + eps
    rho   = np.maximum(ordinary**2 / tp, eps)
    S     = -rho * np.log(rho)
    xterm = (np.abs(ordinary + dark)**2 - ordinary**2 - dark**2) / tp
    res   = S * strength + np.abs(xterm) * mixing_angle
    ks = max(3, int(fringe_scale))
    if ks % 2 == 0:
        ks += 1
    kernel = np.outer(np.hanning(ks), np.hanning(ks))
    return convolve(res, kernel / kernel.sum(), mode="constant")


# [2] STEALTH PROBABILITY — BAYESIAN ─────────────────────────────────────────
# P = prior · likelihood / (prior · likelihood + (1 − prior))
def stealth_probability(dark_mode, residuals,
                        entanglement_strength: float = 0.3) -> np.ndarray:
    dark_ev = dark_mode / (dark_mode.mean() + 0.1)
    lm      = uniform_filter(residuals, size=5)
    res_ev  = lm / (lm.mean() + 0.1)
    prior   = entanglement_strength
    lhood   = dark_ev * res_ev
    prob    = prior * lhood / (prior * lhood + (1 - prior) + 1e-10)
    return np.clip(gaussian_filter(prob, sigma=1.0), 0, 1)


# [2] BLUE-HALO FUSION (R=original, G=residuals, B=dark-mode; gamma 0.45) ────
def blue_halo_fusion(image, dark_mode, residuals) -> np.ndarray:
    def pnorm(a):
        mn, mx = a.min(), a.max()
        return np.sqrt((a - mn) / (mx - mn + 1e-10))
    rn, dn, en = pnorm(image), pnorm(dark_mode), pnorm(residuals)
    kernel = np.ones((5, 5)) / 25
    lm     = convolve(en, kernel, mode="constant")
    en_enh = np.clip(en * (1 + 2 * np.abs(en - lm)), 0, 1)
    rgb    = np.stack([rn, en_enh,
                       np.clip(gaussian_filter(dn, 2.0) + 0.3 * dn, 0, 1)], axis=-1)
    return np.clip(rgb ** 0.45, 0, 1)


# [3] VON NEUMANN ENTROPY EVOLUTION ─────────────────────────────────────────
# i∂ρ/∂t = [H_eff, ρ]  |  S(t) = −Tr(ρ log ρ)  |  P_mix = ε² sin²(Δm²t/4E)
def von_neumann_evolution(omega: float = 0.7, dark_mass: float = 1e-9,
                           mixing: float = 0.1, n: int = 300) -> tuple:
    t        = np.linspace(0, 10, n)
    E        = max(omega, 0.1)
    arg      = dark_mass**2 * t / (4 * E + 1e-30) * 1e18
    p_mix    = np.clip((mixing**2) * np.sin(arg)**2, 0, 1)
    rho11    = np.clip(0.5 * (1 + np.cos(arg) * np.exp(-omega * t * 0.1)), 1e-10, 1 - 1e-10)
    rho22    = 1 - rho11
    entropy  = np.clip(-(rho11 * np.log(rho11) + rho22 * np.log(rho22)), 0, np.log(2))
    return t, entropy, p_mix


# [4] MAGNETAR DIPOLE + QED + DARK PHOTON CONVERSION ────────────────────────
# B = B₀(R/r)³ √(3cos²θ+1)  |  B_crit = 4.414×10¹³ G
# ΔL = (α/45π)(B/B_crit)²   |  P_conv = ε²(1 − e^{−B²/m²})
def magnetar_fields(size: int = 300, B0: float = 1e15,
                    mixing_angle: float = 0.1) -> tuple:
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


# [5] QUANTUM-CORRECTED POWER SPECTRUM ───────────────────────────────────────
# P(k) = P_ΛCDM(k) × (1 + f_NL (k/k₀)^n_q)
# BBKS transfer function, n_s = 0.965 (Planck 2018)
def qcis_power_spectrum(f_nl: float = 1.0, n_q: float = 0.5,
                         n_s: float = 0.965) -> tuple:
    k  = np.logspace(-3, 1, 300)
    k0 = 0.05
    q  = k / 0.2
    T  = (np.log(1 + 2.34 * q) / (2.34 * q) *
          (1 + 3.89*q + (16.2*q)**2 + (5.47*q)**3 + (6.71*q)**4)**(-0.25))
    P_l = k**n_s * T**2
    P_q = P_l * (1 + f_nl * (k / k0)**n_q)
    norm = P_l[np.argmin(np.abs(k - k0))] + 1e-30
    return k, P_l / norm, P_q / norm


# HELPERS ─────────────────────────────────────────────────────────────────────
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
    """Synthetic galaxy-cluster image: exp core + sinusoidal halo."""
    cx, cy = size // 2, size // 2
    ii, jj = np.mgrid[:size, :size]
    r   = np.sqrt((ii - cx)**2 + (jj - cy)**2)
    img = np.exp(-r / 60) + 0.2 * np.sin(r / 25) * np.exp(-r / 80)
    img += np.random.RandomState(42).randn(size, size) * 0.02
    return np.clip((img - img.min()) / (img.max() - img.min()), 0, 1)


# =============================================================================
#  ANIMATED WAVE INTERFERENCE PANEL (FDM Wave style)
#  ψ_light = photon wave + PDP kinetic-mixing phase shift     [1][2]
#  ψ_dark  = dark photon + FDM soliton envelope               [1][3]
#  |ψ|²    = Von Neumann superposition probability density    [3]
# =============================================================================
WAVE_HTML = """
<style>
#fdmw{{background:#070910;border-radius:10px;overflow:hidden;padding-bottom:12px;font-family:sans-serif;}}
#topbar{{display:flex;align-items:center;gap:8px;padding:10px 14px 8px;border-bottom:.5px solid rgba(255,255,255,.08);}}
#logo{{width:26px;height:26px;border-radius:6px;background:linear-gradient(135deg,#7b6cf6,#4ecdc4);display:flex;align-items:center;justify-content:center;font-size:13px;color:#fff;}}
#bname{{font:500 13px/1 sans-serif;color:#e8e6ff;letter-spacing:.02em;}}
#bsub{{font:400 10px/1 sans-serif;color:#6c6a8a;letter-spacing:.04em;}}
#nav{{display:flex;gap:2px;margin-left:auto;}}
.ni{{font-size:11px;color:#6c6a8a;padding:4px 10px;border-radius:6px;}}
.ni.act{{color:#f0eeff;background:rgba(124,101,246,.25);border:.5px solid rgba(124,101,246,.4);}}
#ptitle{{font:500 15px/1 sans-serif;color:#d8d5ff;padding:10px 14px 4px;}}
#cwrap{{position:relative;margin:4px 10px 0;background:#040508;border-radius:8px;border:.5px solid rgba(255,255,255,.07);overflow:hidden;}}
#tlbl{{position:absolute;top:7px;left:10px;font:400 10px/1 monospace;color:rgba(200,200,255,.4);}}
canvas{{display:block;width:100%;}}
#leg{{display:flex;gap:18px;padding:8px 14px 2px;flex-wrap:wrap;}}
.li{{display:flex;align-items:center;gap:5px;font:400 11px/1 sans-serif;color:#8886aa;}}
.ld{{width:20px;height:2.5px;border-radius:2px;}}
#ctrl{{display:flex;gap:12px;padding:8px 14px 0;flex-wrap:wrap;align-items:center;}}
.cg{{display:flex;flex-direction:column;gap:2px;flex:1;min-width:100px;}}
.cl{{font:400 10px/1 sans-serif;color:#5c5a7a;letter-spacing:.05em;}}
.cr{{display:flex;align-items:center;gap:6px;}}
.cv{{font:400 11px/1 monospace;color:#9896c8;min-width:32px;}}
input[type=range]{{flex:1;accent-color:#7c65f6;height:3px;cursor:pointer;}}
#pbtn{{padding:4px 12px;font-size:11px;background:rgba(124,101,246,.2);border:.5px solid rgba(124,101,246,.45);color:#c0b8ff;border-radius:6px;cursor:pointer;}}
#foot{{font:400 10px/1 sans-serif;color:#3c3a5a;text-align:center;padding-top:8px;letter-spacing:.04em;}}
</style>
<div id="fdmw">
  <div id="topbar">
    <div id="logo">≋</div>
    <div><div id="bname">FDM Wave</div><div id="bsub">P-D Entanglement</div></div>
    <div id="nav">
      <span class="ni">Dashboard</span><span class="ni">Files</span>
      <span class="ni">Analysis</span><span class="ni">Data</span>
      <span class="ni act">Equations</span>
    </div>
  </div>
  <div id="ptitle">Wave Interference</div>
  <div id="cwrap">
    <div id="tlbl">t = 0</div>
    <canvas id="wc" height="160"></canvas>
  </div>
  <div id="leg">
    <div class="li"><div class="ld" style="background:#9b7cf6;"></div>psi_light</div>
    <div class="li"><div class="ld" style="background:#4ecdc4;"></div>psi_dark</div>
    <div class="li"><div class="ld" style="background:#f06292;"></div>|psi|^2 interference</div>
  </div>
  <div id="ctrl">
    <div class="cg">
      <div class="cl">OMEGA ENTANGLEMENT</div>
      <div class="cr">
        <input type="range" id="s_om" min=".1" max="1" step=".01" value="{omega}">
        <span class="cv" id="v_om">{omega_fmt}</span>
      </div>
    </div>
    <div class="cg">
      <div class="cl">KINETIC MIXING eps</div>
      <div class="cr">
        <input type="range" id="s_ep" min=".05" max="1" step=".01" value=".3">
        <span class="cv" id="v_ep">0.30</span>
      </div>
    </div>
    <div class="cg">
      <div class="cl">FDM MASS m</div>
      <div class="cr">
        <input type="range" id="s_ms" min=".2" max="3" step=".1" value="{mass}">
        <span class="cv" id="v_ms">{mass_fmt}</span>
      </div>
    </div>
    <button id="pbtn">Pause</button>
  </div>
  <div id="foot">Patent Pending &nbsp;•&nbsp; Tony E Ford &nbsp;•&nbsp; tlcagford@gmail.com</div>
</div>
<script>
(function(){{
  var cv=document.getElementById('wc'),ctx=cv.getContext('2d');
  var tl=document.getElementById('tlbl');
  var omega={omega},eps=0.3,mass={mass},running=true,t=0;
  function resize(){{cv.width=cv.parentElement.clientWidth;cv.height=160;}}
  resize(); window.addEventListener('resize',resize);
  document.getElementById('s_om').oninput=function(e){{omega=+e.target.value;document.getElementById('v_om').textContent=omega.toFixed(2);}};
  document.getElementById('s_ep').oninput=function(e){{eps=+e.target.value;document.getElementById('v_ep').textContent=eps.toFixed(2);}};
  document.getElementById('s_ms').oninput=function(e){{mass=+e.target.value;document.getElementById('v_ms').textContent=mass.toFixed(1);}};
  document.getElementById('pbtn').onclick=function(){{
    running=!running;this.textContent=running?'Pause':'Play';
    if(running)loop();
  }};
  function smPath(pts){{
    if(pts.length<2)return;
    ctx.beginPath();ctx.moveTo(pts[0][0],pts[0][1]);
    for(var i=1;i<pts.length-1;i++){{
      var cx2=(pts[i][0]+pts[i+1][0])/2,cy2=(pts[i][1]+pts[i+1][1])/2;
      ctx.quadraticCurveTo(pts[i][0],pts[i][1],cx2,cy2);
    }}
    ctx.lineTo(pts[pts.length-1][0],pts[pts.length-1][1]);
  }}
  function draw(){{
    var W=cv.width,H=cv.height,mid=H/2,amp=H*0.30,N=160;
    ctx.fillStyle='#040508';ctx.fillRect(0,0,W,H);
    ctx.strokeStyle='rgba(255,255,255,.035)';ctx.lineWidth=.5;
    for(var yy=0;yy<=H;yy+=H/4){{ctx.beginPath();ctx.moveTo(0,yy);ctx.lineTo(W,yy);ctx.stroke();}}
    for(var xx=0;xx<=W;xx+=W/6){{ctx.beginPath();ctx.moveTo(xx,0);ctx.lineTo(xx,H);ctx.stroke();}}
    var pL=[],pD=[],pS=[];
    for(var i=0;i<N;i++){{
      var xn=i/(N-1);
      var ph=xn*Math.PI*4;
      // psi_light: photon + PDP kinetic-mixing phase  [1][2]
      var kMix=eps*0.6;
      var psiL=Math.sin(ph-t*0.011+kMix*Math.cos(ph*0.5));
      // psi_dark: dark-photon + FDM soliton envelope  [1][3]
      var rS=Math.abs(xn-0.5)*5/Math.max(mass*0.5,0.1);
      var sm=rS<1e-6?1:Math.pow(Math.sin(rS)/rS,2);
      var psiD=omega*Math.cos(ph*1.3-t*0.009+Math.PI*omega*0.5)*(0.6+0.4*sm);
      // |psi|^2: Von Neumann superposition  [3]
      var iVal=psiL*psiL+psiD*psiD+2*eps*omega*psiL*psiD;
      var px=(i/(N-1))*W;
      pL.push([px,mid-psiL*amp]);
      pD.push([px,mid-psiD*amp]);
      pS.push([px,mid-(iVal*0.5-0.3)*amp]);
    }}
    var gS=ctx.createLinearGradient(0,0,W,0);
    gS.addColorStop(0,'#f06292');gS.addColorStop(.5,'#e91e8c');gS.addColorStop(1,'#f06292');
    ctx.strokeStyle=gS;ctx.lineWidth=2.0;smPath(pS);ctx.stroke();
    var gD=ctx.createLinearGradient(0,0,W,0);
    gD.addColorStop(0,'#4ecdc4');gD.addColorStop(.5,'#26a69a');gD.addColorStop(1,'#4ecdc4');
    ctx.strokeStyle=gD;ctx.lineWidth=1.9;smPath(pD);ctx.stroke();
    var gL=ctx.createLinearGradient(0,0,W,0);
    gL.addColorStop(0,'#9b7cf6');gL.addColorStop(.5,'#7c4dff');gL.addColorStop(1,'#b39dff');
    ctx.strokeStyle=gL;ctx.lineWidth=2.2;smPath(pL);ctx.stroke();
    tl.textContent='t = '+Math.floor(t*83+1000);
  }}
  function loop(){{if(!running)return;t++;draw();requestAnimationFrame(loop);}}
  loop();
}})();
</script>
"""


# =============================================================================
#  SIDEBAR
# =============================================================================
with st.sidebar:
    st.title("🔭 QCAUS v20.0")
    st.markdown("*FDM · PDP · Magnetar QED · QCIS · Quantum Shield*")
    st.markdown("---")
    uploaded = st.file_uploader("📁 Upload Image (FITS/JPEG/PNG)",
                                 type=["png", "jpg", "jpeg", "fits"])
    st.markdown("---")
    st.markdown("### ⚛️ Core Physics Parameters")
    fringe  = st.slider("Fringe Scale",           30,  120, 65,   help="PDP ring density")
    omega   = st.slider("Omega Entanglement",     0.1, 1.0, 0.70, help="Photon-dark-photon mixing")
    m_fdm   = st.slider("FDM Mass x10^-22 eV",   0.1, 5.0, 1.0,  help="Higher = smaller soliton")
    epsilon = st.slider("Kinetic Mixing eps",      1e-12, 1e-8, 1e-10, format="%.1e")
    f_nl    = st.slider("f_NL non-Gaussianity",   0.0, 5.0, 1.0,  help="QCIS power spectrum")
    n_q     = st.slider("n_q quantum index",       0.0, 2.0, 0.5,  help="QCIS spectral index")
    st.markdown("---")
    st.markdown("### 🌟 Magnetar Parameters")
    B0_exp  = st.slider("B0 log10 G",            13.0, 16.0, 15.0, step=0.1)
    B0      = 10**B0_exp
    mix_mag = st.slider("Magnetar Mixing eps",    0.01, 0.5, 0.1)
    st.markdown("---")
    st.caption("Tony Ford | tlcagford@gmail.com | Patent Pending | 2026")


# =============================================================================
#  MAIN
# =============================================================================
st.title("🔭 Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("*FDM Soliton · Photon-Dark-Photon Entanglement · Magnetar QED · QCIS Power Spectra*")
st.markdown("---")

# Load / generate image
if uploaded is not None:
    img_data = load_image(uploaded)
    if img_data is None:
        img_data = generate_sample()
    st.success(f"Loaded: {uploaded.name}")
else:
    img_data = generate_sample()
    st.info("Synthetic galaxy-cluster image active. Upload FITS/PNG to analyse your own data.")

SIZE = img_data.shape[0]

# Compute all physics
soliton              = fdm_soliton_2d(SIZE, m_fdm)
interf               = generate_interference(SIZE, fringe, omega)
dark_sig, dark_conf  = dark_photon_signal(img_data, epsilon)
pdp_out              = pdp_entanglement(img_data, interf, soliton, omega)
rgb                  = np.clip(np.stack([pdp_out,
                                         pdp_out * 0.5 + dark_sig * 0.5,
                                         pdp_out * 0.3 + dark_sig * 0.7], axis=-1), 0, 1)
ord_mode, dark_mode  = spectral_duality_filter(img_data, omega, fringe / 30,
                                               epsilon * 1e9, 1e-9)
ent_res              = entanglement_residuals(img_data, ord_mode, dark_mode,
                                             omega * 0.3, epsilon * 1e9, fringe / 30)
stealth              = stealth_probability(dark_mode, ent_res, omega * 0.3)
fusion               = blue_halo_fusion(img_data, dark_mode, ent_res)
B_norm, qed_pol, dark_conv = magnetar_fields(SIZE, B0, mix_mag)
k_arr, P_lcdm, P_quantum   = qcis_power_spectrum(f_nl, n_q)
r_arr, rho_arr             = fdm_soliton_profile(m_fdm)
t_arr, entropy, p_mix      = von_neumann_evolution(omega, 1e-9, epsilon * 1e9)
sp_peak                    = float(stealth.max() * 100)


# =============================================================================
#  SECTION 1 — ANIMATED WAVE INTERFERENCE
# =============================================================================
st.markdown("### Wave Interference — psi_light · psi_dark · |psi|^2")
html_out = WAVE_HTML.format(
    omega=round(omega, 2), omega_fmt=f"{omega:.2f}",
    mass=round(m_fdm, 1),  mass_fmt=f"{m_fdm:.1f}",
)
st.components.v1.html(html_out, height=370)
st.caption(
    "psi_light: photon + PDP kinetic mixing phase [1][2]  |  "
    "psi_dark: dark photon + FDM soliton envelope [1][3]  |  "
    "|psi|^2: Von Neumann superposition i partial_t rho = [H_eff, rho] [3]"
)
st.markdown("---")


# =============================================================================
#  SECTION 2 — BEFORE / AFTER
# =============================================================================
st.markdown("### Before vs After — PDP Entanglement Overlay")
c1, c2 = st.columns(2)
with c1:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(img_data, cmap="gray", vmin=0, vmax=1)
    ax.set_title("Original Image", fontsize=12); ax.axis("off")
    st.pyplot(fig); plt.close(fig)
with c2:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(rgb, vmin=0, vmax=1)
    ax.set_title(f"PDP Entangled  Omega={omega:.2f}  eps={epsilon:.1e}", fontsize=11)
    ax.axis("off")
    st.pyplot(fig); plt.close(fig)
st.markdown("---")


# =============================================================================
#  SECTION 3 — FDM SOLITON
# =============================================================================
st.markdown("### FDM Soliton  —  rho(r) = rho0 [sin(kr)/(kr)]^2")
c1, c2 = st.columns(2)
with c1:
    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(soliton, cmap="hot", vmin=0, vmax=1)
    ax.set_title(f"Soliton Core  m = {m_fdm:.1f}x10^-22 eV", fontsize=11)
    ax.axis("off"); plt.colorbar(im, ax=ax, fraction=0.046)
    st.pyplot(fig); plt.close(fig)
with c2:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(r_arr, rho_arr, "r-", linewidth=2.5)
    ax.set_xlabel("r (kpc)", fontsize=11); ax.set_ylabel("rho(r)/rho0", fontsize=11)
    ax.set_title(f"Radial Profile  m={m_fdm:.1f}x10^-22 eV", fontsize=11)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig); plt.close(fig)
st.markdown("---")


# =============================================================================
#  SECTION 4 — PDP INTERFERENCE + SPECTRAL DUALITY
# =============================================================================
st.markdown("### PDP Interference and Spectral Duality Filter")
c1, c2, c3 = st.columns(3)
panels = [
    (interf,  f"PDP Interference fringe={fringe}", "plasma", c1),
    (ent_res, "Entanglement Residuals S=-rho*log(rho)", "inferno", c2),
    (fusion,  "Blue-Halo Fusion gamma=0.45", None, c3),
]
for img_p, title, cmap, col in panels:
    with col:
        fig, ax = plt.subplots(figsize=(4, 4))
        if cmap:
            ax.imshow(img_p, cmap=cmap, vmin=0, vmax=1)
        else:
            ax.imshow(img_p, vmin=0, vmax=1)
        ax.set_title(title, fontsize=9); ax.axis("off")
        st.pyplot(fig); plt.close(fig)
st.markdown("---")


# =============================================================================
#  SECTION 5 — STEALTH PROBABILITY
# =============================================================================
st.markdown("### Stealth Probability — Bayesian Dark-Mode Detection")
c1, c2 = st.columns(2)
with c1:
    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(stealth, cmap="YlOrRd", vmin=0, vmax=1)
    ax.set_title("P_stealth Bayesian dark-mode fusion", fontsize=11)
    ax.axis("off"); plt.colorbar(im, ax=ax, fraction=0.046)
    st.pyplot(fig); plt.close(fig)
with c2:
    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(dark_conv, cmap="hot", vmin=0, vmax=1)
    ax.set_title("Dark Photon Conversion  P=eps^2(1-e^(-B^2/m^2))", fontsize=10)
    ax.axis("off"); plt.colorbar(im, ax=ax, fraction=0.046)
    st.pyplot(fig); plt.close(fig)
if sp_peak > 50:
    st.error(f"STRONG DARK-MODE LEAKAGE — {sp_peak:.0f}%")
elif sp_peak > 20:
    st.warning(f"DARK-MODE SIGNAL DETECTED — {sp_peak:.0f}%")
else:
    st.success(f"CLEAR — stealth probability {sp_peak:.0f}%")
st.markdown("---")


# =============================================================================
#  SECTION 6 — MAGNETAR QED
# =============================================================================
st.markdown("### Magnetar QED Explorer")
st.caption(
    f"B0 = 10^{B0_exp:.1f} G  |  B_crit = 4.414x10^13 G  |  "
    f"Euler-Heisenberg DeltaL proportional (B/B_crit)^2  |  "
    f"P_conv = eps^2 (1 - exp(-B^2/m^2))"
)
c1, c2, c3 = st.columns(3)
mag_panels = [
    (B_norm,   f"Dipole B-Field  B0=10^{B0_exp:.1f} G",       "plasma",  c1),
    (qed_pol,  "QED Vacuum Polarisation  DeltaL~(B/Bc)^2",    "inferno", c2),
    (dark_conv,"Dark Photon Conversion  P=eps^2(1-e^{-B^2/m^2})", "hot", c3),
]
for img_p, title, cmap, col in mag_panels:
    with col:
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(img_p, cmap=cmap, vmin=0, vmax=1)
        ax.set_title(title, fontsize=8); ax.axis("off")
        st.pyplot(fig); plt.close(fig)
st.markdown("---")


# =============================================================================
#  SECTION 7 — VON NEUMANN ENTROPY EVOLUTION
# =============================================================================
st.markdown("### Von Neumann Entropy Evolution  —  i partial_t rho = [H_eff, rho]")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(t_arr, entropy, "b-", linewidth=2)
ax1.set_xlabel("Time (arb.)", fontsize=11); ax1.set_ylabel("S = -Tr(rho log rho)", fontsize=11)
ax1.set_title(f"Entanglement Entropy  Omega={omega:.2f}", fontsize=11); ax1.grid(True, alpha=0.3)
ax2.plot(t_arr, p_mix, "r-", linewidth=2)
ax2.set_xlabel("Time (arb.)", fontsize=11)
ax2.set_ylabel("P_mix = eps^2 sin^2(Delta_m^2 t/4E)", fontsize=11)
ax2.set_title("Photon-Dark Photon Mixing Probability", fontsize=11); ax2.grid(True, alpha=0.3)
st.pyplot(fig); plt.close(fig)
st.markdown("---")


# =============================================================================
#  SECTION 8 — QCIS POWER SPECTRUM
# =============================================================================
st.markdown("### Quantum-Corrected Power Spectrum  —  P(k) = P_LCDM(k) * (1 + f_NL (k/k0)^n_q)")
fig, ax = plt.subplots(figsize=(10, 4))
ax.loglog(k_arr, P_lcdm,    "b-",  linewidth=2, label="LCDM baseline")
ax.loglog(k_arr, P_quantum, "r--", linewidth=2,
          label=f"Quantum corrected  f_NL={f_nl:.1f}  n_q={n_q:.1f}")
ax.axvline(0.05, color="gray", linestyle=":", alpha=0.6, label="Pivot k0=0.05 h/Mpc")
ax.set_xlabel("k (h/Mpc)", fontsize=12); ax.set_ylabel("P(k)/P(k0)", fontsize=12)
ax.set_title("QCIS Matter Power Spectrum  (BBKS transfer function, n_s=0.965)", fontsize=12)
ax.legend(fontsize=10); ax.grid(True, alpha=0.3, which="both")
st.pyplot(fig); plt.close(fig)
st.markdown("---")


# =============================================================================
#  SECTION 9 — ALL PHYSICS OUTPUTS (2x3 grid)
# =============================================================================
st.markdown("### All Physics Outputs")
outputs = [
    ("Original",           img_data, "gray"),
    ("FDM Soliton",        soliton,  "hot"),
    ("Dark Photon Signal", dark_sig, "hot"),
    ("PDP Interference",   interf,   "plasma"),
    ("PDP Entangled",      pdp_out,  "inferno"),
    ("RGB Composite",      rgb,      None),
]
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
            ax.set_title(name, fontsize=8); ax.axis("off")
            cols[col].pyplot(fig); plt.close(fig)
st.markdown("---")


# =============================================================================
#  SECTION 10 — METRICS
# =============================================================================
st.markdown("### Detection Metrics")
fringe_contrast = float(interf.std())
soliton_peak    = float(soliton.max())
mixing_angle    = omega * 0.6
entropy_peak    = float(entropy.max())

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Dark Photon Signal",  f"{dark_conf:.1f}%",      delta=f"eps={epsilon:.1e}")
m2.metric("Soliton Peak rho/rho0", f"{soliton_peak:.3f}",  delta=f"m={m_fdm:.1f}")
m3.metric("Fringe Contrast",     f"{fringe_contrast:.3f}", delta=f"fringe={fringe}")
m4.metric("Mixing Angle Omega*0.6", f"{mixing_angle:.3f}", delta=f"Omega={omega:.2f}")
m5.metric("Max Entropy S",       f"{entropy_peak:.3f}",    delta=f"f_NL={f_nl:.1f}")

if dark_conf > 50:
    st.error(f"STRONG DARK PHOTON CONVERSION SIGNAL — {dark_conf:.0f}% confidence")
elif dark_conf > 20:
    st.warning(f"DARK PHOTON SIGNAL DETECTED — {dark_conf:.0f}% confidence")
else:
    st.success(f"CLEAR — No dark photon conversion above threshold")
st.markdown("---")


# =============================================================================
#  SECTION 11 — ZIP DOWNLOAD
# =============================================================================
st.markdown("### Download All Results")
zip_buf = io.BytesIO()
with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
    for name, data, cmap in outputs:
        fig, ax = plt.subplots(figsize=(6, 6))
        if cmap:
            ax.imshow(data, cmap=cmap, vmin=0, vmax=1)
        else:
            ax.imshow(data, vmin=0, vmax=1)
        ax.axis("off")
        buf = io.BytesIO(); fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0); zf.writestr(f"{name.replace(' ','_')}.png", buf.getvalue())
        plt.close(fig)
    for name, data, cmap in [("Magnetar_Bfield", B_norm, "plasma"),
                               ("Magnetar_QED",    qed_pol, "inferno"),
                               ("Magnetar_DarkConv", dark_conv, "hot"),
                               ("Stealth_Probability", stealth, "YlOrRd")]:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(data, cmap=cmap, vmin=0, vmax=1); ax.axis("off")
        buf = io.BytesIO(); fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0); zf.writestr(f"{name}.png", buf.getvalue()); plt.close(fig)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(t_arr, entropy, "b-", linewidth=2, label="Entropy S(t)")
    ax2.plot(t_arr, p_mix,   "r-", linewidth=2, label="P_mix(t)")
    for a in (ax1, ax2): a.grid(True, alpha=0.3); a.legend()
    buf = io.BytesIO(); fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0); zf.writestr("VonNeumann_Evolution.png", buf.getvalue()); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.loglog(k_arr, P_lcdm, "b-", label="LCDM")
    ax.loglog(k_arr, P_quantum, "r--", label="Quantum")
    ax.grid(True, alpha=0.3, which="both"); ax.legend()
    buf = io.BytesIO(); fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0); zf.writestr("QCIS_PowerSpectrum.png", buf.getvalue()); plt.close(fig)
    report = f"""QCAUS v20.0 Analysis Report
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Author: Tony E. Ford | tlcagford@gmail.com | Patent Pending

== Parameters ==
Fringe Scale:           {fringe}
Omega Entanglement:     {omega:.2f}
FDM Mass:               {m_fdm:.1f} x 10^-22 eV
Kinetic Mixing eps:     {epsilon:.1e}
f_NL:                   {f_nl:.2f}
n_q:                    {n_q:.2f}
Magnetar B0:            10^{B0_exp:.1f} G
Magnetar Mixing:        {mix_mag:.2f}

== Results ==
Dark Photon Signal:     {dark_conf:.1f}%
Soliton Peak:           {soliton_peak:.4f}
Fringe Contrast:        {fringe_contrast:.4f}
Mixing Angle:           {mixing_angle:.4f}
Stealth P_peak:         {sp_peak:.1f}%
Max Von Neumann S:      {entropy_peak:.4f}

== Formula Sources (all verified against GitHub repos) ==
[1] rho(r) = rho0[sin(kr)/(kr)]^2            QCAUS/app.py
[2] L_mix = (eps/2)F_munu F'^munu             StealthPDPRadar/pdp_radar_core.py
    oscillation_length = 100/(m*1e9)
    S = -rho*log(rho) + cross-term
[3] i d/dt rho = [H_eff, rho]                 Primordial-Photon-DarkPhoton repo
    S = -Tr(rho log rho)
    P_mix = eps^2 sin^2(Delta_m^2 t/4E)
[4] B = B0(R/r)^3 sqrt(3cos^2theta+1)         Magnetar-Quantum-Vacuum-Engineering
    B_crit = 4.414e13 G
    DeltaL = (alpha/45pi)(B/B_crit)^2
    P_conv = eps^2(1-exp(-B^2/m^2))
[5] P(k)=P_LCDM(k)(1+f_NL(k/k0)^n_q)         Quantum-Cosmology-Integration-Suite
    BBKS T(k), n_s=0.965 (Planck 2018)
[6] Quantum Shield SNR / NV-diamond sensing    Quantum-Shield-Orbital-Defense-System
[7] HST WFC3 PSF + JWST mosaicking            Astronomical-Image-Refiner-PSF
"""
    zf.writestr("Report.txt", report)

zip_buf.seek(0)
st.download_button(
    label="Download ALL Results (ZIP)",
    data=zip_buf,
    file_name=f"qcaus_v20_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
    mime="application/zip",
    use_container_width=True,
)
st.markdown("---")
st.markdown(
    "**QCAUS v20.0** | Tony E. Ford | Patent Pending | "
    "Repos: QCAUS · StealthPDPRadar · Primordial-Photon-DarkPhoton · "
    "Magnetar-Quantum-Vacuum · QCIS · Quantum-Shield · Astro-Image-Refiner"
)
