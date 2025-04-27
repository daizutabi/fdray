# Camera

![](scene/camera.ipynb){#. exec="1"}

[`Camera`][fdray.Camera] class is used to configure the camera settings
for the rendering.

## Positioning

We use a right-handed spherical coordinate system for camera
positioning.

![alt](){#positioning source="tabbed-right"}

In the above figure, the camera is positioned at:

- Longitude: 30 degrees
- Latitude: 40 degrees

The camera position is determined through a two-step transformation:

1. First, rotate 30 degrees counterclockwise from the x-axis toward
   the y-axis in the x-y plane
2. Then, elevate 40 degrees from that position toward the z-axis

This coordinate system allows for intuitive camera positioning:

- Longitude controls the horizontal rotation around the scene
- Latitude controls the vertical angle from the ground plane

### Implementation

The camera implementation is based on the following Qiita article:

- Title: Efficient Camera Settings in POV-Ray
- Author: @Hyrodium (Yuto Horikawa)
- URL: <https://qiita.com/Hyrodium/items/af91b1ddb8ea2c4359c2>
- Date: 2017-12-07

This implementation adopts the spherical coordinate system and uses
the calculation methods for direction, right, and up vectors as
proposed in the article. The sky parameter is also included as it's
essential for proper orientation.

## View scale

The `view_scale` parameter controls how much of the scene is visible
in the rendered image. It functions similarly to adjusting a camera's
field of view.

=== "Result"

    |       `view_scale = 1`       |       `view_scale = 2`       |       `view_scale = 3`       |
    |:----------------------------:|:----------------------------:|:----------------------------:|
    | ![](){`scene_view_scale(1)`} | ![](){`scene_view_scale(2)`} | ![](){`scene_view_scale(3)`} |

=== "Source"

    ![](){#view-scale}

### Basic Operation

- A larger view scale shows more of the scene by "zooming out"
- A smaller view scale shows less of the scene by "zooming in"

### Technical Implementation

- The coordinate range rendered extends from `-view_scale` to `+view_scale`
- Directly affects the apparent size of objects in the scene
- Controls the viewing frustum without changing camera position

### Parameter Relationships

- Independent of camera position and orientation (longitude, latitude)
- Works in conjunction with the camera's distance parameter

## Distance

The `distance` parameter controls the camera's perspective effect.
This parameter significantly affects how the 3D scene is rendered,
particularly the perspective distortion.

=== "Result"

    |       `distance = 3`       |       `distance = 10`       |       `distance = 30`       |
    |:--------------------------:|:--------------------------:|:--------------------------:|
    | ![](){`scene_distance(3)`} | ![](){`scene_distance(10)`} | ![](){`scene_distance(30)`} |

=== "Source"

    ![](){#distance}

### Visual Effects

#### When distance is small

- Creates a fisheye lens-like effect
- Produces strong perspective distortion
- Objects appear more curved at the edges
- Similar to viewing through a wide-angle lens

#### When distance is large

- Approaches orthogonal projection
- Reduces perspective distortion
- Creates a more natural depth perception
- Similar to viewing through a telephoto lens

### Technical Details

The `distance` parameter:

- Affects the perspective matrix calculation
- Does not change the actual size of objects, only their apparent
  perspective
- Represents the distance between the camera position (`camera_pos`) and
  the object's center (`center`)
- Smaller distances bring the camera closer to the object, creating
  stronger perspective effects
- Larger distances move the camera away from the object, resulting in a
  more orthogonal-like view

### Important Notes

- The `distance` parameter only affects perspective, not object size
- Smaller distances create more dramatic perspective effects
- Larger distances create more natural, less distorted views
- The effect is similar to changing the focal length of a camera lens

## Orbital Location

Calculate a position in orbit around the camera's location

Imagine tilting your head up (`angle`) and then rotating
counter-clockwise (`rotation`):

- First, move `forward` along viewing direction (0: at `camera.location`,
  1: at `camera.look_at`). Negative values move behind the camera.
- Then, tilt up from viewing direction by `angle` degrees
- Finally, rotate counter-clockwise from up by `rotation` degrees
  (0: up, 90: left, 180: down, 270: right)

![alt](){#orbital-location-source source="only"}

|     Rendered image from x axis     |       Top view (y-z plane)       |
|:----------------------------------:|:--------------------------------:|
| ![alt](){#orbital-location-source} | ![alt](){#orbital-location-plot} |

## Movies

### Camera

<video controls autoplay muted loop>
  <source src="../../assets/camera-longitude.mp4" type="video/mp4">
</video>
<video controls autoplay muted loop>
  <source src="../../assets/camera-latitude.mp4" type="video/mp4">
</video>

<video controls autoplay muted loop>
  <source src="../../assets/camera-view-scale.mp4" type="video/mp4">
</video>
<video controls autoplay muted loop>
  <source src="../../assets/camera-distance.mp4" type="video/mp4">
</video>

<video controls autoplay muted loop>
  <source src="../../assets/camera-tilt.mp4" type="video/mp4">
</video>
<video controls autoplay muted loop>
  <source src="../../assets/camera-look-at.mp4" type="video/mp4">
</video>

### Orbital Location

<video controls autoplay muted loop>
  <source src="../../assets/camera-orbital-forward.mp4" type="video/mp4">
</video>
<video controls autoplay muted loop>
  <source src="../../assets/camera-orbital-angle.mp4" type="video/mp4">
</video>
<video controls autoplay muted loop>
  <source src="../../assets/camera-orbital-rotation.mp4" type="video/mp4">
</video>
