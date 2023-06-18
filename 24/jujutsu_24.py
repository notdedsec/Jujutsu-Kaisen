#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import E24 as SRC


OP = 3189
ED = None

AA_RANGES = [(OP+1687, OP+1709), (OP+1052, OP+1067), (OP+1942, OP+2010)] + [(33303, 33453)]
CURSED_BANDING_RANGES = [(OP+219, OP+262), (OP+364, OP+377), (OP+439, OP+508), (OP+784, OP+825), (OP+1052, OP+1067), (OP+1135, OP+1165)]
NO_DENOISE_RANGES = [(7138, 7703)]

flt = Filter(SRC, AA_RANGES, CURSED_BANDING_RANGES, NO_DENOISE_RANGES)
enc = Encoder(SRC, flt.process())


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
