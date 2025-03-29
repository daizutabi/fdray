from __future__ import annotations

from typing import Any, List, Optional, Tuple, Union

import numpy as np

from fdray.core.color import Color
from fdray.core.texture import Finish, Normal, NormalMap, Pigment, Texture, TextureMap


def solid_texture(color: Color | tuple[float, float, float] | str) -> Texture:
    """Create a solid color texture.

    Args:
        color: Color object, RGB tuple (range 0-1), or color name

    Returns:
        Texture: Solid color texture
    """
    if not isinstance(color, Color):
        color = Color(color)

    return Texture(Pigment(color=color))


def checker_texture(
    color1: Color | tuple[float, float, float] | str,
    color2: Color | tuple[float, float, float] | str,
    scale: float = 1.0,
) -> Texture:
    """Create a checker pattern texture.

    Args:
        color1: First color
        color2: Second color
        scale: Pattern scale (default: 1.0)

    Returns:
        Texture: Checker pattern texture
    """
    if not isinstance(color1, Color):
        color1 = Color(color1)
    if not isinstance(color2, Color):
        color2 = Color(color2)

    # Define checker pattern
    checker = f"checker {color1} {color2}"

    # Apply scale
    if scale != 1.0:
        return Texture(Pigment(pattern=checker, scale=scale))

    return Texture(Pigment(pattern=checker))


def gradient_texture(
    color1: Color | tuple[float, float, float] | str,
    color2: Color | tuple[float, float, float] | str,
    direction: str = "x",
    scale: float = 1.0,
) -> Texture:
    """Create a gradient texture.

    Args:
        color1: Start color
        color2: End color
        direction: Gradient direction ('x', 'y', 'z')
        scale: Pattern scale (default: 1.0)

    Returns:
        Texture: Gradient texture
    """
    if not isinstance(color1, Color):
        color1 = Color(color1)
    if not isinstance(color2, Color):
        color2 = Color(color2)

    # Validate direction
    if direction not in ["x", "y", "z"]:
        raise ValueError("direction must be one of 'x', 'y', or 'z'")

    # Define gradient pattern
    gradient = f"gradient {direction} color_map {{ [{0} {color1}] [{1} {color2}] }}"

    # Apply scale
    if scale != 1.0:
        return Texture(Pigment(pattern=gradient, scale=scale))

    return Texture(Pigment(pattern=gradient))


def marble_texture(
    color1: Color | tuple[float, float, float] | str,
    color2: Color | tuple[float, float, float] | str,
    turbulence: float = 0.5,
    scale: float = 1.0,
) -> Texture:
    """Create a marble texture.

    Args:
        color1: Primary color
        color2: Secondary color
        turbulence: Turbulence strength (default: 0.5)
        scale: Pattern scale (default: 1.0)

    Returns:
        Texture: Marble texture
    """
    if not isinstance(color1, Color):
        color1 = Color(color1)
    if not isinstance(color2, Color):
        color2 = Color(color2)

    # Define marble pattern
    marble = f"marble color_map {{ [{0} {color1}] [{1} {color2}] }}"

    # Apply scale and turbulence
    return Texture(Pigment(pattern=marble, turbulence=turbulence, scale=scale))


def wood_texture(
    color1: Color | tuple[float, float, float] | str,
    color2: Color | tuple[float, float, float] | str,
    turbulence: float = 0.1,
    scale: float = 1.0,
) -> Texture:
    """Create a wood texture.

    Args:
        color1: Primary color
        color2: Secondary color
        turbulence: Turbulence strength (default: 0.1)
        scale: Pattern scale (default: 1.0)

    Returns:
        Texture: Wood texture
    """
    if not isinstance(color1, Color):
        color1 = Color(color1)
    if not isinstance(color2, Color):
        color2 = Color(color2)

    # Define wood pattern
    wood = f"wood color_map {{ [{0} {color1}] [{1} {color2}] }}"

    # Apply scale and turbulence
    return Texture(Pigment(pattern=wood, turbulence=turbulence, scale=scale))


def glossy_texture(
    color: Color | tuple[float, float, float] | str,
    reflection: float = 0.3,
    specular: float = 0.6,
    roughness: float = 0.01,
) -> Texture:
    """Create a glossy texture.

    Args:
        color: Base color
        reflection: Reflection coefficient (default: 0.3)
        specular: Specular reflection strength (default: 0.6)
        roughness: Surface roughness (default: 0.01)

    Returns:
        Texture: Glossy texture
    """
    if not isinstance(color, Color):
        color = Color(color)

    return Texture(
        Pigment(color=color),
        Finish(reflection=reflection, specular=specular, roughness=roughness),
    )


def matte_texture(
    color: Color | tuple[float, float, float] | str,
    diffuse: float = 0.9,
) -> Texture:
    """Create a matte texture.

    Args:
        color: Base color
        diffuse: Diffuse reflection strength (default: 0.9)

    Returns:
        Texture: Matte texture
    """
    if not isinstance(color, Color):
        color = Color(color)

    return Texture(
        Pigment(color=color),
        Finish(diffuse=diffuse, specular=0.0),
    )


