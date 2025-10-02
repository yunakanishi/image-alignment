"""
Tests for the interactive image alignment widget.
"""
import numpy as np
import pytest

from image_alignment._widget import InteractiveImageAlignment


class MockWidget:
    """Mock widget class for testing padding functionality without Qt dependencies."""
    
    def _pad_image_to_position(self, small_image: np.ndarray, target_shape, translate):
        """Padding method copied from InteractiveImageAlignment for testing."""
        # Convert translate to integer pixel coordinates
        if len(translate) != len(target_shape):
            # Handle 2D vs 3D cases
            if len(target_shape) == 2 and len(translate) >= 2:
                offset_y, offset_x = int(translate[-2]), int(translate[-1])
            elif len(target_shape) == 3 and len(translate) >= 3:
                offset_z, offset_y, offset_x = int(translate[-3]), int(translate[-2]), int(translate[-1])
            else:
                offset_y, offset_x = 0, 0
                if len(target_shape) == 3:
                    offset_z = 0
        else:
            if len(target_shape) == 2:
                offset_y, offset_x = int(translate[0]), int(translate[1])
            else:
                offset_z, offset_y, offset_x = int(translate[0]), int(translate[1]), int(translate[2])
        
        # Create padded image filled with zeros
        padded = np.zeros(target_shape, dtype=small_image.dtype)
        
        # Calculate bounds for placement
        if len(target_shape) == 2:
            h, w = small_image.shape[:2]
            
            # Ensure placement is within bounds
            start_y = max(0, offset_y)
            start_x = max(0, offset_x)
            end_y = min(target_shape[0], offset_y + h)
            end_x = min(target_shape[1], offset_x + w)
            
            # Calculate corresponding regions in source image
            src_start_y = max(0, -offset_y)
            src_start_x = max(0, -offset_x)
            src_end_y = src_start_y + (end_y - start_y)
            src_end_x = src_start_x + (end_x - start_x)
            
            # Place the image
            if end_y > start_y and end_x > start_x:
                padded[start_y:end_y, start_x:end_x] = small_image[src_start_y:src_end_y, src_start_x:src_end_x]
        
        else:  # 3D case
            d, h, w = small_image.shape[:3]
            
            start_z = max(0, offset_z)
            start_y = max(0, offset_y)
            start_x = max(0, offset_x)
            end_z = min(target_shape[0], offset_z + d)
            end_y = min(target_shape[1], offset_y + h)
            end_x = min(target_shape[2], offset_x + w)
            
            src_start_z = max(0, -offset_z)
            src_start_y = max(0, -offset_y)
            src_start_x = max(0, -offset_x)
            src_end_z = src_start_z + (end_z - start_z)
            src_end_y = src_start_y + (end_y - start_y)
            src_end_x = src_start_x + (end_x - start_x)
            
            if end_z > start_z and end_y > start_y and end_x > start_x:
                padded[start_z:end_z, start_y:end_y, start_x:end_x] = \
                    small_image[src_start_z:src_end_z, src_start_y:src_end_y, src_start_x:src_end_x]
        
        return padded


def test_pad_image_to_position_2d():
    """Test padding functionality for 2D images."""
    # Create a small test image
    small_image = np.ones((10, 15), dtype=np.uint8) * 255
    target_shape = (50, 60)
    translate = (5.0, 10.0)  # offset_y=5, offset_x=10
    
    # Create mock widget instance
    widget = MockWidget()
    
    # Test padding
    padded = widget._pad_image_to_position(small_image, target_shape, translate)
    
    # Check shape
    assert padded.shape == target_shape
    
    # Check that the small image is placed correctly
    assert np.all(padded[5:15, 10:25] == 255)  # Where the small image should be
    assert np.all(padded[0:5, :] == 0)  # Above should be zeros
    assert np.all(padded[:, 0:10] == 0)  # Left should be zeros


def test_pad_image_to_position_edge_cases():
    """Test padding with edge cases (negative offsets, out of bounds)."""
    small_image = np.ones((10, 10), dtype=np.uint8) * 128
    target_shape = (20, 20)
    
    widget = MockWidget()
    
    # Test negative offset (should crop the small image)
    translate = (-5.0, -3.0)
    padded = widget._pad_image_to_position(small_image, target_shape, translate)
    assert padded.shape == target_shape
    # Only part of the small image should be visible at top-left
    assert np.all(padded[0:5, 0:7] == 128)
    
    # Test offset that goes beyond target bounds
    translate = (15.0, 15.0)
    padded = widget._pad_image_to_position(small_image, target_shape, translate)
    assert padded.shape == target_shape
    # Only part of the small image should fit
    assert np.all(padded[15:20, 15:20] == 128)


def test_pad_image_to_position_3d():
    """Test padding functionality for 3D images."""
    small_image = np.ones((5, 10, 15), dtype=np.uint8) * 200
    target_shape = (20, 50, 60)
    translate = (2.0, 5.0, 10.0)  # offset_z=2, offset_y=5, offset_x=10
    
    widget = MockWidget()
    
    padded = widget._pad_image_to_position(small_image, target_shape, translate)
    
    # Check shape
    assert padded.shape == target_shape
    
    # Check that the small image is placed correctly
    assert np.all(padded[2:7, 5:15, 10:25] == 200)
    
    # Check some zero regions
    assert np.all(padded[0:2, :, :] == 0)  # Before z
    assert np.all(padded[:, 0:5, :] == 0)  # Before y
    assert np.all(padded[:, :, 0:10] == 0)  # Before x


def test_different_dtypes():
    """Test that padding preserves different data types."""
    dtypes = [np.uint8, np.uint16, np.float32, np.float64]
    
    for dtype in dtypes:
        small_image = np.ones((5, 5), dtype=dtype) * 100
        target_shape = (10, 10)
        translate = (2.0, 3.0)
        
        widget = MockWidget()
        padded = widget._pad_image_to_position(small_image, target_shape, translate)
        
        assert padded.dtype == dtype
        assert padded.shape == target_shape
        assert np.all(padded[2:7, 3:8] == 100)


if __name__ == "__main__":
    # Run basic tests
    test_pad_image_to_position_2d()
    test_pad_image_to_position_edge_cases()
    test_pad_image_to_position_3d()
    test_different_dtypes()
    print("All tests passed!")