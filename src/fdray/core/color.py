"""Color definitions and utilities for ray tracing.

This module provides classes and functions for creating and manipulating
colors in POV-Ray scenes. It supports:

1. Named colors (e.g., "red", "blue") and hex color codes (including #RRGGBBAA format)
2. RGB and RGBA color specifications with optional filter and transmit properties
3. Alpha transparency conversion to POV-Ray's transmit property
4. String serialization to POV-Ray SDL format

The module offers a rich set of predefined color names compatible with
common web color standards.
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from fdray.data.color import colorize_direction

from .base import Map

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from typing import Self

    from fdray.typing import RGB, ColorLike


class Color:
    """A color representation with support for POV-Ray color properties.

    This class handles various color formats and provides conversion to
    POV-Ray SDL syntax. Colors can be specified by name, hex code
    (including #RRGGBBAA format), RGB or RGBA tuple, or by copying another
    Color object. Optional properties include alpha transparency, filter,
    and transmit values.

    Args:
        color: Color specification. Can be:
            - A Color object
            - String name (e.g., "red")
            - Hex code (e.g., "#00FF00" or "#00FF00FF" with alpha)
            - RGB tuple (e.g., (1.0, 0.0, 0.0))
            - RGBA tuple (e.g., (1.0, 0.0, 0.0, 0.5))
        alpha: Alpha transparency (0.0 = fully transparent, 1.0 = fully opaque).
            If provided, converts to transmit value (transmit = 1 - alpha).
            Takes precedence over alpha in RGBA tuple or hex code.
        filter: Filter property for POV-Ray (how much color filters through).
            Only used when specified as a keyword argument.
        transmit: Transmit property for POV-Ray (how much light passes through).
            Only used when specified as a keyword argument.
        include_color: Whether to include the "color" keyword in string output.
            Defaults to True.

    Note:
        Alpha can be specified in multiple ways, with the following precedence:
        1. Explicit `alpha` parameter
        2. Alpha component in an RGBA tuple
        3. Alpha component in a hex color code (#RRGGBBAA)

    Attributes:
        red (float): Red component (0.0 to 1.0)
        green (float): Green component (0.0 to 1.0)
        blue (float): Blue component (0.0 to 1.0)
        name (str | None): Color name if created from a named color
        filter (float | None): Filter property (how much color filters through)
        transmit (float | None): Transmit property (how much light passes through)
        include_color (bool): Whether to include "color" keyword in output

    Examples:
        ```python
        Color("red")
        Color((1.0, 0.0, 0.0))
        Color((1.0, 0.0, 0.0, 0.5))  # RGBA with alpha=0.5
        Color("blue", alpha=0.5)
        Color("#00FF00", filter=0.3)
        Color("#00FF00FF")  # Hex color with alpha
        Color(existing_color, transmit=0.7)
        ```
    """

    red: float
    green: float
    blue: float
    name: str | None
    filter: float | None
    transmit: float | None

    def __init__(
        self,
        color: ColorLike,
        alpha: float | None = None,
        *,
        filter: float | None = None,
        transmit: float | None = None,
    ) -> None:
        if isinstance(color, Color):
            self.name = color.name
            self.red, self.green, self.blue = color.red, color.green, color.blue
            filter = filter or color.filter  # noqa: A001
            transmit = transmit or color.transmit

        elif isinstance(color, str):
            if color.startswith("#") and len(color) == 9:
                alpha = int(color[7:9], 16) / 255
                color = color[:7]

            color = rgb(color)

            if isinstance(color, str):
                self.name = color
                self.red, self.green, self.blue = 0, 0, 0
            else:
                self.name = None
                self.red, self.green, self.blue = color

        else:
            self.name = None
            if len(color) == 3:
                self.red, self.green, self.blue = color
            elif len(color) == 4:
                self.red, self.green, self.blue, alpha = color

        if alpha is not None:
            transmit = 1 - alpha

        self.filter = filter
        self.transmit = transmit

    def __iter__(self) -> Iterator[str]:
        if self.name is not None:
            yield self.name
            if self.filter is not None:
                yield f"filter {self.filter:.3g}"
            if self.transmit is not None:
                yield f"transmit {self.transmit:.3g}"
            return

        rgb = f"{self.red:.3g}, {self.green:.3g}, {self.blue:.3g}"
        if self.filter is not None and self.transmit is not None:
            yield f"rgbft <{rgb}, {self.filter:.3g}, {self.transmit:.3g}>"
        elif self.filter is not None:
            yield f"rgbf <{rgb}, {self.filter:.3g}>"
        elif self.transmit is not None:
            yield f"rgbt <{rgb}, {self.transmit:.3g}>"
        else:
            yield f"rgb <{rgb}>"

    def __str__(self) -> str:
        return " ".join(self)

    @classmethod
    def from_direction(cls, direction: Sequence[float], axis: int = 2) -> Self:
        """Create a color from a direction vector.

        Args:
            direction (Sequence[float]): The direction vector to colorize.
            axis (int): The axis to colorize.

        Returns:
            Color: The color corresponding to the direction vector.
        """
        return cls(colorize_direction(direction, axis))


class Background(Color):
    def __str__(self) -> str:
        return f"background {{ {super().__str__()} }}"


class ColorMap(Map):
    cls = Color


def rgb(color: str) -> RGB | str:
    """Return the RGB color as a tuple of floats.

    Converts a color name or hex code to an RGB tuple with values
    ranging from 0.0 to 1.0. If the input is a hex code with alpha
    (#RRGGBBAA), the alpha component is ignored for this function.
    If the input is not recognized as a valid color name or hex code,
    returns the input string unchanged.

    Args:
        color: The color name (e.g., "red") or hex code
            (e.g., "#00FF00" or "#00FF00FF")

    Returns:
        A tuple of three floats (red, green, blue) or the original string
        if not recognized as a valid color.

    Examples:
        >>> rgb("red")
        (1.0, 0.0, 0.0)

        >>> rgb("#00FF00")
        (0.0, 1.0, 0.0)

        >>> rgb("#00FF00FF")  # Alpha component is ignored
        (0.0, 1.0, 0.0)
    """
    if color.islower():
        color = getattr(ColorName, color.upper(), color)

    if not isinstance(color, str) or not color.startswith("#") or len(color) < 7:
        return color

    r, g, b = color[1:3], color[3:5], color[5:7]
    return int(r, 16) / 255, int(g, 16) / 255, int(b, 16) / 255


class ColorName(StrEnum):
    """Color name enumeration with hex values."""

    ALICEBLUE = "#F0F8FF"
    ANTIQUEWHITE = "#FAEBD7"
    AQUA = "#00FFFF"
    AQUAMARINE = "#7FFFD4"
    AZURE = "#F0FFFF"
    BEIGE = "#F5F5DC"
    BISQUE = "#FFEBCD"
    BLACK = "#000000"
    BLANCHEDALMOND = "#FFEBCD"
    BLUE = "#0000FF"
    BLUEVIOLET = "#8A2BE2"
    BROWN = "#A52A2A"
    BURLYWOOD = "#DEB887"
    CADETBLUE = "#5F9EA0"
    CHARTREUSE = "#7FFF00"
    CHOCOLATE = "#D2691E"
    CORAL = "#FF7F50"
    CORNFLOWERBLUE = "#6495ED"
    CORNSILK = "#FFF8DC"
    CRIMSON = "#DC143C"
    CYAN = "#00FFFF"
    DARKBLUE = "#00008B"
    DARKCYAN = "#008B8B"
    DARKGOLDENROD = "#B8860B"
    DARKGRAY = "#A9A9A9"
    DARKGREEN = "#006400"
    DARKGREY = "#A9A9A9"
    DARKKHAKI = "#BDB76B"
    DARKMAGENTA = "#8B008B"
    DARKOLIVEGREEN = "#556B2F"
    DARKORANGE = "#FF8C00"
    DARKORCHID = "#9932CC"
    DARKRED = "#8B0000"
    DARKSALMON = "#E9967A"
    DARKSEAGREEN = "#8FBC8F"
    DARKSLATEBLUE = "#483D8B"
    DARKSLATEGRAY = "#2F4F4F"
    DARKSLATEGREY = "#2F4F4F"
    DARKTURQUOISE = "#00CED1"
    DARKVIOLET = "#9400D3"
    DEEPPINK = "#FF1493"
    DEEPSKYBLUE = "#00BFFF"
    DIMGRAY = "#696969"
    DIMGREY = "#696969"
    DODGERBLUE = "#1E90FF"
    FIREBRICK = "#B22222"
    FLORALWHITE = "#FFFAF0"
    FORESTGREEN = "#228B22"
    FUCHSIA = "#FF00FF"
    GAINSBORO = "#DCDCDC"
    GHOSTWHITE = "#F8F8FF"
    GOLD = "#FFD700"
    GOLDENROD = "#DAA520"
    GRAY = "#808080"
    GREEN = "#008000"
    GREENYELLOW = "#ADFF2F"
    GREY = "#808080"
    HONEYDEW = "#F0FFF0"
    HOTPINK = "#FF69B4"
    INDIANRED = "#CD5C5C"
    INDIGO = "#4B0082"
    IVORY = "#FFFFF0"
    KHAKI = "#F0E68C"
    LAVENDER = "#E6E6FA"
    LAVENDERBLUSH = "#FFF0F5"
    LAWNGREEN = "#7CFC00"
    LEMONCHIFFON = "#FFFACD"
    LIGHTBLUE = "#ADD8E6"
    LIGHTCORAL = "#F08080"
    LIGHTCYAN = "#E0FFFF"
    LIGHTGOLDENRODYELLOW = "#FAFAD2"
    LIGHTGRAY = "#D3D3D3"
    LIGHTGREEN = "#90EE90"
    LIGHTGREY = "#D3D3D3"
    LIGHTPINK = "#FFB6C1"
    LIGHTSALMON = "#FFA07A"
    LIGHTSEAGREEN = "#20B2AA"
    LIGHTSKYBLUE = "#87CEFA"
    LIGHTSLATEGRAY = "#778899"
    LIGHTSLATEGREY = "#778899"
    LIGHTSTEELBLUE = "#B0C4DE"
    LIGHTYELLOW = "#FFFFE0"
    LIME = "#00FF00"
    LIMEGREEN = "#32CD32"
    LINEN = "#FAF0E6"
    MAGENTA = "#FF00FF"
    MAROON = "#800000"
    MEDIUMAQUAMARINE = "#66CDAA"
    MEDIUMBLUE = "#0000CD"
    MEDIUMORCHID = "#BA55D3"
    MEDIUMPURPLE = "#9370DB"
    MEDIUMSEAGREEN = "#3CB371"
    MEDIUMSLATEBLUE = "#7B68EE"
    MEDIUMSPRINGGREEN = "#00FA9A"
    MEDIUMTURQUOISE = "#48D1CC"
    MEDIUMVIOLETRED = "#C71585"
    MIDNIGHTBLUE = "#191970"
    MINTCREAM = "#F5FFFA"
    MISTYROSE = "#FFE4E1"
    MOCCASIN = "#FFE4B5"
    NAVAJOWHITE = "#FFDEAD"
    NAVY = "#000080"
    OLDLACE = "#FDF5E6"
    OLIVE = "#808000"
    OLIVEDRAB = "#6B8E23"
    ORANGE = "#FFA500"
    ORANGERED = "#FF4500"
    ORCHID = "#DA70D6"
    PALEGOLDENROD = "#EEE8AA"
    PALEGREEN = "#98FB98"
    PALETURQUOISE = "#AFEEEE"
    PALEVIOLETRED = "#DB7093"
    PAPAYAWHIP = "#FFEFD5"
    PEACHPUFF = "#FFDAB9"
    PERU = "#CD853F"
    PINK = "#FFC0CB"
    PLUM = "#DDA0DD"
    POWDERBLUE = "#B0E0E6"
    PURPLE = "#800080"
    REBECCAPURPLE = "#663399"
    RED = "#FF0000"
    ROSYBROWN = "#BC8F8F"
    ROYALBLUE = "#4169E1"
    SADDLEBROWN = "#8B4513"
    SALMON = "#FA8072"
    SANDYBROWN = "#F4A460"
    SEAGREEN = "#2E8B57"
    SEASHELL = "#FFF5EE"
    SIENNA = "#A0522D"
    SILVER = "#C0C0C0"
    SKYBLUE = "#87CEEB"
    SLATEBLUE = "#6A5ACD"
    SLATEGRAY = "#708090"
    SLATEGREY = "#708090"
    SNOW = "#FFFAFA"
    SPRINGGREEN = "#00FF7F"
    STEELBLUE = "#4682B4"
    TAN = "#D2B48C"
    TEAL = "#008080"
    THISTLE = "#D8BFD8"
    TOMATO = "#FF6347"
    TURQUOISE = "#40E0D0"
    VIOLET = "#EE82EE"
    WHEAT = "#F5DEB3"
    WHITE = "#FFFFFF"
    WHITESMOKE = "#F5F5F5"
    YELLOW = "#FFFF00"
    YELLOWGREEN = "#9ACD32"


COLOR_PALETTE = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]