def metallic_texture(
    color: Color | tuple[float, float, float] | str,
    reflection: float = 0.8,
    metallic: float = 1.0,
    specular: float = 0.7,
) -> Texture:
    """Create a metallic texture.

    Args:
        color: Base color
        reflection: Reflection coefficient (default: 0.8)
        metallic: Metallic quality (default: 1.0)
        specular: Specular reflection strength (default: 0.7)

    Returns:
        Texture: Metallic texture
    """
    if not isinstance(color, Color):
        color = Color(color)

    return Texture(
        Pigment(color=color),
        Finish(reflection=reflection, metallic=metallic, specular=specular),
    )


def bumpy_texture(
    color: Color | tuple[float, float, float] | str,
    bump_strength: float = 0.5,
    scale: float = 1.0,
) -> Texture:
    """Create a bumpy texture.

    Args:
        color: Base color
        bump_strength: Bump strength (default: 0.5)
        scale: Pattern scale (default: 1.0)

    Returns:
        Texture: Bumpy texture
    """
    if not isinstance(color, Color):
        color = Color(color)

    # Define bumpy normal map
    bumps = f"bumps {bump_strength}"

    return Texture(
        Pigment(color=color),
        Normal(pattern=bumps, scale=scale),
    )


def data_texture(
    data: np.ndarray,
    colormap: str = "viridis",
    min_value: float | None = None,
    max_value: float | None = None,
    scale: float = 1.0,
) -> Texture:
    """Generate a texture dynamically from a dataset.

    Args:
        data: 2D numpy array (image data or height map)
        colormap: Name of the colormap to use (default: "viridis")
        min_value: Minimum data value (automatically calculated if None)
        max_value: Maximum data value (automatically calculated if None)
        scale: Texture scale (default: 1.0)

    Returns:
        Texture: Data-driven texture
    """
    from fdray.data.color import get_colormap

    # Normalize data
    if min_value is None:
        min_value = float(np.min(data))
    if max_value is None:
        max_value = float(np.max(data))

    if min_value == max_value:
        normalized_data = np.zeros_like(data)
    else:
        normalized_data = (data - min_value) / (max_value - min_value)

    # Get colormap
    colors = get_colormap(colormap, num_colors=256)

    # Convert 2D to 1D (for texture map)
    height, width = normalized_data.shape
    texture_entries = []

    for y in range(height):
        for x in range(width):
            # Normalized positions
            norm_x = x / (width - 1)
            norm_y = y / (height - 1)

            # Get color index from data value
            value = normalized_data[y, x]
            color_idx = min(int(value * 255), 255)
            color = colors[color_idx]

            # Add entry to texture map
            texture_entries.append(((norm_x, norm_y, 0), Texture(Pigment(color=color))))

    # Create texture map
    texture_map = TextureMap(*texture_entries)

    # Apply scale
    if scale != 1.0:
        return Texture(texture_map).scale(scale)

    return Texture(texture_map)


def height_texture(
    height_map: np.ndarray,
    base_color: Color | tuple[float, float, float] | str = "gray",
    min_height: float | None = None,
    max_height: float | None = None,
    bump_strength: float = 0.5,
    scale: float = 1.0,
) -> Texture:
    """Generate a texture from a height map.

    Args:
        height_map: 2D numpy array (height map)
        base_color: Base color (default: "gray")
        min_height: Minimum height (automatically calculated if None)
        max_height: Maximum height (automatically calculated if None)
        bump_strength: Bump strength (default: 0.5)
        scale: Texture scale (default: 1.0)

    Returns:
        Texture: Height map-based texture
    """
    if not isinstance(base_color, Color):
        base_color = Color(base_color)

    # Normalize heights
    if min_height is None:
        min_height = float(np.min(height_map))
    if max_height is None:
        max_height = float(np.max(height_map))

    if min_height == max_height:
        normalized_heights = np.zeros_like(height_map)
    else:
        normalized_heights = (height_map - min_height) / (max_height - min_height)

    # Convert to bump map
    height, width = normalized_heights.shape
    bump_entries = []

    for y in range(height):
        for x in range(width):
            # Normalized positions
            norm_x = x / (width - 1)
            norm_y = y / (height - 1)

            # Height value
            h_value = normalized_heights[y, x]
            local_bump = bump_strength * h_value

            # Add entry to bump map
            bump_pattern = f"bumps {local_bump}"
            bump_entries.append(((norm_x, norm_y, 0), Normal(pattern=bump_pattern)))

    # Create normal map
    normal_map = NormalMap(*bump_entries)

    # Create texture
    return Texture(
        Pigment(color=base_color),
        normal_map,
        scale=scale,
    )


