#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import E22 as SRC
from kaisen_common.utils import blank_mask


OP = 744
ED = 29852

AA_RANGES = [(OP+1687, OP+1709), (OP+1052, OP+1067), (OP+1942, OP+2010)] + [(17183, 17213)]
CURSED_BANDING_RANGES = [(OP+219, OP+262), (OP+364, OP+377), (OP+439, OP+508), (OP+784, OP+825), (OP+1052, OP+1067), (OP+1135, OP+1165)]
NO_DENOISE_RANGES = [(2901, 3291), (6055, 6331), (19460, 19660)]

MASKS = {
    (2901, 3291): blank_mask(SRC.clip_cut),
    (5087, 5303): blank_mask(SRC.clip_cut)
}

ZONES = {
    (ED, ED+2156): dict(b=0.85)
}

flt = Filter(SRC, AA_RANGES, CURSED_BANDING_RANGES, NO_DENOISE_RANGES, MASKS)
enc = Encoder(SRC, flt.process(), zones=ZONES)


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
