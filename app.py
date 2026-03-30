import numpy as np
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

def ensure_square(img: np.ndarray) -> np.ndarray:
    """
    Ensure image is square by cropping center.
    Handles both grayscale and RGB/RGBA arrays.
    """
    if len(img.shape) == 2:
        # Grayscale image
        h, w = img.shape
        if h == w:
            return img
        min_dim = min(h, w)
        top = (h - min_dim) // 2
        left = (w - min_dim) // 2
        return img[top:top+min_dim, left:left+min_dim]
    else:
        # Color image (RGB or RGBA)
        h, w, c = img.shape
        if h == w:
            return img
        min_dim = min(h, w)
        top = (h - min_dim) // 2
        left = (w - min_dim) // 2
        return img[top:top+min_dim, left:left+min_dim, :]

def pdp_entanglement_overlay(image: np.ndarray, interference: np.ndarray,
                              soliton: np.ndarray, omega: float,
                              fdm_mass: float = 1e-22, 
                              kinetic_mixing: float = 1e-12) -> np.ndarray:
    """
    Create entanglement overlay with FDM mass and kinetic mixing effects.
    Automatically ensures all inputs are square.
    """
    # Ensure all inputs are square
    image = ensure_square(image)
    interference = ensure_square(interference)
    soliton = ensure_square(soliton)
    
    # Handle grayscale vs color
    if len(image.shape) == 2:
        # Convert grayscale to 3-channel for consistent processing
        image = np.stack([image] * 3, axis=-1)
    
    # Ensure interference and soliton are 3-channel if needed
    if len(interference.shape) == 2:
        interference = np.stack([interference] * 3, axis=-1)
    if len(soliton.shape) == 2:
        soliton = np.stack([soliton] * 3, axis=-1)
    
    # Shape validation
    assert image.shape == interference.shape == soliton.shape, \
        f"shape mismatch after squaring: {image.shape}, {interference.shape}, {soliton.shape}"
    
    # Apply FDM mass and kinetic mixing scaling
    # FDM mass affects fringe spacing and visibility (typical scale ~ 1e-22 eV)
    mass_scale = 1.0 / (1.0 + fdm_mass / 1e-22)
    interference = interference * mass_scale
    
    # Kinetic mixing affects coupling strength (typical scale ~ 1e-12)
    mix_scale = 1.0 + kinetic_mixing / 1e-12
    interference = interference * mix_scale
    
    # Mixing strength parameter based on omega (magnetar B-field)
    m = omega * 0.6
    
    # Blend the components
    result = np.clip(image * (1 - m * 0.4) + 
                     interference * m * 0.5 +
                     soliton * m * 0.4, 0, 1)
    
    return result

# In your main app code where you call the function, ensure you're passing square arrays:
def prepare_data_for_overlay(img_gray, ord_mode, dark_mode, omega_val, kin_mix_val):
    """
    Prepare and validate data for entanglement overlay
    """
    # Generate interference pattern (ensure square)
    h, w = img_gray.shape
    min_dim = min(h, w)
    
    # Create interference pattern with matching square dimensions
    x = np.linspace(-np.pi, np.pi, min_dim)
    y = np.linspace(-np.pi, np.pi, min_dim)
    X, Y = np.meshgrid(x, y)
    
    # Interference fringes (affected by kinetic mixing)
    interference = 0.5 * (1 + np.cos(omega_val * 20 * X * (1 + kin_mix_val)))
    
    # Soliton field (localized perturbation)
    soliton = np.exp(-((X-0.5)**2 + (Y-0.5)**2) / 0.2) * omega_val
    
    # Crop img_gray to square before passing
    img_gray_square = ensure_square(img_gray)
    
    return img_gray_square, interference, soliton

# In your Streamlit app, when calling pdp_entanglement_overlay:
try:
    # Prepare data with proper dimensions
    img_square, interference, soliton = prepare_data_for_overlay(
        img_gray, ord_mode, dark_mode, omega_pd * 0.3, kin_mix * 1e9
    )
    
    # Create overlay with FDM parameters
    pdp_out = pdp_entanglement_overlay(
        img_square, 
        interference, 
        soliton, 
        omega_pd * 0.3,
        fdm_mass=1e-22,  # Adjust based on your physics model
        kinetic_mixing=kin_mix * 1e9
    )
    
except AssertionError as e:
    st.error(f"Shape mismatch error: {e}")
    st.info("Make sure all inputs have the same dimensions. The system will try to auto-crop to square.")
    # Fallback: use the square version only
    img_square = ensure_square(img_gray)
    min_dim = img_square.shape[0]
    x = np.linspace(-np.pi, np.pi, min_dim)
    X, Y = np.meshgrid(x, x)
    interference = 0.5 * (1 + np.cos(omega_pd * 0.3 * 20 * X))
    soliton = np.exp(-((X-0.5)**2 + (Y-0.5)**2) / 0.2) * (omega_pd * 0.3)
    pdp_out = pdp_entanglement_overlay(
        img_square, interference, soliton, omega_pd * 0.3,
        fdm_mass=1e-22, kinetic_mixing=kin_mix * 1e9
    )
