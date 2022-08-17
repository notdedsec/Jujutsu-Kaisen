#!C:/KaizokuEncoder/python
from kaisen_common import src, flt, enc

SRC = src.OP1

AA_RANGES = [(277, 441), (650, 686), (877, 931), (1373, 1399), (1515, 1535)]
DB_RANGES = [(1293, 1306), (1572, 1589), (1691, 1756)]

def filter():
    src = SRC.clip_cut
    res = flt.rescale(src)
    msk = flt.detailmask(res)
    den = flt.denoise(res, msk)
    aaa = flt.antialias(den, AA_RANGES)
    deh = flt.dehalo(aaa)
    deb = flt.deband(deh, msk, DB_RANGES)
    grn = flt.grain(deb)
    return grn

if __name__ == '__main__':
    brr = enc.Encoder(SRC, filter())
    brr.run()
    brr.clean()
else:
    filter().set_output()
