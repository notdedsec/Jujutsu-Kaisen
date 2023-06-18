#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import E06 as SRC


OP = 816
ED = 31290

AA_RANGES = [(OP+277, OP+441), (OP+650, OP+686), (OP+877, OP+931), (OP+1373, OP+1399), (OP+1515, OP+1535)]
CURSED_BANDING_RANGES = [(OP+1167, OP+1177), (OP+1293, OP+1306), (OP+1382, OP+1416), (OP+1572, OP+1589), (OP+1691, OP+1756)]
NO_DENOISE_RANGES = [(28115, 28481), (28589, 28733), (28805, 28979)]

LETTERBOX_RANGES = {
    (28115, 28481): dict(height=156),
    (28589, 28733): dict(height=156),
    (28805, 28979): dict(height=156)
}

ZONES = {
    (28115, 28481): dict(b=0.85),
    (28589, 28733): dict(b=0.85),
    (28805, 28979): dict(b=0.85)
}

flt = Filter(SRC, AA_RANGES, CURSED_BANDING_RANGES, NO_DENOISE_RANGES, {}, LETTERBOX_RANGES)
enc = Encoder(SRC, flt.process(), zones=ZONES, shift=ED)


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
