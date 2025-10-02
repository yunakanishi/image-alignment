# image-alignment

[![License MIT](https://img.shields.io/pypi/l/image-alignment.svg?color=green)](https://github.com/yunakanishi/image-alignment/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/image-alignment.svg?color=green)](https://pypi.org/project/image-alignment)
[![Python Version](https://img.shields.io/pypi/pyversions/image-alignment.svg?color=green)](https://python.org)
[![tests](https://github.com/yunakanishi/image-alignment/workflows/tests/badge.svg)](https://github.com/yunakanishi/image-alignment/actions)
[![codecov](https://codecov.io/gh/yunakanishi/image-alignment/branch/main/graph/badge.svg)](https://codecov.io/gh/yunakanishi/image-alignment)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/image-alignment)](https://napari-hub.org/plugins/image-alignment)
[![npe2](https://img.shields.io/badge/plugin-npe2-blue?link=https://napari.org/stable/plugins/index.html)](https://napari.org/stable/plugins/index.html)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)

Interactive image alignment with automatic padding for napari

## Features

- **Interactive Image Alignment**: Visually position a small image over a large base image using napari's interactive tools
- **Automatic Padding**: Automatically pad the small image with zeros to match the base image's dimensions based on the chosen position
- **Support for 2D and 3D images**: Works with both 2D and 3D image data
- **Real-time preview**: See the positioning in real-time with a semi-transparent overlay

----------------------------------

This [napari] plugin was generated with [copier] using the [napari-plugin-template] (None).

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/napari-plugin-template#getting-started

and review the napari docs for plugin developers:
https://napari.org/stable/plugins/index.html
-->

## Installation

You can install `image-alignment` via [pip]:

```
pip install image-alignment
```

If napari is not already installed, you can install `image-alignment` with napari and Qt via:

```
pip install "image-alignment[all]"
```


To install latest development version :

```
pip install git+https://github.com/yunakanishi/image-alignment.git
```

## Usage

### Interactive Image Alignment

1. **Load your images**: Open napari and load both your large base image and small image that you want to align.

2. **Open the alignment widget**: Go to `Plugins > image-alignment > Interactive Image Alignment`

3. **Select images**: 
   - Choose your large base image from the "Base Image (Large)" dropdown
   - Choose your small image from the "Small Image" dropdown

4. **Start alignment**: Click "Start Interactive Alignment" to begin the positioning process

5. **Position the image**: 
   - A semi-transparent red overlay of your small image will appear
   - Use napari's pan/translate tools to drag this overlay to your desired position
   - The overlay represents where your small image will be placed on the base image

6. **Apply padding**: Once you're satisfied with the position, click "Apply Padding"
   - A new layer will be created with your small image padded to match the base image size
   - The small image will be positioned exactly where you placed the overlay

### Example Use Case

```python
import napari
import numpy as np
from image_alignment import InteractiveImageAlignment

# Create sample images
large_image = np.random.rand(4000, 3000)  # Large base image
small_image = np.random.rand(1000, 2000)  # Small image to align

# Start napari
viewer = napari.Viewer()
viewer.add_image(large_image, name="Base")
viewer.add_image(small_image, name="Small")

# Add alignment widget
alignment_widget = InteractiveImageAlignment(viewer)
viewer.window.add_dock_widget(alignment_widget, name="Alignment")

napari.run()
```

### Running the Demo

A demo script is included to test the functionality:

```bash
python demo_alignment.py
```



## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"image-alignment" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[copier]: https://copier.readthedocs.io/en/stable/
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[napari-plugin-template]: https://github.com/napari/napari-plugin-template

[file an issue]: https://github.com/yunakanishi/image-alignment/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
