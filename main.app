# ─────────────────────────────────────────────────────────────────────────────
#  FULL DROP-IN REPLACEMENT: Paste these TWO functions into app.py
#  Recommended location: right after the imports and before the first physics
#  function (fdm_soliton_2d). They require NO extra dependencies (Pillow is
#  already in requirements.txt).
# ─────────────────────────────────────────────────────────────────────────────

from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
from datetime import datetime

def add_infographics(
    img_input: Image.Image | np.ndarray,
    title: str,
    metrics: dict[str, str],
    scale_kpc_per_pixel: float | None = None,
    legend_items: list[tuple[tuple[int, int, int], str]] | None = None,
    width: int = 800
) -> Image.Image:
    """
    FULLY ANNOTATED INFOGRAPHIC FOR ANY IMAGE (Before, After, soliton, PDP, radar, etc.)
    Drop-in ready — works with both PIL Image and numpy arrays (grayscale or RGB).
    """
    # Convert input to PIL RGB
    if isinstance(img_input, np.ndarray):
        if img_input.ndim == 2:  # grayscale
            img_input = np.stack([img_input] * 3, axis=-1)
        img = Image.fromarray((img_input * 255).clip(0, 255).astype(np.uint8))
    else:
        img = img_input.convert("RGB").copy()

    # Resize to consistent width if needed (keeps aspect ratio)
    if img.width != width:
        ratio = width / img.width
        new_h = int(img.height * ratio)
        img = img.resize((width, new_h), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(img)
    w, h = img.size

    # Try system fonts first, then fallback
    try:
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_med   = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_large = ImageFont.load_default(size=32)
        font_med   = ImageFont.load_default(size=24)
        font_small = ImageFont.load_default(size=18)

    # Top banner (semi-transparent dark)
    banner_h = 90
    banner = Image.new("RGBA", (w, banner_h), (0, 0, 0, 0))
    banner_draw = ImageDraw.Draw(banner)
    banner_draw.rectangle([(0, 0), (w, banner_h)], fill=(0, 0, 0, 200))
    img.paste(banner, (0, 0), banner)

    # Main title
    draw.text((30, 18), title, fill=(255, 255, 255), font=font_large)

    # Metrics panel (right side)
    metrics_str = "\n".join(f"{k}: {v}" for k, v in metrics.items())
    panel_w = 380
    panel_x = w - panel_w - 20
    draw.rectangle([(panel_x, 15), (w - 20, 80)], fill=(0, 0, 0, 220), outline=(0, 255, 120), width=4)
    draw.text((panel_x + 20, 22), metrics_str, fill=(0, 255, 120), font=font_med)

    # Scale bar (bottom-left)
    if scale_kpc_per_pixel is not None:
        bar_px = 220
        bar_kpc = bar_px * scale_kpc_per_pixel
        y = h - 70
        draw.line([(40, y), (40 + bar_px, y)], fill=(255, 255, 255), width=10)
        draw.text((40, y + 15), f"{bar_kpc:.1f} kpc", fill=(255, 255, 255), font=font_small)

    # Legend (bottom-right, if provided)
    if legend_items:
        y_start = h - 110
        for i, (color, label) in enumerate(legend_items):
            draw.rectangle([(w - 260, y_start + i * 32), (w - 230, y_start + i * 32 + 24)], fill=color)
            draw.text((w - 220, y_start + i * 32 + 2), label, fill=(255, 255, 255), font=font_small)

    # Timestamp + QCAUS branding
    draw.text((w - 380, h - 32), f"QCAUS v20.0 • {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
              fill=(180, 180, 180), font=font_small)

    return img


def create_before_after_composite(
    before_annotated: Image.Image,
    after_annotated: Image.Image,
    metrics: dict[str, str]
) -> Image.Image:
    """
    CLEAN SIDE-BY-SIDE BEFORE/AFTER WITH FULL DATA PANEL BELOW.
    Drop-in replacement for the current SECTION 2 matplotlib pair.
    """
    w, h = before_annotated.size
    composite = Image.new("RGB", (w * 2 + 40, h + 180), (15, 15, 30))  # extra height for data panel

    # Paste images
    composite.paste(before_annotated, (0, 0))
    composite.paste(after_annotated, (w + 40, 0))

    draw = ImageDraw.Draw(composite)

    # Labels
    try:
        font_lbl = ImageFont.truetype("arial.ttf", 36)
    except:
        font_lbl = ImageFont.load_default(size=36)
    draw.text((40, 20), "BEFORE — Raw HST/JWST", fill=(255, 255, 255), font=font_lbl)
    draw.text((w + 80, 20), "AFTER — QCAUS PDP + FDM Enhanced", fill=(0, 255, 120), font=font_lbl)

    # Full metrics panel at bottom
    metrics_str = "\n".join(f"• {k}: {v}" for k, v in metrics.items())
    try:
        font_metrics = ImageFont.truetype("arial.ttf", 22)
    except:
        font_metrics = ImageFont.load_default(size=22)
    draw.text((40, h + 30), metrics_str, fill=(200, 255, 200), font=font_metrics)

    return composite
