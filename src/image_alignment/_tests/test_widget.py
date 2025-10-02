import numpy as np

from image_alignment._widget import InteractiveImageAlignment


def test_interactive_image_alignment_widget(make_napari_viewer):
    """Test InteractiveImageAlignment widget initialization and basic functionality."""
    viewer = make_napari_viewer()
    
    # Create test images
    base_image = np.random.random((200, 200))
    small_image = np.random.random((100, 100))
    
    # Add layers to viewer
    base_layer = viewer.add_image(base_image, name="base_image")
    small_layer = viewer.add_image(small_image, name="small_image")
    
    # Create widget
    my_widget = InteractiveImageAlignment(viewer)
    
    # Test widget initialization
    assert my_widget._viewer == viewer
    assert my_widget._overlay_layer is None
    assert not my_widget._is_aligning
    
    # Test layer selection
    my_widget._base_image_combo.value = base_layer
    my_widget._small_image_combo.value = small_layer
    
    # Test that start button is enabled after selecting layers
    assert my_widget._start_alignment_btn.enabled
    assert not my_widget._apply_padding_btn.enabled


def test_image_padding_function(make_napari_viewer):
    """Test the _pad_image_to_position method."""
    viewer = make_napari_viewer()
    widget = InteractiveImageAlignment(viewer)
    
    # Create test data
    small_image = np.ones((50, 50))
    target_shape = (100, 100)
    translate = (25, 25)  # Center position
    
    # Test padding
    padded = widget._pad_image_to_position(small_image, target_shape, translate)
    
    # Check result shape
    assert padded.shape == target_shape
    
    # Check that the small image is placed correctly (non-zero values should be in center)
    assert np.sum(padded[25:75, 25:75]) > 0  # Center should have values
    assert np.sum(padded[0:25, 0:25]) == 0   # Top-left corner should be empty
