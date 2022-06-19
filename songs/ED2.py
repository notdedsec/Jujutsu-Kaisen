#!C:/KaizokuEncoder/python
from kaisen_common import src, flt, enc

ED = src.ED2

AA_RANGES = []
DB_RANGES = []

def filter():
    src = ED.clip_cut
    res = flt.rescale(src)
    aaa = flt.antialias(res, AA_RANGES)
    deh = flt.dehalo(aaa)
    den = flt.denoise(deh)
    deb = flt.deband(den, DB_RANGES)
    gra = flt.grain(deb)
    fin = flt.finalize(gra)
    return fin

if __name__ == '__main__':
    brr = enc.Encoder(ED, filter())
    brr.run()
    brr.clean()
else:
    filter().set_output()
