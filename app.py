    # ── MAGNETAR QED PLOTS (ADD THIS SECTION) ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### ⚡ Magnetar QED — Dipole Field, QED Polarization, Dark Photon Conversion")
    
    # Create 3 magnetar plots
    fig_mag, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot 1: Dipole B-field
    im1 = axes[0].imshow(B_n, cmap='plasma', vmin=0, vmax=1)
    axes[0].set_title(f"Magnetar Dipole B-Field\nB0 = 10^{B0_exp:.1f} G", fontsize=12)
    axes[0].axis('off')
    plt.colorbar(im1, ax=axes[0], fraction=0.046, label="|B| / B_max")
    
    # Plot 2: QED Vacuum Polarization
    im2 = axes[1].imshow(qed_n, cmap='inferno', vmin=0, vmax=1)
    axes[1].set_title(f"QED Vacuum Polarization\nΔL ∝ (B/B_crit)²", fontsize=12)
    axes[1].axis('off')
    plt.colorbar(im2, ax=axes[1], fraction=0.046, label="ΔL / ΔL_max")
    
    # Plot 3: Dark Photon Conversion
    im3 = axes[2].imshow(conv_n, cmap='hot', vmin=0, vmax=1)
    axes[2].set_title(f"Dark Photon Conversion\nP = ε²(1 - e^{-B²/m²})", fontsize=12)
    axes[2].axis('off')
    plt.colorbar(im3, ax=axes[2], fraction=0.046, label="P_conv / P_max")
    
    fig_mag.tight_layout()
    st.pyplot(fig_mag)
    plt.close(fig_mag)
    
    # Add magnetar parameter summary
    st.caption(f"""
    **Magnetar Parameters**  
    • Surface B-field: 10^{B0_exp:.1f} G ({10**B0_exp:.1e} G)  
    • Critical field: 4.414×10¹³ G  
    • B/B_crit = {10**B0_exp / 4.414e13:.2e}  
    • Kinetic mixing ε = {mix_mag:.3f}  
    • Dark photon mass m' = 1.0×10⁻⁹ eV (default)
    """)
