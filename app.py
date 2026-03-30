import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button
from typing import Tuple, Optional

def ensure_square(img: np.ndarray) -> np.ndarray:
    """Ensure image is square by cropping center or padding"""
    h, w = img.shape[:2]
    if h == w:
        return img
    
    # Crop to square (center)
    min_dim = min(h, w)
    top = (h - min_dim) // 2
    left = (w - min_dim) // 2
    return img[top:top+min_dim, left:left+min_dim]

def pdp_entanglement_overlay(image: np.ndarray, interference: np.ndarray,
                              soliton: np.ndarray, omega: float,
                              fdm_mass: Optional[float] = None,
                              kinetic_mixing: Optional[float] = None) -> np.ndarray:
    """
    Create entanglement overlay with FDM mass and kinetic mixing effects.
    
    Parameters:
    -----------
    image : np.ndarray
        Base image (grayscale or RGB)
    interference : np.ndarray
        Interference pattern array (must match image shape)
    soliton : np.ndarray
        Soliton field array (must match image shape)
    omega : float
        Angular frequency parameter (related to magnetar B-field)
    fdm_mass : float, optional
        Fuzzy Dark Matter mass (affects fringe scaling)
    kinetic_mixing : float, optional
        Kinetic mixing parameter (affects coupling strength)
    """
    # Ensure all inputs are square
    image = ensure_square(image)
    interference = ensure_square(interference)
    soliton = ensure_square(soliton)
    
    # Shape validation
    assert image.shape == interference.shape == soliton.shape, \
        f"shape mismatch after squaring: {image.shape}, {interference.shape}, {soliton.shape}"
    
    # Apply FDM mass and kinetic mixing scaling if provided
    if fdm_mass is not None:
        # FDM mass affects fringe spacing and visibility
        mass_scale = 1.0 / (1.0 + fdm_mass / 1e-22)  # typical FDM scale ~ 1e-22 eV
        interference = interference * mass_scale
    
    if kinetic_mixing is not None:
        # Kinetic mixing affects coupling strength
        mix_scale = kinetic_mixing / 1e-12  # normalize to typical values
        interference = interference * (1 + mix_scale)
    
    # Original parameter m based on omega
    m = omega * 0.6
    
    # Blend the components
    result = np.clip(image * (1 - m * 0.4) + 
                     interference * m * 0.5 +
                     soliton * m * 0.4, 0, 1)
    
    return result

