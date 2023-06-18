#!C:/KaizokuEncoderV2/python

from kaisen_common.filters import Filter
from kaisen_common.encoder import Encoder
from kaisen_common.sources import ED1 as SRC


flt = Filter(SRC)
enc = Encoder(SRC, flt.process(), shift=1)


if __name__ == '__main__':
    enc.run()
    enc.clean()
    enc.compare()
