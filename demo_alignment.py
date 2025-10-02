"""
Demo script for testing the Interactive Image Alignment widget.
This script creates sample images and demonstrates the alignment functionality.
"""
import numpy as np
import napari

def create_demo_images():
    """Create demo images for testing alignment."""
    # Create a large base image (4000x3000 like in the example)
    base_height, base_width = 300, 400  # Scaled down for demo
    base_image = np.zeros((base_height, base_width), dtype=np.uint8)
    
    # Add some pattern to the base image to make positioning easier
    for i in range(0, base_height, 50):
        base_image[i:i+10, :] = 100
    for j in range(0, base_width, 50):
        base_image[:, j:j+10] = 150
    
    # Create a small image (1000x2000 like in the example)
    small_height, small_width = 100, 200  # Scaled down for demo
    small_image = np.ones((small_height, small_width), dtype=np.uint8) * 255
    
    # Add some distinctive pattern to the small image
    small_image[40:60, 80:120] = 128  # Gray rectangle
    small_image[10:30, 50:150] = 64   # Dark rectangle
    
    return base_image, small_image

def main():
    """Run the demo."""
    # Create napari viewer
    viewer = napari.Viewer()
    
    # Create demo images
    base_image, small_image = create_demo_images()
    
    # Add images to viewer
    base_layer = viewer.add_image(base_image, name="Base Image (Large)")
    small_layer = viewer.add_image(small_image, name="Small Image")
    
    # Import and add the alignment widget
    from image_alignment import InteractiveImageAlignment
    alignment_widget = InteractiveImageAlignment(viewer)
    viewer.window.add_dock_widget(alignment_widget, name="Image Alignment")
    
    print("Demo started!")
    print("1. Select 'Base Image (Large)' as the base image")
    print("2. Select 'Small Image' as the small image")
    print("3. Click 'Start Interactive Alignment'")
    print("4. Drag the red overlay to position the small image")
    print("5. Click 'Apply Padding' to create the aligned image")
    
    # Start napari
    napari.run()

if __name__ == "__main__":
    main()