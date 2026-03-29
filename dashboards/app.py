import streamlit as st
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import io
import pandas as pd
from PIL import Image

# ====================== PATH FIX ======================
current_file = Path(__file__).resolve()
repo_root = current_file.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
# =====================================================

from core.theory import PDPTwoFieldTheory

# FITS + DICOM support
try:
    from astropy.io import fits
    from astropy.visualization import ImageNormalize, LogStretch, PercentileInterval
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False

try:
    import pydicom
    PYDICOM_AVAILABLE = True
except ImportError:
    PYDICOM_AVAILABLE = False

st.set_page_config(page_title="QCAUS", page_icon="🌌", layout="wide")

st.title("🌌 QCAUS — Quantum Cosmology & Astrophysics Unified Suite")
st.markdown("**Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework**")

st.sidebar.title("QCAUS v1.0")
st.sidebar.caption("Unified Framework by Tony E. Ford")
st.sidebar.markdown("Contact: tlcagford@gmail.com")
st.sidebar.success("✅ CSV • PNG • DICOM • FITS supported\nBio projects removed")

tab_home, tab_cosmo, tab_astro, tab_defense, tab_radar, tab_theory = st.tabs([
    "🏠 Home", 
    "🌌 Cosmology", 
    "⭐ Astrophysics", 
    "🛡️ Scalar Defense", 
    "📡 Stealth PDP Radar", 
    "📜 Unified Theory"
])

with tab_home:
    st.header("Welcome to QCAUS")
    st.markdown("Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework")
    st.• Multi-format file processing active (CSV, PNG, DICOM, FITS)")

with tab_cosmo:
    st.header("Cosmology Simulator")
    theory = PDPTwoFieldTheory()
    st.pyplot(theory.demo_plot_soliton())
    st.caption("Real FDM soliton core from consolidated theory")

