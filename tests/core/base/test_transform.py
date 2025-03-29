from fdray.core.base import Transform, Transformable


def test_transform_scale():
    x = Transform(scale=(1, 2, 3))
    assert str(x) == "scale <1, 2, 3>"


def test_transform_rotate():
    x = Transform(rotate=(1, 2, 3))
    assert str(x) == "rotate <1, 2, 3>"


def test_transform_translate():
    x = Transform(translate=(1, 2, 3))
    assert str(x) == "translate <1, 2, 3>"


def test_transform_all():
    x = Transform(scale=10, rotate=(1, 2, 3), translate=(1, 2, 3))
    assert str(x) == "transform { scale 10 rotate <1, 2, 3> translate <1, 2, 3> }"


def test_transformable_scale_vector():
    x = Transformable("x").scale(1, 2, 3)
    assert str(x) == "transformable { x scale <1, 2, 3> }"


def test_transformable_scale_scalar():
    x = Transformable("x").scale(1)
    assert str(x) == "transformable { x scale 1 }"


def test_transformable_scale_str():
    x = Transformable("x").scale("2*x")
    assert str(x) == "transformable { x scale 2*x }"


def test_transformable_rotate():
    x = Transformable("x").rotate(1, 2, 3)
    assert str(x) == "transformable { x rotate <1, 2, 3> }"


def test_transformable_rotate_str():
    x = Transformable("x").rotate("2*x")
    assert str(x) == "transformable { x rotate 2*x }"


def test_transformable_translate():
    x = Transformable("x").translate(1, 2, 3)
    assert str(x) == "transformable { x translate <1, 2, 3> }"


def test_transformable_translate_str():
    x = Transformable("x").translate("2*x")
    assert str(x) == "transformable { x translate 2*x }"
