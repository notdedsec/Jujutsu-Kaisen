#!C:/KaizokuEncoder/python
import sys
sys.path.append('..')
from encode import enc, flt

from BDMV.NC import OP2 as OP

AA_RANGES = [(1687, 1709), (1052, 1067), (1942, 2010)]
DB_RANGES = [(219, 262), (364, 377), (439, 508), (784, 825), (1052, 1067), (1135, 1165), (1852, 1885)]

def filter():
    src = OP.clip_cut
    res = flt.rescale(src)
    aaa = flt.antialias(res, AA_RANGES)
    deh = flt.dehalo(aaa)
    den = flt.denoise(deh)
    deb = flt.deband(den, deh, DB_RANGES)
    gra = flt.grain(deb)
    fin = flt.finalize(gra)
    return fin

if __name__ == '__main__':
    brr = enc.Encoder(OP, filter())
    brr.run()
    brr.clean()
else:
    filter().set_output()
