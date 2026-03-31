# =============================================================================
#  PROCESSING + DISPLAY
# =============================================================================
if img_data is not None:

    B0     = 10**b0_log10
    B_CRIT = 4.414e13

    # ── FORCE SQUARE IMAGE (prevents shape crashes) ──────────────────────
    if img_data.ndim == 3:
        img_gray = np.mean(img_data, axis=-1)
    else:
        img_gray = img_data.copy().astype(np.float32)

    h, w = img_gray.shape
    SIZE = min(h, w)

    if h != w or img_gray.shape != (SIZE, SIZE):
        img_pil = Image.fromarray((img_gray * 255).astype(np.uint8))
        img_pil = img_pil.resize((SIZE, SIZE), Image.LANCZOS)
        img_gray = np.array(img_pil, dtype=np.float32) / 255.0

    # ── SINGLE clean computation pass ───────────────────────────────
    soliton = fdm_soliton_2d(SIZE, fdm_mass)
    interf  = generate_interference_pattern(SIZE, fringe_scale, omega_pd)

    ord_mode, dark_mode = pdp_spectral_duality(
        img_gray, omega_pd, fringe_scale, kin_mix * 1e9, 1e-9)

    ent_res = entanglement_residuals(
        img_gray, ord_mode, dark_mode, omega_pd * 0.3, kin_mix * 1e9, fringe_scale)

    pdp_out = pdp_entanglement_overlay(img_gray, interf, soliton, omega_pd)

    fusion  = blue_halo_fusion(img_gray, dark_mode, ent_res)
    dp_prob = dark_photon_detection_prob(dark_mode, ent_res, omega_pd * 0.3)
    dp_peak = float(dp_prob.max() * 100)

    B_n, qed_n, conv_n = magnetar_physics(SIZE, B0, magnetar_eps)
    k_arr, P_lcdm, P_quantum = qcis_power_spectrum(f_nl, n_q)
    em_comp = em_spectrum_composite(img_gray, f_nl, n_q)
    r_arr, rho_arr = fdm_soliton_profile(fdm_mass)

    # ── Display starts here (everything below is your original code) ─────
    st.markdown("## Before vs After")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📷 Original Image")
        st.image(arr_to_pil(img_gray, cmap="gray"), use_container_width=True)
        st.markdown(get_download_link(img_gray, "original.png", "📥 Download", "gray"),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(f"### 🔮 PDP Entangled  Ω={omega_pd:.2f}")
        st.markdown("*image·(1−m·0.4) + interference·m·0.5 + soliton·m·0.4   m=Ω·0.6*")
        st.image(arr_to_pil(pdp_out, cmap="inferno"), use_container_width=True)
        st.markdown(get_download_link(pdp_out, "pdp_entangled.png", "📥 Download", "inferno"),
                    unsafe_allow_html=True)

    # (Paste the rest of your display code exactly as it was — Annotated Maps, Dark Photon section, Magnetar QED, FDM profile, QCIS spectrum, EM mapping, Detection Metrics, Verified Formulas, etc.)
