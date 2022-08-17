#!C:/KaizokuEncoder/python
from kaisen_common import src, flt, enc

SRC = src.E07

OP = 3117
ED = 30569

AA_RANGES = [(OP+277, OP+441), (OP+650, OP+686), (OP+877, OP+931), (OP+1373, OP+1399), (OP+1515, OP+1535)] + [(8113, 8161), (8185, 8254), (25577, 25612), (16318, 16356), (33052, 33158)]
DB_RANGES = [(OP+1293, OP+1306), (OP+1572, OP+1589), (OP+1699, OP+1756)]

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
    brr = enc.Encoder(SRC, filter(), ED)
    brr.run()
    brr.clean()
    brr.compare()
else:
    filter().set_output()
