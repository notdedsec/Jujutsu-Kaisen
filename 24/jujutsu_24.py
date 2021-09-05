#!C:/KaizokuEncoder/python
import sys
sys.path.append('..')
from encode import enc, flt

from BDMV.EP import E24 as EP
from BDMV.NC import OP2 as NCOP
from BDMV.NC import ED2 as NCED

OP = 3189
ED = None

AA_RANGES = [(OP+1687, OP+1709), (OP+1052, OP+1067), (OP+1942, OP+2010)] + [(33303, 33453)]
DB_RANGES = [(OP+219, OP+262), (OP+364, OP+377), (OP+439, OP+508), (OP+784, OP+825), (OP+784, OP+825), (OP+1052, OP+1067), (OP+1135, OP+1165), (OP+1852, OP+1885)]

def filter():
    src = EP.clip_cut
    res = flt.rescale(src)
    aaa = flt.antialias(res, AA_RANGES)
    deh = flt.dehalo(aaa)
    den = flt.denoise(deh)
    deb = flt.deband(den, deh, DB_RANGES)
    mnc = flt.mask_nc(deb, src, NCOP, NCED, OP, ED)
    gra = flt.grain(mnc)
    fin = flt.finalize(gra)
    return fin

if __name__ == '__main__':
    brr = enc.Encoder(EP, filter())
    brr.run()
    brr.clean()
    brr.compare()
else:
    filter().set_output()
