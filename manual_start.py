"""
Manual napari startup script for testing the Interactive Image Alignment plugin.
"""
import napari
import numpy as np

def main():
    """Manually start napari with the plugin."""
    # Create napari viewer
    viewer = napari.Viewer()
    
    # Load some sample images (optional - you can load your own)
    # Create sample data
    large_image = np.random.rand(400, 600) * 255  # 400x600 large image
    small_image = np.random.rand(150, 200) * 255  # 150x200 small image
    
    # Add to viewer
    viewer.add_image(large_image, name="Large Image")
    viewer.add_image(small_image, name="Small Image")
    
    print("Napari started!")
    print("To use the Image Alignment plugin:")
    print("1. Go to Plugins → image-alignment → Interactive Image Alignment")
    print("2. Select your large and small images")
    print("3. Click 'Start Interactive Alignment'")
    print("4. Drag the overlay to position it")
    print("5. Click 'Apply Padding' to finalize")
    
    # Start napari event loop
    napari.run()

if __name__ == "__main__":
    main()