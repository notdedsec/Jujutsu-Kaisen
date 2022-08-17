#!C:/KaizokuEncoder/python
from kaisen_common import src, flt, enc

SRC = src.OP2

AA_RANGES = [(1687, 1709), (1052, 1067), (1942, 2010)]
DB_RANGES = [(219, 262), (364, 377), (439, 508), (784, 825), (1052, 1067), (1135, 1165)]

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
