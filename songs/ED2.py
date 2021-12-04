#!C:/KaizokuEncoder/python
import sys
sys.path.append('..')
from encode import enc, flt

from BDMV.NC import ED2 as ED

AA_RANGES = []
DB_RANGES = []

def filter():
    src = ED.clip_cut
    res = flt.rescale(src)
    aaa = flt.antialias(res, AA_RANGES)
    deh = flt.dehalo(aaa)
    den = flt.denoise(deh)
    deb = flt.deband(den, deh, DB_RANGES)
    gra = flt.grain(deb)
    fin = flt.finalize(gra)
    return fin

if __name__ == '__main__':
    brr = enc.Encoder(ED, filter())
    brr.run()
    brr.clean()
else:
    filter().set_output()
