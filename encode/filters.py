import vapoursynth as vs
from typing import Optional, Tuple, Union

import lvsfunc as lvf
import vardefunc as vdf
from adptvgrnMod import adptvgrnMod
from debandshit import dumb3kdb
from vsutil import depth
from xvs import mwcfix

core = vs.core

def rescale(clip: vs.VideoNode) -> vs.VideoNode:
    clip = depth(clip, 16)
    scale = lvf.scale.descale(clip, height=844, kernel=lvf.kernels.Bicubic(b=0, c=1/2))
    return scale

def fix_lineart(clip: vs.VideoNode, heavy: Union[int, Tuple[int, int]]) -> vs.VideoNode:
    clip = depth(clip, 16)
    aa = lvf.aa.upscaled_sraa(clip, 1.4)
    aa = lvf.rfs(clip, aa, ranges=heavy)
    cwarp = mwcfix(aa)
    return cwarp

def denoise(clip: vs.VideoNode) -> vs.VideoNode:
    decsiz = vdf.noise.decsiz(clip, min_in=80 << 8, max_in=200 << 8)
    return decsiz

def deband(clip: vs.VideoNode, lineart: vs.VideoNode, heavy: Union[int, Tuple[int, int]]) -> vs.VideoNode:
    mask = lvf.mask.detail_mask(clip, brz_b=0.05)
    deband = dumb3kdb(clip, radius=16, threshold=28)
    deband_h = dumb3kdb(clip, radius=18, threshold=48)
    deband = lvf.rfs(deband, deband_h, ranges=heavy)
    deband = core.std.MaskedMerge(deband, lineart, mask)
    return deband

def grain(clip: vs.VideoNode) -> vs.VideoNode:
    grain = adptvgrnMod(clip, strength=0.2, sharp=72, luma_scaling=10, static=True)
    return grain

def mask_nc(ep: vs.VideoNode, src: vs.VideoNode, ncop: vs.VideoNode, nced: vs.VideoNode,
            opstart: Optional[int] = None, edstart: Optional[int] = None) -> vs.VideoNode:
    ncop = depth(nced.clip_cut, 16)
    nced = depth(nced.clip_cut, 16)
    merge = depth(ep, 16)
    if opstart:
        mask_op = vdf.mask.Difference().creditless_oped(src, ncop, nced, opstart=opstart, opend=opstart+2159)
        merge = core.std.MaskedMerge(merge, src, mask_op)
    if edstart:
        mask_ed = vdf.mask.Difference().creditless_oped(src, ncop, nced, edstart=edstart, edend=edstart+2157)
        merge = core.std.MaskedMerge(merge, src, mask_ed)
    return merge
