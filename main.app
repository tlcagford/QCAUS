# =============================================================================
#  ONE FULL DROP-IN REPLACEMENT BLOCK
#  Paste this ENTIRE block over your current "SECTION 2 — Before vs After" 
#  (and any following matplotlib st.pyplot blocks for soliton/PDP/radar).
#  It includes BOTH functions + the complete Streamlit display logic.
#  Zero extra dependencies. Works with your existing variables.
# =============================================================================

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import numpy as np

# ── INFRASTRUCTURE: Single unified infographic engine ────────────────────────
def qcaus_full_infographic(
    img_input: np.ndarray | Image.Image,
    title: str,
    metrics: dict[str, str],
    scale_kpc_per_pixel: float | None = None,
    legend_items: list[tuple[tuple[int,int,int], str]] | None = None
) -> Image.Image:
    """ONE function that annotates ANY image (Before, After, soliton, PDP, radar, etc.)"""
    # Convert numpy → PIL
    if isinstance(img_input, np.ndarray):
        if img_input.ndim == 2:
            img_input = np.stack([img_input]*3, axis=-1)
        arr = (img_input.clip(0,1) * 255).astype(np.uint8)
        img = Image.fromarray(arr)
    else:
        img = img_input.convert("RGB").copy()

    # Standardize width
    w, h = img.size
    if w > 800:
        ratio = 800 / w
        img = img.resize((800, int(h*ratio)), Image.Resampling.LANCZOS)
        w, h = img.size

    draw = ImageDraw.Draw(img)

    # Fonts (graceful fallback)
    try:
        font_l = ImageFont.truetype("arial.ttf", 34)
        font_m = ImageFont.truetype("arial.ttf", 24)
        font_s = ImageFont.truetype("arial.ttf", 18)
    except:
        font_l = ImageFont.load_default(size=34)
        font_m = ImageFont.load_default(size=24)
        font_s = ImageFont.load_default(size=18)

    # Top banner
    banner = Image.new("RGBA", (w, 95), (0,0,0,0))
    bd = ImageDraw.Draw(banner)
    bd.rectangle([0,0,w,95], fill=(0,0,0,210))
    img.paste(banner, (0,0), banner)

    draw.text((30, 18), title, fill=(255,255,255), font=font_l)

    # Metrics panel
    metrics_txt = "\n".join(f"{k}: {v}" for k,v in metrics.items())
    panel_x = w - 400
    draw.rectangle([panel_x, 18, w-20, 88], fill=(0,0,0,230), outline=(0,255,140), width=4)
    draw.text((panel_x+20, 24), metrics_txt, fill=(0,255,140), font=font_m)

    # Scale bar
    if scale_kpc_per_pixel:
        bar_px = 220
        bar_kpc = bar_px * scale_kpc_per_pixel
        y = h - 72
        draw.line([(40, y), (40+bar_px, y)], fill=(255,255,255), width=10)
        draw.text((42, y+18), f"{bar_kpc:.1f} kpc", fill=(255,255,255), font=font_s)

    # Legend
    if legend_items:
        y = h - 130
        for i, (color, label) in enumerate(legend_items):
            draw.rectangle([(w-280, y+i*34), (w-250, y+i*34+26)], fill=color)
            draw.text((w-240, y+i*34+3), label, fill=(255,255,255), font=font_s)

    # Timestamp
    draw.text((w-410, h-34), f"QCAUS v20.0 • {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
              fill=(170,170,170), font=font_s)

    return img


def qcaus_before_after_composite(before_img: Image.Image, after_img: Image.Image, metrics: dict) -> Image.Image:
    """Side-by-side composite with full data panel (one single call)"""
    w, h = before_img.size
    comp = Image.new("RGB", (w*2 + 40, h + 200), (15,15,35))

    comp.paste(before_img, (0, 0))
    comp.paste(after_img, (w + 40, 0))

    draw = ImageDraw.Draw(comp)
    try:
        f_big = ImageFont.truetype("arial.ttf", 38)
        f_med = ImageFont.truetype("arial.ttf", 24)
    except:
        f_big = ImageFont.load_default(size=38)
        f_med = ImageFont.load_default(size=24)

    draw.text((40, 15), "BEFORE — Raw HST/JWST", fill=(255,255,255), font=f_big)
    draw.text((w+80, 15), "AFTER — QCAUS PDP+FDM Enhanced", fill=(0,255,140), font=f_big)

    metrics_txt = "\n".join(f"• {k}: {v}" for k,v in metrics.items())
    draw.text((40, h+35), metrics_txt, fill=(200,255,200), font=f_med)

    return comp


# =============================================================================
#  REPLACEMENT UI CODE — paste this where your old SECTION 2 was
# =============================================================================
st.markdown("### Before vs After — Full Infographic Composite")

# Build metrics once (reuse your existing variables)
metrics = {
    "FDM Max Density": f"{soliton.max():.3f}",
    "PDP Mixing Ratio": f"{omega:.3f}",
    "Min Entropy": f"{ent_res.min():.2f}",
    "Dark Photon Conf.": f"{dark_conf:.1f}%",
    "Scale": f"{scale_kpc_per_pixel:.2f} kpc/px" if 'scale_kpc_per_pixel' in locals() else "0.42 kpc/px"
}

legend = [
    ((0, 255, 0),   "FDM Soliton"),
    ((0, 100, 255), "PDP Entanglement"),
    ((255, 80, 80), "Original Signal")
]

# Create annotated versions of EVERY image
before_annotated = qcaus_full_infographic(img_data, "BEFORE — Raw Data", metrics, scale_kpc_per_pixel, legend)
after_annotated  = qcaus_full_infographic(rgb, "AFTER — QCAUS Enhanced", metrics, scale_kpc_per_pixel, legend)

# Side-by-side composite
composite = qcaus_before_after_composite(before_annotated, after_annotated, metrics)

# Display + auto-save
st.image(composite, use_container_width=True)
composite.save("output/composite_before_after_infographic.png")

st.success("✅ Full infographic composite saved → output/composite_before_after_infographic.png")

# Quick extra annotated maps (add these lines wherever you had soliton/PDP displays)
st.markdown("### Additional Annotated Maps")
soliton_ann = qcaus_full_infographic(soliton, "FDM SOLITON MAP", metrics, legend_items=[((0,255,0),"FDM Density")])
pdp_ann     = qcaus_full_infographic(ent_res, "PDP ENTANGLEMENT MAP", metrics, legend_items=[((0,100,255),"PDP Halo")])

col1, col2 = st.columns(2)
col1.image(soliton_ann, use_container_width=True)
col2.image(pdp_ann, use_container_width=True)

soliton_ann.save("output/fdm_soliton_infographic.png")
pdp_ann.save("output/pdp_entanglement_infographic.png")
