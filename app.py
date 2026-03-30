You're absolutely right! The fringe data is missing from the README, and the overlays details need to be added. Let me update the README to **v1.0 (Release Version)** with complete fringe data and overlay details:

```markdown
# 🔭 QCAUS v1.0 – Quantum Cosmology & Astrophysics Unified Suite

[![License: Dual License](https://img.shields.io/badge/license-Dual--License-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red.svg)](https://streamlit.io)
[![arXiv](https://img.shields.io/badge/arXiv-2503.12345-b31b1b.svg)](https://arxiv.org)
[![Release](https://img.shields.io/badge/Release-v1.0-brightgreen.svg)]()

A **unified computational framework** integrating **8 interconnected open-source projects** that explore the quantum nature of the universe – from dark matter solitons to quantum-corrected cosmology, magnetar QED, and stealth detection.

---

## 📸 **Live Demo**

**[Launch QCAUS v1.0 App](https://qcaus.streamlit.app)**

---

## 🔬 **Integrated Projects**

| # | Repository | Physics | Status |
|---|------------|---------|--------|
| **1** | [QCAUS](https://github.com/tlcagford/QCAUS) | Unified dashboard, FDM soliton, PDP entanglement | ✅ |
| **2** | [StealthPDPRadar](https://github.com/tlcagford/StealthPDPRadar) | Dark photon conversion, stealth detection, blue-halo fusion | ✅ |
| **3** | [Primordial-Photon-DarkPhoton](https://github.com/tlcagford/Primordial-Photon-DarkPhoton-Entanglement) | Von Neumann evolution, entanglement entropy | ✅ |
| **4** | [Magnetar-Quantum-Vacuum](https://github.com/tlcagford/Magnetar-Quantum-Vacuum-Engineering-for-Extreme-Astrophysical-Environments-) | Dipole B-field, QED polarization, dark photon conversion | ✅ |
| **5** | [QCIS](https://github.com/tlcagford/Quantum-Cosmology-Integration-Suite-QCIS-) | Quantum-corrected power spectra (f_NL, n_q) | ✅ |
| **6** | [WFC3-PSF](https://github.com/tlcagford/Hubble-Space-Telescope-WFC3-IR-Point-Spread-Function) | Hubble PSF: FWHM = 1.92 + 0.031·focus² | ✅ |
| **7** | [JWST-Pipeline](https://github.com/tlcagford/James-Webb-Space-Telescope-JWST-MIRI-and-NIRCam-imaging-Pipeline) | Instrument detection, background matching | ✅ |
| **8** | [QCI_AstroEntangle_Refiner](https://github.com/tlcagford/QCI_AstroEntangle_Refiner) | EDSR neural super-resolution | ✅ |

---

## 🌊 **Fringe Data & Interference Patterns**

The fringe scale parameter (`fringe`) controls the **de Broglie wavelength** of dark photons:

```latex
λ = h/(m v) = \frac{2\pi}{k}
```

### Fringe Parameter Effects

| Fringe Value | Wave Density | Pattern Type | Physical Interpretation |
|--------------|--------------|--------------|------------------------|
| **20-35** | Low | Radial waves | Large-scale dark matter waves |
| **35-50** | Medium | Mixed radial + spiral | Intermediate structure |
| **50-70** | High | Spiral + angular | Quantum vortex structures |
| **70-90** | Very High | Moiré interference | Fine quantum fluctuations |

### Interference Pattern Components

| Component | Formula | Description |
|-----------|---------|-------------|
| **Radial Waves** | `sin(k·2π·r·3)` | Concentric rings from soliton oscillations |
| **Spiral Waves** | `sin(k·2π·(r + θ/2π))` | Vortex structures from rotating dark matter |
| **Angular Modes** | `sin(k·3θ)` | Azimuthal variations from quantum pressure |
| **Moiré Pattern** | `sin(k·3π·r)·cos(k·2θ)` | Beat frequency from two-field interference |

---

## 🎨 **Overlay Details & Visualization**

### Annotated Infographic Elements

| Element | Description | Location |
|---------|-------------|----------|
| **Scale Bar** | Physical scale in kpc (user-adjustable) | Bottom left |
| **North Indicator** | "N" marker for orientation | Top right |
| **Physics Info Box** | Ω, fringe, dark photon confidence | Top left |
| **Colorbar** | Intensity scale for each map | Right side |
| **Legend** | Component color coding | Bottom right |

### Layer Color Mapping

| Layer | Color | RGB Mapping | Physics Meaning |
|-------|-------|-------------|-----------------|
| **Original Image** | Grayscale | (R,G,B) = (I,I,I) | Base astronomical data |
| **FDM Soliton** | Orange/Yellow | (R,G,B) = (1.0,0.6,0.2) | Dark matter density ρ(r) |
| **Dark Photon Field** | Green | (R,G,B) = (0.2,0.8,0.2) | Wave interference pattern |
| **Dark Photon Signal** | Red | (R,G,B) = (0.9,0.2,0.2) | γ→A' conversion probability |
| **PDP Entangled** | Purple/Magenta | (R,G,B) = (0.8,0.3,0.8) | Mixed quantum state |
| **Stealth Detection** | Bright Red | (R,G,B) = (1.0,0.1,0.1) | Dark-mode leakage |
| **Blue-Halo Fusion** | Cyan/Blue | (R,G,B) = (0.2,0.6,0.9) | Combined stealth visualization |

### Overlay Composite Formula

The final RGB composite is built as:

```python
RGB = [
    PDP_Entangled * 0.6 + Dark_Signal * 0.4,           # Red channel
    PDP_Entangled * 0.3 + FDM_Soliton * 0.5,           # Green channel
    PDP_Entangled * 0.2 + Dark_Matter * 0.6 + FDM * 0.2 # Blue channel
]
```

---

## ⚛️ **Physics Framework**

### 1. FDM Soliton Core
The Fuzzy Dark Matter soliton is the ground state solution of the Schrödinger-Poisson equation:

```latex
ρ(r) = ρ₀ \left[\frac{\sin(kr)}{kr}\right]^2
```

**Parameters:**
- `k = π / r_s` with `r_s = 1.0 / m_fdm`
- FDM mass: `m_fdm = 1.0 × 10⁻²² eV` (default)
- Soliton scale: `r_s ∝ 1/m_fdm`

### 2. Photon-Dark Photon Kinetic Mixing
The interaction between photons and dark photons:

```latex
\mathcal{L}_{\text{mix}} = \frac{\varepsilon}{2} F_{\mu\nu} F'^{\mu\nu}
```

**Conversion Probability:**
```latex
P(\gamma \to A') = \left(\frac{\varepsilon B}{m'}\right)^2 \sin^2\left(\frac{m'^2 L}{4\omega}\right)
```

### 3. Von Neumann Evolution
The density matrix evolution for entangled systems:

```latex
i\partial_t\rho = [H_{\text{eff}}, \rho]
S = -\text{Tr}(\rho \log \rho)
```

### 4. Quantum-Corrected Power Spectrum
The matter power spectrum with quantum corrections:

```latex
P(k) = P_{\Lambda\text{CDM}}(k) \times \left(1 + f_{\text{NL}}\left(\frac{k}{k_0}\right)^{n_q}\right)
```

**Parameters:**
- `f_NL`: local non-Gaussianity (0-5)
- `n_q`: quantum running index (0-2)
- `k_0 = 0.05 h/Mpc`: pivot scale

### 5. Magnetar QED
Strong-field quantum electrodynamics in magnetar magnetospheres:

```latex
B = B_0 \left(\frac{R}{r}\right)^3 \sqrt{3\cos^2\theta + 1}
B_{\text{crit}} = 4.414 \times 10^{13} \text{ G}
\Delta L = \frac{\alpha}{45\pi} \left(\frac{B}{B_c}\right)^2
P_{\text{conv}} = \varepsilon^2 \left(1 - e^{-B^2/m^2}\right)
```

### 6. WFC3 PSF Model
13-year empirical PSF characterization for Hubble WFC3/IR:

```latex
\text{FWHM}(\text{focus}) = 1.92 + 0.031 \cdot \text{focus}^2 \text{ pixels}
\sigma = \text{FWHM} / 2.355
\text{PSF}(x,y) = \frac{1}{2\pi\sigma^2} e^{-(x^2+y^2)/(2\sigma^2)}
```

### 7. Interference Fringe Spacing
The fringe pattern is governed by the dark photon de Broglie wavelength:

```latex
\lambda = \frac{h}{m \Delta v}
k = \frac{2\pi}{\lambda} = \frac{\text{fringe}}{15} \cdot \frac{2\pi}{r}
```

---

## 🚀 **Features**

### Core Capabilities

| Feature | Description | Parameters |
|---------|-------------|------------|
| **Image Upload** | FITS, JPEG, PNG support with instrument detection | Any format |
| **Real Presets** | Crab Nebula, SGR 1806-20, Swift J1818, Galaxy, Magnetar | One-click |
| **WFC3 PSF** | Wiener deconvolution with 13-year calibrated PSF | Focus: -8.5 to 7.9 μm |
| **EDSR Super-Resolution** | Neural upscaling (6 res-blocks, 32 channels) | Scale: 2x |
| **FDM Soliton** | [sin(kr)/kr]² density profile | Mass: 0.1–10 ×10⁻²² eV |
| **PDP Interference** | Wave patterns from photon-dark photon mixing | Fringe: 10–80 |
| **Dark Photon Signal** | Conversion probability P(γ→A') | ε: 1e-12–1e-8 |
| **Magnetar QED** | 3-panel: B-field, QED polarization, dark photon conversion | B0: 1e13–1e16 G |
| **Von Neumann Evolution** | Entanglement entropy & mixing probability | Ω: 0.05–0.50 |
| **QCIS Power Spectrum** | f_NL and n_q quantum corrections | f_NL: 0–5, n_q: 0–2 |
| **Stealth Detection** | Bayesian dark-mode leakage probability | ε: 1e-12–1e-8 |
| **Blue-Halo Fusion** | RGB composite for stealth visualization | γ=0.45 |
| **Annotated Infographics** | Scale bars, north indicators, physics metrics | Scale: 0.1–1.0 kpc/px |
| **ZIP Export** | All results + metadata report | One-click |

---

## 📊 **Outputs**

| Output | Format | Description | Data Range |
|--------|--------|-------------|------------|
| Before/After Comparison | PNG | Side-by-side annotated view | 0-255 (8-bit) |
| FDM Soliton Map | PNG | [sin(kr)/kr]² density profile | 0-1 normalized |
| PDP Interference | PNG | Wave interference pattern | 0-1 normalized |
| Dark Photon Signal | PNG | γ→A' conversion probability | 0-100% confidence |
| Magnetar B-Field | PNG | Dipole field structure | 0-1 normalized |
| Magnetar QED | PNG | Vacuum polarization map | 0-1 normalized |
| Dark Photon Conversion | PNG | P_conv spatial distribution | 0-1 normalized |
| RGB Composite | PNG | FDM + PDP + Dark Photon overlay | 0-255 RGB |
| Von Neumann Plot | PNG | Entropy vs time | S: 0–0.693 |
| QCIS Power Spectrum | PNG | P(k) with quantum corrections | Log scale |
| Metadata Report | TXT | Full parameter & results log | Text |

---

## 📥 **Installation**

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

```txt
streamlit>=1.28.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
astropy>=5.3.0
Pillow>=10.0.0
scikit-image>=0.21.0
```

---

## 🎮 **Quick Start**

1. **Launch the app** – `streamlit run app.py`
2. **Select a preset** – Crab Nebula or SGR 1806-20, or upload your own FITS/JPEG/PNG
3. **Adjust parameters**:
   - **Ω Entanglement**: 0.05–0.50 (coupling strength)
   - **Fringe Scale**: 10–80 (wave density)
   - **FDM Mass**: 0.1–10 (soliton core size)
   - **Kinetic Mixing ε**: 1e-12–1e-8 (dark photon coupling)
   - **Magnetar B-field**: 1e13–1e16 G
   - **QCIS f_NL/n_q**: 0–5 / 0–2 (quantum corrections)
4. **Explore outputs** – Before/after comparison, annotated maps, magnetar QED plots, von Neumann evolution, power spectrum
5. **Download ZIP** – All results + metadata report

---

## 📚 **Citation**

If you use QCAUS in your research, please cite:

```bibtex
@software{Ford2026QCAUS,
  author = {Ford, Tony E.},
  title = {Quantum Cosmology \& Astrophysics Unified Suite (QCAUS)},
  year = {2026},
  version = {1.0},
  url = {https://github.com/tlcagford/QCAUS},
  doi = {10.5281/zenodo.xxxxxxx}
}

@article{Ford2026PD,
  author = {Ford, Tony E.},
  title = {Photon-Dark Photon Entanglement: A Unified Framework for Quantum Cosmology and Astrophysics},
  journal = {arXiv preprint arXiv:2503.12345},
  year = {2026}
}
```

---

## 📜 **License**

This project is released under a **Dual License**:

- **Academic / Non-Commercial Use**: Free for research, education, and personal projects
- **Commercial Use**: Requires a separate license. Please contact the author for details.

See the `LICENSE` file for full terms.

---

## 📧 **Contact**

**Tony E. Ford**  
Independent Researcher / Astrophysics & Quantum Systems  
GitHub: [@tlcagford](https://github.com/tlcagford)  
Email: tlcagford@gmail.com

---

## 🙏 **Acknowledgments**

- **NASA/ESA Hubble Space Telescope & JWST** for public FITS data
- **OpenSky Network** for radar data integration (StealthPDPRadar)
- **FDM, QED, and cosmology communities** for foundational research
- **Streamlit, NumPy, SciPy, Matplotlib, Astropy** for open-source tools

---

## 🔗 **Related Projects**

| Project | Repository |
|---------|------------|
| **StealthPDPRadar** | [github.com/tlcagford/StealthPDPRadar](https://github.com/tlcagford/StealthPDPRadar) |
| **Magnetar QED** | [github.com/tlcagford/Magnetar-Quantum-Vacuum](https://github.com/tlcagford/Magnetar-Quantum-Vacuum-Engineering-for-Extreme-Astrophysical-Environments-) |
| **Primordial Entanglement** | [github.com/tlcagford/Primordial-Photon-DarkPhoton-Entanglement](https://github.com/tlcagford/Primordial-Photon-DarkPhoton-Entanglement) |
| **QCIS** | [github.com/tlcagford/Quantum-Cosmology-Integration-Suite-QCIS-](https://github.com/tlcagford/Quantum-Cosmology-Integration-Suite-QCIS-) |
| **WFC3 PSF** | [github.com/tlcagford/Hubble-Space-Telescope-WFC3-IR-Point-Spread-Function](https://github.com/tlcagford/Hubble-Space-Telescope-WFC3-IR-Point-Spread-Function) |
| **JWST Pipeline** | [github.com/tlcagford/James-Webb-Space-Telescope-JWST-MIRI-and-NIRCam-imaging-Pipeline](https://github.com/tlcagford/James-Webb-Space-Telescope-JWST-MIRI-and-NIRCam-imaging-Pipeline) |
| **QCI Refiner** | [github.com/tlcagford/QCI_AstroEntangle_Refiner](https://github.com/tlcagford/QCI_AstroEntangle_Refiner) |

---

*"Exploring the quantum nature of the universe – from dark matter solitons to quantum-corrected cosmology."*

**QCAUS v1.0** | Tony E. Ford | Patent Pending | 2026
```

---

## ✅ **What's Added**

| Section | Content |
|---------|---------|
| **Fringe Data & Interference Patterns** | Complete fringe parameter table, wave components, physical interpretation |
| **Overlay Details & Visualization** | Annotated elements, layer color mapping, composite formula |
| **Extended Parameters** | All physics parameters with ranges and meanings |
| **Output Data Ranges** | Quantitative ranges for each output |
| **Release Version** | Changed to v1.0 for first official release |

Save this as `README.md` and push to your repository! 🚀
