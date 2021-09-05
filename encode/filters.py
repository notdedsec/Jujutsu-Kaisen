import vapoursynth as vs
from vardautomation import FileInfo
from typing import Optional, Tuple, Union

import lvsfunc as lvf
import vardefunc as vdf
from cooldegrain import CoolDegrain
from adptvgrnMod import adptvgrnMod
from xvs import WarpFixChromaBlend
from debandshit import dumb3kdb
from vsutil import depth

core = vs.core

def rescale(clip: vs.VideoNode) -> vs.VideoNode:
    scale = lvf.scale.descale(clip, height=844, kernel=lvf.kernels.Bicubic(b=0, c=1/2))
    return depth(scale, 16)

def antialias(clip: vs.VideoNode, heavy: Optional[Union[int, Tuple[int, int]]] = None) -> vs.VideoNode:
    aa_lo = lvf.aa.taa(clip, lvf.aa.nnedi3())
    aa_hi = lvf.aa.upscaled_sraa(clip, 1.5)
    aa_clamp = lvf.aa.clamp_aa(clip, aa_lo, aa_hi, strength=2)
    aa = lvf.rfs(aa_clamp, aa_hi, ranges=heavy)
    return aa

def dehalo(clip: vs.VideoNode) -> vs.VideoNode:
    halo_mask = lvf.mask.halo_mask(clip, brz=0.25)
    dehalo = lvf.dehalo.bidehalo(clip, sigmaS=1.2)
    merge = core.std.MaskedMerge(clip, dehalo, halo_mask)
    cwarp = WarpFixChromaBlend(merge, thresh=72)
    return cwarp

def denoise(clip: vs.VideoNode) -> vs.VideoNode:
    adaptive_mask = adptvgrnMod(clip, luma_scaling=8, show_mask=True)
    denoise_hi = CoolDegrain(clip, thsad=64, thsadc=48, blksize=8, overlap=4)
    denoise_lo = CoolDegrain(clip, thsad=18, thsadc=48, blksize=8, overlap=4)
    denoise = core.std.MaskedMerge(denoise_hi, denoise_lo, adaptive_mask)
    return denoise

def deband(clip: vs.VideoNode, lineart: vs.VideoNode, heavy: Optional[Union[int, Tuple[int, int]]] = None) -> vs.VideoNode:
    detail_mask = lvf.mask.detail_mask(clip, sigma=1, brz_a=0.15, brz_b=0.075)
    deband_lo = dumb3kdb(clip, radius=16, threshold=36)
    deband_hi = dumb3kdb(clip, radius=18, threshold=72)
    deband_replace = lvf.rfs(deband_lo, deband_hi, ranges=heavy)
    deband = core.std.MaskedMerge(deband_replace, lineart, detail_mask)
    return deband

def mask_nc(clip: vs.VideoNode, src: vs.VideoNode, ncop: FileInfo, nced: FileInfo, OP: Optional[int] = None, ED: Optional[int] = None) -> vs.VideoNode:
    mask_op = vdf.dcm(src, src[OP:OP+ncop.clip_cut.num_frames], ncop.clip_cut, OP, thr=128, prefilter=True) if OP else core.std.BlankClip(src)
    mask_ed = vdf.dcm(src, src[ED:ED+nced.clip_cut.num_frames], nced.clip_cut, ED, thr=128, prefilter=True) if ED else core.std.BlankClip(src)
    credit_mask = depth(core.std.Expr([mask_op, mask_ed], expr = 'x y +'), 16)
    merge = core.std.MaskedMerge(depth(clip, 16), depth(src, 16), credit_mask)
    return merge

def grain(clip: vs.VideoNode) -> vs.VideoNode:
    grain = adptvgrnMod(clip, strength=0.25, cstrength=0.05, size=1.1, sharp=70, luma_scaling=10, static=True)
    return grain

def finalize(clip: vs.VideoNode) -> vs.VideoNode:
    return depth(clip, 10)
