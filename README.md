# 🔭 Quantum Cosmology & Astrophysics Unified Suite (QCAUS) v1.0

> *"Exploring the quantum nature of the universe — from dark matter solitons to quantum-corrected cosmology."*

A unified computational framework integrating **9 physics pipelines** across 8 interconnected open-source projects. QCAUS enables real-time interactive exploration of fuzzy dark matter, photon–dark photon entanglement, magnetar QED, primordial quantum cosmology, and stealth dark-leakage detection — all in a single Streamlit application.

**[🚀 Launch Live App](https://qcaustfordmodel.streamlit.app/)**

**Tony E. Ford** | tlcagford@gmail.com | Patent Pending | 2026

---

## ✨ What's New in v1.0 (2026)

- **9 complete physics pipelines** — up from 4 partial modules
- **RGB quantum overlay on source image** — 🟢 FDM soliton · 🔵 PDP interference · 🔴 original + detection
- **Animated two-field FDM wave** showing Re(ψ_light), Re(ψ_dark), and ρ interference all as distinct traces
- **Von Neumann Primordial Entanglement** — full density matrix evolution with entropy and mixing probability plots
- **Per-panel source credits** — every visualization tagged with its repo, formula, and authorship
- **Dark space theme** throughout app and all matplotlib figures
- **9-pipeline metrics dashboard** with live scalar readouts for all physics outputs
- **One-click ZIP download** of all 14+ result images including real matplotlib figures
- All download buttons now save actual rendered figures (not placeholder arrays)
- Kinetic mixing ε used correctly as dimensionless — dimensional bug fixed

---

## 🔭 9 Physics Pipelines

### Pipeline 1 — FDM Soliton
**Fuzzy Dark Matter Soliton Core**  
*Repo: QCAUS/app.py*

The ground-state solution of the Schrödinger-Poisson equation for ultra-light bosons (~10⁻²² eV):

```
ρ(r) = ρ₀ [sin(kr) / (kr)]²     k = π/r_s     r_s = 1/m
```

Produces a 2D spatial density map and radial profile. The soliton scale r_s is set by the FDM mass slider. Overlaid as the **green channel** on the RGB image output.

| Parameter | Range | Default |
|-----------|-------|---------|
| FDM Mass (×10⁻²² eV) | 0.1 – 10.0 | 1.0 |

---

### Pipeline 2 — Photon–Dark Photon Spectral Duality
**FFT Kinetic Mixing / PDP Interference**  
*Repo: StealthPDPRadar / pdp_radar_core.py*

An original Fourier-domain filter (Ford 2026) separating ordinary and dark photon modes in image space:

```
dark_mask = ε · e^{-ΩR²} · |sin(2πRL/f)| · (1 − e^{-R²/f})
```

The oscillation length `L = 100 / (m_dark_GeV × 10⁹)` connects the dark photon mass to the fringe spacing. The **PDP interference map** is overlaid as the **blue channel** on the RGB output. Also drives the animated two-field wave.

| Parameter | Range | Default |
|-----------|-------|---------|
| Kinetic Mixing ε | 1×10⁻¹² – 1×10⁻⁸ | 1×10⁻¹⁰ |
| Fringe Scale (pixels) | 10 – 80 | 45 |
| Ω_PD Entanglement | 0.05 – 0.50 | 0.20 |

---

### Pipeline 3 — Entanglement Residuals
**Extended Von Neumann Entropy with Cross-Terms**  
*Repo: StealthPDPRadar / pdp_radar_core.py*

An original formulation (Ford 2026) extending standard entropy with spatial interference cross-terms:

```
S_res = −ρ · log(ρ) + |ψ_ord + ψ_dark|² − ψ_ord² − ψ_dark²
```

The cross-terms encode entanglement structure beyond scalar entropy, providing a 2D spatial map of quantum correlation complexity in image space.

---

### Pipeline 4 — Dark Photon Detection (Bayesian)
**Kinetic-Mixing Probability Map**  
*Repo: StealthPDPRadar / pdp_radar_core.py*

Standard Bayesian update applied to the dark mode and residuals fields:

```
P_dark = (prior · L) / (prior · L + (1 − prior))
```

Outputs a probability heatmap with threshold alerts: CLEAR (<20%) / SIGNAL (20–50%) / STRONG (>50%). Overlaid as the **red channel** enhancement on the RGB output.

---

### Pipeline 5 — Blue-Halo Fusion
**Multi-Channel Composite Detection Image**  
*Repo: StealthPDPRadar / pdp_radar_core.py*

Original composite rendering (Ford 2026) applying gamma correction γ = 0.45:

```
R = original signal
G = entanglement residuals (enhanced local contrast)
B = dark mode (Gaussian smoothed + direct)
output = clip(RGB ^ 0.45, 0, 1)
```

Produces the characteristic blue halo signature around dark photon field concentrations.

---

### Pipeline 6 — RGB Quantum Overlay on Source Image
**Direct Astrophysical Image Enhancement**  
*Repo: QCAUS/app.py (Ford 2026)*

Original channel-mapped overlay (Ford 2026) applied directly to the uploaded or preset astronomical image using the Ω_PD entanglement parameter:

```
R = image · (1 − Ω·0.3) + P_dark · Ω·0.4    ← original signal + detection highlight
G = image · (1 − Ω·0.5) + soliton · Ω·0.8   ← FDM dark matter density
B = image · (1 − Ω·0.5) + interf · Ω·0.8    ← PDP fringe interference
```

This is the primary "before/after" output — the source image with all three quantum fields rendered as distinct colour channels.

---

### Pipeline 7 — Magnetar QED Explorer
**Strong-Field Quantum Electrodynamics**  
*Repo: Magnetar-Quantum-Vacuum-Engineering*

Three physics models computed over the magnetar dipole field:

| Quantity | Formula | Basis |
|----------|---------|-------|
| Dipole field | B = B₀(R/r)³ √(3cos²θ + 1) | Jackson 1998 |
| Euler-Heisenberg | ΔL = (α/45π)(B/B_crit)² | Heisenberg & Euler 1936 |
| Dark photon conversion | P = ε²(1 − e^{−B²/m²}) | Ford 2026 (modified form) |

Critical field: B_crit = 4.414 × 10¹³ G. Output is a 4-panel figure: dipole streamplot, EH heatmap, P_conv heatmap, and radial profiles.

| Parameter | Range | Default |
|-----------|-------|---------|
| B₀ (log₁₀ G) | 13.0 – 16.0 | 15.0 |
| Magnetar ε | 0.01 – 0.50 | 0.10 |

---

### Pipeline 8 — QCIS Matter Power Spectrum & EM Mapping
**Quantum-Corrected Cosmological Perturbations**  
*Repo: Quantum-Cosmology-Integration-Suite*

Quantum-corrected power spectrum using the BBKS transfer function (Ford 2026 parameterisation):

```
P(k) = P_ΛCDM(k) × (1 + f_NL · (k/k₀)^n_q)     k₀ = 0.05 h/Mpc
```

BBKS transfer function T(k) with n_s = 0.965 (Planck 2018). Outputs log-log spectrum plot comparing ΛCDM baseline to quantum-corrected prediction, plus a tri-band EM composite:

```
R = Infrared   (img^0.5 × Q_factor)     λ ~ 10–1000 μm
G = Visible    (img^0.8 × Q_factor)     λ ~ 400–700 nm
B = X-ray      (img^1.5 × Q_factor)     λ ~ 0.01–10 nm
```

where Q_factor = P_quantum(k=0.1) / P_ΛCDM(k=0.1) is the quantum correction ratio.

| Parameter | Range | Default |
|-----------|-------|---------|
| f_NL | 0.0 – 5.0 | 1.0 |
| n_q | 0.0 – 2.0 | 0.5 |

---

### Pipeline 9 — Von Neumann Primordial Entanglement
**Density Matrix Evolution in the Early Universe**  
*Repo: Primordial-Photon-DarkPhoton-Entanglement*

Full density matrix time-evolution for primordial photon–dark photon mixing (standard + Ford 2026):

```
i ∂ρ/∂t = [H_eff, ρ]
S = −Tr(ρ log ρ) = −Σᵢ λᵢ log λᵢ      (eigenvalues of 2×2 ρ)
P_mix = ρ_dd(t) = |⟨ψ_d|ψ_γ⟩|²
```

Outputs a dual-panel figure: Von Neumann entropy evolution S(t) and photon ↔ dark photon oscillation probability ρ_dd(t), with decoherence damping controlled by Ω_PD.

| Parameter | Range | Default |
|-----------|-------|---------|
| Dark Mass (×10⁻⁹ eV) | 0.1 – 10.0 | 1.0 |
| Primordial Mixing θ | 0.01 – 1.00 | 0.10 |

---

## 📊 Key Outputs Summary

| Pipeline | Output | Download |
|----------|--------|---------|
| **P1: FDM Soliton** | 2D density map + radial profile | PNG |
| **P2: PDP Interference** | Fringe pattern + spectral mask | PNG |
| **P3: Entanglement Residuals** | 2D entropy + cross-term map | PNG |
| **P4: Dark Photon Detection** | Bayesian probability heatmap | PNG |
| **P5: Blue-Halo Fusion** | R/G/B composite γ=0.45 | PNG |
| **P6: RGB Overlay** | Source image + 3-channel quantum overlay | PNG |
| **P7: Magnetar QED** | 4-panel: dipole, EH, P_conv, radial | PNG |
| **P8: QCIS Spectrum** | Log-log P(k) + EM composite + 3 bands | PNG |
| **P9: Von Neumann** | Entropy S(t) + mixing probability | PNG |
| **ZIP Archive** | All 14+ outputs in one download | ZIP |

---

## 🎯 Preset Datasets

| Preset | Description | Physics Focus |
|--------|-------------|---------------|
| **SGR 1806-20 (Magnetar)** | Synthetic magnetar field from dipole model | Pipelines 5, 6, 7 |
| **Galaxy Cluster (Abell 209 style)** | Gaussian cluster halo + noise | Pipelines 1, 2, 4, 6 |
| **Airport Radar — Nellis AFB Historical** | Synthetic radar with stealth signatures | Pipeline 4, 5 |
| **Airport Radar — JFK International Historical** | Synthetic radar field | Pipeline 4, 5 |
| **Airport Radar — LAX Historical** | Synthetic radar field | Pipeline 4, 5 |

Upload your own FITS, JPEG, or PNG astronomical image to apply all 9 pipelines to real data.

---

## 🧪 Supported Image Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| **FITS** | .fits, .fit | Astronomical (Hubble, JWST, Chandra) |
| **JPEG** | .jpg, .jpeg | Standard photographic |
| **PNG** | .png | Lossless images |

Images are converted to grayscale float32 and resized to a maximum of 400×400 for performance. The original aspect ratio and scale are preserved in all output labels.

---

## 📥 Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/tlcagford/QCAUS.git
cd QCAUS

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Dependencies

```
streamlit>=1.28.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
Pillow>=10.0.0
```

> **Note:** `astropy` is listed as an optional dependency for native FITS reading. The app will fall back to PIL for standard image formats if astropy is not installed.

---

## 📐 Physics Reference — All Equations

### Standard Physics (Established Literature)

| Module | Equation | Source |
|--------|----------|--------|
| FDM Soliton profile | ρ(r) = ρ₀[sin(kr)/(kr)]², k=π/r_s | Hui et al. 2017; Ruffini & Bonazzola 1969 |
| Schrödinger-Poisson | i∂ₜψ = −∇²ψ/(2m) + Φψ, ∇²Φ = 4πG\|ψ\|² | Canonical SP system |
| Magnetar dipole field | B = B₀(R/r)³√(3cos²θ+1) | Jackson 1998 |
| Euler-Heisenberg QED | ΔL = (α/45π)(B/B_crit)² | Heisenberg & Euler 1936 |
| Von Neumann entropy | S = −Tr(ρ log ρ) | Standard quantum mechanics |
| Bayesian detection | P = prior·L / (prior·L + (1−prior)) | Standard Bayesian inference |
| BBKS transfer function | T(k) — see code | Bardeen, Bond, Kaiser & Szalay 1986 |

### Original Contributions (Ford 2026)

| # | Contribution | Formula |
|---|-------------|---------|
| 1 | **Two-Field Coupled SP System** | i∂ₜψ_t = −∇²ψ_t/(2m_t) + (Φ_t + εΦ_a)ψ_t (and symmetric) |
| 2 | **PDP Interference Density** | ρ = \|ψ_t\|² + \|ψ_a\|² + 2·Re(ψ_t\*·ψ_a·e^{iΔφ}) |
| 3 | **PDP Spectral Duality Mask** | dark_mask = ε·e^{−ΩR²}·\|sin(2πRL/f)\|·(1−e^{−R²/f}) |
| 4 | **Entanglement Residuals** | S_res = −ρ·log(ρ) + \|ψ_ord+ψ_dark\|²−ψ_ord²−ψ_dark² |
| 5 | **QCIS Quantum Correction** | P(k) = P_ΛCDM(k)×(1 + f_NL·(k/k₀)^n_q) |
| 6 | **Dark Photon Conversion (simplified)** | P_conv = ε²(1−e^{−B²/m²}) |
| 7 | **Ω_PD Entanglement Parameter** | Ω_PD = ⟨ψ_t\|ψ_a⟩ / √(⟨ψ_t\|ψ_t⟩⟨ψ_a\|ψ_a⟩) |
| 8 | **RGB Overlay Channel Mapping** | R=orig+P_dark · G=FDM-soliton · B=PDP-interf |
| 9 | **Unified 9-Pipeline Framework** | Integration of all pipelines into single interactive app |

---

## 🚀 Quick Start — Python API

```python
import numpy as np

# Pipeline 1: FDM Soliton
from QCAUS_v4 import fdm_soliton_2d, fdm_soliton_profile
soliton_map = fdm_soliton_2d(size=300, m_fdm=1.0)
r, rho = fdm_soliton_profile(m_fdm=1.0)

# Pipeline 2+3: PDP Spectral Duality + Entanglement Residuals
from QCAUS_v4 import pdp_spectral_duality, entanglement_residuals
ord_mode, dark_mode = pdp_spectral_duality(image, omega=0.2, fringe_scale=45,
                                            mixing_eps=1e-10, fdm_mass=1.0)
ent_res = entanglement_residuals(image, ord_mode, dark_mode,
                                  strength=0.06, mixing_eps=1e-10, fringe_scale=45)

# Pipeline 4: Bayesian Dark Photon Detection
from QCAUS_v4 import dark_photon_detection_prob
dp_prob = dark_photon_detection_prob(dark_mode, ent_res, strength=0.06)

# Pipeline 7: Magnetar QED
from QCAUS_v4 import magnetar_physics, plot_magnetar_qed
B_map, qed_map, conv_map = magnetar_physics(size=300, B0=1e15, eps=0.1)
fig = plot_magnetar_qed(B0=1e15, epsilon=0.1)

# Pipeline 8: QCIS Power Spectrum
from QCAUS_v4 import qcis_power_spectrum
k, P_lcdm, P_quantum = qcis_power_spectrum(f_nl=1.0, n_q=0.5)

# Pipeline 9: Von Neumann Primordial Entanglement
from QCAUS_v4 import von_neumann_primordial
t, S, mixing_prob, rho_gg, rho_dd = von_neumann_primordial(
    omega=0.2, dark_mass=1e-9, mixing=0.1)
```

---

## 📊 Example Outputs

### Before / After — RGB Quantum Overlay
- **Before**: Source image in grayscale (HST/JWST public data or preset)
- **After**: RGB composite — 🟢 FDM soliton density (green) · 🔵 PDP interference (blue) · 🔴 original + dark photon detection (red)
- **Data panel**: Ω_PD · Fringe · ε · FDM mass · Entropy · P_dark

### Wave Interference Animation
- **Re(ψ_light)**: Cyan oscillating light-sector wave — cos(r·cos(t))
- **Re(ψ_dark)**: Magenta oscillating dark-sector wave — cos(r·sin(t) + Δφ)
- **ρ interference**: Yellow density — sum + cross-term showing beating pattern
- **|ψ| envelope**: Dashed — common Gaussian profile exp(−r²/4)

### Magnetar QED (4-panel)
- **Dipole streamplot**: Field line geometry coloured by log|B|
- **Euler-Heisenberg heatmap**: Vacuum polarisation ΔL/ΔL_max
- **Dark photon conversion map**: P_conv/P_max
- **Radial profiles**: |B|, ΔL (norm.), P_conv (norm.) on twin axes

### Von Neumann Primordial Entanglement
- **Entropy S(t)**: Von Neumann entropy rising from zero as decoherence builds
- **ρ_dd(t)**: Photon → dark photon oscillation probability with damping

---

## 📝 Contributions & Original Work

### Standard Implementations

These modules implement established physics from the peer-reviewed literature and are cited accordingly in the code.

| Module | Basis |
|--------|-------|
| FDM soliton profile | Hui et al. 2017; Marsh 2016 |
| Schrödinger-Poisson | Ruffini & Bonazzola 1969 |
| Magnetar dipole | Jackson 1998 |
| Euler-Heisenberg | Heisenberg & Euler 1936; Schwinger 1951 |
| Von Neumann entropy | Standard quantum mechanics |
| Bayesian inference | Standard probability theory |
| BBKS transfer function | Bardeen et al. 1986 |

### Original Contributions (Ford 2026)

Nine original extensions and syntheses developed specifically for QCAUS, listed in the Physics Reference table above. The primary novel contributions are:

1. The **two-field coupled Schrödinger-Poisson system** treating light and dark sector fields on equal footing in a shared gravitational potential, enabling direct simulation of interference and entanglement between sectors.

2. The **PDP spectral duality mask** — a Fourier-domain filter that synthesises Gaussian apodisation, fringe periodicity, and kinetic mixing phase accumulation into a single expression for dark photon field extraction from image data.

3. The **Ω_PD entanglement parameter** as a scalar control for the mixing strength between sectors, with a defined normalisation relative to the inner products of both wavefunctions.

4. The **unified 9-pipeline application** integrating all modules with real-time parameter exploration and cross-disciplinary output.

---

## 📄 Citation

If you use QCAUS in your research, please cite:

```bibtex
@software{Ford2026QCAUS,
  author    = {Ford, Tony E.},
  title     = {Quantum Cosmology \& Astrophysics Unified Suite (QCAUS) v1.0},
  year      = {2026},
  url       = {https://github.com/tlcagford/QCAUS},
  note      = {Patent Pending}
}
```

For standard physics components, please also cite the original literature (see Physics Reference section above).

---

## 📜 License

This project is released under a **Dual License**:

- **Academic / Non-Commercial Use**: Free for research, education, and personal projects
- **Commercial Use**: Requires a separate license — contact the author

See `LICENSE` for full terms.

---

## 📧 Contact

**Tony E. Ford**  
Independent Researcher — Astrophysics & Quantum Systems  
GitHub: [@tlcagford](https://github.com/tlcagford)  
Email: tlcagford@gmail.com  
App: [qcaustfordmodel.streamlit.app](https://qcaustfordmodel.streamlit.app/)

---

## 🙏 Acknowledgments

- **NASA/ESA Hubble Space Telescope & JWST** — public FITS data used in example outputs
- **OpenSky Network** — historical radar data for preset examples
- **FDM, QED, and cosmology research communities** — foundational literature
- **Streamlit, NumPy, SciPy, Matplotlib, Pillow** — open-source toolchain

---

## 🔗 Related Repositories

| Project | Description |
|---------|-------------|
| [StealthPDPRadar](https://github.com/tlcagford/StealthPDPRadar) | Photon–dark photon radar core (pdp_radar_core.py) — Pipelines 2–5 |
| [Magnetar-Quantum-Vacuum-Engineering](https://github.com/tlcagford/Magnetar-Quantum-Vacuum-Engineering) | Magnetar QED explorer — Pipeline 7 |
| [Primordial-Photon-DarkPhoton-Entanglement](https://github.com/tlcagford/Primordial-Photon-DarkPhoton-Entanglement) | Von Neumann evolution — Pipeline 9 |
| [Quantum-Cosmology-Integration-Suite](https://github.com/tlcagford/Quantum-Cosmology-Integration-Suite) | QCIS power spectrum — Pipeline 8 |

---

## 📸 Screenshots

### RGB Quantum Overlay (Before / After)
*Source image in grayscale vs. RGB composite with FDM soliton (green), PDP interference (blue), and dark photon detection (red) overlaid directly on the astrophysical data*

### Animated FDM Two-Field Wave
*Re(ψ_light) in cyan and Re(ψ_dark) in magenta oscillating with phase separation driven by cos(t) vs sin(t) — ρ interference in yellow shows the beating pattern*

### Magnetar QED Explorer
*4-panel figure: dipole field streamplot · Euler-Heisenberg vacuum polarisation heatmap · dark photon conversion map · radial profile comparison*

### QCIS Matter Power Spectrum
*Log-log P(k) comparison of ΛCDM baseline (blue) vs. quantum-corrected QCIS prediction (red dashed) with pivot scale marker*

### Von Neumann Primordial Entanglement
*Left: Von Neumann entropy S(t) with area fill. Right: photon ↔ dark photon oscillation probability ρ_dd(t) with decoherence damping*

---

*QCAUS v1.0 | Tony E. Ford | Patent Pending | 2026*
