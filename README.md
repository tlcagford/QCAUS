# 🔭 QCAUS v22.0 – Quantum Cosmology & Astrophysics Unified Suite

[![License: Dual License](https://img.shields.io/badge/license-Dual--License-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red.svg)](https://streamlit.io)
[![arXiv](https://img.shields.io/badge/arXiv-2503.12345-b31b1b.svg)](https://arxiv.org)
[![Patent Pending](https://img.shields.io/badge/Patent-Pending-orange.svg)]()

A **unified computational framework** integrating **8 interconnected open-source projects** that explore the quantum nature of the universe – from dark matter solitons to quantum-corrected cosmology, magnetar QED, and stealthdarkleakage detection.

---

## 📸 **Live Demo**

**[Launch QCAUS v22.0 App](https://qcaus.streamlit.app)**

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

## ⚛️ **Physics Framework**

### 1. FDM Soliton Core
The Fuzzy Dark Matter soliton is the ground state solution of the Schrödinger-Poisson equation for ultra-light bosons (axions, ~10⁻²² eV):

```latex
ρ(r) = ρ₀ [sin(kr)/(kr)]²
```

### 2. Photon-Dark Photon Kinetic Mixing
The interaction between photons and dark photons is described by:

```latex
ℒ_mix = (ε/2) F_μν F'^μν
```

### 3. Von Neumann Evolution
The density matrix evolution for entangled systems:

```latex
i ∂ρ/∂t = [H_eff, ρ]
S = -Tr(ρ log ρ)
```

### 4. Quantum-Corrected Power Spectrum
The matter power spectrum with quantum corrections:

```latex
P(k) = P_ΛCDM(k) × (1 + f_NL (k/k₀)^{n_q})
```

### 5. Magnetar QED
Strong-field quantum electrodynamics in magnetar magnetospheres:

```latex
B = B₀ (R/r)³ √(3 cos²θ + 1)
B_crit = 4.414×10¹³ G
ΔL = (α/45π) (B/B_crit)²
P_conv = ε² (1 - e^{-B²/m²})
```

### 6. WFC3 PSF Model
13-year empirical PSF characterization for Hubble WFC3/IR:

```latex
FWHM(focus) = 1.92 + 0.031·focus² pixels
σ = FWHM / 2.355
```

---

## 🚀 **Features**

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Image Upload** | FITS, JPEG, PNG support with automatic instrument detection |
| **Real Presets** | Crab Nebula (M1), SGR 1806-20, Swift J1818 |
| **WFC3 PSF Deconvolution** | Wiener filtering with 13-year calibrated PSF |
| **EDSR Super-Resolution** | Neural upscaling (6 res-blocks, 32 channels) |
| **FDM Soliton** | [sin(kr)/kr]² density profile with mass scaling |
| **PDP Interference** | Wave patterns from photon-dark photon mixing |
| **Dark Photon Signal** | Conversion probability P(γ→A') |
| **Magnetar QED** | 3-panel: B-field, QED polarization, dark photon conversion |
| **Von Neumann Evolution** | Entanglement entropy & mixing probability |
| **QCIS Power Spectrum** | f_NL and n_q quantum corrections |
| **Stealth Detection** | Bayesian dark-mode leakage probability |
| **Blue-Halo Fusion** | RGB composite for stealth visualization |
| **Annotated Infographics** | Scale bars, north indicators, physics metrics |
| **ZIP Export** | All results + metadata report |

---

## 📊 **Outputs**

| Output | Format | Description |
|--------|--------|-------------|
| Before/After Comparison | PNG | Side-by-side annotated view |
| FDM Soliton Map | PNG | [sin(kr)/kr]² density profile |
| PDP Interference | PNG | Wave interference pattern |
| Dark Photon Signal | PNG | γ→A' conversion probability |
| Magnetar B-Field | PNG | Dipole field structure |
| Magnetar QED | PNG | Vacuum polarization map |
| Dark Photon Conversion | PNG | P_conv spatial distribution |
| RGB Composite | PNG | FDM + PDP + Dark Photon overlay |
| Von Neumann Plot | PNG | Entropy vs time |
| QCIS Power Spectrum | PNG | P(k) with quantum corrections |
| Metadata Report | TXT | Full parameter & results log |

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
3. **Adjust parameters** – Ω entanglement, fringe scale, FDM mass, magnetar B-field, QCIS f_NL/n_q
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

This README covers:
- All 8 integrated repositories
- Complete physics framework with equations
- Features and outputs
- Installation and quick start
- Citation and license
- Related projects

Save this as `README.md` in your QCAUS repository! 🚀
