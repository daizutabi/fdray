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

from typing import TYPE_CHECKING, final

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

            if isinstance(color, Color):
                self.name = color.name
                self.red, self.green, self.blue = color.red, color.green, color.blue
            elif isinstance(color, str):
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
    cls: type = Color


def rgb(color: str) -> str | RGB | Color:
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
        str | tuple[float, float, float] | Color: A tuple of three floats
        (red, green, blue) or the original string if not recognized as a
        valid color.

    Examples:
        >>> color = rgb("red")
        >>> color.red
        1.0
        >>> color.green
        0.0
        >>> color.blue
        0.0

        >>> rgb("#00FF00")
        (0.0, 1.0, 0.0)

        >>> rgb("#00FF00FF")  # Alpha component is ignored
        (0.0, 1.0, 0.0)
    """
    if color.islower() and hasattr(ColorName, color.upper()):
        return getattr(ColorName, color.upper())

    if not isinstance(color, str) or not color.startswith("#") or len(color) < 7:  # pyright: ignore[reportUnnecessaryIsInstance]
        return color

    r, g, b = color[1:3], color[3:5], color[5:7]
    return int(r, 16) / 255, int(g, 16) / 255, int(b, 16) / 255


@final
class ColorName:
    """Color name enumeration with hex values."""

    ALICEBLUE = Color("#F0F8FF")
    ANTIQUEWHITE = Color("#FAEBD7")
    AQUA = Color("#00FFFF")
    AQUAMARINE = Color("#7FFFD4")
    AZURE = Color("#F0FFFF")
    BEIGE = Color("#F5F5DC")
    BISQUE = Color("#FFEBCD")
    BLACK = Color("#000000")
    BLANCHEDALMOND = Color("#FFEBCD")
    BLUE = Color("#0000FF")
    BLUEVIOLET = Color("#8A2BE2")
    BROWN = Color("#A52A2A")
    BURLYWOOD = Color("#DEB887")
    CADETBLUE = Color("#5F9EA0")
    CHARTREUSE = Color("#7FFF00")
    CHOCOLATE = Color("#D2691E")
    CORAL = Color("#FF7F50")
    CORNFLOWERBLUE = Color("#6495ED")
    CORNSILK = Color("#FFF8DC")
    CRIMSON = Color("#DC143C")
    CYAN = Color("#00FFFF")
    DARKBLUE = Color("#00008B")
    DARKCYAN = Color("#008B8B")
    DARKGOLDENROD = Color("#B8860B")
    DARKGRAY = Color("#A9A9A9")
    DARKGREEN = Color("#006400")
    DARKGREY = Color("#A9A9A9")
    DARKKHAKI = Color("#BDB76B")
    DARKMAGENTA = Color("#8B008B")
    DARKOLIVEGREEN = Color("#556B2F")
    DARKORANGE = Color("#FF8C00")
    DARKORCHID = Color("#9932CC")
    DARKRED = Color("#8B0000")
    DARKSALMON = Color("#E9967A")
    DARKSEAGREEN = Color("#8FBC8F")
    DARKSLATEBLUE = Color("#483D8B")
    DARKSLATEGRAY = Color("#2F4F4F")
    DARKSLATEGREY = Color("#2F4F4F")
    DARKTURQUOISE = Color("#00CED1")
    DARKVIOLET = Color("#9400D3")
    DEEPPINK = Color("#FF1493")
    DEEPSKYBLUE = Color("#00BFFF")
    DIMGRAY = Color("#696969")
    DIMGREY = Color("#696969")
    DODGERBLUE = Color("#1E90FF")
    FIREBRICK = Color("#B22222")
    FLORALWHITE = Color("#FFFAF0")
    FORESTGREEN = Color("#228B22")
    FUCHSIA = Color("#FF00FF")
    GAINSBORO = Color("#DCDCDC")
    GHOSTWHITE = Color("#F8F8FF")
    GOLD = Color("#FFD700")
    GOLDENROD = Color("#DAA520")
    GRAY = Color("#808080")
    GREEN = Color("#008000")
    GREENYELLOW = Color("#ADFF2F")
    GREY = Color("#808080")
    HONEYDEW = Color("#F0FFF0")
    HOTPINK = Color("#FF69B4")
    INDIANRED = Color("#CD5C5C")
    INDIGO = Color("#4B0082")
    IVORY = Color("#FFFFF0")
    KHAKI = Color("#F0E68C")
    LAVENDER = Color("#E6E6FA")
    LAVENDERBLUSH = Color("#FFF0F5")
    LAWNGREEN = Color("#7CFC00")
    LEMONCHIFFON = Color("#FFFACD")
    LIGHTBLUE = Color("#ADD8E6")
    LIGHTCORAL = Color("#F08080")
    LIGHTCYAN = Color("#E0FFFF")
    LIGHTGOLDENRODYELLOW = Color("#FAFAD2")
    LIGHTGRAY = Color("#D3D3D3")
    LIGHTGREEN = Color("#90EE90")
    LIGHTGREY = Color("#D3D3D3")
    LIGHTPINK = Color("#FFB6C1")
    LIGHTSALMON = Color("#FFA07A")
    LIGHTSEAGREEN = Color("#20B2AA")
    LIGHTSKYBLUE = Color("#87CEFA")
    LIGHTSLATEGRAY = Color("#778899")
    LIGHTSLATEGREY = Color("#778899")
    LIGHTSTEELBLUE = Color("#B0C4DE")
    LIGHTYELLOW = Color("#FFFFE0")
    LIME = Color("#00FF00")
    LIMEGREEN = Color("#32CD32")
    LINEN = Color("#FAF0E6")
    MAGENTA = Color("#FF00FF")
    MAROON = Color("#800000")
    MEDIUMAQUAMARINE = Color("#66CDAA")
    MEDIUMBLUE = Color("#0000CD")
    MEDIUMORCHID = Color("#BA55D3")
    MEDIUMPURPLE = Color("#9370DB")
    MEDIUMSEAGREEN = Color("#3CB371")
    MEDIUMSLATEBLUE = Color("#7B68EE")
    MEDIUMSPRINGGREEN = Color("#00FA9A")
    MEDIUMTURQUOISE = Color("#48D1CC")
    MEDIUMVIOLETRED = Color("#C71585")
    MIDNIGHTBLUE = Color("#191970")
    MINTCREAM = Color("#F5FFFA")
    MISTYROSE = Color("#FFE4E1")
    MOCCASIN = Color("#FFE4B5")
    NAVAJOWHITE = Color("#FFDEAD")
    NAVY = Color("#000080")
    OLDLACE = Color("#FDF5E6")
    OLIVE = Color("#808000")
    OLIVEDRAB = Color("#6B8E23")
    ORANGE = Color("#FFA500")
    ORANGERED = Color("#FF4500")
    ORCHID = Color("#DA70D6")
    PALEGOLDENROD = Color("#EEE8AA")
    PALEGREEN = Color("#98FB98")
    PALETURQUOISE = Color("#AFEEEE")
    PALEVIOLETRED = Color("#DB7093")
    PAPAYAWHIP = Color("#FFEFD5")
    PEACHPUFF = Color("#FFDAB9")
    PERU = Color("#CD853F")
    PINK = Color("#FFC0CB")
    PLUM = Color("#DDA0DD")
    POWDERBLUE = Color("#B0E0E6")
    PURPLE = Color("#800080")
    REBECCAPURPLE = Color("#663399")
    RED = Color("#FF0000")
    ROSYBROWN = Color("#BC8F8F")
    ROYALBLUE = Color("#4169E1")
    SADDLEBROWN = Color("#8B4513")
    SALMON = Color("#FA8072")
    SANDYBROWN = Color("#F4A460")
    SEAGREEN = Color("#2E8B57")
    SEASHELL = Color("#FFF5EE")
    SIENNA = Color("#A0522D")
    SILVER = Color("#C0C0C0")
    SKYBLUE = Color("#87CEEB")
    SLATEBLUE = Color("#6A5ACD")
    SLATEGRAY = Color("#708090")
    SLATEGREY = Color("#708090")
    SNOW = Color("#FFFAFA")
    SPRINGGREEN = Color("#00FF7F")
    STEELBLUE = Color("#4682B4")
    TAN = Color("#D2B48C")
    TEAL = Color("#008080")
    THISTLE = Color("#D8BFD8")
    TOMATO = Color("#FF6347")
    TURQUOISE = Color("#40E0D0")
    VIOLET = Color("#EE82EE")
    WHEAT = Color("#F5DEB3")
    WHITE = Color("#FFFFFF")
    WHITESMOKE = Color("#F5F5F5")
    YELLOW = Color("#FFFF00")
    YELLOWGREEN = Color("#9ACD32")


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
