def test_colormap():
    from fdray.data.color import get_colormap

    colormap = get_colormap("viridis")
    assert len(colormap) == 256
    assert str(colormap[0]) == "rgb <0.267, 0.00487, 0.329>"


def test_colormap_num_colors():
    from fdray.data.color import get_colormap

    colormap = get_colormap("viridis", num_colors=10)
    assert len(colormap) == 10
