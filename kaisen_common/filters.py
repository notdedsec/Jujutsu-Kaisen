import lvsfunc as lvf
import kagefunc as kgf
import havsfunc as haf
import vardefunc as vdf
from typing import Tuple, Optional
from vardautomation import FileInfo
from vsutil import depth, plane, iterate
from adptvgrnMod import adptvgrnMod
from xvs import WarpFixChromaBlend
from debandshit import dumb3kdb

import vapoursynth as vs
core = vs.core

descale_args = dict(
    height = 844,
    kernel = lvf.kernels.Bicubic()
)


def rescale(clip: vs.VideoNode) -> vs.VideoNode:
    scale = lvf.scale.descale(clip, **descale_args)
    resample = depth(scale, 16)
    return resample


def detailmask(clip: vs.VideoNode, strength: int = 8500) -> vs.VideoNode:
    mask = kgf.retinex_edgemask(clip, 2)
    mask = mask.std.Binarize(strength)
    mask = mask.std.Inflate()
    return mask


def denoise(clip: vs.VideoNode, mask: vs.VideoNode, skip: Optional[Tuple[int, int]] = None) -> vs.VideoNode:
    denoise = haf.SMDegrain(clip, tr=3, thSAD=64, thSADC=48, RefineMotion=True)
    merge = core.std.MaskedMerge(denoise, clip, mask)
    merge = vdf.misc.merge_chroma(plane(merge, 0), denoise)
    replace = lvf.rfs(merge, clip, ranges=skip)
    decsiz = vdf.noise.decsiz(replace, min_in=45000, max_in=55000)
    return decsiz


def antialias(clip: vs.VideoNode, strong: Optional[Tuple[int, int]] = None) -> vs.VideoNode:
    nnee = lvf.aa.nneedi3_clamp(clip, 2)
    sraa = lvf.aa.upscaled_sraa(clip, 2)
    replace = lvf.rfs(nnee, sraa, ranges=strong)
    return replace


def dehalo(clip: vs.VideoNode) -> vs.VideoNode:
    dehalo = haf.FineDehalo(clip, rx=2, darkstr=0, thlimi=16, thmi=64)
    clean = haf.EdgeCleaner(dehalo, strength=8, smode=1, hot=True)
    cwarp = WarpFixChromaBlend(clean, thresh=96)
    restore = core.std.Expr([dehalo, cwarp], 'x y min')
    return restore


def deband(clip: vs.VideoNode, mask: vs.VideoNode, strong: Optional[Tuple[int, int]] = None) -> vs.VideoNode:
    deband_lo = dumb3kdb(clip, radius=16, threshold=28)
    deband_hi = dumb3kdb(clip, radius=16, threshold=64)
    replace = lvf.rfs(deband_lo, deband_hi, ranges=strong)
    merge = core.std.MaskedMerge(replace, clip, mask)
    return merge


def restore(clip: vs.VideoNode, src: vs.VideoNode, ext: FileInfo = None, EXT: Optional[Tuple[int, int]] = None) -> vs.VideoNode:
    src = depth(src, 32)
    descale = lvf.scale.descale(src, **descale_args, upscaler=None).resize.Bicubic(1920, 1080)
    mask = lvf.scale.descale_detail_mask(plane(src, 0), descale)
    src, mask = depth(src, 16), depth(mask, 16)
    mask = iterate(mask, core.std.Deflate, 2)
    mask = iterate(mask, core.std.Inflate, 8)

    if EXT != None:
        mask_ext = core.imwri.Read(ext.path).resize.Point(format=mask.format.id, matrix=1)
        mask_ext = core.std.AssumeFPS(mask_ext*len(mask), mask)
        mask = lvf.rfs(mask, mask_ext, ranges=EXT)

    restored = core.std.MaskedMerge(clip, src, mask)
    return restored


def grain(clip: vs.VideoNode) -> vs.VideoNode:
    grain = adptvgrnMod(clip, strength=0.2, sharp=60, static=True)
    final = depth(grain, 10)
    return final


def comp(src, fin, mod = None):
    frames = [x for x in range(1, min(len(src), len(fin))) if x % mod == 0] if mod else None
    comp = lvf.comp(src , fin, frames)
    return comp

