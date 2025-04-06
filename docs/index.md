# fdray

fdray is a Python library that provides a clean interface to POV-Ray,
making it easy to create and render 3D scenes programmatically.

## Features

- **Simple Scene Description**: Express 3D scenes in clean, readable
  Python code
- **Pythonic API**: Natural integration with Python's ecosystem
- **POV-Ray Integration**: Seamless integration with a high-quality
  rendering engine
- **Jupyter Support**: Interactive scene development in Jupyter
  notebooks

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- POV-Ray team for their excellent ray tracing engine
- The Python community for inspiration and support
