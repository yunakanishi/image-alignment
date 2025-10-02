"""
This module contains the interactive image alignment widget.

The widget allows positioning a small image over a large image and 
padding it to match the large image's dimensions.

References:
- Widget specification: https://napari.org/stable/plugins/building_a_plugin/guides.html#widgets
- magicgui docs: https://pyapp-kit.github.io/magicgui/
"""
from typing import TYPE_CHECKING, Tuple

import numpy as np
from magicgui.widgets import Container, create_widget, PushButton, Label

if TYPE_CHECKING:
    import napari


class InteractiveImageAlignment(Container):
    """Widget for interactive image alignment with automatic padding."""
    
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self._viewer = viewer
        self._overlay_layer = None
        self._base_image_layer = None
        self._small_image_layer = None
        self._is_aligning = False
        
        # Create widgets
        self._base_image_combo = create_widget(
            label="Base Image (Large)", annotation="napari.layers.Image"
        )
        self._small_image_combo = create_widget(
            label="Small Image", annotation="napari.layers.Image"
        )
        
        self._start_alignment_btn = PushButton(text="Start Interactive Alignment")
        self._apply_padding_btn = PushButton(text="Apply Padding")
        self._apply_padding_btn.enabled = False
        
        self._status_label = Label(value="Select base and small images, then click 'Start Interactive Alignment'")
        
        # Connect callbacks
        self._start_alignment_btn.clicked.connect(self._start_alignment)
        self._apply_padding_btn.clicked.connect(self._apply_padding)
        self._base_image_combo.changed.connect(self._on_layer_selection_changed)
        self._small_image_combo.changed.connect(self._on_layer_selection_changed)
        
        # Layout widgets
        self.extend([
            self._base_image_combo,
            self._small_image_combo,
            self._start_alignment_btn,
            self._apply_padding_btn,
            self._status_label,
        ])
    
    def _on_layer_selection_changed(self):
        """Update button states when layer selection changes."""
        base_selected = self._base_image_combo.value is not None
        small_selected = self._small_image_combo.value is not None
        
        self._start_alignment_btn.enabled = base_selected and small_selected
        
        if base_selected and small_selected:
            self._status_label.value = "Ready to start alignment"
        else:
            self._status_label.value = "Select both base and small images"
    
    def _start_alignment(self):
        """Start interactive alignment mode."""
        base_layer = self._base_image_combo.value
        small_layer = self._small_image_combo.value
        
        if base_layer is None or small_layer is None:
            self._status_label.value = "Please select both images"
            return
        
        self._base_image_layer = base_layer
        self._small_image_layer = small_layer
        
        # Create an overlay of the small image for positioning
        self._create_overlay_layer()
        
        # Enable dragging mode
        self._is_aligning = True
        self._start_alignment_btn.enabled = False
        self._apply_padding_btn.enabled = True
        self._status_label.value = "Drag the overlay image to position it. Click 'Apply Padding' when ready."
    
    def _create_overlay_layer(self):
        """Create an overlay layer for the small image."""
        if self._overlay_layer is not None:
            try:
                self._viewer.layers.remove(self._overlay_layer)
            except ValueError:
                pass
        
        # Create overlay with the small image data
        overlay_data = self._small_image_layer.data.copy()
        overlay_name = f"{self._small_image_layer.name}_overlay"
        
        # Add as image layer with some transparency
        self._overlay_layer = self._viewer.add_image(
            overlay_data,
            name=overlay_name,
            opacity=0.7,
            blending='additive',
            colormap='red'
        )
        
        # Make it the active layer for easy manipulation
        self._viewer.layers.selection.active = self._overlay_layer
    
    def _apply_padding(self):
        """Apply padding to the small image based on current overlay position."""
        if self._overlay_layer is None or self._base_image_layer is None:
            self._status_label.value = "Error: Missing layers"
            return
        
        # Get dimensions first
        base_shape = self._base_image_layer.data.shape
        small_shape = self._small_image_layer.data.shape
        
        # Get the current position of the overlay (use extent.world for accuracy)
        overlay_extent = self._overlay_layer.extent
        base_extent = self._base_image_layer.extent

        # Get the top-left corner of each layer in world coordinates
        overlay_world_pos = overlay_extent.world[0]
        base_world_pos = base_extent.world[0]

        # Calculate relative position in world coordinates and convert to pixels
        relative_world_pos = overlay_world_pos - base_world_pos
        relative_translate = tuple(int(round(relative_world_pos[i])) for i in range(len(relative_world_pos)))

        # Also get base_translate for later use
        base_translate = self._base_image_layer.translate
        
        # If overlay wasn't moved, fall back to center placement
        if all(abs(t) < 0.5 for t in relative_translate):
            center_y = (base_shape[0] - small_shape[0]) // 2
            center_x = (base_shape[1] - small_shape[1]) // 2
            relative_translate = (center_y, center_x)
        
        # Calculate padding based on overlay position
        padded_image = self._pad_image_to_position(
            self._small_image_layer.data,
            base_shape,
            relative_translate,
        )

        # Add the padded image as a new layer (positioned with base layer translate)
        padded_name = f"{self._small_image_layer.name}_aligned"
        aligned_layer = self._viewer.add_image(
            padded_image,
            name=padded_name,
            opacity=0.8,
            translate=base_translate,
        )

        # Clean up overlay and reset UI
        try:
            self._viewer.layers.remove(self._overlay_layer)
        except ValueError:
            pass
        self._overlay_layer = None

        self._is_aligning = False
        self._start_alignment_btn.enabled = True
        self._apply_padding_btn.enabled = False
        self._status_label.value = f"Alignment complete! Created layer: {padded_name}"
    
    def _pad_image_to_position(self, small_image: np.ndarray, target_shape: Tuple[int, ...], 
                              translate: Tuple[float, ...]) -> np.ndarray:
        """Pad the small image to match target shape based on translation."""
        # IMPORTANT: napari translate is in world coordinates, not pixel coordinates
        # We need to convert world coordinates to pixel coordinates
        print(f"Raw translate: {translate}, target_shape dimensions: {len(target_shape)}")
        
        # For now, assume scale is (1, 1) - in the future we should get this from the layer
        # napari coordinates are in (row, col) order, which is (y, x)
        if len(target_shape) == 2:
            # 2D case: translate should be (y, x) in world coordinates
            if len(translate) >= 2:
                # Convert world coordinates to pixel coordinates
                # For now, assume 1:1 mapping (scale = 1)
                offset_y, offset_x = int(round(translate[0])), int(round(translate[1]))
            else:
                offset_y, offset_x = 0, 0
        else:
            # 3D case: translate should be (z, y, x) in world coordinates
            if len(translate) >= 3:
                offset_z, offset_y, offset_x = int(round(translate[0])), int(round(translate[1])), int(round(translate[2]))
            elif len(translate) >= 2:
                offset_z = 0
                offset_y, offset_x = int(round(translate[0])), int(round(translate[1]))
            else:
                offset_z, offset_y, offset_x = 0, 0, 0
        
        # Debug: Print offset information
        if len(target_shape) == 2:
            print(f"Calculated pixel offsets: y={offset_y}, x={offset_x}")
        else:
            print(f"Calculated pixel offsets: z={offset_z}, y={offset_y}, x={offset_x}")
        
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
            
            # Debug: Print placement information
            print(f"Placement: start_y={start_y}, start_x={start_x}, end_y={end_y}, end_x={end_x}")
            print(f"Source: src_start_y={src_start_y}, src_start_x={src_start_x}, src_end_y={src_end_y}, src_end_x={src_end_x}")
            
            # Place the image
            if end_y > start_y and end_x > start_x:
                padded[start_y:end_y, start_x:end_x] = small_image[src_start_y:src_end_y, src_start_x:src_end_x]
                print(f"Successfully placed image at position ({start_y}:{end_y}, {start_x}:{end_x})")
            else:
                print("Warning: Invalid placement bounds - image not placed")
        
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
