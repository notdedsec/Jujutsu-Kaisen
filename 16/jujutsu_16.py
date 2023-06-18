#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import E16 as SRC


OP = 5586
ED = 29851

AA_RANGES = [(OP+1687, OP+1709), (OP+1052, OP+1067), (OP+1942, OP+2010)]
CURSED_BANDING_RANGES = [(OP+219, OP+262), (OP+364, OP+377), (OP+439, OP+508), (OP+784, OP+825), (OP+1052, OP+1067), (OP+1135, OP+1165)]
NO_DENOISE_RANGES = [(246, 440), (5283, 5348), (27292, 27928)]


LETTERBOX_RANGES = {
    (5283, 5348): dict(height=132)
}

ZONES = {
    (246, 440): dict(b=0.85),
    (27292, 27928): dict(b=0.85),
    (ED, ED+2156): dict(b=0.85)
}

flt = Filter(SRC, AA_RANGES, CURSED_BANDING_RANGES, NO_DENOISE_RANGES, {}, LETTERBOX_RANGES)
enc = Encoder(SRC, flt.process(), zones=ZONES)


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
