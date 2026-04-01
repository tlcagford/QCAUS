# ── PRELOADED TEST FILES DATABASE WITH THUMBNAILS ─────────────────────────────────────────────
# Base URL for thumbnails (using NASA/ESA/STScI public imagery)
THUMBNAIL_BASE = "https://science.nasa.gov/wp-content/uploads/2023/09"

PRELOADED_FILES = {
    # ==================== REAL ASTRONOMICAL DATA ====================
    "🌌 Abell 1689 (HST ACS F814W)": {
        "type": "real",
        "instrument": "HST ACS",
        "filter": "F814W",
        "target": "Abell 1689",
        "description": "Galaxy cluster at z=0.183, used for FDM soliton validation",
        "path": "data/abell1689_hst_f814w.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/abell1689-hst-768x692.jpg",
        "thumbnail_alt": "Abell 1689 Hubble ACS",
        "tags": ["galaxy_cluster", "lensing", "validation"],
        "redshift": 0.183,
        "ra": "13h11m29.5s",
        "dec": "-01°20′17″"
    },
    "🌌 Abell 1689 (JWST NIRCam F200W)": {
        "type": "real",
        "instrument": "JWST NIRCam",
        "filter": "F200W",
        "target": "Abell 1689",
        "description": "Same cluster, higher resolution for fringe detection",
        "path": "data/abell1689_jwst_f200w.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/abell1689-jwst-768x768.jpg",
        "thumbnail_alt": "Abell 1689 JWST NIRCam",
        "tags": ["galaxy_cluster", "lensing", "validation"],
        "redshift": 0.183,
        "ra": "13h11m29.5s",
        "dec": "-01°20′17″"
    },
    "🦀 Crab Nebula (HST ACS F606W)": {
        "type": "real",
        "instrument": "HST ACS",
        "filter": "F606W",
        "target": "Crab Nebula",
        "description": "Supernova remnant with central pulsar, magnetar analog",
        "path": "data/crab_hst_f606w.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/crab-nebula-hst-768x768.jpg",
        "thumbnail_alt": "Crab Nebula Hubble",
        "tags": ["supernova_remnant", "pulsar", "magnetar_analog"],
        "distance_kpc": 2.0,
        "pulsar_period_ms": 33
    },
    "🦀 Crab Nebula (JWST NIRCam F200W)": {
        "type": "real",
        "instrument": "JWST NIRCam",
        "filter": "F200W",
        "target": "Crab Nebula",
        "description": "Infrared view revealing pulsar wind nebula structure",
        "path": "data/crab_jwst_f200w.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/crab-jwst-768x768.jpg",
        "thumbnail_alt": "Crab Nebula JWST",
        "tags": ["supernova_remnant", "pulsar_wind"],
        "distance_kpc": 2.0
    },
    "⭐ Swift J1818.0-1607 (Magnetar)": {
        "type": "real",
        "instrument": "Swift/XRT",
        "filter": "X-ray (0.3-10 keV)",
        "target": "Swift J1818.0-1607",
        "description": "Young magnetar discovered 2020, B ~ 2.5×10¹⁴ G",
        "path": "data/swift_j1818_xrt.fits",
        "thumbnail": "https://swift.gsfc.nasa.gov/results/2020/200312_J1818/j1818_xrt_thumb.jpg",
        "thumbnail_alt": "Swift J1818.0-1607 XRT",
        "tags": ["magnetar", "xray", "high_field"],
        "b_field_g": 2.5e14,
        "period_s": 1.36,
        "discovery_year": 2020
    },
    "🌠 M87 (HST ACS F814W)": {
        "type": "real",
        "instrument": "HST ACS",
        "filter": "F814W",
        "target": "M87",
        "description": "Giant elliptical galaxy with central black hole",
        "path": "data/m87_hst_f814w.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/m87-hst-768x768.jpg",
        "thumbnail_alt": "M87 Hubble",
        "tags": ["galaxy", "elliptical", "black_hole"],
        "distance_mpc": 16.4,
        "bh_mass_sun": 6.5e9
    },
    "🌀 Whirlpool Galaxy (M51 HST)": {
        "type": "real",
        "instrument": "HST ACS",
        "filter": "F606W",
        "target": "M51",
        "description": "Classic spiral galaxy with companion",
        "path": "data/m51_hst_f606w.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/m51-hst-768x768.jpg",
        "thumbnail_alt": "Whirlpool Galaxy",
        "tags": ["galaxy", "spiral", "interacting"],
        "distance_mpc": 7.6
    },
    "✨ Carina Nebula (JWST NIRCam)": {
        "type": "real",
        "instrument": "JWST NIRCam",
        "filter": "F200W",
        "target": "Carina Nebula",
        "description": "Massive star-forming region, cosmic cliffs",
        "path": "data/carina_jwst_f200w.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/carina-jwst-768x768.jpg",
        "thumbnail_alt": "Carina Nebula JWST",
        "tags": ["nebula", "star_formation", "jwst"],
        "distance_kpc": 7.6
    },
    "🌟 Pillars of Creation (JWST)": {
        "type": "real",
        "instrument": "JWST NIRCam",
        "filter": "F200W",
        "target": "Eagle Nebula",
        "description": "Iconic star-forming pillars",
        "path": "data/pillars_jwst_f200w.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/pillars-jwst-768x768.jpg",
        "thumbnail_alt": "Pillars of Creation JWST",
        "tags": ["nebula", "star_formation", "iconic"],
        "distance_kpc": 7.0
    },
    "🌌 Sombrero Galaxy (M104 HST)": {
        "type": "real",
        "instrument": "HST ACS",
        "filter": "F814W",
        "target": "M104",
        "description": "Edge-on spiral with prominent dust lane",
        "path": "data/m104_hst_f814w.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/sombrero-hst-768x768.jpg",
        "thumbnail_alt": "Sombrero Galaxy",
        "tags": ["galaxy", "edge_on", "dust_lane"],
        "distance_mpc": 9.5
    },
    "✨ Orion Nebula (HST)": {
        "type": "real",
        "instrument": "HST ACS",
        "filter": "F658N",
        "target": "Orion Nebula",
        "description": "Nearest massive star-forming region",
        "path": "data/orion_hst_f658n.fits",
        "thumbnail": "https://science.nasa.gov/wp-content/uploads/2023/09/orion-hst-768x768.jpg",
        "thumbnail_alt": "Orion Nebula",
        "tags": ["nebula", "star_formation", "hst"],
        "distance_kpc": 0.41
    },
    
    # ==================== SYNTHETIC TEST PATTERNS ====================
    "🎯 Point Source (PSF Test)": {
        "type": "synthetic",
        "instrument": "Simulated",
        "filter": "Generic",
        "target": "PSF Test",
        "description": "Single point source for PSF characterization",
        "path": "synthetic",
        "generator": "point_source",
        "thumbnail": None,  # Will be generated dynamically
        "thumbnail_alt": "Point Source",
        "tags": ["psf", "calibration", "test"]
    },
    "🔵 Gaussian Blob (Smooth Profile)": {
        "type": "synthetic",
        "instrument": "Simulated",
        "filter": "Generic",
        "target": "Gaussian Test",
        "description": "2D Gaussian for testing soliton overlay",
        "path": "synthetic",
        "generator": "gaussian",
        "thumbnail": None,
        "thumbnail_alt": "Gaussian Blob",
        "tags": ["smooth", "test"]
    },
    "🌀 Spiral Galaxy (Sersic Profile)": {
        "type": "synthetic",
        "instrument": "Simulated",
        "filter": "Generic",
        "target": "Spiral Test",
        "description": "Sersic profile galaxy for realistic morphology tests",
        "path": "synthetic",
        "generator": "sersic",
        "thumbnail": None,
        "thumbnail_alt": "Synthetic Spiral",
        "tags": ["galaxy", "sersic", "realistic"]
    },
    "🎭 Interference Fringe Pattern": {
        "type": "synthetic",
        "instrument": "Simulated",
        "filter": "Generic",
        "target": "Fringe Test",
        "description": "Concentric rings for testing PDP fringe overlay",
        "path": "synthetic",
        "generator": "fringe",
        "thumbnail": None,
        "thumbnail_alt": "Fringe Pattern",
        "tags": ["fringe", "interference", "pdp"]
    },
    "📊 Noise Test (Gaussian)": {
        "type": "synthetic",
        "instrument": "Simulated",
        "filter": "Generic",
        "target": "Noise Test",
        "description": "Gaussian noise field for SNR testing",
        "path": "synthetic",
        "generator": "noise",
        "thumbnail": None,
        "thumbnail_alt": "Noise Field",
        "tags": ["noise", "snr", "test"]
    },
    "🎨 Color Composite (RGB)": {
        "type": "synthetic",
        "instrument": "Simulated",
        "filter": "RGB",
        "target": "Color Test",
        "description": "RGB composite for testing color overlays",
        "path": "synthetic",
        "generator": "rgb_composite",
        "thumbnail": None,
        "thumbnail_alt": "RGB Composite",
        "tags": ["color", "rgb", "test"]
    },
    "🌌 Simulated FDM Soliton Core": {
        "type": "synthetic",
        "instrument": "Simulated",
        "filter": "Generic",
        "target": "FDM Test",
        "description": "Pure FDM soliton profile for overlay testing",
        "path": "synthetic",
        "generator": "fdm_soliton",
        "thumbnail": None,
        "thumbnail_alt": "FDM Soliton",
        "tags": ["fdm", "soliton", "theory"]
    },
    "🔮 Simulated Dark Photon Fringe": {
        "type": "synthetic",
        "instrument": "Simulated",
        "filter": "Generic",
        "target": "Dark Photon Test",
        "description": "Pure PDP fringe field for overlay testing",
        "path": "synthetic",
        "generator": "pdp_fringe",
        "thumbnail": None,
        "thumbnail_alt": "Dark Photon Fringe",
        "tags": ["pdp", "fringe", "theory"]
    },
}


