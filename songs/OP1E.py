#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import OP1E as SRC


AA_RANGES = [(277, 441), (650, 686), (877, 931), (1373, 1399), (1515, 1535)]
CURSED_BANDING_RANGES = [(1167, 1177), (1293, 1306), (1382, 1416), (1572, 1589), (1700, 1756)]

flt = Filter(SRC, AA_RANGES, CURSED_BANDING_RANGES)
enc = Encoder(SRC, flt.process())


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
