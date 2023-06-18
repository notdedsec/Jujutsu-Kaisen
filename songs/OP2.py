#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import OP2 as SRC


AA_RANGES = [(1687, 1709), (1052, 1067), (1942, 2010)]
CURSED_BANDING_RANGES = [(219, 262), (364, 377), (439, 508), (784, 825), (1052, 1067), (1135, 1165)]

flt = Filter(SRC, AA_RANGES, CURSED_BANDING_RANGES)
enc = Encoder(SRC, flt.process())


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
