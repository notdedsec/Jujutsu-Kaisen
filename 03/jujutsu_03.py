#!C:/KaizokuEncoder/python
import sys
sys.path.append('..')

import vapoursynth as vs
core = vs.core

from vsutil import depth
from encode import enc, flt

from BDMV.EP import E03  as EP
from BDMV.NC import OP1B as NCOP
from BDMV.NC import ED1  as NCED

OP = 4603
ED = 30569

AA_RANGES = [(2357, 2441)]
DB_RANGES = [(OP+6, OP+32), (OP+1062, OP+1116), (OP+1335, OP+1414), (OP+1656, OP+1755)]

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
    brr = enc.Encoder(EP, filter(), ED)
    brr.run()
    brr.clean()
    brr.compare()
else:
    filter().set_output()
