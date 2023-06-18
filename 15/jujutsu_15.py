#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import E15 as SRC
from kaisen_common.utils import blank_mask


OP = 3525
ED = 29850

AA_RANGES = [(OP+1687, OP+1709), (OP+1052, OP+1067), (OP+1942, OP+2010)] + [(21086, 21230)]
CURSED_BANDING_RANGES = [(OP+219, OP+262), (OP+364, OP+377), (OP+439, OP+508), (OP+784, OP+825), (OP+1052, OP+1067), (OP+1135, OP+1165)]
NO_DENOISE_RANGES = [(11442, 13989), (27256, 27376), (27664, 27916)]

LETTERBOX_RANGES = {
    (11442, 13989): dict(height=132)
}

MASKS = {
    (135, 231): blank_mask(SRC.clip_cut),
    (1308, 1404): blank_mask(SRC.clip_cut)
}

ZONES = {
    (ED, ED+2156): dict(b=0.85)
}

flt = Filter(SRC, AA_RANGES, CURSED_BANDING_RANGES, NO_DENOISE_RANGES, MASKS, LETTERBOX_RANGES)
enc = Encoder(SRC, flt.process(), zones=ZONES)


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
