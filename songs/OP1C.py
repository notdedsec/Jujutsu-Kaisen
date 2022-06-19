#!C:/KaizokuEncoder/python
from kaisen_common import src, flt, enc

OP = src.OP1C

AA_RANGES = [(277, 441), (650, 686), (877, 931), (1373, 1399), (1515, 1535)]
DB_RANGES = [(64, 144), (1094, 1117), (1138, 1178), (1293, 1306), (1408, 1441), (1572, 1589), (1691, 1756), (1928, 2020)]

def filter():
    src = OP.clip_cut
    res = flt.rescale(src)
    aaa = flt.antialias(res, AA_RANGES)
    deh = flt.dehalo(aaa)
    den = flt.denoise(deh)
    deb = flt.deband(den, DB_RANGES)
    gra = flt.grain(deb)
    fin = flt.finalize(gra)
    return fin

if __name__ == '__main__':
    brr = enc.Encoder(OP, filter())
    brr.run()
    brr.clean()
else:
    filter().set_output()
