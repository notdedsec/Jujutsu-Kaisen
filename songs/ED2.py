#!C:/KaizokuEncoder/python
from kaisen_common import src, flt, enc

SRC = src.ED2

AA_RANGES = []
DB_RANGES = []

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
