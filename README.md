# fdray - Python Ray Tracing Interface for POV-Ray

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Python Version][python-v-image]][python-v-link]
[![Build Status][GHAction-image]][GHAction-link]
[![Coverage Status][codecov-image]][codecov-link]

fdray is a Python library that provides a clean interface to POV-Ray,
making it easy to create and render 3D scenes programmatically.

## Features

- **Simple Scene Description**: Express 3D scenes in clean, readable Python code
- **Pythonic API**: Natural integration with Python's ecosystem
- **POV-Ray Integration**: Seamless integration with a high-quality rendering engine
- **Jupyter Support**: Interactive scene development in Jupyter notebooks

## Installation

```bash
pip install fdray
```

Requires POV-Ray to be installed:

- **Linux**: `sudo apt-get install povray`
- **macOS**: `brew install povray`
- **Windows**: Download from [POV-Ray website](https://www.povray.org/download/)

## Quick Start

```python
from fdray import Camera, Color, LightSource, Scene, Sphere

# Create a simple scene
scene = Scene(
    Camera(longitude=20, latitude=30),
    LightSource(0, Color("white")),  # 0: at camera location
    Sphere((0, 0, 0), 1, Color("red")),
)

# Render the scene
scene.render(width=800, height=600)
```

## Documentation

For detailed documentation and examples, visit our
[documentation site](https://daizutabi.github.io/fdray/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- POV-Ray team for their excellent ray tracing engine
- The Python community for inspiration and support

<!-- Badges -->
[pypi-v-image]: https://img.shields.io/pypi/v/fdray.svg
[pypi-v-link]: https://pypi.org/project/fdray/
[python-v-image]: https://img.shields.io/pypi/pyversions/fdray.svg
[python-v-link]: https://pypi.org/project/fdray
[GHAction-image]: https://github.com/daizutabi/fdray/actions/workflows/ci.yaml/badge.svg?branch=main&event=push
[GHAction-link]: https://github.com/daizutabi/fdray/actions?query=event%3Apush+branch%3Amain
[codecov-image]: https://codecov.io/github/daizutabi/fdray/coverage.svg?branch=main
[codecov-link]: https://codecov.io/github/daizutabi/fdray?branch=main