class EntanglementViz:
    """Interactive visualization with magnetar B-field control and area selection"""
    
    def __init__(self, image: np.ndarray, interference: np.ndarray, 
                 soliton: np.ndarray, omega_init: float = 1.0):
        # Ensure all inputs are square
        self.base_image = ensure_square(image)
        self.interference = ensure_square(interference)
        self.soliton = ensure_square(soliton)
        self.omega = omega_init
        
        # FDM parameters
        self.fdm_mass = 1e-22  # eV
        self.kinetic_mixing = 1e-12
        
        # Setup figure
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.2, left=0.1)
        
        # Initial display
        self.update_display()
        
        # Setup controls
        self.setup_controls()
        
        # Setup area selection
        self.selector = RectangleSelector(
            self.ax, self.on_select,
            useblit=True,
            button=[1],
            minspanx=5, minspany=5,
            spancoords='pixels',
            interactive=True
        )
        
        # Store selected region
        self.selected_region = None
        
    def setup_controls(self):
        """Setup slider and button controls"""
        # Omega slider (magnetar B-field)
        ax_omega = plt.axes([0.1, 0.05, 0.65, 0.03])
        self.slider_omega = plt.Slider(
            ax_omega, 'Magnetar B-field (ω)', 0, 2, 
            valinit=self.omega, valstep=0.01
        )
        self.slider_omega.on_changed(self.update_omega)
        
        # FDM mass slider
        ax_mass = plt.axes([0.1, 0.09, 0.65, 0.03])
        self.slider_mass = plt.Slider(
            ax_mass, 'FDM Mass (log₁₀ eV)', -23, -21, 
            valinit=np.log10(self.fdm_mass), valstep=0.1
        )
        self.slider_mass.on_changed(self.update_mass)
        
        # Kinetic mixing slider
        ax_mix = plt.axes([0.1, 0.13, 0.65, 0.03])
        self.slider_mix = plt.Slider(
            ax_mix, 'Kinetic Mixing (log₁₀)', -14, -10, 
            valinit=np.log10(self.kinetic_mixing), valstep=0.1
        )
        self.slider_mix.on_changed(self.update_mixing)
        
        # Start button
        ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])
        self.button = Button(ax_button, 'Start')
        self.button.on_clicked(self.start_processing)
        
    def update_omega(self, val):
        """Update omega parameter"""
        self.omega = val
        self.update_display()
        
    def update_mass(self, val):
        """Update FDM mass parameter"""
        self.fdm_mass = 10**val
        self.update_display()
        
    def update_mixing(self, val):
        """Update kinetic mixing parameter"""
        self.kinetic_mixing = 10**val
        self.update_display()
        
    def on_select(self, eclick, erelease):
        """Handle region selection"""
        x1, y1 = int(eclick.xdata), int(eclick.ydata)
        x2, y2 = int(erelease.xdata), int(erelease.ydata)
        self.selected_region = (min(x1, x2), min(y1, y2), 
                                 max(x1, x2), max(y1, y2))
        print(f"Selected region: {self.selected_region}")
        
    def start_processing(self, event):
        """Process selected region and show detailed analysis"""
        if self.selected_region is None:
            print("Please select an area first!")
            return
            
        x1, y1, x2, y2 = self.selected_region
        
        # Extract region from current overlay
        current_overlay = self.update_display(return_array=True)
        region = current_overlay[y1:y2, x1:x2]
        
        # Create analysis figure
        fig_analysis, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Plot selected region
        axes[0, 0].imshow(region, cmap='viridis')
        axes[0, 0].set_title('Selected Region')
        axes[0, 0].axis('off')
        
        # Plot intensity profile
        center_y = region.shape[0] // 2
        profile = region[center_y, :]
        axes[0, 1].plot(profile)
        axes[0, 1].set_title('Horizontal Intensity Profile')
        axes[0, 1].set_xlabel('Pixel')
        axes[0, 1].set_ylabel('Intensity')
        
        # FFT analysis
        fft_region = np.fft.fft2(region)
        fft_mag = np.abs(np.fft.fftshift(fft_region))
        axes[1, 0].imshow(np.log(fft_mag + 1), cmap='gray')
        axes[1, 0].set_title('FFT Magnitude (log scale)')
        axes[1, 0].axis('off')
        
        # Entanglement fringe visibility
        fringe_visibility = (np.max(profile) - np.min(profile)) / \
                           (np.max(profile) + np.min(profile) + 1e-10)
        axes[1, 1].text(0.5, 0.5, 
                       f'Fringe Visibility: {fringe_visibility:.3f}\n'
                       f'ω = {self.omega:.2f}\n'
                       f'FDM Mass: {self.fdm_mass:.2e} eV\n'
                       f'Kinetic Mixing: {self.kinetic_mixing:.2e}',
                       transform=axes[1, 1].transAxes,
                       ha='center', va='center',
                       fontsize=12)
        axes[1, 1].set_title('Parameters')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.show()
        
    def update_display(self, return_array=False):
        """Update the main display with current parameters"""
        # Generate overlay with current FDM parameters
        overlay = pdp_entanglement_overlay(
            self.base_image, self.interference, self.soliton, 
            self.omega,
            fdm_mass=self.fdm_mass,
            kinetic_mixing=self.kinetic_mixing
        )
        
        if return_array:
            return overlay
        
        self.ax.clear()
        self.ax.imshow(overlay, cmap='gray')
        self.ax.set_title(f'Entanglement Fringes (ω={self.omega:.2f})')
        self.ax.axis('off')
        
        # Reattach selector
        if hasattr(self, 'selector'):
            self.selector = RectangleSelector(
                self.ax, self.on_select,
                useblit=True,
                button=[1],
                minspanx=5, minspany=5,
                spancoords='pixels',
                interactive=True
            )
        
        plt.draw()
        return overlay

# Example usage:
if __name__ == "__main__":
    # Create sample data
    size = 512
    x = np.linspace(-np.pi, np.pi, size)
    y = np.linspace(-np.pi, np.pi, size)
    X, Y = np.meshgrid(x, y)
    
    # Base image (gaussian blob)
    base = np.exp(-(X**2 + Y**2) / 4)
    
    # Interference pattern (fringes)
    interference = 0.5 * (1 + np.cos(20 * X))
    
    # Soliton field (localized)
    soliton = np.exp(-((X-1)**2 + (Y-1)**2) / 0.5)
    
    # Launch interactive visualization
    viz = EntanglementViz(base, interference, soliton, omega_init=1.0)
    plt.show()