def gradient_from_data(
    data: np.ndarray,
    low_color: Color | tuple[float, float, float] | str = "blue",
    high_color: Color | tuple[float, float, float] | str = "red",
    min_value: float | None = None,
    max_value: float | None = None,
    direction: str = "y",
    scale: float = 1.0,
) -> Texture:
    """Generate a gradient texture based on data.

    Args:
        data: 1D numpy array (data values)
        low_color: Color for minimum values (default: "blue")
        high_color: Color for maximum values (default: "red")
        min_value: Minimum data value (automatically calculated if None)
        max_value: Maximum data value (automatically calculated if None)
        direction: Gradient direction ('x', 'y', 'z') (default: "y")
        scale: Texture scale (default: 1.0)

    Returns:
        Texture: Data-driven gradient texture
    """
    if not isinstance(low_color, Color):
        low_color = Color(low_color)
    if not isinstance(high_color, Color):
        high_color = Color(high_color)

    # データの正規化
    if min_value is None:
        min_value = float(np.min(data))
    if max_value is None:
        max_value = float(np.max(data))

    if min_value == max_value:
        normalized_data = np.zeros_like(data)
    else:
        normalized_data = (data - min_value) / (max_value - min_value)

    # 方向の検証
    if direction not in ["x", "y", "z"]:
        raise ValueError("direction must be one of 'x', 'y', or 'z'")

    # 色の割合を計算
    color_positions = []
    n = len(normalized_data)

    for i, value in enumerate(normalized_data):
        pos = i / (n - 1) if n > 1 else 0
        r = low_color.red + (high_color.red - low_color.red) * value
        g = low_color.green + (high_color.green - low_color.green) * value
        b = low_color.blue + (high_color.blue - low_color.blue) * value
        color = Color((r, g, b))
        color_positions.append((pos, color))

    # グラデーションパターンの定義
    color_map_str = " ".join(f"[{pos} {color}]" for pos, color in color_positions)
    gradient = f"gradient {direction} color_map {{ {color_map_str} }}"

    # スケールの適用
    if scale != 1.0:
        return Texture(Pigment(pattern=gradient, scale=scale))

    return Texture(Pigment(pattern=gradient))


def image_texture(
    image_data: np.ndarray,
    scale: float = 1.0,
    alpha: np.ndarray | None = None,
) -> Texture:
    """Generate a texture from image data.

    Args:
        image_data: 3D numpy array (RGB image data with shape [height, width, 3])
        scale: Texture scale (default: 1.0)
        alpha: Alpha transparency data (optional, 2D numpy array)

    Returns:
        Texture: Image-based texture
    """
    # Validate image data
    if image_data.ndim != 3 or image_data.shape[2] != 3:
        raise ValueError("image_data must be a 3D array with shape [height, width, 3]")

    # Normalize image data (to 0-1 range)
    if image_data.max() > 1.0:
        image_data = image_data / 255.0

    height, width, _ = image_data.shape
    texture_entries = []

    for y in range(height):
        for x in range(width):
            # Normalized positions
            norm_x = x / (width - 1)
            norm_y = y / (height - 1)

            # RGB values
            r, g, b = image_data[y, x]
            color = Color((r, g, b))

            # Transparency
            if alpha is not None:
                a = alpha[y, x]
                pigment = Pigment(color=color, filter=a)
            else:
                pigment = Pigment(color=color)

            # Add entry to texture map
            texture_entries.append(((norm_x, norm_y, 0), Texture(pigment)))

    # Create texture map
    texture_map = TextureMap(*texture_entries)

    # Apply scale
    if scale != 1.0:
        return Texture(texture_map).scale(scale)

    return Texture(texture_map)


def heatmap_texture(
    data: np.ndarray,
    colormap: str = "inferno",
    min_value: float | None = None,
    max_value: float | None = None,
    scale: float = 1.0,
    emissive: bool = True,
) -> Texture:
    """Generate a heatmap texture from a dataset.

    Args:
        data: 2D numpy array (heatmap data)
        colormap: Name of the colormap to use (default: "inferno")
        min_value: Minimum data value (automatically calculated if None)
        max_value: Maximum data value (automatically calculated if None)
        scale: Texture scale (default: 1.0)
        emissive: Whether to add emission effect (default: True)

    Returns:
        Texture: Heatmap texture
    """
    from fdray.data.color import get_colormap

    # Normalize data
    if min_value is None:
        min_value = float(np.min(data))
    if max_value is None:
        max_value = float(np.max(data))

    if min_value == max_value:
        normalized_data = np.zeros_like(data)
    else:
        normalized_data = (data - min_value) / (max_value - min_value)

    # Get colormap
    colors = get_colormap(colormap, num_colors=256)

    # Convert 2D to 1D (for texture map)
    height, width = normalized_data.shape
    texture_entries = []

    for y in range(height):
        for x in range(width):
            # Normalized positions
            norm_x = x / (width - 1)
            norm_y = y / (height - 1)

            # Get color index from data value
            value = normalized_data[y, x]
            color_idx = min(int(value * 255), 255)
            color = colors[color_idx]

            # Emission effect
            if emissive:
                # Emission intensity proportional to value
                emission = value
                finish = Finish(emission=emission)
                texture_entries.append(
                    ((norm_x, norm_y, 0), Texture(Pigment(color=color), finish)),
                )
            else:
                texture_entries.append(
                    ((norm_x, norm_y, 0), Texture(Pigment(color=color))),
                )

    # Create texture map
    texture_map = TextureMap(*texture_entries)

    # Apply scale
    if scale != 1.0:
        return Texture(texture_map).scale(scale)

    return Texture(texture_map)
