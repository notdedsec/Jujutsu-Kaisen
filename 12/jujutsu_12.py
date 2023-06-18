#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import E12 as SRC


OP = 2805
ED = 30569

AA_RANGES = [(OP+277, OP+441), (OP+650, OP+686), (OP+877, OP+931), (OP+1373, OP+1399), (OP+1515, OP+1535)] + [(15005, 15072), (26191, 26246)]
CURSED_BANDING_RANGES = [(OP+1167, OP+1177), (OP+1293, OP+1306), (OP+1382, OP+1416), (OP+1572, OP+1589), (OP+1700, OP+1756)]
NO_DENOISE_RANGES = [(17655, 17775)]

ZONES = {
    (16392, 16680): dict(b=0.90),
    (17495, 17639): dict(b=0.90),
    (17775, 17841): dict(b=0.90)
}

flt = Filter(SRC, AA_RANGES, CURSED_BANDING_RANGES, NO_DENOISE_RANGES)
enc = Encoder(SRC, flt.process(), zones=ZONES, shift=ED)


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
