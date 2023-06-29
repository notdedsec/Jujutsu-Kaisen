#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import E07 as SRC


OP = 3117
ED = 30569

AA_RANGES = [(OP+277, OP+441), (OP+650, OP+686), (OP+877, OP+931), (OP+1373, OP+1399), (OP+1515, OP+1535)] + [(8113, 8161), (8185, 8254), (25577, 25612), (16318, 16356), (33052, 33158)]
CURSED_BANDING_RANGES = [(OP+1167, OP+1177), (OP+1293, OP+1306), (OP+1382, OP+1416), (OP+1572, OP+1589), (OP+1691, OP+1756)]
NO_DENOISE_RANGES = [(10097, 10563), (24128, 24312)] + [(16694, 16926), (17184, 17614), (17978, 19430), (20674, 21030), (21371, 22917)]

ZONES = {
    (21031, 21370): dict(b=1.25)
}

flt = Filter(SRC, AA_RANGES, CURSED_BANDING_RANGES, NO_DENOISE_RANGES)
enc = Encoder(SRC, flt.process(), zones=ZONES, shift=ED)


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
