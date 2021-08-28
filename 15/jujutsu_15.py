#!C:/KaizokuEncoder/python
import sys
sys.path.append('..')

import vapoursynth as vs
core = vs.core

from vsutil import depth
from encode import enc, flt

from BDMV.EP import E15 as EP
from BDMV.NC import OP2 as NCOP
from BDMV.NC import ED2 as NCED

OP = 3525
ED = 29850

AA_RANGES = [(21086, 21230)]
DB_RANGES = []

def filter() -> vs.VideoNode:
    src = depth(EP.clip_cut, 16)
    res = flt.rescale(src)
    fix = flt.fix_lineart(res, AA_RANGES)
    den = flt.denoise(fix)
    deb = flt.deband(den, fix, DB_RANGES)
    gra = flt.grain(deb)
    mnc = flt.mask_nc(gra, src, NCOP, NCED, OP, ED)
    fin = depth(mnc, 10)
    fin.set_output()
    return fin

if __name__ == '__main__':
    brr = enc.Encoder(EP, filter())
    brr.run()
    brr.clean()
    brr.compare()
else:
    filter().set_output()
