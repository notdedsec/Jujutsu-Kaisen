import os
import vapoursynth as vs
import mvsfunc as mvf
import lvsfunc as lvf
import fvsfunc as fvf
import havsfunc as haf
import kagefunc as kgf
import vsTAAmbk as taa
from nnedi3_rpow2 import nnedi3_rpow2

core = vs.core
core.max_cache_size = 18000

source = os.path.join(os.getcwd(), "jujutsu_02.mkv")
src = lvf.src(source)
src = fvf.Depth(src, 16)

op = 8272
ec = None
ed = 32008

heavy_denoise = [(34332, len(src))]
strong_aa     = [(14399, 14596)]
static_grain  = [(34332, len(src))]
dynamic_grain = []

if op:
    heavy_denoise += [(op+6, op+32), (op+1062, op+1116), (op+1335, op+1414), (op+1656, op+1755)]
    static_grain  += [(op+6, op+30), (op+931, op+1015), (op+1167, op+1303), (op+1335, op+1512), (op+1551, op+1590), (op+1656, op+1755), (op+1928, op+2047)]

if ec: 
    heavy_denoise += [(ec-120, ec+120)]
    dynamic_grain += [(ec-120, ec+120)]

Y, U, V = kgf.split(src)
descale = kgf.inverse_scale(Y, height=844, kernel='bicubic', b=1/3, c=2/5, mask_detail=True)
descale = fvf.Depth(descale, 16)

denoise   = mvf.BM3D(descale, sigma=1.8)
denoise_h = mvf.BM3D(descale, sigma=4.2)
denoise   = lvf.rfs(denoise, denoise_h, ranges=heavy_denoise)

aa_ee = taa.TAAmbk(denoise, aatype='Eedi3')
aa_nn = taa.TAAmbk(denoise, aatype='Nnedi3')
aa    = lvf.rfs(aa_nn, aa_ee, ranges=strong_aa)

upscale = nnedi3_rpow2(aa).resize.Spline36(src.width, src.height)
upscale = kgf.join([upscale, U, V])

dehalo = haf.DeHalo_alpha(upscale, rx=2.2, darkstr=0)
if ed: 
    dehalo = lvf.rfs(dehalo, upscale, ranges=[(ed, ed+2157)])

deband   = core.f3kdb.Deband(dehalo, range=18, y=48, cb=40, cr=40, grainy=0, grainc=0, output_depth=16)

grain   = kgf.adaptive_grain(deband, 0.25, luma_scaling=8)
grain_s = kgf.adaptive_grain(deband, strength=1.4, luma_scaling=8, static=True)
grain_d = kgf.adaptive_grain(deband, strength=3.6, luma_scaling=4, static=False)
grain   = lvf.rfs(grain, grain_s, ranges=static_grain)
grain   = lvf.rfs(grain, grain_d, ranges=dynamic_grain)

final = fvf.Depth(grain, 10)
final.set_output()
