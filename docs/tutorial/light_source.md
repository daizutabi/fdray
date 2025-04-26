# Light Source

![](scene/light_source.ipynb){#. exec="1"}

[`LightSource`][fdray.LightSource] class is used to configure the light
source settings for the rendering.

## Example

Here's a complete example of a scene with a light source:

![Light source example](){#light-source-example source="1"}

## Basic Usage

The `LightSource` class creates a light source in the 3D scene that provides
illumination for rendered objects. A basic light source can be created with just
a position and an optional color:

```python
from fdray import LightSource, Color

# Basic white light at absolute position (1, 2, 3)
light1 = LightSource((1, 2, 3), "white", from_camera=False)

# Colored light using RGB values
light2 = LightSource((1, 2, 3), (0.8, 0.6, 0.3), from_camera=False)

# Using Color object
light3 = LightSource((1, 2, 3), Color("blue"), from_camera=False)
```

## Parameters

The `LightSource` class accepts the following parameters:

- `location`: Position of the light source. This can be:

    - A tuple of coordinates `(x, y, z)` for absolute positioning
    - A scalar value or tuple for camera-relative positioning (see below)
    - A string for direct POV-Ray expressions

- `color`: Color of the light. Can be specified as:

    - A string with a color name ("white", "red", etc.)
    - An RGB tuple with values between 0 and 1
    - A `Color` object

- `from_camera`: Boolean that determines if the light is positioned relative
  to the camera:

    - `True` (default): The light position is calculated relative to the camera
    - `False`: The coordinates are used as absolute position

- `shadowless`: Boolean that determines if the light casts shadows:

    - `True`: The light does not cast shadows
    - `False` (default): The light casts shadows

- `fade_distance`: Distance at which the light begins to fade (optional)

- `fade_power`: Rate at which the light intensity decreases with distance (optional)

## Camera-Relative Positioning

One of the most powerful features of the `LightSource` class is camera-relative
positioning, which allows you to place lights relative to the camera's position
and orientation.

### Using a Scalar Value

When `from_camera=True` and `location` is a single number, the light is placed
at a position calculated using `camera.orbital_location(location)`:

```python
# Light at the camera position (like a headlamp)
light = LightSource(0, "white")

# Light positioned forward from the camera (between camera and look_at point)
light = LightSource(0.5, "white")  # Halfway to the look_at point
```

### Using Tuple for Orbital Positioning

For more control, you can provide a tuple of (forward, angle, rotation) to
precisely position the light relative to the camera:

```python
# Light positioned above and to the left of the camera
light = LightSource((0.5, 30, -45), "white")

# Parameters:
# - 0.5: Half the distance from camera to look_at
# - 30: Tilted up 30 degrees from viewing direction
# - -45: Rotated 45 degrees clockwise from the up direction
```

This uses the camera's `orbital_location` method which calculates positions
based on:

1. Forward distance along viewing direction
2. Upward angle from viewing direction
3. Rotation around viewing direction

## Important Notes

When using camera-relative positioning (`from_camera=True`), you cannot directly
convert a light source to a string. Instead, you need to use `Scene.to_str()` or
`LightSource.to_str(camera)` to properly calculate the absolute position:

```python
camera = Camera(30, 40)
light = LightSource(0, "white")

# This will raise an error
# str(light)

# Use this instead:
light.to_str(camera)  # Returns the POV-Ray string with calculated position
```