# ── GENERATE THUMBNAIL FOR SYNTHETIC PATTERNS ─────────────────────────────────────────────
def generate_synthetic_thumbnail(generator, size=100):
    """Generate a small thumbnail for synthetic patterns."""
    if generator == "point_source":
        img = generate_point_source(size=size, fwhm=size//10)
    elif generator == "gaussian":
        img = generate_gaussian(size=size, sigma=size//8)
    elif generator == "sersic":
        img = generate_sersic(size=size, re=size//4)
    elif generator == "fringe":
        img = generate_fringe(size=size, wavelength=size//5)
    elif generator == "noise":
        img = generate_noise(size=size)
    elif generator == "rgb_composite":
        img = generate_rgb_composite(size=size)
    elif generator == "fdm_soliton":
        img = generate_fdm_soliton(size=size, r_c=size//4)
    elif generator == "pdp_fringe":
        img = generate_pdp_fringe(size=size, wavelength=size//5)
    else:
        img = generate_point_source(size=size)
    
    # Ensure 2D for display
    if img.ndim == 3:
        img = img.mean(axis=2)
    
    return img


# ── DISPLAY FILE CARD WITH THUMBNAIL ─────────────────────────────────────────────
def display_file_card(name, info):
    """Display a file card with thumbnail and metadata."""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if info.get("thumbnail"):
            # Real astronomical thumbnail from NASA/ESA
            st.image(
                info["thumbnail"],
                width=80,
                caption=None,
                use_container_width=False
            )
        else:
            # Generate synthetic thumbnail
            generator = info.get("generator")
            if generator:
                thumb = generate_synthetic_thumbnail(generator, size=80)
                fig, ax = plt.subplots(figsize=(1, 1))
                ax.imshow(thumb, cmap='viridis', origin='lower')
                ax.axis('off')
                st.pyplot(fig, clear_figure=True)
                plt.close(fig)
            else:
                st.markdown("🖼️")
    
    with col2:
        st.markdown(f"**{name}**")
        st.caption(f"{info['instrument']} | {info['filter']} | {info['target']}")
        st.caption(info['description'])
        
        # Show tags as badges
        tags = info.get("tags", [])
        tag_html = " ".join([f'<span style="background:#335588; padding:2px 6px; border-radius:12px; font-size:10px; margin-right:4px;">{tag}</span>' for tag in tags[:3]])
        if tag_html:
            st.markdown(f"<div style='margin-top: 4px;'>{tag_html}</div>", unsafe_allow_html=True)
        
        # Add metadata for real files
        if info["type"] == "real":
            metadata = []
            if "redshift" in info:
                metadata.append(f"z = {info['redshift']}")
            if "distance_kpc" in info:
                metadata.append(f"d = {info['distance_kpc']} kpc")
            if "distance_mpc" in info:
                metadata.append(f"d = {info['distance_mpc']} Mpc")
            if "b_field_g" in info:
                metadata.append(f"B = {info['b_field_g']:.1e} G")
            if metadata:
                st.caption(" | ".join(metadata))
        
        # Load button
        if st.button("📂 Load", key=f"load_{name}"):
            return True, info
    
    return False, None
