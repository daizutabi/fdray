from __future__ import annotations

from typing import Any


def camel_to_snake(camel_str: str) -> str:
    """Convert a CamelCase string to snake_case.

    Transform a string from CamelCase convention to
    snake_case by inserting underscores before capital letters
    and converting all characters to lowercase.

    Args:
        camel_str: A string in CamelCase format to be converted.

    Returns:
        A string converted to snake_case format.

    Examples:
        >>> camel_to_snake("CamelCase")
        'camel_case'
    """
    if not camel_str:
        return ""

    result = camel_str[0].lower()

    for char in camel_str[1:]:
        if char.isupper():
            result += "_" + char.lower()
        else:
            result += char

    return result


def convert(arg: Any) -> str:
    if isinstance(arg, dict):
        return " ".join(f"{k} {convert(v)}" for k, v in arg.items())

    if isinstance(arg, list | tuple):
        arg = ", ".join(str(x) for x in arg)
        return f"<{arg}>"

    return str(arg)


class Element:
    args: list[Any]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = list(args)
        if kwargs:
            self.args.append(kwargs)

    def __str__(self) -> str:
        """Convert the element to a string.

        Args:
            indent (int): The number of spaces to indent the element.

        Returns:
            str: The rendered element.
        """
        name = camel_to_snake(self.__class__.__name__)
        body = "\n".join(convert(arg) for arg in self.args)
        return f"{name} {{ {body} }}"


class Camera(Element):
    pass


class Texture(Element):
    pass


class Pigment(Element):
    pass


class Sphere(Element):
    pass


class Box(Element):
    pass


class Cone(Element):
    pass


class Cylinder(Element):
    pass


class Plane(Element):
    pass
