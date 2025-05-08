from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING

import numpy as np
from PIL import Image
from PIL.Image import Resampling

if TYPE_CHECKING:
    from polars import DataFrame


def from_spherical_coordinates(
    step_phi: int = 3,
    step_theta: int = 2,
) -> DataFrame:
    import polars as pl
    from polars import DataFrame

    angles = product(range(0, 360, step_phi), range(0, 180 + step_theta, step_theta))
    return (
        DataFrame(angles, schema=["phi", "theta"])
        .with_columns(
            phi=pl.col("phi").radians(),
            theta=pl.col("theta").radians(),
        )
        .with_columns(
            x=pl.col("theta").sin() * pl.col("phi").cos(),
            y=pl.col("theta").cos(),
            z=pl.col("theta").sin() * pl.col("phi").sin(),
        )
        .select("x", "y", "z")
        .unique()
    )


def to_spherical_coordinates(
    df: DataFrame,
    x: str = "x",
    y: str = "y",
    z: str = "z",
) -> DataFrame:
    """Convert Cartesian coordinates to spherical coordinates.

    This function converts Cartesian coordinates (x, y, z) to spherical coordinates
    (theta, phi) and handles special cases:

    - Normalizes phi to [0, 360] degrees
    - Duplicates data at poles (theta = 0, 180) for all phi values
    - Adds data at phi = 360 for continuity

    The coordinate transformation follows these equations:

    ```python
    # Cartesian to spherical
    theta = arccos(y)  # polar angle [0, 180] degrees
    phi = arctan2(z, x)  # azimuthal angle [0, 360] degrees

    # Spherical to Cartesian
    x = sin(theta) * cos(phi)
    y = cos(theta)
    z = sin(theta) * sin(phi)
    ```

    The coordinates correspond to POV-Ray's uv_mapping as follows:

        - North pole (theta = 0°) is at y = 1
        - South pole (theta = 180°) is at y = -1
        - phi = 0° is along the positive x-axis
        - The image's top edge (v = 0) maps to y = 1
        - The image's bottom edge (v = 1) maps to y = -1
        - The image's left and right edges connect at x-axis

    Args:
        df (DataFrame): Input DataFrame containing Cartesian coordinates.
        x (str, optional): Column name for x-coordinate. Defaults to "x".
        y (str, optional): Column name for y-coordinate. Defaults to "y".
        z (str, optional): Column name for z-coordinate. Defaults to "z".

    Returns:
        DataFrame: DataFrame with added theta and phi columns.

    Raises:
        ValueError: If required columns are missing.
    """
    import polars as pl

    df = df.with_columns(
        theta=pl.col(y).arccos().degrees().round().cast(pl.Int64),
        phi=pl.arctan2(z, x).degrees().round().cast(pl.Int64),
    ).with_columns(
        phi=pl.when(pl.col("phi") < 0)
        .then(pl.col("phi") + 360)
        .otherwise(pl.col("phi")),
    )

    # Handle poles (theta = 0, 180)
    df_pole = (
        df.filter(pl.col("theta").is_in([0, 180]))
        .with_columns(phi=df["phi"].unique().to_list())
        .explode("phi")
    )
    df = pl.concat([df_pole, df]).unique(["theta", "phi"])

    # Add data at phi = 360 for continuity
    df_meridian = df.filter(pl.col("phi") == 0).with_columns(
        phi=pl.lit(360).cast(pl.Int64),
    )
    return pl.concat([df, df_meridian]).sort("theta", "phi")


def visualize_spherical_data(
    df: DataFrame,
    value: str,
    phi: str = "phi",
    theta: str = "theta",
    scale: float = 1,
    vmin: float | None = None,
    vmax: float | None = None,
    cmap_name: str = "jet",
) -> Image.Image:
    """Visualize spherical coordinate data as an image.

    Args:
        df (DataFrame): Input DataFrame containing spherical coordinate data.
        value (str): Column name for the values to be visualized.
        phi (str, optional): Column name for azimuthal angle. Defaults to "phi".
        theta (str, optional): Column name for polar angle. Defaults to "theta".
        scale (float, optional): Scale factor for the output image. Defaults to 1.
        vmin (float | None, optional): Minimum value for normalization.
            Defaults to None.
        vmax (float | None, optional): Maximum value for normalization.
            Defaults to None.
        cmap_name (str, optional): Name of the colormap to use. Defaults to "jet".

    Returns:
        Image.Image: The generated spherical image.

    Raises:
        ValueError: If required columns are missing or if scale is invalid.
        KeyError: If the specified colormap does not exist.
    """
    import matplotlib as mpl

    df = df.sort(theta, phi)
    n_theta = df[theta].n_unique()
    n_phi = df[phi].n_unique()
    array = df[value].to_numpy().reshape((n_theta, n_phi))

    if vmin is None:
        vmin = np.min(array)
    if vmax is None:
        vmax = np.max(array)
    if vmin != vmax:
        array = (array - vmin) / (vmax - vmin)  # type: ignore

    cmap = mpl.colormaps[cmap_name]
    array = (255 * cmap(array)).astype(np.uint8)
    image = Image.fromarray(array)

    if scale == 1:
        return image

    size = (round(image.width * scale), round(image.height * scale))
    return image.resize(size, Resampling.LANCZOS)
