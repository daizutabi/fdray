from fdray.color import Color
from fdray.pigment import Pigment, PigmentMap


def test_pigment():
    pigment = Pigment(Color("red"))
    assert str(pigment) == "pigment { rgb <1, 0, 0> }"


def test_pigment_pattern():
    pigment = Pigment("checker", Color("red"), Color("blue"))
    x = "pigment {\n  checker\n  rgb <1, 0, 0>\n  rgb <0, 0, 1>\n}"
    assert str(pigment) == x


def test_pigment_map():
    pigment = PigmentMap((0, Pigment("Red")), (1, "Blue"))
    assert str(pigment) == "pigment_map { [0 Red] [1 Blue] }"
