#!/usr/bin/env python3
"""
Polarization Analysis Script for Astronomical Data

This script reads 4 FITS files containing polarization data and creates
polarization maps including Stokes parameters, polarization intensity,
and polarization angle visualizations.

Usage:
    python polarization.py [folder_path]
    
If no folder path is provided, it will look in the current directory.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import glob
from astropy.io import fits
from astropy import units as u
from astropy.wcs import WCS
import warnings

# Suppress some common warnings
warnings.filterwarnings('ignore', category=UserWarning)

class PolarizationAnalyzer:
    """Class to handle polarization analysis of astronomical FITS data."""
    
    def __init__(self, folder_path='.'):
        """
        Initialize the polarization analyzer.
        
        Parameters:
        -----------
        folder_path : str
            Path to the folder containing FITS files
        """
        self.folder_path = folder_path
        self.fits_files = []
        self.data = {}
        self.headers = {}
        self.wcs = None
        
    def find_fits_files(self):
        """Find all FITS files in the specified folder."""
        patterns = ['*.fit', '*.fits', '*.fts']
        self.fits_files = []
        
        for pattern in patterns:
            files = glob.glob(os.path.join(self.folder_path, pattern))
            self.fits_files.extend(files)
        
        self.fits_files.sort()  # Sort for consistent ordering
        
        if len(self.fits_files) == 0:
            raise FileNotFoundError(f"No FITS files found in {self.folder_path}")
        
        print(f"Found {len(self.fits_files)} FITS files:")
        for i, file in enumerate(self.fits_files):
            print(f"  {i+1}: {os.path.basename(file)}")
            
        return self.fits_files
    
    def load_fits_data(self, max_files=4):
        """
        Load FITS data from files.
        
        Parameters:
        -----------
        max_files : int
            Maximum number of files to load (default: 4 for Stokes I, Q, U, V)
        """
        if not self.fits_files:
            self.find_fits_files()
        
        # Use up to max_files
        files_to_load = self.fits_files[:max_files]
        
        print(f"\nLoading {len(files_to_load)} FITS files...")
        
        for i, file_path in enumerate(files_to_load):
            try:
                with fits.open(file_path) as hdul:
                    # Get the primary HDU or first image HDU
                    for hdu in hdul:
                        if hdu.data is not None:
                            self.data[f'image_{i}'] = hdu.data.astype(np.float64)
                            self.headers[f'image_{i}'] = hdu.header
                            
                            # Store WCS information from first file
                            if self.wcs is None:
                                try:
                                    self.wcs = WCS(hdu.header)
                                except:
                                    print(f"Warning: Could not parse WCS from {file_path}")
                            break
                
                print(f"  Loaded: {os.path.basename(file_path)} - Shape: {self.data[f'image_{i}'].shape}")
                
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
                continue
        
        if len(self.data) == 0:
            raise ValueError("No valid FITS data could be loaded")
            
        print(f"Successfully loaded {len(self.data)} images")
        
    def calculate_stokes_parameters(self):
        """
        Calculate Stokes parameters from the loaded images.
        Assumes the first 4 images correspond to different polarization states.
        """
        if len(self.data) < 2:
            raise ValueError("Need at least 2 images for polarization analysis")
        
        # Get image data
        images = [self.data[f'image_{i}'] for i in range(min(4, len(self.data)))]
        
        # Ensure all images have the same shape
        shapes = [img.shape for img in images]
        if not all(shape == shapes[0] for shape in shapes):
            print("Warning: Images have different shapes. Will crop to minimum dimensions.")
            min_shape = tuple(min(dim) for dim in zip(*shapes))
            images = [img[:min_shape[0], :min_shape[1]] for img in images]
        
        # Calculate Stokes parameters
        # This is a general approach - you may need to adjust based on your specific data
        if len(images) == 4:
            # Standard Stokes parameters I, Q, U, V
            self.stokes_I = images[0]  # Total intensity
            self.stokes_Q = images[1] - images[3]  # Linear polarization (0° - 90°)
            self.stokes_U = images[2] - images[0]  # Linear polarization (45° - 135°)
            self.stokes_V = np.zeros_like(self.stokes_I)  # Circular polarization (if available)
            
        elif len(images) == 3:
            # Three images: total intensity and two linear polarization states
            self.stokes_I = images[0]
            self.stokes_Q = images[1] - images[2]
            self.stokes_U = images[2] - images[1]
            self.stokes_V = np.zeros_like(self.stokes_I)
            
        elif len(images) == 2:
            # Two images: simple difference
            self.stokes_I = (images[0] + images[1]) / 2
            self.stokes_Q = images[0] - images[1]
            self.stokes_U = np.zeros_like(self.stokes_I)
            self.stokes_V = np.zeros_like(self.stokes_I)
        
        # Calculate derived parameters
        self.linear_polarization = np.sqrt(self.stokes_Q**2 + self.stokes_U**2)
        self.total_polarization = np.sqrt(self.stokes_Q**2 + self.stokes_U**2 + self.stokes_V**2)
        
        # Polarization angle (in degrees)
        self.polarization_angle = 0.5 * np.arctan2(self.stokes_U, self.stokes_Q) * 180 / np.pi
        
        # Polarization fraction
        with np.errstate(divide='ignore', invalid='ignore'):
            self.polarization_fraction = self.linear_polarization / np.abs(self.stokes_I)
            self.polarization_fraction[self.stokes_I == 0] = 0
            self.polarization_fraction = np.clip(self.polarization_fraction, 0, 1)
        
        print("Calculated Stokes parameters and polarization properties")
        
    def create_polarization_maps(self, output_folder='polarization_output'):
        """Create and save polarization visualization plots."""
        
        if not hasattr(self, 'stokes_I'):
            raise ValueError("Stokes parameters not calculated. Run calculate_stokes_parameters() first.")
        
        # Create output folder
        os.makedirs(output_folder, exist_ok=True)
        
        # Set up the plot style
        plt.style.use('default')
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Polarization Analysis Results', fontsize=16, fontweight='bold')
        
        # 1. Stokes I (Total Intensity)
        ax = axes[0, 0]
        im1 = ax.imshow(self.stokes_I, cmap='hot', origin='lower')
        ax.set_title('Stokes I (Total Intensity)')
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        plt.colorbar(im1, ax=ax, label='Intensity')
        
        # 2. Stokes Q
        ax = axes[0, 1]
        im2 = ax.imshow(self.stokes_Q, cmap='RdBu_r', origin='lower')
        ax.set_title('Stokes Q')
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        plt.colorbar(im2, ax=ax, label='Q Parameter')
        
        # 3. Stokes U
        ax = axes[0, 2]
        im3 = ax.imshow(self.stokes_U, cmap='RdBu_r', origin='lower')
        ax.set_title('Stokes U')
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        plt.colorbar(im3, ax=ax, label='U Parameter')
        
        # 4. Linear Polarization Intensity
        ax = axes[1, 0]
        im4 = ax.imshow(self.linear_polarization, cmap='viridis', origin='lower')
        ax.set_title('Linear Polarization Intensity')
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        plt.colorbar(im4, ax=ax, label='Polarization Intensity')
        
        # 5. Polarization Angle
        ax = axes[1, 1]
        im5 = ax.imshow(self.polarization_angle, cmap='hsv', origin='lower', vmin=-90, vmax=90)
        ax.set_title('Polarization Angle')
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        plt.colorbar(im5, ax=ax, label='Angle (degrees)')
        
        # 6. Polarization Fraction
        ax = axes[1, 2]
        # Mask very low intensity regions for better visualization
        mask = self.stokes_I > 0.1 * np.max(self.stokes_I)
        pol_frac_masked = np.where(mask, self.polarization_fraction, np.nan)
        im6 = ax.imshow(pol_frac_masked, cmap='plasma', origin='lower', vmin=0, vmax=1)
        ax.set_title('Polarization Fraction')
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        plt.colorbar(im6, ax=ax, label='Fraction')
        
        plt.tight_layout()
        
        # Save the main polarization map
        output_path = os.path.join(output_folder, 'polarization_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved polarization analysis plot: {output_path}")
        
        # Create polarization vector plot
        self.create_vector_plot(output_folder)
        
        plt.show()
        
    def create_vector_plot(self, output_folder='polarization_output'):
        """Create a polarization vector overlay plot."""
        
        # Subsample the data for vector plotting
        step = max(1, min(self.stokes_I.shape) // 20)  # About 20 vectors per dimension
        y_coords, x_coords = np.mgrid[0:self.stokes_I.shape[0]:step, 0:self.stokes_I.shape[1]:step]
        
        # Get subsampled polarization data
        I_sub = self.stokes_I[::step, ::step]
        Q_sub = self.stokes_Q[::step, ::step]
        U_sub = self.stokes_U[::step, ::step]
        pol_int_sub = self.linear_polarization[::step, ::step]
        
        # Calculate vector components (perpendicular to magnetic field)
        # Vector length proportional to polarization intensity
        pol_length = pol_int_sub / np.max(pol_int_sub) * step * 0.8
        pol_angle_rad = 0.5 * np.arctan2(U_sub, Q_sub)
        
        dx = pol_length * np.cos(pol_angle_rad)
        dy = pol_length * np.sin(pol_angle_rad)
        
        # Create vector plot
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Background: Total intensity
        im = ax.imshow(self.stokes_I, cmap='gray', origin='lower', alpha=0.7)
        
        # Overlay polarization vectors
        # Only show vectors where polarization is significant
        threshold = 0.1 * np.max(pol_int_sub)
        mask = pol_int_sub > threshold
        
        quiver = ax.quiver(x_coords[mask], y_coords[mask], 
                          dx[mask], dy[mask],
                          pol_int_sub[mask],
                          cmap='hot', scale_units='xy', scale=1,
                          width=0.003, headwidth=3, headlength=4)
        
        ax.set_title('Polarization Vectors over Total Intensity', fontsize=14, fontweight='bold')
        ax.set_xlabel('X (pixels)')
        ax.set_ylabel('Y (pixels)')
        
        # Add colorbars
        cbar1 = plt.colorbar(im, ax=ax, label='Total Intensity', shrink=0.8, pad=0.02)
        cbar2 = plt.colorbar(quiver, ax=ax, label='Polarization Intensity', shrink=0.8, pad=0.1)
        
        plt.tight_layout()
        
        # Save vector plot
        vector_path = os.path.join(output_folder, 'polarization_vectors.png')
        plt.savefig(vector_path, dpi=300, bbox_inches='tight')
        print(f"Saved polarization vector plot: {vector_path}")
        
        plt.show()
        
    def save_results_to_fits(self, output_folder='polarization_output'):
        """Save calculated Stokes parameters and derived quantities to FITS files."""
        
        os.makedirs(output_folder, exist_ok=True)
        
        # Prepare header with basic information
        header = fits.Header()
        header['OBJECT'] = 'Polarization Analysis'
        header['DATE'] = '2025-07-28'
        header['COMMENT'] = 'Generated by polarization analysis script'
        
        # Copy WCS information if available
        if self.wcs is not None:
            header.update(self.wcs.to_header())
        
        # Save Stokes parameters
        fits_files_to_save = [
            ('stokes_I.fits', self.stokes_I, 'Stokes I parameter'),
            ('stokes_Q.fits', self.stokes_Q, 'Stokes Q parameter'),
            ('stokes_U.fits', self.stokes_U, 'Stokes U parameter'),
            ('stokes_V.fits', self.stokes_V, 'Stokes V parameter'),
            ('linear_polarization.fits', self.linear_polarization, 'Linear polarization intensity'),
            ('polarization_angle.fits', self.polarization_angle, 'Polarization angle in degrees'),
            ('polarization_fraction.fits', self.polarization_fraction, 'Polarization fraction')
        ]
        
        for filename, data, description in fits_files_to_save:
            header['COMMENT'] = description
            hdu = fits.PrimaryHDU(data, header=header)
            output_path = os.path.join(output_folder, filename)
            hdu.writeto(output_path, overwrite=True)
            print(f"Saved: {output_path}")

def main():
    """Main function to run the polarization analysis."""
    
    # Get folder path from command line argument or use current directory
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = '.'
    
    print("="*60)
    print("Polarization Analysis for Astronomical FITS Data")
    print("="*60)
    print(f"Analyzing FITS files in: {os.path.abspath(folder_path)}")
    
    try:
        # Initialize analyzer
        analyzer = PolarizationAnalyzer(folder_path)
        
        # Find and load FITS files
        analyzer.find_fits_files()
        analyzer.load_fits_data(max_files=4)
        
        # Calculate polarization parameters
        analyzer.calculate_stokes_parameters()
        
        # Create visualizations
        analyzer.create_polarization_maps()
        
        # Save results
        analyzer.save_results_to_fits()
        
        print("\n" + "="*60)
        print("Polarization analysis completed successfully!")
        print("Check the 'polarization_output' folder for results.")
        print("="*60)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please make sure you have FITS files (.fit, .fits, or .fts) in the specified folder.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()