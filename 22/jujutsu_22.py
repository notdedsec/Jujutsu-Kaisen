#!C:/KaizokuEncoder/python
from kaisen_common import src, flt, enc

EP = src.E22
NCOP = src.OP2
NCED = src.ED2

OP = 744
ED = 29852

AA_RANGES = [(OP+1687, OP+1709), (OP+1052, OP+1067), (OP+1942, OP+2010)] + [(17183, 17213)]
DB_RANGES = [(OP+219, OP+262), (OP+364, OP+377), (OP+439, OP+508), (OP+784, OP+825), (OP+1052, OP+1067), (OP+1135, OP+1165), (OP+1852, OP+1885)]

def filter():
    src = EP.clip_cut
    res = flt.rescale(src)
    aaa = flt.antialias(res, AA_RANGES)
    deh = flt.dehalo(aaa)
    den = flt.denoise(deh)
    deb = flt.deband(den, DB_RANGES)
    rst = flt.restore(deb, src, NCOP, NCED, OP, ED)
    gra = flt.grain(rst)
    fin = flt.finalize(gra)
    return fin

if __name__ == '__main__':
    brr = enc.Encoder(EP, filter())
    brr.run()
    brr.clean()
    brr.compare()
else:
    filter().set_output()
