import lvsfunc as lvf
import havsfunc as haf
import vardefunc as vdf
import debandshit as dbs
from vardautomation import FileInfo
from typing import Optional, Tuple, Union
from cooldegrain import CoolDegrain
from adptvgrnMod import adptvgrnMod
from xvs import WarpFixChromaBlend
from vsutil import depth, iterate

import vapoursynth as vs
core = vs.core

descale_args = dict(height=844, kernel=lvf.kernels.Catrom())

def rescale(clip: vs.VideoNode) -> vs.VideoNode:
    scale = lvf.scale.descale(clip, **descale_args)
    return depth(scale, 16)

def antialias(clip: vs.VideoNode, heavy: Optional[Union[int, Tuple[int, int]]] = None) -> vs.VideoNode:
    aa_lo = lvf.aa.taa(clip, lvf.aa.nnedi3())
    aa_hi = lvf.aa.upscaled_sraa(clip, 2)
    aa_clamp = lvf.aa.clamp_aa(clip, aa_lo, aa_hi)
    aa = lvf.rfs(aa_clamp, aa_hi, ranges=heavy)
    return aa

def dehalo(clip: vs.VideoNode) -> vs.VideoNode:
    halo_mask = lvf.mask.halo_mask(clip, rad=1)
    dehalo = haf.DeHalo_alpha(clip, darkstr=0)
    merge = core.std.MaskedMerge(clip, dehalo, halo_mask)
    dering = haf.EdgeCleaner(merge, strength=8, smode=1, hot=True)
    cwarp = WarpFixChromaBlend(dering, thresh=48)
    return cwarp

def denoise(clip: vs.VideoNode) -> vs.VideoNode:
    denoise = CoolDegrain(clip, thsad=48, blksize=8, overlap=4)
    detail_mask = lvf.mask.detail_mask(clip, rad=1, brz_b=0.024)
    adaptive_mask = adptvgrnMod(denoise, luma_scaling=180, show_mask=True)
    autistic_mask = core.std.Expr([adaptive_mask, detail_mask], 'x y +')
    merge = core.std.MaskedMerge(denoise, clip, autistic_mask)
    return merge

def deband(clip: vs.VideoNode, heavy: Optional[Union[int, Tuple[int, int]]] = None) -> vs.VideoNode:
    detail_mask = lvf.mask.detail_mask(clip, sigma=1, rad=1, brz_b=0.024)
    deband_lo = dbs.dumb3kdb(clip, radius=16, threshold=36)
    deband_hi = dbs.dumb3kdb(clip, radius=18, threshold=72)
    deband_replace = lvf.rfs(deband_lo, deband_hi, ranges=heavy)
    deband = core.std.MaskedMerge(deband_replace, clip, detail_mask)
    return deband

def restore(
    clip: vs.VideoNode, src: vs.VideoNode, ncop: FileInfo, nced: FileInfo, OP: Optional[int] = None, ED: Optional[int] = None,
    ext: Optional[FileInfo] = None, EXT: Optional[Union[int, Tuple[int, int]]] = None, show_mask: Optional[bool] = False
) -> vs.VideoNode:

    mask = lvf.scale.descale(clip, show_mask=True, **descale_args)
    mask = depth(iterate(mask, core.std.Inflate, 4), 16)

    if OP != None:
        mask_op = vdf.dcm(src, src[OP:OP+ncop.clip_cut.num_frames], ncop.clip_cut, OP, thr=128, prefilter=True)
        mask_op = depth(iterate(mask, core.std.Inflate, 4), 16)
        mask = lvf.rfs(mask, mask_op, [(OP, OP+ncop.clip_cut.num_frames)])

    if ED != None:
        mask_ed = vdf.dcm(src, src[ED:ED+nced.clip_cut.num_frames], nced.clip_cut, ED, thr=128, prefilter=True)
        mask_ed = depth(iterate(mask, core.std.Inflate, 4), 16)
        mask = lvf.rfs(mask, mask_ed, [(ED, ED+nced.clip_cut.num_frames)])

    if EXT != None:
        mask_ext = core.imwri.Read(ext.path).resize.Point(format=mask.format.id, matrix=1)
        mask_ext = core.std.AssumeFPS(mask_ext*len(mask), mask)
        mask = lvf.rfs(mask, mask_ext, ranges=EXT)

    restored = core.std.MaskedMerge(depth(clip, 16), depth(src, 16), mask)
    return mask if show_mask else restored

def grain(clip: vs.VideoNode) -> vs.VideoNode:
    grain = adptvgrnMod(clip, strength=0.15, sharp=80, luma_scaling=10, static=True)
    return grain

def finalize(clip: vs.VideoNode) -> vs.VideoNode:
    return depth(clip, 10)
