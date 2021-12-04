#!C:/KaizokuEncoder/python
import sys
sys.path.append('..')
from encode import enc, flt

from BDMV.EP import E11  as EP
from BDMV.NC import OP1D as NCOP
from BDMV.NC import ED1  as NCED

OP = 3285
ED = 31649

AA_RANGES = [(OP+277, OP+441), (OP+650, OP+686), (OP+877, OP+931), (OP+1373, OP+1399), (OP+1515, OP+1535)]
DB_RANGES = [(OP+64, OP+144), (OP+1094, OP+1117), (OP+1138, OP+1178), (OP+1293, OP+1306), (OP+1408, OP+1441), (OP+1572, OP+1589), (OP+1699, OP+1756), (OP+1928, OP+2020)]

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
    brr = enc.Encoder(EP, filter(), ED)
    brr.run()
    brr.clean()
    brr.compare()
else:
    filter().set_output()
