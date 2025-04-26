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
        color: Color specification.
            Can be:

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
        >>> Color("red") # doctest: +SKIP
        >>> Color((1.0, 0.0, 0.0)) # doctest: +SKIP
        >>> Color((1.0, 0.0, 0.0, 0.5))  # RGBA with alpha=0.5 # doctest: +SKIP
        >>> Color("blue", alpha=0.5) # doctest: +SKIP
        >>> Color("#00FF00", filter=0.3) # doctest: +SKIP
        >>> Color("#00FF00FF")  # Hex color with alpha # doctest: +SKIP
        >>> Color(existing_color, transmit=0.7) # doctest: +SKIP
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
    color = cnames.get(color, color)

    if not isinstance(color, str) or not color.startswith("#") or len(color) < 7:
        return color

    r, g, b = color[1:3], color[3:5], color[5:7]
    return int(r, 16) / 255, int(g, 16) / 255, int(b, 16) / 255


cnames = {
    "aliceblue": "#F0F8FF",
    "antiquewhite": "#FAEBD7",
    "aqua": "#00FFFF",
    "aquamarine": "#7FFFD4",
    "azure": "#F0FFFF",
    "beige": "#F5F5DC",
    "bisque": "#FFE4C4",
    "black": "#000000",
    "blanchedalmond": "#FFEBCD",
    "blue": "#0000FF",
    "blueviolet": "#8A2BE2",
    "brown": "#A52A2A",
    "burlywood": "#DEB887",
    "cadetblue": "#5F9EA0",
    "chartreuse": "#7FFF00",
    "chocolate": "#D2691E",
    "coral": "#FF7F50",
    "cornflowerblue": "#6495ED",
    "cornsilk": "#FFF8DC",
    "crimson": "#DC143C",
    "cyan": "#00FFFF",
    "darkblue": "#00008B",
    "darkcyan": "#008B8B",
    "darkgoldenrod": "#B8860B",
    "darkgray": "#A9A9A9",
    "darkgreen": "#006400",
    "darkgrey": "#A9A9A9",
    "darkkhaki": "#BDB76B",
    "darkmagenta": "#8B008B",
    "darkolivegreen": "#556B2F",
    "darkorange": "#FF8C00",
    "darkorchid": "#9932CC",
    "darkred": "#8B0000",
    "darksalmon": "#E9967A",
    "darkseagreen": "#8FBC8F",
    "darkslateblue": "#483D8B",
    "darkslategray": "#2F4F4F",
    "darkslategrey": "#2F4F4F",
    "darkturquoise": "#00CED1",
    "darkviolet": "#9400D3",
    "deeppink": "#FF1493",
    "deepskyblue": "#00BFFF",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1E90FF",
    "firebrick": "#B22222",
    "floralwhite": "#FFFAF0",
    "forestgreen": "#228B22",
    "fuchsia": "#FF00FF",
    "gainsboro": "#DCDCDC",
    "ghostwhite": "#F8F8FF",
    "gold": "#FFD700",
    "goldenrod": "#DAA520",
    "gray": "#808080",
    "green": "#008000",
    "greenyellow": "#ADFF2F",
    "grey": "#808080",
    "honeydew": "#F0FFF0",
    "hotpink": "#FF69B4",
    "indianred": "#CD5C5C",
    "indigo": "#4B0082",
    "ivory": "#FFFFF0",
    "khaki": "#F0E68C",
    "lavender": "#E6E6FA",
    "lavenderblush": "#FFF0F5",
    "lawngreen": "#7CFC00",
    "lemonchiffon": "#FFFACD",
    "lightblue": "#ADD8E6",
    "lightcoral": "#F08080",
    "lightcyan": "#E0FFFF",
    "lightgoldenrodyellow": "#FAFAD2",
    "lightgray": "#D3D3D3",
    "lightgreen": "#90EE90",
    "lightgrey": "#D3D3D3",
    "lightpink": "#FFB6C1",
    "lightsalmon": "#FFA07A",
    "lightseagreen": "#20B2AA",
    "lightskyblue": "#87CEFA",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#B0C4DE",
    "lightyellow": "#FFFFE0",
    "lime": "#00FF00",
    "limegreen": "#32CD32",
    "linen": "#FAF0E6",
    "magenta": "#FF00FF",
    "maroon": "#800000",
    "mediumaquamarine": "#66CDAA",
    "mediumblue": "#0000CD",
    "mediumorchid": "#BA55D3",
    "mediumpurple": "#9370DB",
    "mediumseagreen": "#3CB371",
    "mediumslateblue": "#7B68EE",
    "mediumspringgreen": "#00FA9A",
    "mediumturquoise": "#48D1CC",
    "mediumvioletred": "#C71585",
    "midnightblue": "#191970",
    "mintcream": "#F5FFFA",
    "mistyrose": "#FFE4E1",
    "moccasin": "#FFE4B5",
    "navajowhite": "#FFDEAD",
    "navy": "#000080",
    "oldlace": "#FDF5E6",
    "olive": "#808000",
    "olivedrab": "#6B8E23",
    "orange": "#FFA500",
    "orangered": "#FF4500",
    "orchid": "#DA70D6",
    "palegoldenrod": "#EEE8AA",
    "palegreen": "#98FB98",
    "paleturquoise": "#AFEEEE",
    "palevioletred": "#DB7093",
    "papayawhip": "#FFEFD5",
    "peachpuff": "#FFDAB9",
    "peru": "#CD853F",
    "pink": "#FFC0CB",
    "plum": "#DDA0DD",
    "powderblue": "#B0E0E6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#FF0000",
    "rosybrown": "#BC8F8F",
    "royalblue": "#4169E1",
    "saddlebrown": "#8B4513",
    "salmon": "#FA8072",
    "sandybrown": "#F4A460",
    "seagreen": "#2E8B57",
    "seashell": "#FFF5EE",
    "sienna": "#A0522D",
    "silver": "#C0C0C0",
    "skyblue": "#87CEEB",
    "slateblue": "#6A5ACD",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#FFFAFA",
    "springgreen": "#00FF7F",
    "steelblue": "#4682B4",
    "tan": "#D2B48C",
    "teal": "#008080",
    "thistle": "#D8BFD8",
    "tomato": "#FF6347",
    "turquoise": "#40E0D0",
    "violet": "#EE82EE",
    "wheat": "#F5DEB3",
    "white": "#FFFFFF",
    "whitesmoke": "#F5F5F5",
    "yellow": "#FFFF00",
    "yellowgreen": "#9ACD32",
}

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
