"""
Simple test script to debug the alignment issue.
"""
import numpy as np
import napari
from image_alignment import InteractiveImageAlignment

def main():
    """Test the alignment functionality with simple data."""
    # Create viewer
    viewer = napari.Viewer()
    
    # Create very simple test images
    # Large image: 200x300 with distinct pattern
    large_image = np.zeros((200, 300), dtype=np.uint8)
    large_image[::20, :] = 100  # Horizontal lines every 20 pixels
    large_image[:, ::30] = 150  # Vertical lines every 30 pixels
    
    # Small image: 50x80 with solid color
    small_image = np.ones((50, 80), dtype=np.uint8) * 255  # White rectangle
    
    # Add to viewer
    base_layer = viewer.add_image(large_image, name="Base Image (Large)")
    small_layer = viewer.add_image(small_image, name="Small Image")
    
    # Add alignment widget
    alignment_widget = InteractiveImageAlignment(viewer)
    viewer.window.add_dock_widget(alignment_widget, name="Alignment Test")
    
    print("Test setup complete!")
    print("Base image shape:", large_image.shape)
    print("Small image shape:", small_image.shape)
    print("\nInstructions:")
    print("1. Select both images in the widget")
    print("2. Click 'Start Interactive Alignment'")
    print("3. Move the red overlay (it should be visible)")
    print("4. Click 'Apply Padding' and check the console output")
    
    napari.run()

if __name__ == "__main__":
    main()