with tab_astro:
    st.header("Astrophysics — Multi-Format Processing (CSV, PNG, DICOM, FITS)")
    
    theory = PDPTwoFieldTheory()
    
    st.subheader("📤 Drag & Drop Files for PDP Processing")
    uploaded_files = st.file_uploader(
        "Upload CSV, PNG, DICOM (.dcm), or FITS files",
        type=None,
        accept_multiple_files=True,
        help="All files processed with Photon-Dark-Photon FDM + QED effects"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        B = st.slider("B-field (×10¹⁴ G)", 0.1, 20.0, 5.0, 0.1)
    with col2:
        phase_shift = st.slider("Dark-Photon Phase Shift", 0.0, 4.0, 1.0, 0.1)
    with col3:
        energy_kev = st.slider("Photon Energy (keV)", 1.0, 500.0, 100.0, 1.0)
    
    if uploaded_files:
        st.success(f"✅ Indicom: {len(uploaded_files)} file(s) processed with PDP theory")
        
        for uploaded_file in uploaded_files:
            filename = uploaded_file.name.lower()
            st.subheader(f"Processing: {uploaded_file.name}")
            
            try:
                # PNG / Image
                if filename.endswith(('.png', '.jpg', '.jpeg')) or uploaded_file.type.startswith("image"):
                    img = Image.open(uploaded_file).convert("RGB")
                    img_array = np.array(img)
                    
                    h, w = img_array.shape[:2]
                    x = np.linspace(-5, 5, w)
                    y = np.linspace(-5, 5, h)
                    X, Y = np.meshgrid(x, y)
                    r = np.sqrt(X**2 + Y**2)
                    soliton = theory.fdm_soliton_profile(r, core_radius=4.0)
                    interference = theory.entanglement_interference(
                        np.sqrt(soliton), np.sqrt(soliton)*0.4, delta_phi=phase_shift
                    )
                    
                    overlay = (img_array.astype(float) * 0.7 + interference[..., np.newaxis] * 255 * 0.8).clip(0, 255).astype(np.uint8)
                    overlay_img = Image.fromarray(overlay)
                    
                    col_a, col_b = st.columns(2)
                    with col_a: st.image(img, caption="Original")
                    with col_b: st.image(overlay_img, caption="Processed: PDP Interference + QED")
                    
                    buf = io.BytesIO()
                    overlay_img.save(buf, format="PNG")
                    buf.seek(0)
                    st.download_button("⬇️ Download Processed PNG", buf, f"qcaus_pdp_{uploaded_file.name}", "image/png")
                
                # CSV
                elif filename.endswith('.csv') or uploaded_file.type == "text/csv":
                    df = pd.read_csv(uploaded_file)
                    st.dataframe(df.head())
                    
                    if not df.empty:
                        col_name = df.columns[0]
                        values = df[col_name].values.astype(float)
                        qed_factor = theory.magnetar_qed_correction(B * 1e14)
                        processed = values * qed_factor * (1 + 0.3 * np.sin(phase_shift + np.arange(len(values))))
                        
                        df_processed = df.copy()
                        df_processed[col_name + "_QED_PDP"] = processed
                        st.dataframe(df_processed)
                        
                        csv_buf = io.StringIO()
                        df_processed.to_csv(csv_buf, index=False)
                        st.download_button("⬇️ Download Processed CSV", csv_buf.getvalue(), f"qcaus_pdp_{uploaded_file.name}", "text/csv")
                
                # DICOM
                elif filename.endswith('.dcm') and PYDICOM_AVAILABLE:
                    ds = pydicom.dcmread(io.BytesIO(uploaded_file.read()))
                    pixel_array = ds.pixel_array.astype(float)
                    
                    st.write("**DICOM Info:**", getattr(ds, 'Modality', 'N/A'))
                    
                    qed_factor = theory.magnetar_qed_correction(B * 1e14)
                    h, w = pixel_array.shape
                    r = np.sqrt(np.meshgrid(np.linspace(-5,5,w), np.linspace(-5,5,h))[0]**2 + 
                               np.meshgrid(np.linspace(-5,5,w), np.linspace(-5,5,h))[1]**2)
                    soliton = theory.fdm_soliton_profile(r, core_radius=4.0)
                    interference = theory.entanglement_interference(np.sqrt(soliton), np.sqrt(soliton)*0.35, delta_phi=phase_shift)
                    
                    processed_array = pixel_array * qed_factor + interference * np.max(np.abs(pixel_array)) * 0.6
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        fig, ax = plt.subplots()
                        ax.imshow(pixel_array, cmap='gray')
                        ax.set_title("Original DICOM")
                        st.pyplot(fig)
                    with col_b:
                        fig, ax = plt.subplots()
                        ax.imshow(processed_array, cmap='plasma')
                        ax.set_title("Processed: PDP + QED")
                        st.pyplot(fig)
                    
                    png_buf = io.BytesIO()
                    plt.imsave(png_buf, processed_array, cmap='plasma', format='png')
                    png_buf.seek(0)
                    st.download_button("⬇️ Download Processed PNG", png_buf, f"qcaus_pdp_{uploaded_file.name}.png", "image/png")
                
                # FITS
                elif filename.endswith('.fits') and ASTROPY_AVAILABLE:
                    with fits.open(io.BytesIO(uploaded_file.read())) as hdul:
                        data = hdul[0].data
                    
                    norm = ImageNormalize(data, interval=PercentileInterval(99.5), stretch=LogStretch())
                    original_img = norm(data)
                    
                    h, w = data.shape
                    x = np.linspace(-5, 5, w)
                    y = np.linspace(-5, 5, h)
                    X, Y = np.meshgrid(x, y)
                    r = np.sqrt(X**2 + Y**2)
                    soliton = theory.fdm_soliton_profile(r, core_radius=4.0)
                    interference = theory.entanglement_interference(np.sqrt(soliton), np.sqrt(soliton)*0.4, delta_phi=phase_shift)
                    
                    qed_factor = theory.magnetar_qed_correction(B * 1e14)
                    processed_data = data * qed_factor + interference * np.max(np.abs(data)) * 0.6
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        fig, ax = plt.subplots()
                        ax.imshow(original_img, cmap='gray', origin='lower')
                        ax.set_title("Original FITS")
                        st.pyplot(fig)
                    with col_b:
                        fig, ax = plt.subplots()
                        ax.imshow(processed_data, cmap='plasma', origin='lower')
                        ax.set_title("Processed: PDP + QED")
                        st.pyplot(fig)
                    
                    # Download processed FITS
                    hdu = fits.PrimaryHDU(processed_data)
                    buf = io.BytesIO()
                    hdu.writeto(buf, overwrite=True)
                    buf.seek(0)
                    st.download_button("⬇️ Download Processed FITS", buf, f"qcaus_pdp_{uploaded_file.name}", "application/fits")
                
                else:
                    st.info(f"File {uploaded_file.name} uploaded — basic support active.")
                    
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
    
    else:
        st.info("Drag & drop CSV, PNG, DICOM (.dcm), or FITS files here to process with your Photon-Dark-Photon theory.")

with tab_defense:
    st.header("Scalar Defense Simulator")
    theory = PDPTwoFieldTheory()
    phi = st.slider("Gravitational potential engineering", 0.0, 5.0, 1.5)
    r = np.linspace(0, 15, 400)
    psi1 = np.exp(-r**2)
    psi2 = np.exp(-(r - 3)**2)
    rho_total = theory.entanglement_interference(psi1, psi2, delta_phi=phi)
    st.line_chart(rho_total, use_container_width=True)
    st.caption("Coupled Schrödinger-Poisson interference")

with tab_radar:
    st.header("Stealth PDP Radar — Live Leakage Detection")
    theory = PDPTwoFieldTheory()
    if st.button("Run Radar Scan"):
        signal = np.random.randn(200) * 0.5 + np.sin(np.linspace(0, 10, 200))
        detected = theory.radar_leakage_detector(signal)
        if detected:
            st.error("🚨 DARK-PHOTON LEAKAGE DETECTED!")
        else:
            st.success("✅ No detectable leakage — target is stealth")
        st.line_chart(signal)

with tab_theory:
    st.header("Unified Theory — Single Source of Truth")
    st.markdown("All processing uses the consolidated Photon-Dark-Photon Two-Field FDM core.")
    st.caption("von Neumann • Schrödinger-Poisson • FDM solitons • Entanglement interference • Magnetar QED")

st.markdown("---")
st.caption("QCAUS • Photon-Dark-Photon Two-Field Fuzzy Dark Matter Framework • tlcagford@gmail.com")
