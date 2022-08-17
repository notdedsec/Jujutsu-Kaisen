#!C:/KaizokuEncoder/python
from kaisen_common import src, flt, enc

SRC = src.E18

OP = 3789
ED = 29849

AA_RANGES = [(OP+1687, OP+1709), (OP+1052, OP+1067), (OP+1942, OP+2010)] + [(32211, 32405)]
DB_RANGES = [(OP+219, OP+262), (OP+364, OP+377), (OP+439, OP+508), (OP+784, OP+825), (OP+1052, OP+1067), (OP+1135, OP+1165)]

def filter():
    src = SRC.clip_cut
    res = flt.rescale(src)
    msk = flt.detailmask(res)
    den = flt.denoise(res, msk)
    aaa = flt.antialias(den, AA_RANGES)
    deh = flt.dehalo(aaa)
    deb = flt.deband(deh, msk, DB_RANGES)
    rst = flt.restore(deb, src)
    grn = flt.grain(rst)
    return grn

if __name__ == '__main__':
    brr = enc.Encoder(SRC, filter())
    brr.run()
    brr.clean()
    brr.compare()
else:
    filter().set_output()
