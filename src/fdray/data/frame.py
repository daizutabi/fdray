from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from PIL import Image
from PIL.Image import Resampling

if TYPE_CHECKING:
    from polars import DataFrame


def with_angles(df: DataFrame, x: str = "x", y: str = "y", z: str = "z") -> DataFrame:
    import polars as pl

    df = df.with_columns(
        theta=pl.col(x).arccos().degrees().round().cast(pl.Int64),
        phi=pl.arctan2(z, y).degrees().round().cast(pl.Int64),
    ).with_columns(
        phi=pl.when(pl.col("phi") < 0)
        .then(pl.col("phi") + 360)
        .otherwise(pl.col("phi")),
    )

    df_pole = (
        df.filter(pl.col("theta").is_in([0, 180]))
        .with_columns(phi=df["phi"].unique().to_list())
        .explode("phi")
    )
    df = pl.concat([df_pole, df]).unique(["theta", "phi"])

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
    array = array[:, ::-1]

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
