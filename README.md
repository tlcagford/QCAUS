# 🌌 Quantum Cosmology & Astrophysics Unified Suite (QCAUS)

A unified computational framework integrating 8 interconnected open-source projects that explore the quantum nature of the universe – from dark matter solitons to quantum-corrected cosmology, magnetar QED, and stealthdarkleakage detection. 

**[Launch QCAUS App](https://qcaustfordmodel.streamlit.app/)**

**Real-time quantum cosmology & astrophysics visualization tool**

**Features**
- Annotated Before/After overlays with live data panels (Ω, Fringe, Mixing, Entropy, Ω_FDM)
- All 8 verified physics modules
- Individual download buttons under every image
- One-click ZIP of all results
- Preset data including historical airport radar

**Run**
```bash
streamlit run app.py
---
7. 
**Real-time quantum cosmology & astrophysics visualization tool**

**Features**

- Annotated Before/After overlays with live data panels (Ω, Fringe, Mixing, Entropy, Ω_FDM)
- All 8 verified physics modules
- Individual download buttons under every image
- One-click ZIP of all results
- Preset data including historical airport radar

**Run**

    streamlit run app.py

---

## 🔭 Projects Overview

### 1. QCI AstroEntangle Refiner
**FDM Soliton Physics + Photon-DarkPhoton Entanglement Overlay**

| Feature | Description |
|---------|-------------|
| **FDM Soliton** | Fuzzy Dark Matter soliton core: ρ(r) = ρ₀ [sin(kr)/(kr)]² |
| **PDP Entanglement** | Photon-DarkPhoton kinetic mixing: ℒ_mix = (ε/2) F_μν F'^μν |
| **Image Processing** | Upload FITS, JPEG, PNG images; apply quantum overlays |
| **Annotated Comparison** | Before/after views with scale bars and metrics |
| **Radar-Style Overlay** | Green speckles (FDM) + Blue halos (PDP) for stealth detection visualization |

### 2. Magnetar QED Explorer
**Strong-Field Quantum Electrodynamics in Magnetar Magnetospheres**

| Feature | Description |
|---------|-------------|
| **Dipole Field** | B = B₀ (R/r)³ (2 cosθ, sinθ) |
| **Vacuum Polarization** | Euler-Heisenberg effect: ΔL = (α/45π) (B/B_crit)² |
| **Dark Photon Conversion** | P_conversion = ε² (1 - e^{-B²/m²}) |
| **Interactive Visualization** | Real-time parameter adjustment for B-field, mixing angle |

### 3. Primordial Photon-DarkPhoton Entanglement
**Von Neumann Evolution in the Expanding Universe**

| Feature | Description |
|---------|-------------|
| **Von Neumann Equation** | i∂ρ/∂t = [H_eff, ρ] |
| **Entanglement Entropy** | S = -Tr(ρ log ρ) |
| **Mixing Probability** | \|⟨ψ_d\|ψ_γ⟩\|² |
| **Time Evolution** | Simulates photon-dark photon oscillation in early universe |

### 4. QCIS – Quantum Cosmology Integration Suite
**Quantum-Corrected Cosmological Perturbations**

| Feature | Description |
|---------|-------------|
| **Quantum-Corrected Power Spectrum** | P(k) = P_ΛCDM(k) × (1 + f_NL (k/k₀)^n_q) |
| **Non-Gaussianity** | f_NL parameter for primordial fluctuations |
| **Spectral Index** | n_q for quantum corrections |
| **ΛCDM Comparison** | Side-by-side comparison with standard cosmology |

---

## 📊 Key Metrics & Outputs

| Project | Key Outputs | Download Format |
|---------|-------------|-----------------|
| **QCI AstroEntangle** | Annotated comparison, radar-style overlay, FDM soliton map, PDP entanglement map | PNG, JSON |
| **Magnetar QED** | B-field map, QED polarization, dark photon conversion | PNG, NPZ |
| **Primordial Entanglement** | Entropy evolution, mixing probability time series | PNG, JSON, NPY |
| **QCIS** | Power spectra, quantum enhancement ratio | PNG, JSON, NPY |

---

## 🧪 Supported Image Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| **FITS** | .fits, .fit | Astronomical images (Hubble, JWST, Chandra) |
| **JPEG** | .jpg, .jpeg | Standard images |
| **PNG** | .png | Lossless images |
| **BMP** | .bmp | Bitmap images |

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
astropy>=5.3.0  # For FITS support
Pillow>=10.0.0  # For image processing
```

---

## 📖 Physics References

### FDM Soliton

The Fuzzy Dark Matter soliton is the ground state solution of the Schrödinger-Poisson equation for ultra-light bosons (axions, ~10⁻²² eV):

### Photon-DarkPhoton Kinetic Mixing

The interaction between photons and dark photons is described by:

where ε is the kinetic mixing angle.

### Von Neumann Evolution

The density matrix evolution for entangled systems:

### Quantum-Corrected Power Spectrum

The matter power spectrum with quantum corrections:

---

## 📝 Contributions & Original Work

This section clarifies which components of QCAUS are **standard implementations of established physics** and which represent **original contributions** by the author.

### Standard Implementations (Established Physics)

The following modules implement well-known equations from the published literature. Each is cited appropriately in the code and documentation.

| Module | Equation / Method | Source |
|--------|-------------------|--------|
| **FDM Soliton** | ρ(r) = ρ₀ [sin(kr)/(kr)]², k = π/r_s, r_s = 1/m | Standard Fuzzy Dark Matter soliton profile (Hui et al. 2017; Ruffini & Bonazzola 1969) |
| **Schrödinger-Poisson System** | i∂ₜψ = -∇²ψ/(2m) + Φψ, ∇²Φ = 4πG\|ψ\|² | Canonical SP system for bosonic dark matter |
| **Magnetar Dipole Field** | B = B₀ (R/r)³ √(3cos²θ + 1) | Standard rotating dipole field (Jackson, 1998) |
| **Euler-Heisenberg QED** | Δℒ = (α/45π) (B/B_crit)² | One-loop vacuum polarization (Heisenberg & Euler 1936) |
| **Von Neumann Entropy** | S = -Tr(ρ log ρ) | Standard quantum entropy |
| **Bayesian Detection** | P_post = (prior·L) / (prior·L + (1-prior)) | Standard Bayesian update |
| **de Broglie Wavelength** | λ = h/(mv) | Standard wave mechanics |

### Original Contributions (Author's Work)

The following represent **original extensions, syntheses, or novel formulations** developed specifically for QCAUS.

#### 1. Two-Field Coupled Schrödinger-Poisson System

An extension of the standard SP system to two interacting fields, modeling light-dark sector coupling:

```
i∂ₜψ_t = -∇²ψ_t/(2m_t) + (Φ_t + εΦ_a)ψ_t
i∂ₜψ_a = -∇²ψ_a/(2m_a) + (Φ_a + εΦ_t)ψ_a
∇²Φ_t = 4πG|ψ_t|²
∇²Φ_a = 4πG|ψ_a|²
```

The coupling term εΦ_a (and symmetric counterpart) provides a non-relativistic analog of kinetic mixing between photon and dark photon sectors. This formulation enables simulation of interference patterns and entanglement metrics in a common gravitational framework.

#### 2. Photon-Dark Photon Interference Density

A novel synthesis of two-field interference applied to light and dark sectors:

```
ρ = |ψ_t|² + |ψ_a|² + 2·Re(ψ_t* ψ_a e^{iΔφ})
```

The phase factor e^{iΔφ} represents relative phase evolution between sectors. This formulation produces observable fringe patterns with spacing λ = 2π/|Δk|, applicable to galactic dynamics and potentially laboratory-scale anomalies.

#### 3. PDP Spectral Duality Expression

An original Fourier-domain filter combining optical fringe analysis with dark photon field modeling:

```
dark_mask = e^{-j(ΩR²)} · |sin(2πRL/f)| · (1 - e^{-j(R²/f)})
```

This expression, implemented in `StealthPDPRadar/pdp_radar_core.py`, synthesizes Gaussian apodization, fringe periodicity, and phase accumulation into a single spectral mask for dark photon field visualization.

#### 4. Entanglement Residuals with Cross-Terms

An extended entropy formulation incorporating interference cross-terms:

```
S = -ρ log ρ + |ψ·ord + ψ·d·ark|² - ψ·ord² - ψ·d·ark²
```

The additional terms encode spatial structure information beyond the standard von Neumann entropy, providing a heuristic metric for entanglement complexity in image-space overlays.

#### 5. Quantum-Corrected Power Spectrum Parameterization

A phenomenological correction to the ΛCDM power spectrum:

```
P(k) = P_ΛCDM(k) × (1 + f_NL (k/k₀)^{n-q})
```

The parameters f_NL (non-Gaussianity amplitude), n (quantum correction index), and q (baseline index) allow flexible modeling of quantum gravitational effects on cosmological structure formation.

#### 6. Dark Photon Conversion Probability (Modified Form)

A simplified exponential model for dark photon production in strong magnetic fields:

```
P_conv = ε² (1 - e^{-(B²/m²)})
```

This form captures the suppression of conversion at low field strengths and saturation at high fields, providing a computationally efficient alternative to full quantum kinetic calculations.

#### 7. Ω_PD Entanglement Parameter

A scalar parameter introduced to quantify the degree of photon-dark photon entanglement in the two-field system:

```
Ω_PD = ⟨ψ_t | ψ_a⟩ / √(⟨ψ_t | ψ_t⟩ ⟨ψ_a | ψ_a⟩)
```

This metric, adjustable via the user interface, controls the mixing strength in interference visualizations.

#### 8. Unified Computational Framework

The primary original contribution is the **integration of all eight modules into a single interactive Streamlit application** with:
- Real-time parameter exploration
- Annotated before/after comparisons with scale bars
- One-click export of all results
- Support for FITS, JPEG, PNG, and BMP formats
- Preset data examples for rapid testing

This unification enables cross-disciplinary exploration of quantum astrophysics models that previously existed only in isolated repositories.

### Citation Recommendation

If you use QCAUS in your research, please cite the framework and note which components are standard vs. original as appropriate.

For standard physics components, cite the original literature (e.g., Hui et al. 2017 for FDM solitons). For original extensions, cite:

> Ford, T. E. (2026). *Quantum Cosmology & Astrophysics Unified Suite (QCAUS)*. GitHub. https://github.com/tlcagford/QCAUS

### Acknowledgments

Standard physics implementations were informed by the following key works:
- **FDM / Schrödinger-Poisson:** Hui et al. (2017), Marsh (2016), Ruffini & Bonazzola (1969)
- **Magnetar QED:** Heisenberg & Euler (1936), Schwinger (1951)
- **Dark Photon Kinetic Mixing:** Holdom (1986), Fabbrichesi et al. (2020)

---

## 🚀 Quick Start Examples

### QCI AstroEntangle Refiner

```python
# Load image and apply FDM + PDP overlays
from qci_astro import process_qci_astro
enhanced, soliton, pdp = process_qci_astro(image_data, omega=0.5, fringe=1.0, soliton_scale=1.0)
```

### Magnetar QED Explorer

```python
# Compute magnetar field and dark photon conversion
from magnetar_qed import process_magnetar
B_mag, qed, dark_photons = process_magnetar(r_grid, theta_grid, B0=1e15, mixing=0.1)
```

### Primordial Entanglement

```python
# Simulate photon-dark photon entanglement evolution
from primordial_entanglement import process_primordial_entanglement
entropy, mixing = process_primordial_entanglement(omega=0.7, dark_mass=1e-9, mixing=0.1)
```

### QCIS Power Spectra

```python
# Compute quantum-corrected power spectrum
from qcis import process_qcis
P_quantum = process_qcis(k_vals, f_nl=1.0, n_q=0.5)
```

---

## 📊 Example Outputs

### Annotated Comparison (Abell-1689)
- **Before**: Standard HST/JWST data with scale bar (100 kpc)
- **After**: FDM Soliton + PDP Entanglement overlays
- **Metrics**: Maximum Mixing Ratio, Minimum Entropy, FDM Value (kpc)

### Radar-Style Overlay
- **Green**: FDM Soliton (dark matter density)
- **Blue**: PDP Entanglement (dark photon field)
- **Red**: Original astrophysical signal

### Magnetar Field Maps
- **B-Field**: Dipole field structure (B ∝ r⁻³)
- **QED Polarization**: Euler-Heisenberg vacuum effects
- **Dark Photons**: Conversion probability maps

### Power Spectra
- **ΛCDM**: Standard cosmology baseline
- **Quantum**: Corrected spectrum with f_NL and n_q parameters

---

## 📄 Citation

If you use QCAUS in your research, please cite:

```bibtex
@software{Ford2026QCAUS,
  author = {Ford, Tony E.},
  title = {Quantum Cosmology \& Astrophysics Unified Suite (QCAUS)},
  year = {2026},
  url = {https://github.com/tlcagford/QCAUS},
  doi = {10.5281/zenodo.xxxxxxx}
}
```

---

## 📜 License

This project is released under a **Dual License**:

- **Academic / Non-Commercial Use**: Free for research, education, and personal projects
- **Commercial Use**: Requires a separate license. Please contact the author for details.

See the `LICENSE` file for full terms.

---

## 📧 Contact

**Tony E. Ford**  
Independent Researcher / Astrophysics & Quantum Systems  
GitHub: @tlcagford  
Email: tlcagford@gmail.com

---

## 🙏 Acknowledgments

- **NASA/ESA Hubble Space Telescope & JWST** for public FITS data
- **OpenSky Network** for radar data integration
- **FDM, QED, and cosmology communities** for foundational research
- **Streamlit, NumPy, SciPy, Matplotlib, Astropy** for open-source tools

---

## 🔗 Related Projects

| Project | Repository |
|---------|------------|
| **StealthPDPRadar** | StealthPDPRadar |
| **Magnetar QED Explorer** | Magnetar-Quantum-Vacuum-Engineering |
| **Primordial Entanglement** | Primordial-Photon-DarkPhoton-Entanglement |
| **QCIS** | Quantum-Cosmology-Integration-Suite |

---

_"Exploring the quantum nature of the universe – from dark matter solitons to quantum-corrected cosmology."_

---

## 📸 Screenshots

### QCI AstroEntangle Refiner
*Annotated before/after comparison of Abell-1689 with FDM Soliton and PDP Entanglement overlays*

### Magnetar QED Explorer
*Magnetar dipole field with quantum vacuum polarization and dark photon conversion*

### Primordial Entanglement
*Von Neumann entropy evolution and photon-dark photon mixing probability*

### QCIS Power Spectra
*Quantum-corrected matter power spectrum vs ΛCDM*

---
